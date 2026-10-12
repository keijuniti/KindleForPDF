import base64
import io
import os
import subprocess
import tempfile
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
import Quartz
from PIL import Image
from src.domain.models.capture_config import CaptureConfig

# macOS の仮想キーコード
KEY_RIGHT_ARROW = 124

# これ未満のウィンドウ(ツールバー等の補助ウィンドウ)は候補に出さない
MIN_WINDOW_SIZE = 200
IGNORED_OWNERS = {"WindowManager", "loginwindow", "UserNotificationCenter", "コントロールセンター", "Control Center", "Dock"}
THUMBNAIL_SIZE = (320, 320)


class OSScreenService:
    """OSレベルの画面操作（キャプチャ・キー入力）を担当する

    対象ウィンドウだけを撮影し、キー入力も対象プロセスに直接送るので、
    キャプチャ中にユーザーが他のアプリを前面にしても止まらない。
    """

    def has_screen_access(self) -> bool:
        """このプロセス(を起動したターミナル)に画面収録権限があるか"""
        return Quartz.CGPreflightScreenCaptureAccess()

    def list_windows(self) -> list[dict]:
        """撮影候補のウィンドウ一覧 (大きい順)。id は screencapture -l に渡す CGWindowID"""
        # ponytail: 他のSpace/最小化中も含めたいので OptionAll。小さい補助ウィンドウは寸法で除外する素朴な判定
        windows = [
            {
                "id": w["kCGWindowNumber"],
                "pid": w["kCGWindowOwnerPID"],
                "name": w.get("kCGWindowOwnerName") or "",
                "title": w.get("kCGWindowName") or "",
                "width": int(w["kCGWindowBounds"]["Width"]),
                "height": int(w["kCGWindowBounds"]["Height"]),
            }
            for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, 0)
            if w.get("kCGWindowLayer") == 0
            and w.get("kCGWindowOwnerName") not in IGNORED_OWNERS
            and w.get("kCGWindowOwnerName")
            and w["kCGWindowBounds"]["Width"] >= MIN_WINDOW_SIZE
            and w["kCGWindowBounds"]["Height"] >= MIN_WINDOW_SIZE
        ]
        return sorted(windows, key=lambda w: w["width"] * w["height"], reverse=True)

    def find_window(self, window_id: int) -> tuple[int, int]:
        """list_windows が返した id から撮影対象の (CGWindowID, PID) を返す"""
        for w in self.list_windows():
            if w["id"] == window_id:
                return w["id"], w["pid"]
        raise ValueError(f"ウィンドウが見つかりません (閉じられた可能性があります): {window_id}")

    def _grab(self, window_id: int) -> Image.Image:
        """対象ウィンドウだけを撮影する (他のウィンドウに隠れていても撮れる)。失敗時は CalledProcessError"""
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        try:
            # -l: ウィンドウID指定 / -o: 影なし / -x: 撮影音なし
            subprocess.run(["screencapture", "-x", "-o", "-l", str(window_id), path], check=True)
            with Image.open(path) as img:
                return img.convert("RGB")
        finally:
            os.remove(path)

    def _with_preview(self, window: dict) -> dict:
        """preview(JPEGのdata URL)を付ける。撮れない/真っ黒なら None (一覧には残して選べるようにする)"""
        try:
            img = self._grab(window["id"])
        except subprocess.CalledProcessError:
            return {**window, "preview": None}
        if not any(hi for _, hi in img.getextrema()):
            return {**window, "preview": None}
        img.thumbnail(THUMBNAIL_SIZE)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=70)
        data = base64.b64encode(buf.getvalue()).decode()
        return {**window, "preview": f"data:image/jpeg;base64,{data}"}

    def list_window_previews(self) -> list[dict]:
        """一覧 + プレビュー。プレビューが取れたものを先頭に並べる (それ以外も選択可能)"""
        # ponytail: 候補数ぶん screencapture を並列で回す素朴な実装。数十個を超えるなら遅延取得に変える
        with ThreadPoolExecutor(max_workers=8) as pool:
            windows = list(pool.map(self._with_preview, self.list_windows()))
        return sorted(windows, key=lambda w: w["preview"] is None)  # stable: 大きい順は保たれる

    def capture_window(self, window_id: int, config: CaptureConfig) -> Image.Image:
        """対象ウィンドウをキャプチャし、設定に合わせて加工する"""
        screenshot = self._grab(window_id)
        if config.use_grayscale:
            screenshot = screenshot.convert("L")

        if config.resize_factor != 1.0:
            new_size = (
                int(screenshot.width * config.resize_factor),
                int(screenshot.height * config.resize_factor),
            )
            screenshot = screenshot.resize(new_size, Image.Resampling.LANCZOS)

        return screenshot

    def press_next_page(self, pid: int):
        """対象プロセスに右矢印キーを直接送ってページをめくる (前面でなくても届く)"""
        for key_down in (True, False):
            event = Quartz.CGEventCreateKeyboardEvent(None, KEY_RIGHT_ARROW, key_down)
            Quartz.CGEventPostToPid(pid, event)

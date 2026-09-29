import os
import re
import subprocess
import tempfile
from typing import Optional
import Quartz
from PIL import Image
from src.domain.models.capture_config import CaptureConfig

# macOS の仮想キーコード
KEY_RIGHT_ARROW = 124


class OSScreenService:
    """OSレベルの画面操作（キャプチャ・キー入力）を担当する

    対象ウィンドウだけを撮影し、キー入力も対象プロセスに直接送るので、
    キャプチャ中にユーザーが他のアプリを前面にしても止まらない。
    """

    def _window_info(self, target: str) -> Optional[dict]:
        """"window:<CGWindowID>:0" ラベルなら macOS のウィンドウ情報を返す。それ以外 / 見つからなければ None"""
        match = re.fullmatch(r"window:(\d+):\d+", target.strip())
        if not match:
            return None
        # Chrome のラベルの数値は macOS の CGWindowID
        # ponytail: Chrome 系専用。Safari/Firefox のラベルは形式が違うのでアプリ名一致にフォールバックする
        info = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionIncludingWindow, int(match[1])
        )
        return info[0] if info else None

    def window_owner_name(self, label: str) -> Optional[str]:
        """ラベルのウィンドウを持つアプリ名 (例: "Kindle")。画面表示用"""
        info = self._window_info(label)
        return info.get("kCGWindowOwnerName") if info else None

    def find_window(self, target: str) -> tuple[int, int]:
        """撮影対象の (CGWindowID, PID) を返す

        target はブラウザの getDisplayMedia が返すラベル ("window:<CGWindowID>:0") か、
        手入力されたアプリ名。アプリ名の場合はそのアプリの一番大きい通常ウィンドウを使う。
        """
        info = self._window_info(target)
        if not info and not target.strip().startswith("window:"):
            windows = [
                w for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, 0)
                if w.get("kCGWindowOwnerName") == target.strip() and w.get("kCGWindowLayer") == 0
            ]
            info = max(
                windows,
                key=lambda w: w["kCGWindowBounds"]["Width"] * w["kCGWindowBounds"]["Height"],
                default=None,
            )
        if not info:
            raise ValueError(f"ウィンドウが見つかりません (閉じられた可能性があります): {target}")
        return info["kCGWindowNumber"], info["kCGWindowOwnerPID"]

    def capture_window(self, window_id: int, config: CaptureConfig) -> Image.Image:
        """対象ウィンドウだけをキャプチャし、設定に合わせて加工する (他のウィンドウに隠れていても撮れる)"""
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        try:
            # -l: ウィンドウID指定 / -o: 影なし / -x: 撮影音なし
            subprocess.run(["screencapture", "-x", "-o", "-l", str(window_id), path], check=True)
            with Image.open(path) as img:
                screenshot = img.convert("L" if config.use_grayscale else "RGB")
        finally:
            os.remove(path)

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

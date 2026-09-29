import math
import os
import tempfile
import time
import img2pdf
from src.domain.models.capture_config import CaptureConfig
from src.infrastructure.services.os_screen_service import OSScreenService

# ソースの場所基準で固定 (起動ディレクトリに依存しない)
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "outputs"))


def spread_count(page_count: int) -> int:
    """見開き表示なので、撮影枚数はページ数の半分 (切り上げ)"""
    return math.ceil(page_count / 2)


def safe_output_path(output_dir: str, filename: str) -> str:
    """ディレクトリ部分を捨てて output_dir の外に書けないようにする"""
    name = os.path.basename(filename.strip())
    if not name or name in (".", ".."):
        raise ValueError(f"不正なファイル名です: {filename!r}")
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return os.path.join(output_dir, name)


class CaptureBookUseCase:
    """本を1冊丸ごとキャプチャしてPDF化する手順を管理する"""

    def __init__(self):
        self.screen_service = OSScreenService()

    def execute(self, config: CaptureConfig, window: tuple[int, int]):
        """キャプチャ実行のメインシナリオ。window は find_window で解決済みの (CGWindowID, PID)"""
        window_id, pid = window
        output_path = safe_output_path(OUTPUT_DIR, config.output_filename)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        count = spread_count(config.page_count)

        # 一時画像は失敗しても必ず消え、同時実行でも衝突しない
        with tempfile.TemporaryDirectory() as tmp:
            image_paths = []
            for i in range(count):
                img = self.screen_service.capture_window(window_id, config)
                file_path = os.path.join(tmp, f"page_{i:03d}.jpg")
                img.save(file_path, "JPEG", quality=85)
                image_paths.append(file_path)
                print(f"Progress: {i + 1}/{count}")

                if i < count - 1:
                    self.screen_service.press_next_page(pid)
                    time.sleep(config.interval)

            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(image_paths))

        print(f"完了: {output_path}")
        return output_path

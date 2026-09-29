# find_window / 出力パス / 見開き枚数 の self-check (Kindle 不要・副作用なし)。apps/api で実行:
#   .venv/bin/python -m src.infrastructure.services.os_screen_service_selfcheck
import os
from src.application.usecases.capture_book_usecase import safe_output_path, spread_count
from src.infrastructure.services.os_screen_service import OSScreenService

s = OSScreenService()

# 存在しない CGWindowID / 存在しないアプリ名 / 空文字 は ValueError
for bad in ["window:999999999:0", "NoSuchApp_KindleForPDF", ""]:
    try:
        s.find_window(bad)
        raise AssertionError(f"見つからないはずの対象が通ってしまった: {bad!r}")
    except ValueError:
        pass

assert s.window_owner_name("window:999999999:0") is None
assert s.window_owner_name("Kindle") is None  # ラベル以外は表示名を引かない

# 見開き枚数: 100ページ→50枚, 奇数は切り上げ
assert [spread_count(n) for n in (1, 2, 3, 100)] == [1, 1, 2, 50]

# 出力先の外には書けない / .pdf を補う
assert safe_output_path("/out", "../../etc/x.pdf") == os.path.join("/out", "x.pdf")
assert safe_output_path("/out", "/tmp/book") == os.path.join("/out", "book.pdf")
for bad in ["", "  ", "..", "dir/"]:
    try:
        safe_output_path("/out", bad)
        raise AssertionError(f"不正なファイル名が通ってしまった: {bad!r}")
    except ValueError:
        pass

print("self-check passed")

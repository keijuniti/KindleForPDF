# list_windows・find_window / 出力パス / 見開き枚数 の self-check (Kindle 不要・副作用なし)。apps/api で実行:
#   .venv/bin/python -m src.infrastructure.services.os_screen_service_selfcheck
import os
from src.application.usecases.capture_book_usecase import safe_output_path, spread_count
from src.infrastructure.services.os_screen_service import OSScreenService

s = OSScreenService()

# 存在しない CGWindowID は ValueError
try:
    s.find_window(999999999)
    raise AssertionError("見つからないはずのIDが通ってしまった")
except ValueError:
    pass

# 一覧は id/pid/name を持ち、find_window で同じ (id, pid) に解決でき、大きい順に並ぶ (Kindle 不要)
windows = s.list_windows()
for w in windows[:3]:
    assert {"id", "pid", "name", "title", "width", "height"} <= w.keys()
    assert s.find_window(w["id"]) == (w["id"], w["pid"])
areas = [w["width"] * w["height"] for w in windows]
assert areas == sorted(areas, reverse=True)

# 撮れないウィンドウは一覧に残り preview だけ None (権限なしでも同様)
assert s._with_preview({"id": 999999999})["preview"] is None

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

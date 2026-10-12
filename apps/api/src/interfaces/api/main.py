from fastapi import FastAPI, BackgroundTasks, HTTPException
from src.domain.models.capture_config import CaptureConfig
from src.application.usecases.capture_book_usecase import CaptureBookUseCase, OUTPUT_DIR, safe_output_path
from src.infrastructure.services.os_screen_service import OSScreenService
from src.interfaces.api.middleware import setup_middleware

app = FastAPI(title="Kindle to PDF API")

setup_middleware(app)

capture_usecase = CaptureBookUseCase()
screen_service = OSScreenService()


def require_screen_access():
    # 権限が無いと撮影が "could not create image from window" で無言に失敗するので先に止める
    if not screen_service.has_screen_access():
        raise HTTPException(
            status_code=403,
            detail=(
                "このAPIを起動したターミナルに画面収録の権限がありません。"
                "システム設定 > プライバシーとセキュリティ > 画面収録 でターミナルを許可し、"
                "ターミナルを再起動してからAPIを起動し直してください"
            ),
        )


@app.post("/capture")
def start_capture(config: CaptureConfig, background_tasks: BackgroundTasks):
    # バックグラウンドに回す前に検証し、失敗をクライアントに返す
    try:
        safe_output_path(OUTPUT_DIR, config.output_filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    require_screen_access()
    try:
        window = screen_service.find_window(config.target_window_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    background_tasks.add_task(capture_usecase.execute, config, window)
    return {"status": "success", "message": "Capture started"}

@app.get("/windows")
def list_windows():
    """開いているウィンドウ一覧 (id=CGWindowID, name=アプリ名, title, preview=サムネイル/撮れなければnull)"""
    require_screen_access()
    return screen_service.list_window_previews()

@app.get("/health")
def health_check():
    return {"status": "ok"}

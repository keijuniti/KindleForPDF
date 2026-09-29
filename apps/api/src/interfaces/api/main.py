from fastapi import FastAPI, BackgroundTasks, HTTPException
from src.domain.models.capture_config import CaptureConfig
from src.application.usecases.capture_book_usecase import CaptureBookUseCase, OUTPUT_DIR, safe_output_path
from src.infrastructure.services.os_screen_service import OSScreenService
from src.interfaces.api.middleware import setup_middleware

app = FastAPI(title="Kindle to PDF API")

setup_middleware(app)

capture_usecase = CaptureBookUseCase()
screen_service = OSScreenService()


@app.post("/capture")
def start_capture(config: CaptureConfig, background_tasks: BackgroundTasks):
    # バックグラウンドに回す前に検証し、失敗をクライアントに返す
    try:
        safe_output_path(OUTPUT_DIR, config.output_filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        window = screen_service.find_window(config.target_window_title)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    background_tasks.add_task(capture_usecase.execute, config, window)
    return {"status": "success", "message": "Capture started"}

@app.get("/window-name")
def window_name(label: str):
    """getDisplayMedia のラベル ("window:<id>:0") から表示用のアプリ名を返す"""
    name = screen_service.window_owner_name(label)
    if not name:
        raise HTTPException(status_code=404, detail="ウィンドウが見つかりません")
    return {"name": name}

@app.get("/health")
def health_check():
    return {"status": "ok"}

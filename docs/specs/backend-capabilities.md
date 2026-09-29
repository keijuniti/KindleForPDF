# Backend Capabilities

## What We Can Do

### 1. Window Resolution
- Resolve the target to a macOS `CGWindowID` + PID (Quartz), no focusing needed
- Accepts Chrome's `getDisplayMedia` track label (`window:<CGWindowID>:0`) or a plain
  app name (falls back to that app's largest normal window; Safari/Firefox labels use this path)

**Use case**: Frontend picks the target window via the browser's native screen
picker and sends the track label; backend captures that window even while it is in the background.

### 2. Screen Capture
- Capture full screen or specific window
- Support grayscale conversion (reduce file size)
- Save images as JPEG with configurable quality
- Batch capture with automated page turning

**Use case**: Capture an entire book page-by-page

### 3. Book Automation
- Simulate keyboard events (page navigation)
- Configurable intervals between captures (avoid UI lag)
- Handle double-page spreads (calculates scroll count)
- Generate PDF from captured images

**Use case**: Fully automated Kindle book → PDF conversion

### 4. PDF Generation
- Convert image sequence to single PDF
- Cleanup temporary files after conversion
- Configurable output filename

## API Style

**Framework**: FastAPI (REST)

**Endpoints** (high-level):
- `GET /health` - Health check
- `GET /window-name?label=` - App name for a `getDisplayMedia` label (display only)
- `POST /capture` - Validate config + resolve window (404 if missing), then capture in a background task

**Data Validation**: Pydantic models with camelCase support for frontend

**CORS**: Enabled for local development (`http://localhost:*`)

**Error Handling**: Structured error responses with detail messages

## Architecture Pattern

**Clean Architecture** (see `architecture.md` for layers)

### Key Use Cases
- `CaptureBookUseCase` - Orchestrates entire capture flow (find window → capture window → page turn → PDF)

### Domain Models
- `CaptureConfig` - Configuration for capture operation
  - `target_window_title`: Which app to capture
  - `page_count`: How many pages
  - `interval`: Delay between captures (seconds)
  - `use_grayscale`: Convert to grayscale (bool)
  - `output_filename`: PDF output name

### Infrastructure Services
- `OSScreenService` - Window resolution, per-window capture (`screencapture -l`), key events to a PID (`CGEventPostToPid`), image processing

## Current Limitations

- **macOS only**: Window detection uses macOS-specific APIs
- **No authentication**: Open API (local dev only)
- **No persistence**: No database, outputs are files
- **Single-user**: No concurrent capture support
- **No progress tracking**: Background task, no real-time status

## Future Enhancements

- Multi-platform support (Windows, Linux)
- Websocket for real-time progress
- Cloud storage integration
- Capture history/metadata storage

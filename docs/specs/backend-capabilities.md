# Backend Capabilities

## What We Can Do

### 1. Window Detection
- List all open GUI applications on macOS
- Identify target window by title (e.g., "Kindle")
- Focus/activate a specific window programmatically

**Use case**: Get window list → User selects Kindle app

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
- `GET /windows` - List open applications
- `POST /capture` - Start book capture (background task)

**Data Validation**: Pydantic models with camelCase support for frontend

**CORS**: Enabled for local development (`http://localhost:*`)

**Error Handling**: Structured error responses with detail messages

## Architecture Pattern

**Clean Architecture** (see `architecture.md` for layers)

### Key Use Cases
- `GetWindowsUseCase` - Wraps OS window service
- `CaptureBookUseCase` - Orchestrates entire capture flow (focus → capture → page turn → PDF)

### Domain Models
- `CaptureConfig` - Configuration for capture operation
  - `target_window_title`: Which app to capture
  - `page_count`: How many pages
  - `interval`: Delay between captures (seconds)
  - `use_grayscale`: Convert to grayscale (bool)
  - `output_filename`: PDF output name

### Infrastructure Services
- `OSWindowService` - Window detection and activation
- `OSScreenService` - Screen capture, keyboard automation, image processing

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

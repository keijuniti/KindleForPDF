# Integration Flows

## Core Flow: Kindle Book Capture

**User goal**: Convert an open Kindle book to PDF

### Prerequisites
1. Kindle app is open with book loaded
2. Kindle in **fullscreen mode** (menu bar hidden)
3. User knows total page count

### Step-by-Step Flow

```
┌─────────┐
│ User    │
└────┬────┘
     │
     │ 1. Opens frontend
     v
┌──────────────┐
│  Frontend    │───────────────────────────────────┐
└──────┬───────┘                                   │
       │                                           │
       │ 2. GET /windows                           │
       v                                           │
┌──────────────┐                                   │
│  Backend     │                                   │
│  (FastAPI)   │                                   │
└──────┬───────┘                                   │
       │                                           │
       │ 3. OSWindowService.get_windows()          │
       │    → Returns: [{"title": "Kindle", ...}]  │
       │                                           │
       │ 4. Response with window list              │
       v                                           │
┌──────────────┐                                   │
│  Frontend    │◄──────────────────────────────────┘
└──────┬───────┘
       │
       │ 5. User selects "Kindle" + config
       │    (page_count=100, interval=1.5, grayscale=true)
       │
       │ 6. POST /capture with config
       v
┌──────────────┐
│  Backend     │
└──────┬───────┘
       │
       │ 7. CaptureBookUseCase.execute() [background task]
       │
       ├──> 8. Focus Kindle window
       │
       ├──> 9. Loop (page_count/2 times for double-page spreads):
       │        a. Capture full screen (OSScreenService)
       │        b. Save to temp_images/page_NNN.jpg
       │        c. Simulate "Right Arrow" keypress (page turn)
       │        d. Wait interval seconds
       │
       ├──> 10. Convert images to PDF (img2pdf)
       │         → outputs/book.pdf
       │
       └──> 11. Cleanup temp images
       
       Response immediately: {"status": "success", "message": "Capture started"}
       (actual capture runs in background)
```

### Technical Details

**Window Focus**: Uses macOS `pygetwindow` to activate by title match

**Screen Capture**: Pillow screenshot of entire display (assumes fullscreen Kindle)

**Page Navigation**: `pyautogui.press('right')` for next page

**Double-page handling**: Physical page count ÷ 2 = number of screenshots (Kindle shows spreads)

**Grayscale optimization**: Converts RGB → grayscale before saving (smaller file size)

**PDF conversion**: `img2pdf` library (lossless image→PDF, preserves quality)

### Error Scenarios

| Issue | Handling |
|-------|----------|
| Window not found | UseCase catches exception → API returns 500 with error message |
| Capture fails mid-process | Cleanup partial temp images |
| PDF conversion fails | Temp images preserved for debugging |
| Kindle not in fullscreen | Screenshots include menu bar (user error) |

---

## Future Flow: Real-Time Progress

**Goal**: Show capture progress in frontend

### Proposed Enhancement
```
Frontend ←──[WebSocket]──→ Backend
              ↓
        Progress events:
        - {"page": 10, "total": 100}
        - {"status": "converting"}
        - {"done": true, "file": "book.pdf"}
```

**Not yet implemented** - current version fires background task and returns immediately.

---

## Future Flow: Cloud Upload

**Goal**: Store PDFs in cloud storage (S3, GCS, etc.)

### Proposed Steps
1. After PDF generation
2. Upload to cloud storage
3. Return download URL to frontend
4. (Optional) Delete local file

**Considerations**: Authentication, signed URLs, storage costs

---

## Platform-Specific Notes

### macOS (Current Focus)
- Window detection: Works via `pygetwindow`
- Fullscreen requirement: macOS menu bar must be hidden for clean captures
- Keyboard automation: Requires accessibility permissions for `pyautogui`

### Windows/Linux (Future)
- Different window management APIs needed
- Keyboard simulation may behave differently
- Test fullscreen behavior per platform

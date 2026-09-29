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
│  Frontend    │
└──────┬───────┘
       │
       │ 2. User clicks "Select Window" → browser's native
       │    Screen Capture API (getDisplayMedia) opens the
       │    OS window picker; frontend keeps the track label
       │    ("window:<CGWindowID>:0") and stops the stream
       │
       │ 3. GET /window-name shows the app name (display only);
       │    user may instead type an app name directly
       │
       │ 4. User confirms target + config
       │    (page_count=100, interval=1.5, grayscale=true)
       │
       │ 5. POST /capture with config
       v
┌──────────────┐
│  Backend     │
└──────┬───────┘
       │
       │ 6. Validate config + resolve window ID + PID
       │    (OSScreenService.find_window) → 422/404 on failure
       │
       │ 7. CaptureBookUseCase.execute() [background task]
       │
       ├──> 8. Loop (ceil(page_count/2) times for double-page spreads):
       │        a. Capture only the target window (screencapture -l)
       │        b. Save to a per-run temp dir (tempfile)
       │        c. Post "Right Arrow" to the Kindle PID (skipped after last)
       │        d. Wait interval seconds
       │
       ├──> 9. Convert images to PDF (img2pdf)
       │         → apps/api/outputs/<basename>.pdf
       │
       └──> 10. Temp dir removed automatically (also on failure)
       
       Response immediately: {"status": "success", "message": "Capture started"}
       (actual capture runs in background)
```

### Technical Details

**Window Resolution**: Quartz `CGWindowListCopyWindowInfo` maps the label / app name to a window ID + PID (no focusing)

**Screen Capture**: `screencapture -x -o -l <id>` captures only the target window, even when covered

**Page Navigation**: `CGEventPostToPid` sends Right Arrow straight to the Kindle process, so paging continues while other apps are in front

**Double-page handling**: ceil(page count ÷ 2) = number of screenshots (Kindle shows spreads)

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
- Window detection: Quartz window list (pyobjc)
- Screen capture: Requires Screen Recording permission for the terminal running the API
- Keyboard automation: `CGEventPostToPid` requires Accessibility permission

### Windows/Linux (Future)
- Different window management APIs needed
- Keyboard simulation may behave differently
- Test fullscreen behavior per platform

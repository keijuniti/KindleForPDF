# Frontend Capabilities

## What We Provide

### UI Features (Current/Planned)
- Window selection via the browser's native Screen Capture API (`getDisplayMedia`) — same mechanism Google Meet/Discord use
- Capture configuration form (page count, interval, grayscale toggle)
- Book preview/download interface
- Status display for background capture tasks

**Note**: Frontend is early-stage; core automation logic lives in backend.

## Tech Stack

### Framework
- **Next.js 16.1.1** (App Router)
- **React 19** with **React Compiler** enabled
  - Auto-memoization (no manual `useMemo`/`useCallback` needed)
  - Faster re-renders

### UI Components
- **shadcn/ui** - Copy-paste component system (not an npm package)
- **Radix UI** primitives (accessible, unstyled components)
- **Tailwind CSS v4** - Utility-first styling
- **lucide-react** - Icon library

### Developer Experience
- **Biome** - Single tool for formatting + linting (replaces ESLint + Prettier)
- **TypeScript** - Full type safety
- **Fast Refresh** - Next.js HMR

## Project Structure

```
apps/web/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # Reusable UI components (shadcn/ui)
│   └── lib/              # Utilities, API client
├── public/               # Static assets
└── biome.json            # Biome config
```

## API Integration

**Backend communication**: REST API calls to `http://localhost:8000`

**Expected endpoints** (frontend perspective):
- `GET /window-name?label=` → App name to display for the picked window
- `POST /capture` → Start capture with config
- `GET /health` → Health check

Window selection: the frontend opens the browser's native picker
(`navigator.mediaDevices.getDisplayMedia`), reads the track label, stops the stream
immediately, and sends the label (or a typed app name) as `targetWindowTitle` on
`POST /capture`. `GET /window-name` is only used to show a friendly name.

**Data format**: camelCase (matches JS conventions, backend converts via Pydantic)

## Styling Conventions

- **Utility-first**: Tailwind classes directly in JSX
- **Design system**: shadcn/ui components for consistency
- **Responsive**: Mobile-first approach
- **Dark mode**: (TBD) shadcn supports it out-of-box

## State Management

**Current**: Local component state (React hooks)

**Future considerations**:
- React Context for global state (if needed)
- Server Components where possible (reduce client JS)

## Current Limitations

- No real-time progress updates (backend runs background task)
- No capture history UI
- No authentication/user management
- No error boundary components (yet)

## Future Enhancements

- Websocket connection for live capture progress
- Preview captured pages before PDF generation
- Drag-and-drop configuration
- Capture history browsing
- Download/share PDF interface

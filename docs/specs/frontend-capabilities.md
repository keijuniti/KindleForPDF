# Frontend Capabilities

## What We Provide

### UI Features (Current/Planned)
- Window selection from the list the backend detects (`GET /windows`); the app name is shown and the window id is sent on capture
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
- `GET /windows` → Capturable windows (`id`, `name`, size) detected by the backend
- `POST /capture` → Start capture with config
- `GET /health` → Health check

Window selection: the frontend lists windows from `GET /windows`, shows the picked
app name, and sends its `id` as `targetWindowId` on `POST /capture`. The browser's
`getDisplayMedia` picker is not used: its track labels are not macOS CGWindowIDs.

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

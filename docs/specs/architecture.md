# KindleForPDF Architecture

## System Overview

**Purpose**: Automate screen capture of Kindle app pages and convert them to PDF.

**Components**:
- **Backend**: FastAPI (Python), clean architecture pattern
- **Frontend**: Next.js 14+ with React 19, shadcn/ui components
- **Communication**: REST API (CORS-enabled for local dev)

## Tech Stack

### Backend (`apps/api/`)
- **Runtime**: Python 3.x
- **Framework**: FastAPI + uvicorn
- **Key Libraries**:
  - `pyobjc-framework-Quartz` - Window lookup and key events to a PID
  - `screencapture` (macOS CLI) - Per-window capture
  - `img2pdf` - Image to PDF conversion
  - `Pillow` - Image processing
  - `pydantic` - Data validation

### Frontend (`apps/web/`)
- **Runtime**: Node.js (managed via fnm)
- **Framework**: Next.js 16.1.1
- **React**: v19 with React Compiler enabled
- **UI**: shadcn/ui + Radix UI primitives
- **Styling**: Tailwind CSS v4
- **Linter**: Biome (replaces ESLint/Prettier)

### No Database Yet
- File-based output (temp images → PDF)
- Stateless API (no persistence)

## Architecture Pattern: Clean Architecture

Backend follows clean architecture layers:

```
┌─────────────────────────────────────┐
│ Interfaces (API routes, schemas)   │ ← FastAPI endpoints
├─────────────────────────────────────┤
│ Application (Use Cases)            │ ← Business logic orchestration
├─────────────────────────────────────┤
│ Domain (Models, Interfaces)        │ ← Core business models
├─────────────────────────────────────┤
│ Infrastructure (Services)          │ ← OS/external integrations
└─────────────────────────────────────┘
```

**Dependency rule**: Inner layers know nothing about outer layers.

## Directory Structure

```
apps/
├── api/
│   ├── src/
│   │   ├── domain/          # Business models (CaptureConfig, etc.)
│   │   ├── application/     # Use cases (orchestrate domain + infra)
│   │   ├── infrastructure/  # OS services (window, screen capture)
│   │   └── interfaces/      # API routes, middleware, schemas
│   ├── pyproject.toml
│   └── outputs/             # Generated PDFs
│
└── web/
    ├── src/                 # Next.js app
    └── public/              # Static assets
```

## Key Conventions

### Backend
- **Import style**: Absolute imports from `src/` root (e.g., `from src.domain.models...`)
- **Camel/snake case**: Pydantic models accept camelCase from frontend via `AcceptCamel` util
- **Error handling**: Use cases wrap exceptions, API returns structured errors

### Frontend
- **React Compiler**: Enabled (auto-memoization)
- **Component library**: shadcn/ui (copy-paste components, not npm package)
- **Code quality**: Biome for formatting + linting

## Deployment

Currently **local development only**:
- Backend: `uvicorn src.interfaces.api.main:app --reload`
- Frontend: `npm run dev`

## Future Considerations

- Database for tracking capture history
- Cloud storage for PDFs
- Multi-platform window detection (currently macOS-focused)
- Authentication/multi-user support

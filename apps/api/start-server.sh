cd "$(dirname "$0")"
source .venv/bin/activate

uvicorn src.interfaces.api.main:app --reload

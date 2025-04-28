#!/bin/bash
# Harmonia Workflow Orchestration Engine - Launcher Script

# Default settings
PORT=8002
HOST="0.0.0.0"
DATA_DIR="$HOME/.harmonia"
HERMES_URL="http://localhost:5000/api"
LOG_LEVEL="INFO"
AUTO_REGISTER=true

# Display usage information
function show_usage {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  --port PORT          Port to run the API server on (default: $PORT)"
  echo "  --host HOST          Host to bind the API server to (default: $HOST)"
  echo "  --data-dir DIR       Directory for storing Harmonia data (default: $DATA_DIR)"
  echo "  --hermes-url URL     URL of the Hermes service (default: $HERMES_URL)"
  echo "  --log-level LEVEL    Logging level (default: $LOG_LEVEL)"
  echo "  --no-auto-register   Don't automatically register with Hermes"
  echo "  --init-only          Initialize components and exit (don't start API server)"
  echo "  --help               Show this help message"
}

# Process command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      PORT="$2"
      shift 2
      ;;
    --host)
      HOST="$2"
      shift 2
      ;;
    --data-dir)
      DATA_DIR="$2"
      shift 2
      ;;
    --hermes-url)
      HERMES_URL="$2"
      shift 2
      ;;
    --log-level)
      LOG_LEVEL="$2"
      shift 2
      ;;
    --no-auto-register)
      AUTO_REGISTER=false
      shift
      ;;
    --init-only)
      INIT_ONLY=true
      shift
      ;;
    --help)
      show_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_usage
      exit 1
      ;;
  esac
done

# Ensure data directory exists
mkdir -p "$DATA_DIR"

# Set environment variables
export HARMONIA_PORT="$PORT"
export HARMONIA_HOST="$HOST"
export HARMONIA_DATA_DIR="$DATA_DIR"
export HERMES_URL="$HERMES_URL"
export LOG_LEVEL="$LOG_LEVEL"

# Configure auto-registration
if [ "$AUTO_REGISTER" = true ]; then
  AUTO_REG_FLAG="--auto-register"
else
  AUTO_REG_FLAG=""
fi

# Configure init-only mode
if [ "$INIT_ONLY" = true ]; then
  INIT_FLAG="--init-only"
else
  INIT_FLAG=""
fi

# Find the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if running in a Python virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Warning: Not running in a virtual environment. Consider activating one first."
fi

# Run the Harmonia application
echo "Starting Harmonia Workflow Orchestration Engine..."
echo "  - API Server: $HOST:$PORT"
echo "  - Data Directory: $DATA_DIR"
echo "  - Hermes URL: $HERMES_URL"
echo "  - Log Level: $LOG_LEVEL"
echo "  - Auto-Register: $AUTO_REGISTER"

# Launch the application
python -m harmonia.api.app --port "$PORT" --host "$HOST" --data-dir "$DATA_DIR" \
  --hermes-url "$HERMES_URL" --log-level "$LOG_LEVEL" $AUTO_REG_FLAG $INIT_FLAG
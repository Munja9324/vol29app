#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/root/vol29app"
LOG_DIR="$APP_DIR/deploy"
LOG_FILE="$LOG_DIR/update_from_github.log"
VENV_DIR="$APP_DIR/.venv"

mkdir -p "$LOG_DIR"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] update started"
  cd "$APP_DIR"

  git fetch origin main
  git reset --hard origin/main

  if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
  fi

  "$VENV_DIR/bin/pip" install --upgrade pip
  "$VENV_DIR/bin/pip" install -r requirements.txt

  systemctl restart vol29app
  systemctl is-active vol29app

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] update finished"
} >> "$LOG_FILE" 2>&1

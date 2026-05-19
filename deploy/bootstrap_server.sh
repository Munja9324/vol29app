#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/root/vol29app"
REPO_URL="${1:-}"
BRANCH="${2:-main}"

if [ -z "$REPO_URL" ]; then
  echo "Usage: bash deploy/bootstrap_server.sh <repo-url> [branch]"
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y git python3 python3-venv python3-pip ca-certificates

mkdir -p /root/.ssh
chmod 700 /root/.ssh

if [ ! -d "$APP_DIR/.git" ]; then
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  cd "$APP_DIR"
  git fetch origin "$BRANCH"
  git reset --hard "origin/$BRANCH"
fi

cd "$APP_DIR"
chmod +x deploy/update_from_github.sh

if [ ! -d "$APP_DIR/.venv" ]; then
  python3 -m venv "$APP_DIR/.venv"
fi

"$APP_DIR/.venv/bin/pip" install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r requirements.txt

cp "$APP_DIR/deploy/vol29app.service" /etc/systemd/system/vol29app.service
systemctl daemon-reload
systemctl enable vol29app
systemctl restart vol29app
systemctl --no-pager --full status vol29app || true

echo
echo "Bootstrap completed."
echo "Next steps:"
echo "1. Place /root/vol29app/.env"
echo "2. Place Telegram session file in /root/vol29app/"
echo "3. Run: bash /root/vol29app/deploy/update_from_github.sh"

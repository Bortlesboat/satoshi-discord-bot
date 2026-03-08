#!/bin/bash
# Start Satoshi Discord Bot in a tmux session
cd "$(dirname "$0")"
tmux kill-session -t satoshi-bot 2>/dev/null
tmux new-session -d -s satoshi-bot ".venv/bin/python3 bot.py 2>&1 | tee /tmp/satoshi-bot.log"
echo "Bot started in tmux session 'satoshi-bot'"
echo "To attach: wsl tmux attach -t satoshi-bot"
echo "To check logs: wsl cat /tmp/satoshi-bot.log"

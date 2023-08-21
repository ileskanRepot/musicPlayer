sh -c "uvicorn app:app --reload --port 8001" & PIDUVI=$!
sh -c "cd frontEnd && npm run dev -- --port 8000" & PIDREA=$!

read -r -d '' _ </dev/tty

pkill $PIDUVI
pkill $PIDREA

sh -c "uvicorn app:app --reload --port 8002" & PIDUVI=$!
sh -c "cd frontEnd && npm run dev -- --port 8001" & PIDREA=$!

read -r -d '' _ </dev/tty

pkill $PIDUVI
pkill $PIDREA

sh -c "uvicorn app:app --reload" & PIDUVI=$!
sh -c "cd frontEnd && npm run dev" & PIDREA=$!

read -r -d '' _ </dev/tty

pkill $PIDUVI
pkill $PIDREA

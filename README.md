# musicPlayer

## Launch
### Develop
`uvicorn app:app --reload`

### Deploy
`uvicorn app:app`

## Develop
First you need to change `globalPath` from `app.py` to your music directory. Then you can run `uvicorn app:app --reload`. You should be able to access the app at `localhost:8000` or your specified port
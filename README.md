# musicPlayer

## Launch
### Develop
`uvicorn app:app --reload`



### Deploy
`sudo docker build -t musicserver .`
`docker compose up -d`

Backend:
`docker run -e "DEPLOY=1" -v "$HOME/music:/musicServer/music" -v "$PWD/psw/:/musicServer/psw" -p "8000:8000" ghcr.io/ileskanrepot/musicplayer-backend:latest`

Frontend:
`docker run -p "5173:5173" ghcr.io/ileskanrepot/musicplayer-frontend:latest`
 
## Develop
First you need to change `globalPath` from `app.py` to your music directory. Secondly make directory called `psw` and in that make files called `login.csv` where the first line contains `***REMOVED***` and `token.csv` where the first line contains `userName,token,lastUsed` (Or run `./setUp.sh`). Then you can run `uvicorn app:app --reload`. You should be able to access the app at `localhost:8000` or at your specified port.

## More info about httpS
https://dev.to/rajshirolkar/fastapi-over-https-for-development-on-windows-2p7d

##
Cool docker commands
* Compose up `docker compose up -d`
* Stop all containers `docker container stop $(docker ps -aq)`
* Delete all containers `docker container rm $(docker ps -aq)`
* Delete all images ``
* Fetch and run docker
** `docker image pull ghcr.io/ileskanrepot/musicplayer-backend:latest && docker run -d -e "DEPLOY=1" -v "$HOME/music:/musicServer/music" -v "$PWD/psw/:/musicServer/psw" -p "8000:8000" ghcr.io/ileskanrepot/musicplayer-backend:latest`
** `docker image pull ghcr.io/ileskanrepot/musicplayer-frontend:latest && echo -e "\n" && docker run -d -p "5173:5173" ghcr.io/ileskanrepot/musicplayer-frontend:latest`

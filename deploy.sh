docker container stop $(docker ps -aq)
docker image pull ghcr.io/ileskanrepot/musicplayer-backend:latest && docker run -d -e "DEPLOY=1" -v "$HOME/music:/musicServer/music" -v "$PWD/psw/:/musicServer/psw" -p "8000:8000" ghcr.io/ileskanrepot/musicplayer-backend:latest
docker image pull ghcr.io/ileskanrepot/musicplayer-frontend:latest && echo -e "\n" && docker run -d -p "5173:5173" ghcr.io/ileskanrepot/musicplayer-frontend:latest

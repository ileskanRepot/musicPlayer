from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import Cookie, FastAPI, HTTPException, Response, Form
from os.path import exists
from hashlib import sha512
from secrets import choice
from random import randint
from datetime import datetime, timedelta
from typing import Union
from string import ascii_letters, digits
from os import listdir


from javaScripts import songJS, mainJs, loginJs
from HTMLs import mainPage, songPage, logInPage
from css import mainCSS, footerCSS

globalPath = "/home/ileska/music/"

# [userName: str, token: str, lastUsed: datetime.now]
globalCurrentAuthTokens = []

# Functions
def randomString(size):
	letters = ascii_letters+digits
	return ''.join(choice(letters) for i in range(size))

def getSongs():
	dir_list = [name for name in listdir(globalPath) if name[-4:] == ".mp3"]

	return dir_list

def removeOldAuth(currUser, index):
	if datetime.now() - currUser[2] > timedelta(minutes=15):
		globalCurrentAuthTokens.pop(index)


def isAuthenticated(token,userName):
	ret = False
	for ii,currUser in enumerate(globalCurrentAuthTokens):
		if currUser[0] == userName and currUser[1] == token:
			currUser[2] = datetime.now()
			ret = True
		removeOldAuth(userName, ii)
		
	return ret

def hashedPsw(userName, psw):
	return sha512( str( userName+psw ).encode("utf-8") ).hexdigest()

def createUser(name,psw):
	with open("./login.csv","a") as authFile:
		authFile.write(f"{name},{hashedPsw(name, psw)}")



def login(userName: str, password: str):
	authToken = ""
	isUser = False
	with open("./login.csv","r") as authFile:
		for authStr in authFile.readlines()[1:]:
			splittedAuthStrong = authStr.replace('\n', '').split(',')
			if len(splittedAuthStrong) != 2:
				continue

			dbUserName, dbPassword = splittedAuthStrong
			if userName == dbUserName:
				if hashedPsw(userName,password) == dbPassword:

					tmpCurrAuth = globalCurrentAuthTokens

					for ii, currUser in enumerate(tmpCurrAuth):
						if len(currUser) != 3:
							globalCurrentAuthTokens.pop(ii)
							continue

						# If check if user has already an entry in authtokens
						if currUser[0] == userName:
							currUser[2] = datetime.now()
							authToken = currUser[1]
							isUser = True
							# Remove old authentication
							removeOldAuth(currUser, ii)


					if not isUser:
						authToken = randomString(randint(20, 25))
						globalCurrentAuthTokens.append([userName, authToken, datetime.now()])
						isUser = True

	return isUser, authToken


app = FastAPI()

# HTML
@app.get("/")
async def root():
	return HTMLResponse(mainPage())

@app.get("/outfit.css")
async def root():
	return Response(content = mainCSS(), media_type="text/css")

@app.get("/footer.css")
async def root():
	return Response(content = footerCSS(), media_type="text/css")

@app.get("/app.js")
async def js():
	return Response(content = mainJs(), media_type="text/javascript")

@app.get("/superSecret")
async def logInTest(userName: str = Cookie(default = ""), authToken: str = Cookie(default = "")):
	if authToken != "tmp":
		return "Hävisit"
	return "Correct"

@app.get("/login")
async def loginPage():
	return HTMLResponse(logInPage())

@app.get("/song/{name}")
async def song(name: str):
	return HTMLResponse(songPage(name))

@app.get("/song/{name}/app.js")
async def songjs(name: str):
	return Response(content = songJS(name), media_type="text/javascript")

# API
@app.get("/api/songs")
async def songs():
	return getSongs()

@app.get("/api/song/{name}")
async def song(name: str):
	def iterfile():
		with open(globalPath+name, mode="rb") as file:
			yield from file
	
	if not exists(globalPath+name):
		raise HTTPException(status_code=404, detail="Song not found")

	return StreamingResponse(iterfile(), media_type="audio/opus")

@app.post("/api/login")
async def logInApi(userName: str = Form(""), password: str = Form("")):
	isUser, authToken = login(userName, password)
	if not isUser:
		raise HTTPException(status_code=403, detail="User not found")
	
	return {"token":authToken}

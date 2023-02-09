from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse
from fastapi import Cookie, FastAPI, HTTPException, Response, Form
from os.path import exists
from hashlib import sha512
from secrets import choice
from random import randint
from datetime import datetime, timedelta
from typing import Union
from string import ascii_letters, digits
from os import listdir
from pydantic import BaseModel


from javaScripts import songJS, mainJs, loginJs
from HTMLs import mainPage, songPage, logInPage
from css import mainCSS, footerCSS

app = FastAPI()


class User(BaseModel):
	userName: str = ""
	password: str = ""

globalPath = "/home/ileska/music/"

# [userName: str, token: str, lastUsed: datetime.now]

@app.on_event('startup')
def init_data():
	print("init call")
	

# Functions
def randomString(size):
	letters = ascii_letters+digits
	return ''.join(choice(letters) for i in range(size))

def getSongs():
	dir_list = [name for name in listdir(globalPath) if name[-4:] == ".mp3"]

	return dir_list

def removeOldAuths(currUser, index):
	date = 0
	if type(currUser[2]) == type(datetime(2022,1,1)):
		date = currUser[2]
	if type(currUser[2]) == str:
		date = datetime.strptime(currUser[2],'%Y-%m-%d %H:%M:%S.%f')
	if len(currUser) != 3:
		return
	if datetime.now() - date > timedelta(minutes=15):
		print("Test")



def isAuthenticated(userName,token):
	ret = False
	with open("token.csv","r") as tokenFile:
		for ii,currUserTmp in enumerate(tokenFile.readlines()[1:]):
			currUser = currUserTmp.replace('\n', '').split(",")

			if currUser[0] == userName and currUser[1] == token:
				currUser[2] = datetime.now()
				ret = True
		
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

					with open("./token.csv","r") as tokenFile:

						for ii, currUserTmp in enumerate(tokenFile.readlines()[1:]):
							currUser = currUserTmp.split(',')
							if len(currUser) != 3:
								continue

							# If check if user has already an entry in authtokens
							if currUser[0] == userName:
								currUser[2] = datetime.now()
								authToken = currUser[1]
								isUser = True
							# Remove old authentication



					if not isUser:
						authToken = randomString(randint(20, 25))
						with open("./token.csv","a") as tokenFile:
							tokenFile.write(f"{userName},{authToken},{datetime.now()}")
						isUser = True

	return isUser, authToken



# HTML
@app.get("/")
async def root(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return HTMLResponse(mainPage())

@app.get("/outfit.css")
async def root(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return Response(content = mainCSS(), media_type="text/css")

@app.get("/footer.css")
async def root(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return Response(content = footerCSS(), media_type="text/css")

@app.get("/app.js")
async def js(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return Response(content = mainJs(), media_type="text/javascript")

@app.get("/login")
async def loginPage(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	return HTMLResponse(logInPage())

@app.get("/login.js")
async def loginPage(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	return Response(content = loginJs(), media_type="text/javascript")


@app.get("/song/{name}")
async def song(name: str,userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return HTMLResponse(songPage(name))

@app.get("/song/{name}/app.js")
async def songjs(name: str,userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return Response(content = songJS(name), media_type="text/javascript")

# API
@app.get("/api/songs")
async def songs(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	return getSongs()

@app.get("/api/song/{name}")
async def song(name: str, userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return RedirectResponse(url='/login')
	def iterfile():
		with open(globalPath+name, mode="rb") as file:
			yield from file
	
	if not exists(globalPath+name):
		raise HTTPException(status_code=404, detail="Song not found")

	return StreamingResponse(iterfile(), media_type="audio/opus")

@app.post("/api/login")
async def logInApi(user: User = User()):
	isUser, authToken = login(user.userName, user.password)
	if not isUser:
		raise HTTPException(status_code=403, detail="User not found")
	
	return {"token":authToken}

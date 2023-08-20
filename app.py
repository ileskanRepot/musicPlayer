from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse, FileResponse
from fastapi import Cookie, FastAPI, HTTPException, Response, Form
from os.path import exists, expanduser
from hashlib import sha512
from secrets import choice
from random import randint
from datetime import datetime, timedelta
from typing import Union
from string import ascii_letters, digits
from os import listdir, getenv
from pydantic import BaseModel


from javaScripts import songJS, mainJs, loginJs
from HTMLs import mainPage, songPage, logInPage
from css import mainCSS, footerCSS

app = FastAPI()


class User(BaseModel):
	userName: str = ""
	password: str = ""


globalPath = expanduser("~") + "/music/"
tokenFilePath = "./psw/token.csv"
loginFilePath = "./psw/login.csv"
favicon_path = "./favicon.ico"

if getenv('DEPLOY') == "1":
	globalPath = "/musicServer/music/"
	tokenFilePath = "/musicServer/psw/token.csv"
	loginFilePath = "/musicServer/psw/login.csv"

# [userName: str, token: str, lastUsed: datetime.now]

# Functions
def randomString(size):
	letters = ascii_letters+digits
	return ''.join(choice(letters) for i in range(size))

def getSongs():
	dir_list = [name for name in listdir(globalPath) if name[-4:] == ".mp3"]

	return dir_list

def removeOldAuths():
	curTokens = []
	with open(tokenFilePath,"r") as tokenFile:
		curTokens = tokenFile.readlines()
	tmpTokens = curTokens
	for ii, user in enumerate(tmpTokens[1:]):
		userSplit = user.split(",")

		if len(userSplit) != 3:
			continue
		date = 0
		date = userSplit[2].replace('\n', '')
		if datetime.now() - datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") > timedelta(minutes=15):
			curTokens.remove(f"{userSplit[0]},{userSplit[1]},{userSplit[2]}")
			
	print(curTokens)
	with open(tokenFilePath,"w") as tokenFile:
		for token in curTokens:
			tokenFile.write(token)

def removeAuth(userName,token):
	try:
		curTokens = []
		with open(tokenFilePath,"r") as tokenFile:
			curTokens = tokenFile.readlines()

		# Make temporaly list so I can pop variables out of original
		tmp = curTokens
		for ii, userToken in enumerate(tmp[1:]):
			userSplit = userToken.split(",")
			if len(userSplit) != 3:
				curTokens.pop(ii + 1)
				continue

			if userSplit[0] == userName and userSplit[1] == token:
				curTokens.pop(ii + 1)
				break

		with open(tokenFilePath,"w") as tokenFile:
			for token in curTokens:
				tokenFile.write(token)
		return True

	except:
		return False


def isAuthenticated(userName,token):
	ret = False
	with open(tokenFilePath,"r") as tokenFile:
		for ii,currUserTmp in enumerate(tokenFile.readlines()[1:]):
			currUser = currUserTmp.replace('\n', '').split(",")

			if currUser[0] == userName and currUser[1] == token:
				currUser[2] = datetime.now()
				ret = True
		
	return ret

def hashedPsw(userName, psw):
	return sha512( str( userName+psw ).encode("utf-8") ).hexdigest()

def createUser(name,psw):
	with open(loginFilePath,"a") as authFile:
		authFile.write(f"\n{name},{hashedPsw(name, psw)}")



def login(userName: str, password: str):
	authToken = ""
	isUser = False

	with open(loginFilePath,"r") as authFile:
		for authStr in authFile.readlines()[1:]:
			splittedAuthStrong = authStr.replace('\n', '').split(',')
			if len(splittedAuthStrong) != 2:
				continue

			dbUserName, dbPassword = splittedAuthStrong

			if userName == dbUserName:
				if hashedPsw(userName,password) == dbPassword:

					with open(tokenFilePath,"r") as tokenFile:

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
						with open(tokenFilePath,"a") as tokenFile:
							tokenFile.write(f"{userName},{authToken},{datetime.now()}\n")
						isUser = True

	return isUser, authToken


removeOldAuths()

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

@app.get("/logout")
async def songjs(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	removeAuth(userName,token)
	return RedirectResponse(url='/login')

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

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

@app.get("/api/isLoggedIn")
async def isLoggedIn(userName: str = Cookie(default = ""), token: str = Cookie(default = "")):
	if not isAuthenticated(userName, token):
		return False
	return True
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import FastAPI, HTTPException, Response
from os.path import exists
from os import listdir

from javaScripts import songJS, mainJs
from HTMLs import mainPage, songPage


# Functions
def getSongs():
	path = "/home/ileska/music/"
	dir_list = [name for name in listdir(path) if name[-5:] == ".opus"]

	return dir_list

app = FastAPI()

# HTML
@app.get("/")
async def root():
	return HTMLResponse(mainPage())

@app.get("/app.js")
async def js():
	return Response(content = mainJs(), media_type="text/javascript")

@app.get("/song/{name}")
async def song(name: str):
	print(name)
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
		with open("/home/ileska/music/"+name, mode="rb") as file:
			yield from file
	
	if not exists("/home/ileska/music/"+name):
		raise HTTPException(status_code=404, detail="Song not found")

	return StreamingResponse(iterfile(), media_type="audio/opus")

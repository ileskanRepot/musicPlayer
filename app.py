from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import FastAPI, HTTPException, Response
from os.path import exists
from os import listdir

from javaScripts import songJS, mainJs
from HTMLs import mainPage, songPage
from css import mainCSS, footerCSS

globalPath = "/home/ileska/music/"

# Functions
def getSongs():
	dir_list = [name for name in listdir(globalPath) if name[-4:] == ".mp3"]

	return dir_list

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
"""

@app.get("/api/song/{name}")
async def song(name: str):
	def iterfile():
		with open(globalPath+name, mode="rb") as file:
			return file.read()
	
	if not exists(globalPath+name):
		raise HTTPException(status_code=404, detail="Song not found")

	return Response(iterfile(), media_type="audio/opus")
"""

def songPage(song:str):
	ret = f"""<!DOCTYPE HTML>
<html><head>
<title>{song[0:10]}</title>
</head><body>
	<h1>{song}</h1>
	<br/>
	<button onclick="previous()">⏮︎</button>
	<audio id="song" src="/api/song/{song}" type="audio/opus" controls></audio>
	<button onclick="next()">⏭︎</button>

	<div id="songList" style="display: label;">
	</div>

	<script src="/song/{song}/app.js"></script>
</body></html>
	"""
	return ret

def mainPage():
	with open("index.html", mode="r") as file:
		return file.read()

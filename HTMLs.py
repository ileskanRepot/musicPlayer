def songPage(song:str):
	ret = f"""<!DOCTYPE HTML>
<html><head>
<title>{song[0:10]}</title>
</head><body>
	<h1>{song}</h1>
	<br/>
	<button onclick="previous()">⏮︎</button>
	<audio autoplay preload="metadata" autoplay id="song" controls src="/api/song/{song}" type="audio/opus">
    Lul fool Not supported
  </audio>
	<button onclick="next()">⏭︎</button>

	<div id="songList" style="display: label;">
	</div>

	<script src="/song/{song}/app.js"></script>


</body></html>
	"""
	return ret + footer()

def footer():
  return f"""
  <link rel="stylesheet" href="/footer.css">
  <footer>
  <p>Source: <a href="https://github.com/ileskanRepot/musicPlayer">Github</a> | Creator: Ileska | <a href="/logout">Logout</a></p>
  </footer>
  """

def mainPage():
	with open("index.html", mode="r") as file:
		return file.read() + footer()

def logInPage():
	with open("login.html", mode="r") as file:
		return file.read() + footer()

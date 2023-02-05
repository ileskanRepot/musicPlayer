def songJS(song:str):
	ret = f"""
let cur = 0
let songs = []

const play = () => {{
	if (audio.paused){{
		audio.play()
	}}else{{
		audio.pause()
	}}
}}

const main = async () => {{
  let songList = document.getElementById("songList")
  songs = await JSON.parse(localStorage.getItem("songs"))
  cur = songs.indexOf("{song}")
  let smallSongsList = songs.slice(Math.max(cur-5,0),Math.min(cur+10,songs.length)) 
  
  let stepper = 0
  smallSongsList.forEach(song => {{
    let songReplaced = song.replace(/\.[^/.]+$/, "")
    let whereAmI = location.protocol + '//' + location.host
  	let div = document.createElement("div")
    let link = document.createTextNode(songReplaced)

    let a = document.createElement("a")

    if (Math.min(5,cur) == stepper){{
      a.style.fontWeight = 'bold'
      a.style.color = 'magenta'
    }}
    stepper++

    a.appendChild(link)

    a.href = whereAmI + '/song/' + song

    div.append(a)

    songList.append(div)
  }})

}}

const next = () => {{
  window.location.replace("/song/" + songs[cur+1])
}}

const previous = () => {{
  window.location.replace("/song/" + songs[cur-1])
}}

let audio = document.getElementById("song")

navigator.mediaSession.setActionHandler('previoustrack', () => {{ previous() }});
navigator.mediaSession.setActionHandler('nexttrack', () => {{ next() }});

audio.onended = () => {{next()}}

audio.play()
main()
	"""
	return ret

def mainJs():
	with open("app.js", mode="r") as file:
		return file.read()

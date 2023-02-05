const selectState = () => {
	const shuff = document.getElementById("shuffle")
	return shuff.value
}

const getSongs = async () => {
	let songs = await fetch("/api/songs")
		.then(res => res.json())
	return songs
}

const shuffle = (array) => {
	return array.sort(() => Math.random() < 0.5);
}

const songList = document.getElementById("songList")
const globalSongs = getSongs()

const main = async () => {
	let songs = await globalSongs
	let stat = selectState()
	console.log(songs)
	console.log(typeof songs)

	// 0 set to shuffle
	// 1 set to alphabetic order
	if (stat == 0) {
		songs = shuffle(songs)
		localStorage.setItem("songs", JSON.stringify(songs))

	}
	else if (stat == 1) {
		songs = songs.sort()
		localStorage.setItem("songs", JSON.stringify(songs))

	}

	songList.innerHTML = ""

	songs.forEach(song => {
		let songReplaced = song.replace(/\.[^/.]+$/, "")
		let whereAmI = location.protocol + '//' + location.host
		let div = document.createElement("div")
		let a = document.createElement("a")
		let link = document.createTextNode(songReplaced)
		a.appendChild(link)
		// Remove ".opus"
		a.href = whereAmI + '/song/' + song

		div.append(a)

		songList.append(div)
	})
}

main()

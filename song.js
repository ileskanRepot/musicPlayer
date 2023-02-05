const getSongData = async () => {
  let songs = await fetch("/api/song/")
    .then(res => res.json())
  return songs
}

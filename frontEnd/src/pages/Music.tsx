import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useNavigate } from "../../node_modules/react-router-dom/dist/index";
import useCheckLogin from "./checkLogin";
import settings from "../constants";
import { Link } from "react-router-dom";

type Props = { e: string; i: number };
const LinkColor = ({ e, i }: Props) => {
  const style = { display: "block", color: "blue", fontWeight: "" };

  let urlSplit = window.location.pathname.split("/");
  let name = decodeURI(urlSplit[urlSplit.length - 1]);

  // console.log(e);
  // console.log(name);
  if (e == name) {
    style.color = "magenta";
    style.fontWeight = "bold";
  }
  return (
    <>
      <Link key={i} className="songLink" style={style} to={`/music/${e}`}>
        {e}
      </Link>
    </>
  );
};

const Music = () => {
  const { name } = useParams();

  const [songName, setSongName] = useState<string>("");

  const [smallListsSongs, setSmallListSongs] = useState<string[]>([]);

  const navigate = useNavigate();

  useEffect(() => {
    navigator.mediaSession.setActionHandler("previoustrack", () => {
      {
        previousSong();
      }
    });
    navigator.mediaSession.setActionHandler("nexttrack", () => {
      {
        nextSong();
      }
    });

    let urlSplit = window.location.pathname.split("/");
    let name = decodeURI(urlSplit[urlSplit.length - 1]);

    setSongName(name);

    let songString = localStorage.getItem("songs");
    if (songString) {
      let songs = JSON.parse(songString);
      console.log(songs);
      let cur = songs.indexOf(name);
      console.log(cur);
      setSmallListSongs(
        songs.slice(Math.max(cur - 5, 0), Math.min(cur + 10, songs.length))
      );
    }
  }, [window.location.pathname]);

  const loggedIn = useCheckLogin();
  if (!loggedIn) {
    return null;
  }

  function nextSong() {
    let urlSplit = window.location.pathname.split("/");
    let name = decodeURI(urlSplit[urlSplit.length - 1]);
    let songString = localStorage.getItem("songs");

    if (songString) {
      let songs = JSON.parse(songString);
      console.log(songs);
      let cur = songs.indexOf(name);

      navigate(`/music/${songs[cur + 1]}`);
    }
  }
  function previousSong() {
    let urlSplit = window.location.pathname.split("/");
    let name = decodeURI(urlSplit[urlSplit.length - 1]);
    let songString = localStorage.getItem("songs");

    if (songString) {
      let songs = JSON.parse(songString);
      console.log(songs);
      let cur = songs.indexOf(name);

      navigate(`/music/${songs[cur - 1]}`);
    }
  }

  return (
    <>
      <h1>{songName}</h1>
      <div className="audioDiv">
        <button className="audioBtn" onClick={previousSong}>
          ⏮
        </button>
        <audio
          autoPlay
          preload="metadata"
          id="song"
          controls
          src={`${settings.backendUrl}/api/song/${name}`}
          onEnded={nextSong}
        >
          Lul not supported
        </audio>
        <button className="audioBtn" onClick={nextSong}>
          ⏭
        </button>
      </div>
      <div
        className="songsDiv"
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "start",
        }}
      >
        {smallListsSongs.map((e, i: number) => (
          // if (e){let color="pink"}
          <LinkColor key={i} e={e} i={i} />
        ))}
      </div>
    </>
  );
};

export default Music;

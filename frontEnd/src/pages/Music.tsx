import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
// import { useNavigate } from "../../node_modules/react-router-dom/dist/index";
import useCheckLogin from "./checkLogin";
import settings from "../constants";

const Music = () => {
  const { name } = useParams();

  const [songName, setSongName] = useState<string>("");
  // const navigate = useNavigate();
  useEffect(() => {
    let urlSplit = window.location.pathname.split("/");
    let name = decodeURI(urlSplit[urlSplit.length - 1]);

    setSongName(name);
  }, []);

  const loggedIn = useCheckLogin();
  if (!loggedIn) {
    return null;
  }

  return (
    <>
      <h1>{songName}</h1>
      <button></button>
      <audio
        autoPlay
        preload="metadata"
        id="song"
        controls
        src={`${settings.backendUrl}/api/song/${name}`}
      >
        Lul not supported
      </audio>
      <button></button>
    </>
  );
};

export default Music;

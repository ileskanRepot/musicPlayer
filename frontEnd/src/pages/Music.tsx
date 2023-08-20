import React, { useEffect } from "react";
import { useParams } from "react-router";
// import { useNavigate } from "../../node_modules/react-router-dom/dist/index";
import useCheckLogin from "./checkLogin";

const Music = () => {
  const { name } = useParams();
  // const navigate = useNavigate();

  const loggedIn = useCheckLogin();
  if (!loggedIn) {
    return null;
  }

  return (
    <>
      <h1>Current song here</h1>
      <audio
        autoPlay
        preload="metadata"
        id="song"
        controls
        src={`/api/song/${name}`}
      >
        Lul not supported
      </audio>
    </>
  );
};

export default Music;

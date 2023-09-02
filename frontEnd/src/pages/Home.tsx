import React, { useEffect, useState } from "react";
import useCheckLogin from "./checkLogin";
import { Link } from "react-router-dom";
import settings from "../constants";

const Home = () => {
  const [listsSongs, setListSongs] = useState<string[]>([]);

  useEffect(() => {
    fetch(`${settings.backendUrl}/api/songs`, {
      credentials: "include",
    })
      .then((resp) => resp.json())
      .then((resp) => {
        setListSongs(resp);
        // console.log(JSON.stringify(listsSongs));
        localStorage.setItem("songs", JSON.stringify(resp));
      });
  }, []);

  const loggedIn = useCheckLogin();
  if (!loggedIn) {
    return null;
  }

  return (
    <>
      <h1>List of songs</h1>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "start",
        }}
      >
        {listsSongs.map((e, i) => (
          <Link key={i} style={{ display: "block" }} to={`/music/${e}`}>
            {e.replace(/\.[^/.]+$/, "")}
          </Link>
        ))}
      </div>
    </>
  );
};

export default Home;

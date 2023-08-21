import React, { useEffect, useState } from "react";
import useCheckLogin from "./checkLogin";

const Home = () => {
  const [listsSongs, setListSongs] = useState<string[]>([]);

  useEffect(() => {
    fetch(`/api/songs`, {
      credentials: "include",
    })
      .then((resp) => resp.json())
      .then((resp) => {
        console.log(resp);
        setListSongs(resp);
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
          <a key={i} style={{ display: "block" }} href={`/music/${e}`}>
            {e.replace(/\.[^/.]+$/, "")}
          </a>
        ))}
      </div>
    </>
  );
};

export default Home;

import React from "react";
import settings from "../constants";
import { Link, redirect } from "react-router-dom";

const Logout = () => {
  fetch(`${settings.backendUrl}/api/logout`, {
    credentials: "include",
  }).then((_) => redirect("/"));
  return (
    <h1>
      <Link to="/">HOME</Link>
    </h1>
  );
};

export default Logout;

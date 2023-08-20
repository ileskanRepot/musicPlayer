import React, { useEffect, useState } from "react";
import { useNavigate } from "../../node_modules/react-router-dom/dist/index";

const useCheckLogin = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://localhost:8000/api/isLoggedIn`, {
      credentials: "include",
    })
      .then((resp) => resp.json())
      .then((isLoggedIn) => {
        if (!isLoggedIn) {
          navigate("/login");
        } else {
          setLoggedIn(true);
        }
      });
  }, []);
  return loggedIn;
};

export default useCheckLogin;

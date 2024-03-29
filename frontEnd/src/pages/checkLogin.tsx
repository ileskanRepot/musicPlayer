import { useEffect, useState } from "react";
import { useNavigate } from "../../node_modules/react-router-dom/dist/index";
import settings from "../constants";

const useCheckLogin = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${settings.backendUrl}/api/isLoggedIn`, {
      credentials: "include",
    })
      .then((resp) => resp.json())
      .then((isLoggedIn) => {
        if (!isLoggedIn) {
          navigate(`/login`);
        } else {
          setLoggedIn(true);
        }
      });
  }, []);
  return loggedIn;
};

export default useCheckLogin;

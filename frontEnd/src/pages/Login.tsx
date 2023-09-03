import React, { useState } from "react";
import { useCookies } from "react-cookie";
import { useNavigate } from "../../node_modules/react-router-dom/dist/index";
import settings from "../constants";

const Login = () => {
  let [username, setUsername] = useState("");
  let [password, setPassword] = useState("");
  // let [loginResponse, _] = useState("");

  function updateUser(event: React.ChangeEvent<HTMLInputElement>) {
    setUsername(event.target.value);
  }
  function updatePass(event: React.ChangeEvent<HTMLInputElement>) {
    setPassword(event.target.value);
  }

  const [_, setCookie] = useCookies<string>([]);
  const navigate = useNavigate();

  function login(event: React.MouseEvent<HTMLElement>) {
    event.preventDefault();
    if (username === "" || password === "") {
      return null;
    }

    // let user = { usreName: username, password: password };
    // let data = new FormData();
    // data.append("json", JSON.stringify(user));

    fetch(`${settings.backendUrl}/api/login`, {
      method: "post",
      body: JSON.stringify({ userName: username, password: password }),
      headers: { "Content-Type": "application/json" },
    })
      .then((resp) => resp.json())
      .then((data) => {
        setCookie("userName", username, { path: "/" });
        setCookie("token", data.token, { path: "/" });
        navigate(`/`);
      });

    event.preventDefault();
  }
  return (
    <>
      <h1>LOGIN</h1>
      {/* {loginResponse} */}
      <form>
        <span>
          <label id="usernameLabel">Username</label>
          <input
            value={username}
            id="usernameInput"
            type="text"
            onChange={updateUser}
          ></input>
        </span>

        <span>
          <label id="passwordLabel">Password</label>
          <input
            value={password}
            id="passwordInput"
            type="password"
            onChange={updatePass}
          ></input>
        </span>
        <button id="loginBtn" onClick={login}>
          Login
        </button>
      </form>
    </>
  );
};

export default Login;

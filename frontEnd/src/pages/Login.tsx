import React, { useState } from "react";
import { CookiesProvider, useCookies } from "react-cookie";
import { useNavigate } from "../../node_modules/react-router-dom/dist/index";

const Login = () => {
  let [username, setUsername] = useState("");
  let [password, setPassword] = useState("");

  function updateUser(event: React.ChangeEvent<HTMLInputElement>) {
    setUsername(event.target.value);
  }
  function updatePass(event: React.ChangeEvent<HTMLInputElement>) {
    setPassword(event.target.value);
  }

  const [cookies, setCookie] = useCookies([]);
  const navigate = useNavigate();

  function login(event: React.MouseEvent<HTMLElement>) {
    if (username === "" || password === "") {
      return null;
    }

    // let user = { usreName: username, password: password };
    // let data = new FormData();
    // data.append("json", JSON.stringify(user));

    fetch("/api/login", {
      method: "post",
      body: JSON.stringify({ userName: username, password: password }),
      headers: { "Content-Type": "application/json" },
    })
      .then((resp) => resp.json())
      .then((data) => {
        console.log(data.token);
        setCookie("userName", username, { path: "/" });
        setCookie("token", data.token, { path: "/" });
        navigate("/");
      });

    event.preventDefault();
  }
  return (
    <>
      <h1>LOGIN</h1>
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
        <button onClick={login}>Login</button>
      </form>
    </>
  );
};

export default Login;

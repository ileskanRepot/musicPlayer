// import ReactDOM from "react-dom/client";
// import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./pages/Layout";
import NoPage from "./pages/NoPage";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Music from "./pages/Music";
import Logout from "./pages/Logout";
import "./App.css";
// import { useState } from "react";
import * as React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "../node_modules/react-router-dom/dist/index";

function App() {
  const router = createBrowserRouter([
    // { element: <Layout />}
    {
      path: "/",
      element: <Layout />,
      children: [
        { path: "", element: <Home /> },
        { path: "music/:name", element: <Music /> },
        { path: "login", element: <Login /> },
        { path: "logout", element: <Logout /> },
        { path: "*", element: <NoPage /> },
      ],
    },
  ]);

  // let [auth, setAuth] = useState(false);
  // let reqAuth = (nextState, replace, next) => {
  //   if (!auth) {
  //     replace({
  //       pathname: "/login",
  //       state: { nextPathname: nextState.location.pathname },
  //     });
  //   }
  //   return true;
  // };

  return (
    <RouterProvider router={router} />
    // <>
    //   <BrowserRouter>
    //     <Routes>
    //       <Route path="/" element={<Layout />}>
    //         <Route index element={<Home />} onEnter={reqAuth} />
    //         <Route path="login" element={<Login />} />
    //         <Route path="music/*" element={<Music />} onEnter={reqAuth} />
    //         <Route path="logout" element={<Logout />} onEnter={reqAuth} />
    //         <Route path="*" element={<NoPage />} />
    //       </Route>
    //     </Routes>
    //   </BrowserRouter>
    // </>
  );
}

export default App;

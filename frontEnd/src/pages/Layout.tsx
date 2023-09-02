import React from "react";
import { Outlet, Link } from "react-router-dom";
import useScreenWidth from "./useScreenWidth";
import settings from "../constants";

type Props = { loc: string; textColor: string; text: string };
const LinkColor = ({ loc, textColor, text }: Props) => {
  return (
    <>
      <Link to={loc} style={{ color: textColor, textDecoration: "underline" }}>
        {text}
      </Link>
    </>
  );
};

const Layout = () => {
  const screenWidth = useScreenWidth(450);
  const textColor = "white";

  return (
    <>
      <div
        style={{
          width: "100%",
          backgroundColor: "purple",
          color: textColor,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div className="tobBarButton">
          <Link to={`/`}>
            <img
              style={{ width: "3rem", height: "3rem" }}
              src={`${settings.backendUrl}/api/favicon.ico`}
            ></img>
          </Link>
        </div>
        {screenWidth && (
          <p>
            Source:{" "}
            <LinkColor
              loc="https://github.com/ileskanRepot/musicPlayer"
              text="Github"
              textColor={textColor}
            />{" "}
            | Creator: Ileska
          </p>
        )}
        <div className="tobBarButton">
          <LinkColor loc={`/logout`} text="Logout" textColor={textColor} />
        </div>
      </div>

      <div style={{ margin: "2rem" }}>
        <Outlet />
      </div>
    </>
  );
};

export default Layout;

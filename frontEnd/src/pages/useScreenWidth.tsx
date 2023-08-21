import { useEffect, useState } from "react";
// import { useNavigate } from "../../node_modules/react-router-dom/dist/index";

const useScreenWidth = (minWidth: number) => {
  const [matches, setMatches] = useState(
    window.matchMedia(`(min-width: ${minWidth}px)`).matches
  );

  useEffect(() => {
    window
      .matchMedia(`(min-width: ${minWidth}px)`)
      .addEventListener("change", (e) => setMatches(e.matches));
  }, []);
  return matches;
};

export default useScreenWidth;

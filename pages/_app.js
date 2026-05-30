import { useState, useEffect } from "react";
import "../styles/globals.css";

export default function App({ Component, pageProps }) {
  const [theme, setTheme] = useState("dark");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("fs-theme") || "dark";
    setTheme(saved);
    document.documentElement.setAttribute("data-theme", saved);
    setMounted(true);
  }, []);

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("fs-theme", next);
  };

  if (!mounted) return null;

  return <Component {...pageProps} theme={theme} toggleTheme={toggleTheme} />;
}

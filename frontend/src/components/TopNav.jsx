import { useState } from "react";
import { NavLink } from "react-router-dom";
import { ThermometerIcon, MenuIcon } from "./icons";
import { useNow } from "../hooks/useNow";
import { formatClock } from "../lib/format";

const LINKS = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/history", label: "History" },
  { to: "/about", label: "About" },
];

export function TopNav({ is24h }) {
  const [open, setOpen] = useState(false);
  const now = useNow(1000);

  return (
    <nav className={`nav ${open ? "nav--open" : ""}`}>
      <div className="container nav__inner">
        <NavLink to="/" className="brand" onClick={() => setOpen(false)}>
          <span className="brand__mark">
            <ThermometerIcon style={{ color: "#1a0e04" }} />
          </span>
          <span className="brand__name">
            Temp<span>Cast</span>ML
          </span>
        </NavLink>

        <div className="nav__links">
          {LINKS.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `nav__link ${isActive ? "nav__link--active" : ""}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>

        <div className="nav__meta">
          <span className="nav__clock num">{formatClock(now, is24h)}</span>
        </div>

        <button
          type="button"
          className="nav__toggle"
          aria-label="Toggle navigation"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <MenuIcon style={{ width: 18, height: 18 }} />
        </button>
      </div>
    </nav>
  );
}

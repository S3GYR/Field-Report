import React from "react";
import { NavLink } from "react-router-dom";

const linkStyle: React.CSSProperties = {
  color: "white",
  textDecoration: "none",
  fontWeight: 600,
  fontSize: "0.85rem",
};

export default function Toolbar() {
  const computeStyle = ({ isActive }: { isActive: boolean }) => ({
    ...linkStyle,
    color: isActive ? "var(--accent2)" : linkStyle.color,
  });

  return (
    <nav
      style={{
        background: "#1a1a1a",
        color: "white",
        padding: "10px 24px",
        display: "flex",
        gap: "18px",
        alignItems: "center",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}
    >
      <NavLink style={computeStyle} to="/">
        Dashboard
      </NavLink>
      <NavLink style={computeStyle} to="/photos">
        Photos
      </NavLink>
      <NavLink style={computeStyle} to="/tasks">
        Tâches
      </NavLink>
      <NavLink style={computeStyle} to="/export">
        Export PDF
      </NavLink>
    </nav>
  );
}

import React, { ReactNode } from "react";
import Toolbar from "./Toolbar";

interface Props {
  children: ReactNode;
}

export default function ShellLayout({ children }: Props) {
  return (
    <div className="app-shell">
      <Toolbar />
      <main>{children}</main>
    </div>
  );
}

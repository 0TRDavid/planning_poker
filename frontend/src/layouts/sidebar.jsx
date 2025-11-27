import React, { useState } from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar({ user = { name: "Utilisateur" } }) {
    const [collapsed, setCollapsed] = useState(false);

    const links = [
        { to: "/", label: "Tableau de bord", icon: DashboardIcon },
        { to: "/rooms", label: "Parties", icon: RoomsIcon },
        { to: "/settings", label: "Paramètres", icon: SettingsIcon },
        { to: "/about", label: "À propos", icon: InfoIcon },
    ];

    return (
        <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
            <div className="brand">
                <button
                    aria-label="Basculer la sidebar"
                    className="toggle"
                    onClick={() => setCollapsed((s) => !s)}
                >
                    ☰
                </button>
                {!collapsed && <div className="title">Planning Poker</div>}
            </div>

            <nav className="nav">
                {links.map((l) => (
                    <NavLink
                        key={l.to}
                        to={l.to}
                        className="nav-link"
                        activeClassName="active"
                        exact
                    >
                        <span className="icon">{l.icon()}</span>
                        {!collapsed && <span className="label">{l.label}</span>}
                    </NavLink>
                ))}
            </nav>

            <div className="footer">
                <div className="user">
                    <div className="avatar">{user.name.charAt(0).toUpperCase()}</div>
                    {!collapsed && (
                        <div className="userinfo">
                            <div className="name">{user.name}</div>
                            <button className="logout">Se déconnecter</button>
                        </div>
                    )}
                </div>
            </div>

            <style>{`
                .sidebar {
                    width: 240px;
                    min-height: 100vh;
                    background: linear-gradient(180deg,#1f2937,#111827);
                    color: #e5e7eb;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    transition: width .2s ease;
                }
                .sidebar.collapsed { width: 72px; }

                .brand {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 12px;
                }
                .toggle {
                    background: transparent;
                    border: none;
                    color: inherit;
                    font-size: 18px;
                    cursor: pointer;
                }
                .title { font-weight: 700; font-size: 16px; }

                .nav { display: flex; flex-direction: column; padding: 8px; gap: 6px; }
                .nav-link {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 10px;
                    border-radius: 8px;
                    color: inherit;
                    text-decoration: none;
                    transition: background .12s;
                }
                .nav-link .icon { width: 24px; height: 24px; display: inline-flex; align-items:center; justify-content:center; }
                .nav-link:hover { background: rgba(255,255,255,0.04); }
                .nav-link.active { background: rgba(99,102,241,0.16); color: #c7d2fe; }

                .footer { padding: 12px; border-top: 1px solid rgba(255,255,255,0.04); }
                .user { display: flex; align-items: center; gap: 12px; }
                .avatar {
                    width: 40px; height: 40px; border-radius: 8px;
                    background: #374151; display:flex;align-items:center;justify-content:center;
                    font-weight:700;color:#f3f4f6;
                }
                .userinfo .name { font-size: 14px; }
                .logout {
                    margin-top:6px;
                    background: transparent;
                    border: 1px solid rgba(255,255,255,0.06);
                    color: inherit;
                    padding: 6px 8px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 12px;
                }

                @media (max-width: 720px) {
                    .sidebar { position: fixed; z-index: 40; transform: translateX(0); }
                }
            `}</style>
        </aside>
    );
}

/* Simple SVG icon components */
function DashboardIcon() {
    return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
            <path d="M3 13h8V3H3v10zM13 21h8V11h-8v10zM13 3v6h8V3h-8zM3 21h8v-8H3v8z" fill="currentColor"/>
        </svg>
    );
}
function RoomsIcon() {
    return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
            <path d="M12 3L2 9l10 6 10-6L12 3zm0 13l-9-5v7l9 5 9-5v-7l-9 5z" fill="currentColor"/>
        </svg>
    );
}
function SettingsIcon() {
    return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06A2 2 0 1 1 2.29 16.9l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09c.7 0 1.3-.39 1.51-1a1.65 1.65 0 0 0-.33-1.82L4.32 4.3A2 2 0 1 1 7.15 1.47l.06.06c.5.5 1.2.7 1.82.33.5-.3 1.1-.3 1.6 0l.06.06A1.65 1.65 0 0 0 13 3.09V3a2 2 0 1 1 4 0v.09c0 .7.39 1.3 1 1.51.62.28 1.32.15 1.82-.33l.06-.06A2 2 0 1 1 21.7 7.15l-.06.06c-.5.5-.7 1.2-.33 1.82.3.5.3 1.1 0 1.6l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33c-.5.3-1.1.3-1.6 0z" fill="currentColor"/>
        </svg>
    );
}
function InfoIcon() {
    return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
            <path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" fill="currentColor"/>
        </svg>
    );
} 
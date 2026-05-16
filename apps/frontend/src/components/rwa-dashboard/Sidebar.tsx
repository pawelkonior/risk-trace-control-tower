import { ChevronsLeft } from "lucide-react";

import type { AppContext } from "../../api/types";
import { appNavigation, getViewHref, type AppView } from "../../navigation";

type SidebarProps = {
  activeItem?: AppView | string;
  appContext: AppContext | null;
  collapsed?: boolean;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onCollapseToggle?: () => void;
  onNavigate?: (view: AppView) => void;
};

export function Sidebar({
  activeItem = "Home",
  appContext,
  collapsed = false,
  onAction,
  onCollapseToggle,
  onNavigate,
}: SidebarProps) {
  function handleNav(view: AppView) {
    onNavigate?.(view);
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <img
          alt={appContext?.appName ?? "RiskTrace"}
          className="sidebar-brand-logo"
          src={collapsed ? "/risktrace-logo-sm.png" : "/risktrace-logo.png"}
        />
      </div>

      <nav className="sidebar-nav" aria-label="Primary">
        {appNavigation.map(({ label, icon: Icon, view }) => (
          <a
            key={label}
            aria-current={label === activeItem ? "page" : undefined}
            href={getViewHref(view)}
            className={`sidebar-item${label === activeItem ? " active" : ""}`}
            onClick={(event) => {
              event.preventDefault();
              handleNav(view);
            }}
          >
            <Icon size={18} strokeWidth={1.8} />
            <span>{label}</span>
          </a>
        ))}
      </nav>

      <div className="sidebar-panel status-panel">
        <h2>System Status</h2>
        {(appContext?.systemStatus ?? []).map(({ label, value }) => (
          <div className="status-row" key={label}>
            <span className="status-label">
              <span className="status-dot" />
              {label}
            </span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      <div className="sidebar-user">
        <div className="avatar avatar-lg">{appContext?.user.initials ?? "--"}</div>
        <div className="sidebar-user-details">
          <strong>{appContext?.user.name ?? ""}</strong>
          <span>{appContext?.user.role ?? ""}</span>
          <small>Last login: {appContext?.user.lastLogin ?? "..."}</small>
        </div>
      </div>
      <button
        aria-label={collapsed ? "Expand navigation" : "Collapse navigation"}
        className="collapse-button"
        type="button"
        onClick={() => {
          onCollapseToggle?.();
          if (!onCollapseToggle) {
            onAction?.("navigation.collapse");
          }
        }}
      >
        <ChevronsLeft
          className={collapsed ? "collapse-icon-rotated" : ""}
          size={17}
          strokeWidth={1.8}
        />
        <span>{collapsed ? "Expand" : "Collapse"}</span>
      </button>
    </aside>
  );
}

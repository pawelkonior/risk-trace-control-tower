import type { ReactNode } from "react";
import { useState } from "react";

import type { AppContext } from "../../api/types";
import type { AppView } from "../../navigation";
import { Sidebar } from "./Sidebar";
import { TopBar, type BreadcrumbItem } from "./TopBar";

export function AppShell({
  activeNav = "Home",
  appContext,
  breadcrumbs,
  children,
  comparisonLabel,
  notificationCount,
  onAction,
  onNavigate,
  showSearch,
}: {
  activeNav?: string;
  appContext: AppContext | null;
  breadcrumbs: BreadcrumbItem[];
  children: ReactNode;
  comparisonLabel?: string;
  notificationCount?: number;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onNavigate?: (view: AppView) => void;
  showSearch?: boolean;
}) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className={`rwa-shell${sidebarCollapsed ? " sidebar-collapsed" : ""}`}>
      <Sidebar
        activeItem={activeNav}
        appContext={appContext}
        collapsed={sidebarCollapsed}
        onCollapseToggle={() => {
          setSidebarCollapsed((current) => !current);
          onAction?.("navigation.collapse", { collapsed: !sidebarCollapsed });
        }}
        onAction={onAction}
        onNavigate={onNavigate}
      />
      <main className="rwa-main">
        <TopBar
          breadcrumbs={breadcrumbs}
          appContext={appContext}
          comparisonLabel={comparisonLabel}
          notificationCount={notificationCount}
          onAction={onAction}
          onNavigate={onNavigate}
          showSearch={showSearch}
        />
        {children}
      </main>
    </div>
  );
}

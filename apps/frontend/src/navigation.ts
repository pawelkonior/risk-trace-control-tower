import type { LucideIcon } from "lucide-react";
import { BookOpenCheck, GitBranch, House, LayoutDashboard } from "lucide-react";

export type AppView = "home" | "dashboard" | "lineage" | "briefing";

export type NavigationItem = {
  view: AppView;
  label: string;
  path: string;
  icon: LucideIcon;
};

export const appNavigation: NavigationItem[] = [
  { view: "home", label: "Home", path: "/home", icon: House },
  { view: "dashboard", label: "RWA Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { view: "lineage", label: "Data Lineage", path: "/lineage", icon: GitBranch },
  { view: "briefing", label: "RWA Intelligence Briefing", path: "/briefing", icon: BookOpenCheck },
];

const viewsByPath = new Map(appNavigation.map((item) => [item.path, item.view]));

export function getViewHref(view: AppView): string {
  const item = appNavigation.find((navItem) => navItem.view === view);
  return `#${item?.path ?? "/home"}`;
}

export function getNavigationItem(view: AppView): NavigationItem {
  return appNavigation.find((item) => item.view === view) ?? appNavigation[0];
}

export function resolveViewFromHash(hash: string): AppView {
  const path = hash.replace(/^#/, "") || "/home";
  return viewsByPath.get(path) ?? "home";
}

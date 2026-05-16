import { useEffect, useState } from "react";

import { DataLineagePage } from "./pages/DataLineagePage";
import { HomePage } from "./pages/HomePage";
import { RwaIntelligenceBriefingPage } from "./pages/RwaIntelligenceBriefingPage";
import { RwaDashboardPage } from "./pages/RwaDashboardPage";
import { getViewHref, resolveViewFromHash, type AppView } from "./navigation";

function getInitialView(): AppView {
  return resolveViewFromHash(window.location.hash);
}

export function App() {
  const [view, setView] = useState<AppView>(getInitialView);

  useEffect(() => {
    function syncViewFromHash() {
      setView(resolveViewFromHash(window.location.hash));
    }

    window.addEventListener("hashchange", syncViewFromHash);
    window.addEventListener("popstate", syncViewFromHash);
    return () => {
      window.removeEventListener("hashchange", syncViewFromHash);
      window.removeEventListener("popstate", syncViewFromHash);
    };
  }, []);

  function handleNavigate(nextView: AppView) {
    const nextHash = getViewHref(nextView);
    setView(nextView);

    if (window.location.hash !== nextHash) {
      window.history.pushState(null, "", nextHash);
    }
  }

  if (view === "home") {
    return <HomePage onNavigate={handleNavigate} />;
  }

  if (view === "dashboard") {
    return <RwaDashboardPage onNavigate={handleNavigate} />;
  }

  if (view === "lineage") {
    return <DataLineagePage onNavigate={handleNavigate} />;
  }

  return <RwaIntelligenceBriefingPage onNavigate={handleNavigate} />;
}

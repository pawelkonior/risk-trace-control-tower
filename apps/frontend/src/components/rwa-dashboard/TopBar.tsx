import { useEffect, useMemo, useState } from "react";
import {
  Bell,
  CalendarDays,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  Search,
  X,
} from "lucide-react";

import { searchRwa } from "../../api/rwaApi";
import type { AppContext, SearchResult } from "../../api/types";
import { useNotificationsData } from "../../hooks/useNotificationsData";
import { getViewHref, type AppView } from "../../navigation";

export type BreadcrumbItem = {
  label: string;
  active?: boolean;
  view?: AppView;
};

type TopBarProps = {
  appContext: AppContext | null;
  breadcrumbs: BreadcrumbItem[];
  comparisonLabel?: string;
  notificationCount?: number;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onNavigate?: (view: AppView) => void;
  showSearch?: boolean;
};

export function TopBar({
  appContext,
  breadcrumbs,
  comparisonLabel,
  notificationCount,
  onAction,
  onNavigate,
  showSearch = false,
}: TopBarProps) {
  const [openPanel, setOpenPanel] = useState<
    "calendar" | "search" | "notifications" | "help" | "user" | null
  >(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searchError, setSearchError] = useState<string | null>(null);
  const effectiveNotificationCount = notificationCount ?? appContext?.notificationCount ?? 0;
  const notifications = useNotificationsData(openPanel === "notifications");
  const notificationRows = notifications.data ?? appContext?.notifications ?? [];

  function togglePanel(panel: NonNullable<typeof openPanel>) {
    setOpenPanel((current) => (current === panel ? null : panel));
    onAction?.(`${panel === "calendar" ? "reporting-date" : panel}.open`);
  }

  useEffect(() => {
    if (openPanel !== "search") {
      return;
    }

    const controller = new AbortController();
    searchRwa(searchQuery, controller.signal)
      .then((payload) => {
        setSearchResults(payload.results);
        setSearchError(null);
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }
        setSearchError(error instanceof Error ? error.message : "Search unavailable");
        setSearchResults([]);
      });

    return () => controller.abort();
  }, [openPanel, searchQuery]);

  return (
    <header className="topbar">
      <nav className="breadcrumbs" aria-label="Breadcrumb">
        {breadcrumbs.map((item, index) => {
          const isLast = index === breadcrumbs.length - 1;
          const canNavigate = Boolean(item.view && onNavigate && !isLast);
          return (
            <span className="breadcrumb-part" key={`${item.label}-${index}`}>
              {!canNavigate ? (
                <span aria-current={isLast ? "page" : undefined}>{item.label}</span>
              ) : (
                <a
                  className={item.active ? "active-link" : ""}
                  href={getViewHref(item.view as AppView)}
                  onClick={(event) => {
                    event.preventDefault();
                    onNavigate?.(item.view as AppView);
                  }}
                >
                  {item.label}
                </a>
              )}
              {isLast ? null : <ChevronRight size={14} />}
            </span>
          );
        })}
      </nav>

      <div className="topbar-actions">
        <div className="environment">
          <span>Environment</span>
          <strong>{appContext?.environment ?? "..."}</strong>
        </div>
        <div className="divider" />
        <button
          aria-expanded={openPanel === "calendar"}
          className={`reporting-date reporting-date-button${
            openPanel === "calendar" ? " active" : ""
          }`}
          type="button"
          onClick={() => togglePanel("calendar")}
        >
          <CalendarDays size={16} />
          <div>
            <span>Reporting Date</span>
            <strong>{appContext?.reportingDate ?? "..."}</strong>
          </div>
          <ChevronDown size={14} />
        </button>
        <div className="divider" />
        {comparisonLabel ? <div className="comparison-label">{comparisonLabel}</div> : null}
        {showSearch ? (
          <button
            aria-expanded={openPanel === "search"}
            className={`icon-button${openPanel === "search" ? " active" : ""}`}
            type="button"
            aria-label="Search"
            onClick={() => togglePanel("search")}
          >
            <Search size={18} />
          </button>
        ) : null}
        <button
          aria-expanded={openPanel === "notifications"}
          className={`icon-button notification${openPanel === "notifications" ? " active" : ""}`}
          type="button"
          aria-label="Notifications"
          onClick={() => togglePanel("notifications")}
        >
          <Bell size={18} />
          <span>{effectiveNotificationCount}</span>
        </button>
        <button
          aria-expanded={openPanel === "help"}
          className={`icon-button${openPanel === "help" ? " active" : ""}`}
          type="button"
          aria-label="Help"
          onClick={() => togglePanel("help")}
        >
          <CircleHelp size={18} />
        </button>
        <button
          aria-expanded={openPanel === "user"}
          className={`user-menu-button${openPanel === "user" ? " active" : ""}`}
          type="button"
          onClick={() => togglePanel("user")}
        >
          <span className="avatar avatar-sm">{appContext?.user.initials ?? "--"}</span>
          <ChevronDown size={15} />
        </button>
      </div>

      {openPanel === "calendar" && appContext ? (
        <ReportingCalendarPanel
          appContext={appContext}
          onClose={() => setOpenPanel(null)}
        />
      ) : null}
      {openPanel === "search" ? (
        <SearchPanel
          error={searchError}
          onAction={onAction}
          onClose={() => setOpenPanel(null)}
          query={searchQuery}
          results={searchResults}
          setQuery={setSearchQuery}
        />
      ) : null}
      {openPanel === "notifications" ? (
        <NotificationsPanel
          error={notifications.error}
          isLoading={notifications.isLoading}
          notifications={notificationRows}
          onClose={() => setOpenPanel(null)}
        />
      ) : null}
      {openPanel === "help" && appContext ? (
        <HelpPanel appContext={appContext} onAction={onAction} onClose={() => setOpenPanel(null)} />
      ) : null}
      {openPanel === "user" && appContext ? (
        <UserPanel appContext={appContext} onAction={onAction} onClose={() => setOpenPanel(null)} />
      ) : null}
    </header>
  );
}

function ReportingCalendarPanel({
  appContext,
  onClose,
}: {
  appContext: AppContext;
  onClose: () => void;
}) {
  const days = useMemo(() => calendarDays(appContext.reportingCalendar.reportingDate), [appContext]);
  const availableDates = new Set(appContext.reportingCalendar.availableDates);

  return (
    <section className="topbar-panel calendar-panel" aria-label="Reporting calendar">
      <PanelHeader title="Reporting Date" onClose={onClose} />
      <div className="calendar-panel-month">{appContext.reportingCalendar.monthLabel}</div>
      <div className="calendar-weekdays" aria-hidden="true">
        {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
          <span key={day}>{day}</span>
        ))}
      </div>
      <div className="calendar-grid">
        {days.map((day) => {
          const isSelected = day.date === appContext.reportingCalendar.reportingDate;
          const isAvailable = availableDates.has(day.date);
          return (
            <button
              aria-label={day.date}
              className={`${!day.inMonth ? "muted" : ""}${isSelected ? " selected" : ""}`}
              disabled={!isSelected || !isAvailable}
              key={day.date}
              type="button"
            >
              {day.label}
            </button>
          );
        })}
      </div>
      <p>{appContext.reportingCalendar.lockedReason}</p>
    </section>
  );
}

function SearchPanel({
  error,
  onAction,
  onClose,
  query,
  results,
  setQuery,
}: {
  error: string | null;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onClose: () => void;
  query: string;
  results: SearchResult[];
  setQuery: (query: string) => void;
}) {
  return (
    <section className="topbar-panel search-panel" aria-label="Search panel">
      <PanelHeader title="Search" onClose={onClose} />
      <label className="search-field">
        <Search size={16} />
        <input
          autoFocus
          placeholder="Search metrics, exposures, traces"
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </label>
      {error ? <div className="panel-error">{error}</div> : null}
      <div className="search-results">
        {results.map((result) => (
          <a
            href={result.route}
            key={result.id}
            onClick={() => {
              onAction?.("search.result.open", { resultId: result.id, title: result.title });
              onClose();
            }}
          >
            <span>{result.category}</span>
            <strong>{result.title}</strong>
            <em>{result.description}</em>
          </a>
        ))}
      </div>
    </section>
  );
}

function NotificationsPanel({
  error,
  isLoading,
  notifications,
  onClose,
}: {
  error: string | null;
  isLoading: boolean;
  notifications: AppContext["notifications"];
  onClose: () => void;
}) {
  return (
    <section className="topbar-panel notifications-panel" aria-label="Notifications panel">
      <PanelHeader title="Notifications" onClose={onClose} />
      {error ? <div className="panel-error">{error}</div> : null}
      {isLoading ? <div className="panel-empty">Loading notifications</div> : null}
      {notifications.map((item) => (
        <article className={`notification-row notification-${item.tone}`} key={item.id}>
          <span>{item.createdAt}</span>
          <strong>{item.title}</strong>
          <p>{item.detail}</p>
        </article>
      ))}
    </section>
  );
}

function HelpPanel({
  appContext,
  onAction,
  onClose,
}: {
  appContext: AppContext;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onClose: () => void;
}) {
  return (
    <section className="topbar-panel help-panel" aria-label="Help panel">
      <PanelHeader title="Help" onClose={onClose} />
      {appContext.helpItems.map((item) => (
        <button
          className="panel-list-button"
          key={item.id}
          type="button"
          onClick={() => onAction?.(item.actionId, { topicId: item.id, title: item.title })}
        >
          <strong>{item.title}</strong>
          <span>{item.detail}</span>
        </button>
      ))}
    </section>
  );
}

function UserPanel({
  appContext,
  onAction,
  onClose,
}: {
  appContext: AppContext;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onClose: () => void;
}) {
  return (
    <section className="topbar-panel user-panel" aria-label="User menu">
      <PanelHeader title={appContext.user.name} onClose={onClose} />
      <div className="user-panel-role">{appContext.user.role}</div>
      {appContext.userMenu.map((item) => (
        <button
          className="panel-list-button"
          key={item.id}
          type="button"
          onClick={() => onAction?.(item.actionId, { itemId: item.id })}
        >
          <strong>{item.label}</strong>
          <span>{item.detail}</span>
        </button>
      ))}
    </section>
  );
}

function PanelHeader({ onClose, title }: { onClose: () => void; title: string }) {
  return (
    <div className="topbar-panel-header">
      <h2>{title}</h2>
      <button aria-label={`Close ${title}`} className="icon-button" type="button" onClick={onClose}>
        <X size={16} />
      </button>
    </div>
  );
}

function calendarDays(reportingDate: string) {
  const [year, month] = reportingDate.split("-").map(Number);
  const firstDay = new Date(Date.UTC(year, month - 1, 1));
  const startOffset = (firstDay.getUTCDay() + 6) % 7;
  const start = new Date(Date.UTC(year, month - 1, 1 - startOffset));
  return Array.from({ length: 42 }, (_, index) => {
    const current = new Date(start);
    current.setUTCDate(start.getUTCDate() + index);
    const currentYear = current.getUTCFullYear();
    const currentMonth = current.getUTCMonth() + 1;
    const currentDay = current.getUTCDate();
    return {
      date: [
        currentYear,
        String(currentMonth).padStart(2, "0"),
        String(currentDay).padStart(2, "0"),
      ].join("-"),
      inMonth: currentMonth === month,
      label: String(currentDay),
    };
  });
}

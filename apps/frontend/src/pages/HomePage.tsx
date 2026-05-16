import {
  ArrowRight,
  BellRing,
  CalendarDays,
  CheckCircle2,
  Clock3,
  ShieldCheck,
} from "lucide-react";

import type { AppContext, HomeCard, NotificationItem, SystemStatusItem } from "../api/types";
import { AppShell } from "../components/rwa-dashboard/AppShell";
import { Card } from "../components/rwa-dashboard/Card";
import { PageHeader } from "../components/rwa-dashboard/PageHeader";
import { Toast } from "../components/rwa-dashboard/Toast";
import type { ApiResourceState } from "../hooks/useApiResource";
import { useAppContextData } from "../hooks/useAppContextData";
import { useToast } from "../hooks/useToast";
import { useUiActions } from "../hooks/useUiActions";
import { appNavigation, getViewHref, type AppView } from "../navigation";

type HomePageProps = {
  onNavigate?: (view: AppView) => void;
};

const workingViews = appNavigation.filter((item) => item.view !== "home");

export function HomePage({ onNavigate }: HomePageProps) {
  const { notify, toast } = useToast();
  const appContext = useAppContextData();
  const { runAction } = useUiActions(notify);
  const homeCardsByView = new Map<HomeCard["view"], HomeCard>(
    (appContext.data?.homeCards ?? []).map((item) => [item.view, item])
  );
  const notifications = appContext.data?.notifications ?? [];
  const unreadNotifications =
    notifications.filter((item) => !item.read).length || appContext.data?.notificationCount || 0;

  function handleNavigate(view: AppView) {
    onNavigate?.(view);
  }

  return (
    <AppShell
      activeNav="Home"
      appContext={appContext.data}
      breadcrumbs={[{ label: "Home", active: true }]}
      onAction={runAction}
      onNavigate={onNavigate}
      showSearch
    >
      <div className="rwa-page home-page">
        <PageHeader
          title="Home"
          description="Risk and capital oversight for management review"
        />

        <div className="home-layout">
          <HomeOverviewPanel
            appContext={appContext.data ?? undefined}
            unreadNotifications={unreadNotifications}
          />
          <HomeSystemStatusPanel items={appContext.data?.systemStatus ?? []} />
          <HomeModulesPanel
            homeCardsByView={homeCardsByView}
            onNavigate={handleNavigate}
          />
          <HomeWorkQueuePanel notifications={notifications} />
        </div>
        <HomeContextStatus appContext={appContext} />
        <Toast message={toast} />
      </div>
    </AppShell>
  );
}

function HomeOverviewPanel({
  appContext,
  unreadNotifications,
}: {
  appContext?: AppContext;
  unreadNotifications: number;
}) {
  return (
    <Card className="home-overview-panel">
      <div className="home-overview-copy">
        <div className="home-overview-brand">
          <img
            alt={appContext?.appName ?? "RiskTrace"}
            className="home-overview-logo"
            src="/risktrace-logo-sm.png"
          />
          <div>
            <span className="home-kicker">RiskTrace Control Tower</span>
            <h2>Quarter-end RWA cockpit</h2>
          </div>
        </div>
        <p>
          One place for portfolio exposure, calculation traceability and the management review pack.
        </p>
        <div className="home-overview-ready">
          <ShieldCheck size={16} strokeWidth={2} />
          <span>Management review workspace ready</span>
        </div>
      </div>

      <div className="home-overview-metrics" aria-label="Reporting context">
        <HomeOverviewMetric
          icon={CalendarDays}
          label="Reporting Date"
          value={appContext?.reportingDate ?? "..."}
        />
        <HomeOverviewMetric
          icon={Clock3}
          label="Comparison"
          value={appContext?.comparisonLabel ?? "Prior close"}
        />
        <HomeOverviewMetric
          label="Environment"
          value={appContext?.environment ?? "..."}
          valueClassName="home-env-pill"
        />
        <HomeOverviewMetric icon={BellRing} label="Open Notices" value={String(unreadNotifications)} />
      </div>
    </Card>
  );
}

function HomeOverviewMetric({
  icon: Icon,
  label,
  value,
  valueClassName,
}: {
  icon?: typeof CalendarDays;
  label: string;
  value: string;
  valueClassName?: string;
}) {
  return (
    <div className="home-overview-metric">
      {Icon ? (
        <span className="home-overview-metric-icon">
          <Icon size={15} strokeWidth={2} />
        </span>
      ) : null}
      <span>{label}</span>
      <strong className={valueClassName}>{value}</strong>
    </div>
  );
}

function HomeModulesPanel({
  homeCardsByView,
  onNavigate,
}: {
  homeCardsByView: Map<HomeCard["view"], HomeCard>;
  onNavigate: (view: AppView) => void;
}) {
  return (
    <Card className="home-modules-panel">
      <div className="home-panel-heading">
        <div>
          <span>Workspaces</span>
          <h2>Review Modules</h2>
        </div>
      </div>
      <div className="home-view-grid">
        {workingViews.map(({ icon: Icon, label, view }) => {
          const details = homeCardsByView.get(view as HomeCard["view"]);

          return (
            <a
              className={`home-view-card home-view-card-${details?.tone ?? "blue"}`}
              href={getViewHref(view)}
              key={view}
              onClick={(event) => {
                event.preventDefault();
                onNavigate(view);
              }}
            >
              <div className="home-view-topline">
                <span className="home-view-icon">
                  <Icon size={20} strokeWidth={1.9} />
                </span>
                <span className="home-status">{details?.status ?? ""}</span>
              </div>
              <div>
                <h3>{label}</h3>
                <p>{details?.description ?? ""}</p>
              </div>
              <div className="home-card-footer">
                <strong>{details?.metric ?? "..."}</strong>
                <span className="home-open-link">
                  Open
                  <ArrowRight size={16} strokeWidth={1.9} />
                </span>
              </div>
            </a>
          );
        })}
      </div>
    </Card>
  );
}

function HomeSystemStatusPanel({ items }: { items: SystemStatusItem[] }) {
  return (
    <Card className="home-side-panel">
      <div className="home-panel-heading compact">
        <div>
          <span>Health</span>
          <h2>System Status</h2>
        </div>
        <CheckCircle2 size={19} />
      </div>
      <div className="home-status-list">
        {items.map(({ label, value }) => (
          <div className="home-status-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </Card>
  );
}

function HomeWorkQueuePanel({ notifications }: { notifications: NotificationItem[] }) {
  return (
    <Card className="home-work-panel">
      <div className="home-panel-heading compact">
        <div>
          <span>Attention</span>
          <h2>Review Queue</h2>
        </div>
        <BellRing size={18} />
      </div>
      <div className="home-work-list">
        {notifications.slice(0, 3).map((item) => (
          <div className={`home-work-item home-work-tone-${item.tone}`} key={item.id}>
            <span className="home-work-dot" />
            <div>
              <strong>{item.title}</strong>
              <p>{item.detail}</p>
              <span>{item.createdAt}</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

function HomeContextStatus({ appContext }: { appContext: ApiResourceState<AppContext> }) {
  if (!appContext.error) {
    return null;
  }

  return (
    <div className="api-status api-status-error">
      <span>Data unavailable</span>
      <strong>{appContext.error}</strong>
    </div>
  );
}

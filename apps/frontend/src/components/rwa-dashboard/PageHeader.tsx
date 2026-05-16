import type { LucideIcon } from "lucide-react";

export type PageHeaderAction = {
  label: string;
  icon?: LucideIcon;
  variant?: "primary" | "secondary" | "purple";
  onClick: () => void;
};

type PageHeaderProps = {
  title: string;
  description: string;
  actions?: PageHeaderAction[];
};

export function PageHeader({ title, description, actions = [] }: PageHeaderProps) {
  return (
    <div className="page-header">
      <div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {actions.length ? (
        <div className="header-actions">
          {actions.map(({ label, icon: Icon, variant = "secondary", onClick }) => (
            <button className={`button button-${variant}`} key={label} type="button" onClick={onClick}>
              {Icon ? <Icon size={15} /> : null}
              <span>{label}</span>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}

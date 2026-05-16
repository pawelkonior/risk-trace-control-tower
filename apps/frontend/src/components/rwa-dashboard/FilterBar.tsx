import { useState } from "react";
import { CalendarDays, ChevronDown, RefreshCcw } from "lucide-react";

import type { DashboardFilterOptions, DashboardFilters } from "../../api/types";

type FilterKey = "scenario" | "businessUnit" | "currency";

type FilterBarProps = {
  filterOptions: DashboardFilterOptions;
  filters: DashboardFilters;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onFiltersChange: (filters: DashboardFilters) => void;
};

export function FilterBar({
  filterOptions,
  filters,
  onAction,
  onFiltersChange,
}: FilterBarProps) {
  const [openFilter, setOpenFilter] = useState<FilterKey | null>(null);

  function selectPeriod(period: string) {
    onFiltersChange({ ...filters, period });
    onAction?.("dashboard.filter.period", { period });
  }

  function selectFilter(key: FilterKey, value: string) {
    onFiltersChange({ ...filters, [key]: value });
    setOpenFilter(null);
    onAction?.("dashboard.filter.set", { filter: filterLabels[key], key, value });
  }

  function resetFilters() {
    const defaultFilters: DashboardFilters = {
      period: filterOptions.periods[0] ?? filters.period,
      scenario: filterOptions.scenarios[0] ?? filters.scenario,
      businessUnit: filterOptions.businessUnits[0] ?? filters.businessUnit,
      currency: filterOptions.currencies[0] ?? filters.currency,
    };
    onFiltersChange(defaultFilters);
    setOpenFilter(null);
    onAction?.("dashboard.filter.reset", { filters: defaultFilters });
  }

  return (
    <div className="filter-shell">
      <div className="period-control" aria-label="Period">
        {filterOptions.periods.map((period) => (
          <button
            className={period === filters.period ? "active" : ""}
            key={period}
            type="button"
            onClick={() => selectPeriod(period)}
          >
            <span>{period}</span>
            {period === "Custom" ? <CalendarDays size={13} /> : null}
          </button>
        ))}
      </div>
      <div className="filter-control">
        <FilterDropdown
          label="Scenario"
          value={filters.scenario}
          options={filterOptions.scenarios}
          open={openFilter === "scenario"}
          onToggle={() => setOpenFilter((current) => (current === "scenario" ? null : "scenario"))}
          onSelect={(value) => selectFilter("scenario", value)}
        />
        <FilterDropdown
          label="Business Unit"
          value={filters.businessUnit}
          options={filterOptions.businessUnits}
          open={openFilter === "businessUnit"}
          onToggle={() =>
            setOpenFilter((current) => (current === "businessUnit" ? null : "businessUnit"))
          }
          onSelect={(value) => selectFilter("businessUnit", value)}
        />
        <FilterDropdown
          label="Currency"
          value={filters.currency}
          options={filterOptions.currencies}
          open={openFilter === "currency"}
          onToggle={() => setOpenFilter((current) => (current === "currency" ? null : "currency"))}
          onSelect={(value) => selectFilter("currency", value)}
        />
        <button className="reset-filter" type="button" onClick={resetFilters}>
          <RefreshCcw size={14} />
          <span>Reset Filters</span>
        </button>
      </div>
    </div>
  );
}

const filterLabels: Record<FilterKey, string> = {
  scenario: "Scenario",
  businessUnit: "Business Unit",
  currency: "Currency",
};

function FilterDropdown({
  label,
  value,
  options,
  open,
  onToggle,
  onSelect,
}: {
  label: string;
  value: string;
  options: string[];
  open: boolean;
  onToggle: () => void;
  onSelect: (value: string) => void;
}) {
  return (
    <div className="filter-dropdown-shell">
      <button
        aria-expanded={open}
        className={`filter-dropdown${open ? " open" : ""}`}
        type="button"
        onClick={onToggle}
        onKeyDown={(event) => {
          if (event.key === "Escape") {
            if (open) {
              onToggle();
            }
            event.currentTarget.blur();
          }
        }}
      >
        <span>{label}</span>
        <strong>{value}</strong>
        <ChevronDown size={14} />
      </button>
      {open ? (
        <div className="dropdown-menu" role="menu">
          {options.map((option) => (
            <button
              className={option === value ? "selected" : ""}
              key={option}
              role="menuitem"
              type="button"
              onClick={() => onSelect(option)}
            >
              {option}
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}

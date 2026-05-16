import { useState } from "react";
import { geoNaturalEarth1, geoPath } from "d3-geo";
import { feature } from "topojson-client";
import worldAtlas from "world-atlas/countries-110m.json";
import type { Feature, FeatureCollection, Geometry } from "geojson";
import type { GeometryCollection, Topology } from "topojson-specification";

import type { ApiCountryRwa } from "../../api/types";
import { Card, CardHeader } from "./Card";

type CountryGeometry = Feature<Geometry, { name?: string }>;
type CountryRwaData = ApiCountryRwa[];

type CountryMapCardProps = {
  data: CountryRwaData;
  totalAmount: string;
};

const countryByNumericId: Record<string, string> = {
  "616": "Poland",
  "276": "Germany",
  "250": "France",
  "528": "Netherlands",
  "840": "United States",
  "826": "United Kingdom",
  "380": "Italy",
  "724": "Spain",
  "756": "Switzerland",
};

const worldTopology = worldAtlas as unknown as Topology<{
  countries: GeometryCollection<{ name?: string }>;
}>;
const countryFeatures = (
  feature(worldTopology, worldTopology.objects.countries) as FeatureCollection<
    Geometry,
    { name?: string }
  >
).features as CountryGeometry[];
const projection = geoNaturalEarth1().fitSize([340, 178], { type: "Sphere" });
const pathGenerator = geoPath(projection);

export function CountryMapCard({ data, totalAmount }: CountryMapCardProps) {
  const [activeCountry, setActiveCountry] = useState<string | null>(null);
  const activeItem = data.find((item) => item.country === activeCountry);

  return (
    <Card className="country-card">
      <CardHeader title="RWA by Country (Top 5)" subtitle="(PLN)" />
      <div className="country-layout">
        <div className="map-stack">
          <WorldMap activeCountry={activeCountry} data={data} onActive={setActiveCountry} />
          {activeItem ? (
            <div className="map-tooltip">
              <strong>{activeItem.country}</strong>
              <span>
                {activeItem.amount} RWA · {activeItem.pct}
              </span>
            </div>
          ) : null}
        </div>
        <div className="country-table">
          {data.map((item) => (
            <button
              className={`country-row country-button${
                activeCountry === item.country ? " active" : ""
              }`}
              key={item.country}
              type="button"
              onBlur={() => setActiveCountry(null)}
              onClick={() => setActiveCountry(item.country)}
              onFocus={() => setActiveCountry(item.country)}
              onMouseEnter={() => setActiveCountry(item.country)}
              onMouseLeave={() => setActiveCountry(null)}
            >
              <span className="country-label">
                <i style={{ backgroundColor: item.color }} />
                {item.country}
              </span>
              <strong>{item.amount}</strong>
              <em>{item.pct}</em>
            </button>
          ))}
          <div className="country-row total">
            <span>Total</span>
            <strong>{totalAmount}</strong>
            <em>100%</em>
          </div>
        </div>
      </div>
    </Card>
  );
}

function WorldMap({
  activeCountry,
  data,
  onActive,
}: {
  activeCountry: string | null;
  data: CountryRwaData;
  onActive: (country: string | null) => void;
}) {
  const colorByCountry = new Map(data.map((item) => [item.country, item.color]));

  return (
    <svg
      className="world-map"
      viewBox="0 0 340 190"
      aria-label="World map by RWA country"
      onMouseLeave={() => onActive(null)}
    >
      <path className="map-sphere" d={pathGenerator({ type: "Sphere" }) ?? undefined} />
      {countryFeatures.map((country, index) => {
        const numericId = String(country.id ?? "");
        const countryName = countryByNumericId[numericId] ?? "Others";
        const isTopCountry = Boolean(countryByNumericId[numericId]);
        const isActive =
          activeCountry === countryName || (activeCountry === "Others" && !isTopCountry);
        const isMuted = Boolean(activeCountry && !isActive);
        const path = pathGenerator(country);

        if (!path) {
          return null;
        }

        return (
          <path
            aria-label={country.properties.name ?? countryName}
            className={`map-region${isTopCountry ? " top-country" : ""}${
              isActive ? " active" : ""
            }${isMuted ? " muted" : ""}`}
            d={path}
            fill={colorByCountry.get(countryName) ?? "#d7e7fc"}
            key={`${numericId || country.properties.name || "country"}-${index}`}
            onBlur={() => onActive(null)}
            onFocus={() => onActive(countryName)}
            onMouseEnter={() => onActive(countryName)}
            tabIndex={0}
          />
        );
      })}
    </svg>
  );
}

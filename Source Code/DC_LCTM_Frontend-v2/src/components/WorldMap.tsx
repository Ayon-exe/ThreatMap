/**
 * WorldMap component that displays a world map with attack vectors and malicious IP markers
 * Uses react-simple-maps for rendering the map and handles country hover interactions
 */
import React, { useMemo } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
  Marker,
} from "react-simple-maps";
import { Country, MaliciousIP, Attack } from "../types";
import { countries } from "../data/countries";
import AttackVector from "./AttackVector";

interface WorldMapProps {
  width: number;
  height: number;
  onCountryHover?: (country: Country | null) => void;
  maliciousIPs: MaliciousIP[];
  attacks: Attack[];
}

const WorldMap: React.FC<WorldMapProps> = ({
  width,
  height,
  onCountryHover,
  maliciousIPs,
  attacks,
}) => {
  /**
   * Handles country hover events and finds the corresponding country data
   * @param geo - The geography object from react-simple-maps
   */
  const handleCountryHover = (geo: any) => {
    if (geo) {
      const country = countries.find((c) => c.code === geo.properties.iso_a2);
      onCountryHover?.(country || null);
    } else {
      onCountryHover?.(null);
    }
  };

  // Memoize the geography data URL to prevent unnecessary re-renders
  const geographyUrl = useMemo(
    () => "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json",
    []
  );

  return (
    <div className="relative w-full h-full bg-[#111827] rounded-lg overflow-hidden top-16">
      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: width / 2.01 / Math.PI,
          center: [0, 30],
        }}
        width={width}
        height={height}
        style={{
          backgroundColor: "#111827",
        }}
      >
        <ZoomableGroup>
          {/* Clipping mask for the visible area to prevent overflow */}
          <defs>
            <clipPath id="map-clip">
              <rect width={width} height={height} />
            </clipPath>
          </defs>

          {/* Render world map geography */}
          <Geographies geography={geographyUrl}>
            {({ geographies }) =>
              geographies
                .filter((geo) => geo.properties.name !== "Antarctica")
                .map((geo) => (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    onMouseEnter={() => handleCountryHover(geo)}
                    onMouseLeave={() => handleCountryHover(null)}
                    style={{
                      default: {
                        fill: "#1E293B",
                        stroke: "#334155",
                        strokeWidth: 0.75,
                        outline: "none",
                        transition: "all 250ms",
                      },
                      hover: {
                        fill: "#2D3B4F",
                        stroke: "#475569",
                        strokeWidth: 1,
                        outline: "none",
                        cursor: "pointer",
                      },
                      pressed: {
                        fill: "#334155",
                        stroke: "#64748B",
                        strokeWidth: 1,
                        outline: "none",
                      },
                    }}
                    clipPath="url(#map-clip)"
                  />
                ))
            }
          </Geographies>

          {/* Render attack vectors with clipping mask */}
          <g clipPath="url(#map-clip)">
            {attacks.map((attack) => (
              <AttackVector key={attack.id} attack={attack} />
            ))}
          </g>

          {/* Render malicious IP markers with clipping mask */}
          <g clipPath="url(#map-clip)">
            {maliciousIPs.map((ip, index) => (
              <Marker
                key={`${ip.latitude}-${ip.longitude}-${index}`}
                coordinates={[ip.longitude, ip.latitude]}
              >
                <circle
                  r={1.7}
                  fill="#EF4444"
                  style={{
                    transition: "all 250ms",
                  }}
                />
              </Marker>
            ))}
          </g>
        </ZoomableGroup>
      </ComposableMap>
    </div>
  );
};

export default WorldMap;

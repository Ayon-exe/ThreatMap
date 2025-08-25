/**
 * Main application component for the Live Cyber Threat Map
 * Displays real-time cyber attacks on a world map with attack details and statistics
 */
import { useState, useEffect, useRef } from "react";
import WorldMap from "./components/WorldMap";
import LogoDC from "./Image/logo_DC.png";
import Stats from "./components/Stats";
import { Attack, AttackSeverity, Country, MaliciousIP } from "./types";
import { fetchMaliciousIPsWithRetry } from "./data/maliciousIPs";
import { startThreatSSEConnection } from "./data/threatData";
import News from "./components/news";

function App() {
  // State management
  const [maliciousIPs, setMaliciousIPs] = useState<MaliciousIP[]>([]);
  const [hoveredCountry, setHoveredCountry] = useState<Country | null>(null);
  const [selectedSeverities, setSelectedSeverities] = useState<
    AttackSeverity[]
  >([
    AttackSeverity.LOW,
    AttackSeverity.MEDIUM,
    AttackSeverity.HIGH,
    AttackSeverity.CRITICAL,
  ]);
  const [attackDetails, setAttackDetails] = useState<Attack[]>([]); // For display in attack details panel
  const [currentAttacks, setCurrentAttacks] = useState<Attack[]>([]); // Current attacks being rendered on map

  // Refs for SSE connections and container dimensions
  const maliciousIPSSERef = useRef<EventSource | null>(null);
  const threatSSERef = useRef<EventSource | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  /**
   * Handle real-time threat data from Server-Sent Events (SSE)
   * Filters and processes incoming attack data
   */
  useEffect(() => {
    const handleThreats = (threats: Attack[]) => {
      // Filter threats based on severity and valid coordinates
      const validThreats = threats.filter(
        (attack) =>
          selectedSeverities.includes(attack.severity) &&
          attack.source.code !== "UNK" && // Filter out unknown source
          attack.target.code !== "UNK" && // Filter out unknown target
          attack.source.latitude !== 0 && // Ensure source coordinates are valid
          attack.source.longitude !== 0 &&
          attack.target.latitude !== 0 && // Ensure target coordinates are valid
          attack.target.longitude !== 0
      );

      // Update current attacks for map display
      setCurrentAttacks((prevAttacks) => [...prevAttacks, ...validThreats]);

      // Update attack details for display panel
      setAttackDetails((prev) => [...prev, ...validThreats]);
    };

    const handleError = (error: Event) => {
      console.error("Threat SSE Error:", error);
    };

    // Initialize SSE connection for threat data
    threatSSERef.current = startThreatSSEConnection(handleThreats, handleError);

    // Cleanup SSE connection on component unmount
    return () => {
      if (threatSSERef.current) {
        threatSSERef.current.close();
      }
    };
  }, [selectedSeverities]);

  /**
   * Fetch initial malicious IPs data
   */
  useEffect(() => {
    const fetchIPs = async () => {
      try {
        const ips = await fetchMaliciousIPsWithRetry();
        setMaliciousIPs(ips);
      } catch (error) {
        console.error("Error fetching malicious IPs:", error);
      }
    };

    fetchIPs();
  }, []);

  /**
   * Handle container dimensions for responsive layout
   */
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const { width, height } = containerRef.current.getBoundingClientRect();
        setDimensions({ width, height });
      }
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);

    return () => {
      window.removeEventListener("resize", updateDimensions);
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#111827] text-white">
      {/* Header with logo and title */}
      <header className="bg-[#000129] py-4 border-b border-gray-700 h-14">
        <div className="w-full px-4 relative h-full flex items-center justify-between">
          <div className="flex items-center">
            <img src={LogoDC} alt="Cyber Shield" className="h-13 w-14" />
          </div>
          <h1 className="text-3xl font-bold absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white">
            Live Cyber Threat Map
          </h1>
        </div>
      </header>

      <main className="w-full px-4">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Left sidebar with stats and news */}
          <div className="lg:col-span-2 space-y-4 mt-4">
            <Stats attacks={attackDetails} />
            <News />

            {/* Country hover information */}
            {hoveredCountry && (
              <div className="bg-gray-800 bg-opacity-80 backdrop-blur-sm p-4 rounded-lg border border-gray-700">
                <h3 className="font-medium mb-2">{hoveredCountry.name}</h3>
                <div className="text-sm text-gray-400">
                  <p>Lat: {hoveredCountry.latitude.toFixed(2)}</p>
                  <p>Long: {hoveredCountry.longitude.toFixed(2)}</p>
                </div>
              </div>
            )}
          </div>

          {/* Main map visualization */}
          <div
            ref={containerRef}
            className="lg:col-span-7 bg-[#111827] rounded-lg overflow-hidden relative"
            style={{ height: "85vh", minHeight: "85vh" }}
          >
            <WorldMap
              width={dimensions.width}
              height={dimensions.height}
              onCountryHover={setHoveredCountry}
              maliciousIPs={maliciousIPs}
              attacks={currentAttacks}
            />
          </div>

          {/* Right sidebar with attack details */}
          <div className="lg:col-span-3 space-y-4 mt-4">
            <div className="bg-gray-800 bg-opacity-80 backdrop-blur-sm p-4 rounded-lg border border-gray-700">
              <h3 className="font-bold mb-3">Attack Details</h3>
              <div className="space-y-2 max-h-800 overflow-y-auto">
                {attackDetails
                  .slice(-10)
                  .reverse()
                  .map((attack) => (
                    <div
                      key={attack.id}
                      className="p-2 bg-gray-700 bg-opacity-50 rounded hover:bg-gray-600 cursor-pointer transition-colors"
                    >
                      <div className="flex justify-between items-center">
                        <span className="font-medium">
                          {attack.source.name} → {attack.target.name}
                        </span>
                        <span
                          className={`text-xs px-1.5 py-0.5 rounded-full ${
                            attack.severity === AttackSeverity.CRITICAL
                              ? "bg-red-900 text-red-200"
                              : attack.severity === AttackSeverity.HIGH
                              ? "bg-orange-900 text-orange-200"
                              : attack.severity === AttackSeverity.MEDIUM
                              ? "bg-yellow-900 text-yellow-200"
                              : attack.severity === AttackSeverity.LOW
                              ? "bg-blue-900 text-blue-200"
                              : "bg-purple-900 text-purple-200"
                          }`}
                        >
                          {attack.severity}
                        </span>
                      </div>
                      <div className="text-xs text-gray-400 flex justify-between mt-1">
                        <span>{attack.type.join(", ")}</span>
                        <span>
                          {new Date(attack.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;

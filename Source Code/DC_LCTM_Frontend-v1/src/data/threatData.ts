/**
 * Threat Data Management
 * Handles real-time threat data through Server-Sent Events (SSE)
 * Converts raw SSE data into application-specific Attack objects
 */
import { Attack, AttackType, AttackSeverity, Country } from "../types";
import { v4 as uuidv4 } from "uuid";

/**
 * Interface for raw threat data received from SSE
 */
interface RawSSEThreat {
  "Source Country Code": string;
  "Source Country Name": string;
  "Source Latitude": number | null;
  "Source Longitude": number | null;
  "Destination Country Code": string;
  "Destination Country Name": string;
  "Destination Latitude": number | null;
  "Destination Longitude": number | null;
  "Attack Count": number;
  "Attack Types": string[];
  Timestamp: string;
}

/**
 * Convert raw SSE threat data to our Attack type
 * @param rawThreat - Raw threat data from SSE
 * @returns Converted Attack object
 */
const convertSSEToAttack = (rawThreat: RawSSEThreat): Attack => {
  /**
   * Map severity level based on attack count
   * @param severity - Severity level as string
   * @returns Corresponding AttackSeverity enum value
   */
  const mapSeverity = (severity: string): AttackSeverity => {
    const severityMap: { [key: string]: AttackSeverity } = {
      "1": AttackSeverity.LOW,
      "2": AttackSeverity.LOW,
      "3": AttackSeverity.MEDIUM,
      "4": AttackSeverity.HIGH,
      "5": AttackSeverity.CRITICAL,
    };
    return severityMap[severity] || AttackSeverity.UNKNOWN;
  };

  // Create source country object with fallback values
  const source: Country = {
    code: rawThreat["Source Country Code"] || "UNK",
    name: rawThreat["Source Country Name"] || "Unknown",
    latitude: rawThreat["Source Latitude"] || 0,
    longitude: rawThreat["Source Longitude"] || 0,
  };

  // Create target country object with fallback values
  const target: Country = {
    code: rawThreat["Destination Country Code"] || "UNK",
    name: rawThreat["Destination Country Name"] || "Unknown",
    latitude: rawThreat["Destination Latitude"] || 0,
    longitude: rawThreat["Destination Longitude"] || 0,
  };

  // Create attack object with all available data
  return {
    id: uuidv4(),
    source,
    target,
    type: rawThreat["Attack Types"] as AttackType[],
    severity: mapSeverity(rawThreat["Attack Count"]?.toString() || "0"),
    timestamp: new Date(rawThreat["Timestamp"]),
  };
};

/**
 * Start Server-Sent Events connection for real-time threat data
 * @param onThreat - Callback function to handle incoming threats
 * @param onError - Callback function to handle connection errors
 * @returns EventSource instance for the SSE connection
 */
export const startThreatSSEConnection = (
  onThreat: (threats: Attack[]) => void,
  onError: (error: Event) => void
): EventSource => {
  const eventSource = new EventSource("http://localhost:5000/threats");

  // Handle incoming messages
  eventSource.onmessage = (event) => {
    try {
      const data = event.data;
      if (data === "[]") {
        onThreat([]);
        return;
      }

      const rawThreats: RawSSEThreat[] = JSON.parse(data);
      const threats = rawThreats.map(convertSSEToAttack);
      onThreat(threats);
    } catch (error) {
      console.error("Error parsing SSE data:", error);
    }
  };

  // Handle connection errors
  eventSource.onerror = (error) => {
    console.error("SSE Error:", error);
    onError(error);
    eventSource.close();
  };

  return eventSource;
};

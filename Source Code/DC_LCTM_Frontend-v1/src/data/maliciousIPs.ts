/**
 * Malicious IP Data Management
 * Handles generation and fetching of malicious IP data for the threat map
 */
import { v4 as uuidv4 } from "uuid";
import { MaliciousIP, AttackSeverity } from "../types";

/**
 * Interface for raw malicious IP data from the API
 */
interface RawMaliciousIP {
  ip: string;
  latitude: number;
  longitude: number;
  type: string;
}

/**
 * Convert raw API data to our MaliciousIP type
 * @param rawIP - Raw IP data from the API
 * @returns Converted MaliciousIP object
 */
const convertToMaliciousIP = (rawIP: RawMaliciousIP): MaliciousIP => {
  /**
   * Map severity string from API to AttackSeverity enum
   * @param type - Severity type from API
   * @returns Corresponding AttackSeverity enum value
   */
  const mapSeverity = (type: string): AttackSeverity => {
    const severityMap: { [key: string]: AttackSeverity } = {
      malicious: AttackSeverity.HIGH,
      default: AttackSeverity.MEDIUM,
    };
    return severityMap[type] || AttackSeverity.MEDIUM;
  };

  return {
    id: uuidv4(),
    ip: rawIP.ip,
    latitude: rawIP.latitude,
    longitude: rawIP.longitude,
    timestamp: new Date(),
    severity: mapSeverity(rawIP.type),
  };
};

/**
 * Fetch malicious IPs from the API
 * @returns Promise resolving to array of MaliciousIP objects
 */
export const fetchMaliciousIPs = async (): Promise<MaliciousIP[]> => {
  try {
    const response = await fetch("http://localhost:5000/malicious-ips");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const rawIPs: RawMaliciousIP[] = await response.json();
    return rawIPs.map(convertToMaliciousIP);
  } catch (error) {
    console.error("Error fetching malicious IPs:", error);
    return [];
  }
};

/**
 * Fetch malicious IPs with retry mechanism
 * @param maxRetries - Maximum number of retry attempts (default: 3)
 * @returns Promise resolving to array of MaliciousIP objects
 */
export const fetchMaliciousIPsWithRetry = async (
  maxRetries: number = 3
): Promise<MaliciousIP[]> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const ips = await fetchMaliciousIPs();
      if (ips.length > 0) {
        return ips;
      }
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      if (i === maxRetries - 1) {
        throw error;
      }
      // Wait for 1 second before retrying
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }
  return [];
};

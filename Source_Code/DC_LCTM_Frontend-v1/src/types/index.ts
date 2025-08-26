/**
 * Type definitions for the Live Cyber Threat Map application
 */

/**
 * Represents a country with its geographical information
 */
export interface Country {
  name: string; // Country name
  code: string; // ISO country code
  latitude: number; // Geographical latitude
  longitude: number; // Geographical longitude
}

/**
 * Represents a cyber attack with its source, target, and details
 */
export interface Attack {
  id: string; // Unique identifier for the attack
  source: Country; // Source country of the attack
  target: Country; // Target country of the attack
  type: AttackType[]; // Types of attack (can be multiple)
  severity: AttackSeverity; // Severity level of the attack
  timestamp: Date; // When the attack occurred
}

/**
 * Enumeration of possible cyber attack types
 */
export enum AttackType {
  DDOS = "DDoS Attack", // Distributed Denial of Service
  MALWARE = "Malware", // Malicious software
  PHISHING = "Phishing", // Phishing attempts
  RANSOMWARE = "Ransomware", // Ransomware attacks
  SQL_INJECTION = "SQL Injection", // SQL injection attacks
  XSS = "Cross-Site Scripting", // Cross-site scripting attacks
  ZERO_DAY = "Zero-Day Exploit", // Zero-day vulnerability exploits
  BRUTE_FORCE = "Brute Force", // Brute force attacks
}

/**
 * Enumeration of attack severity levels
 */
export enum AttackSeverity {
  CRITICAL = "Critical", // Most severe attacks
  HIGH = "High", // High severity attacks
  MEDIUM = "Medium", // Medium severity attacks
  LOW = "Low", // Low severity attacks
  UNKNOWN = "Unknown", // Severity not determined
}

/**
 * Represents a malicious IP address with its location and details
 */
export interface MaliciousIP {
  id: string; // Unique identifier for the IP
  ip: string; // IP address
  latitude: number; // Geographical latitude
  longitude: number; // Geographical longitude
  timestamp: Date; // When the IP was detected
  severity: AttackSeverity; // Severity level of the threat
}

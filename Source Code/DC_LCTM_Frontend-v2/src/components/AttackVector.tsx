/**
 * AttackVector component that renders an animated attack vector on the world map
 * Uses GSAP for smooth animations and handles path calculations for proper map display
 */
import React, { useEffect, useRef } from "react";
import { Line, Marker } from "react-simple-maps";
import { Attack, AttackSeverity } from "../types";
import gsap from "gsap";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";

// Register the MotionPathPlugin for GSAP animations
gsap.registerPlugin(MotionPathPlugin);

interface AttackVectorProps {
  attack: Attack;
}

/**
 * Returns the color associated with each attack severity level
 * @param severity - The severity level of the attack
 * @returns The hex color code for the severity
 */
const getSeverityColor = (severity: AttackSeverity): string => {
  switch (severity) {
    case AttackSeverity.CRITICAL:
      return "#dc2626";
    case AttackSeverity.HIGH:
      return "#ea580c";
    case AttackSeverity.MEDIUM:
      return "#ca8a04";
    case AttackSeverity.LOW:
      return "#2563eb";
    case AttackSeverity.UNKNOWN:
      return "#9333ea";
    default:
      return "#9333ea";
  }
};

const AttackVector: React.FC<AttackVectorProps> = ({ attack }) => {
  const color = getSeverityColor(attack.severity);
  const lineRef = useRef<SVGLineElement>(null);
  const markerRef = useRef<SVGGElement>(null);

  // Handle attack vector animation using GSAP
  useEffect(() => {
    if (!lineRef.current || !markerRef.current) return;

    const tl = gsap.timeline();

    // Set initial states for the line and marker
    gsap.set(lineRef.current, {
      strokeDasharray: "100%",
      strokeDashoffset: "100%",
      opacity: 1,
    });

    gsap.set(markerRef.current, {
      opacity: 1,
    });

    // Animate the marker (circle) to reach destination first
    tl.to(
      markerRef.current,
      {
        motionPath: {
          path: lineRef.current,
          align: lineRef.current,
          autoRotate: false,
          alignOrigin: [0.5, 0.5],
          start: 0,
          end: 1,
        },
        duration: 0.8, // Marker moves faster
        ease: "power2.inOut",
      },
      0
    )
      // Animate the line drawing slightly after
      .to(
        lineRef.current,
        {
          start: 0,
          strokeDashoffset: 0,
          duration: 1,
          ease: "power2.inOut",
          opacity: 1,
        },
        0.0 // Slight delay to keep line close to marker
      )
      // Fade both out together
      .to(
        [lineRef.current, markerRef.current],
        {
          opacity: 0,
          duration: 0.3,
        },
        "+=0.2" // Adjusted delay to ensure animation lasts 5 seconds
      );

    return () => {
      tl.kill();
    };
  }, [attack.id]);

  /**
   * Calculates the direct path between source and target coordinates
   * Ensures the path stays within visible map bounds and handles date line crossing
   * @returns The normalized path coordinates or null if path is invalid
   */
  const getDirectPath = () => {
    let fromLng = attack.source.longitude;
    let toLng = attack.target.longitude;
    const fromLat = attack.source.latitude;
    const toLat = attack.target.latitude;

    // Normalize longitude to [-180, 180] range
    const normalizeLng = (lng: number) => {
      while (lng > 180) lng -= 360;
      while (lng < -180) lng += 360;
      return lng;
    };

    fromLng = normalizeLng(fromLng);
    toLng = normalizeLng(toLng);

    // Define strict visible bounds for the map
    const MAP_LNG_MIN = -180;
    const MAP_LNG_MAX = 180;
    const MAP_LAT_MIN = -85;
    const MAP_LAT_MAX = 85;

    // Clamp coordinates to visible bounds
    fromLng = Math.max(MAP_LNG_MIN, Math.min(MAP_LNG_MAX, fromLng));
    toLng = Math.max(MAP_LNG_MIN, Math.min(MAP_LNG_MAX, toLng));
    const fromLatClamped = Math.max(
      MAP_LAT_MIN,
      Math.min(MAP_LAT_MAX, fromLat)
    );
    const toLatClamped = Math.max(MAP_LAT_MIN, Math.min(MAP_LAT_MAX, toLat));

    // Calculate the direct path difference
    let lngDiff = toLng - fromLng;

    // Handle date line crossing
    if (lngDiff > 180) {
      toLng = toLng - 360;
    } else if (lngDiff < -180) {
      toLng = toLng + 360;
    }

    // Final bounds check: ensure both endpoints are within visible area
    if (toLng < MAP_LNG_MIN || toLng > MAP_LNG_MAX) {
      return null;
    }

    // Additional check: ensure the line won't curve outside bounds
    const pathLength = Math.abs(toLng - fromLng);
    const pathHeight = Math.abs(toLatClamped - fromLatClamped);

    if (pathLength > 170 || pathHeight > 160) {
      return null;
    }

    return {
      from: [fromLng, fromLatClamped],
      to: [toLng, toLatClamped],
    };
  };

  const pathResult = getDirectPath();

  if (!pathResult) {
    return null;
  }

  const { from, to } = pathResult;

  return (
    <>
      {/* Attack vector line */}
      <Line
        ref={lineRef as any}
        from={from as [number, number]}
        to={to as [number, number]}
        stroke={color}
        strokeWidth={1.2}
        strokeLinecap="round"
        strokeDasharray="100%"
        strokeDashoffset="100%"
        style={{
          opacity: 1,
        }}
      />
      {/* Attack marker */}
      <Marker ref={markerRef as any} coordinates={from as [number, number]}>
        <circle
          r={2}
          fill={color}
          stroke="#ffffff"
          strokeWidth={0.5}
          style={{
            opacity: 1,
          }}
        />
      </Marker>
    </>
  );
};

export default React.memo(AttackVector);

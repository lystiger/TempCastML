import { useEffect, useRef, useState } from "react";

const prefersReducedMotion = () =>
  typeof window !== "undefined" &&
  window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

/**
 * Smoothly animate a number toward `target` (eased). Re-animates from the
 * current displayed value whenever the target changes, so live updates glide
 * instead of snapping.
 */
export function useCountUp(target, { duration = 900, digits = 1 } = {}) {
  const [value, setValue] = useState(target ?? 0);
  const fromRef = useRef(target ?? 0);
  const rafRef = useRef(0);

  useEffect(() => {
    if (target == null || Number.isNaN(target)) return;
    if (prefersReducedMotion()) {
      setValue(target);
      fromRef.current = target;
      return;
    }

    const from = fromRef.current;
    const start = performance.now();

    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
      const next = from + (target - from) * eased;
      setValue(next);
      if (t < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        fromRef.current = target;
      }
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [target, duration]);

  const safe = value == null || Number.isNaN(value) ? 0 : value;
  return safe.toFixed(digits);
}

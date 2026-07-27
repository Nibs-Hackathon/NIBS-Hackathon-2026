import { useEffect, useState } from 'react';
import { motion, useReducedMotion } from 'motion/react';

// Compact local adaptations of Magic UI primitives, kept intentionally neutral for RigOS.
export function NumberTicker({ value, prefix = '', suffix = '' }) {
  const reduced = useReducedMotion();
  const target = Number(value) || 0;
  const [display, setDisplay] = useState(reduced ? target : 0);

  useEffect(() => {
    if (reduced) return undefined;
    let frame;
    const origin = display;
    const started = performance.now();
    const update = (time) => {
      const progress = Math.min((time - started) / 220, 1);
      setDisplay(origin + ((target - origin) * (1 - ((1 - progress) ** 3))));
      if (progress < 1) frame = requestAnimationFrame(update);
    };
    frame = requestAnimationFrame(update);
    return () => cancelAnimationFrame(frame);
  // This intentionally starts from the rendered value when live telemetry changes.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, reduced]);

  return <>{prefix}{Math.round(reduced ? target : display).toLocaleString()}{suffix}</>;
}

export function AnimatedBorder({ children, className = '' }) {
  const reduced = useReducedMotion();
  return <div className={`animated-border ${className}`}><motion.span aria-hidden="true" className="animated-border-runner" initial={false} animate={reduced ? { x: '0%' } : { x: ['-105%', '205%'] }} transition={{ duration: 2.8, ease: 'linear', repeat: Infinity, repeatDelay: 3.5 }} />{children}</div>;
}

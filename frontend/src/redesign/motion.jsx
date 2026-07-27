import { forwardRef, useEffect, useState } from 'react';
import { motion, useReducedMotion } from 'motion/react';

/** Part 8 — page transition is 120ms fade only (no layout bounce). */
const enter = { duration: 0.12, ease: 'easeOut' };

export function PageMotion({ children, pageKey }) {
  const reduced = useReducedMotion();
  return <motion.div key={pageKey} initial={reduced ? false : { opacity: 0 }} animate={{ opacity: 1 }} transition={enter}>{children}</motion.div>;
}

export function Reveal({ children, delay = 0, className }) {
  const reduced = useReducedMotion();
  return <motion.div className={className} initial={reduced ? false : { opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.15 }} transition={{ ...enter, delay }}>{children}</motion.div>;
}

export function AnimatedNumber({ value, prefix = '', suffix = '' }) {
  const reduced = useReducedMotion();
  const number = Number(value) || 0;
  const [shown, setShown] = useState(reduced ? number : 0);

  useEffect(() => {
    if (reduced) return undefined;
    let frame;
    const initial = shown;
    const start = performance.now();
    const duration = 220;
    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - (1 - progress) ** 3;
      setShown(initial + ((number - initial) * eased));
      if (progress < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  // `shown` deliberately does not restart the count while an animation runs.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [number, reduced]);

  return <>{prefix}{Math.round(reduced ? number : shown).toLocaleString()}{suffix}</>;
}

export const DialogMotion = forwardRef(function DialogMotion(props, ref) {
  const { children, in: open, onEnter, onExited, ...rest } = props;
  const reduced = useReducedMotion();
  useEffect(() => { if (open) onEnter?.(); else onExited?.(); }, [open, onEnter, onExited]);
  return <motion.div ref={ref} {...rest} initial={false} animate={open ? { opacity: 1, scale: 1 } : { opacity: 0, scale: reduced ? 1 : 0.98 }} transition={{ duration: reduced ? 0 : 0.18, ease: [0.16, 1, 0.3, 1] }}>{children}</motion.div>;
});

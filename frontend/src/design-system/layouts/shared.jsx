import { useEffect, useState } from 'react';
import { Box } from '@mui/material';

const COMPACT_MQ = '(max-width: 1023px)';

/** True when layout should use tab collapse (<1024px). */
export function useCompactLayout() {
  const [compact, setCompact] = useState(() => (
    typeof window !== 'undefined' ? window.matchMedia(COMPACT_MQ).matches : false
  ));

  useEffect(() => {
    const media = window.matchMedia(COMPACT_MQ);
    const onChange = () => setCompact(media.matches);
    onChange();
    media.addEventListener('change', onChange);
    return () => media.removeEventListener('change', onChange);
  }, []);

  return compact;
}

/** Slot placeholder for layout previews / empty slots */
export function LayoutPlaceholder({ label = 'Slot', className = '', sx }) {
  return (
    <Box className={`rig-layout-placeholder ${className}`} sx={sx}>
      {label}
    </Box>
  );
}

/** Mobile tab strip for compact layouts */
export function LayoutTabs({ tabs = [], value, onChange, className = '' }) {
  return (
    <Box className={`rig-layout-tabs ${className}`} role="tablist">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          type="button"
          role="tab"
          aria-selected={value === tab.id}
          className={value === tab.id ? 'is-active' : ''}
          onClick={() => onChange?.(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </Box>
  );
}

export function Pane({ children, className = '', bodyClassName = '', sx }) {
  return (
    <Box className={`rig-layout-pane ${className}`} sx={sx}>
      <Box className={`rig-layout-pane-body ${bodyClassName}`}>{children}</Box>
    </Box>
  );
}

import { useMemo } from 'react';
import DotMatrixGlobe from '../../components/react-bits/DotMatrixGlobe';
import '../../components/react-bits/DotMatrixGlobe.css';
import { round } from './shared';

function isEnterpriseScope(facility) {
  return !facility || facility === 'Enterprise view' || facility === 'portfolio' || facility === 'North Sea Portfolio';
}

/** Dot-matrix Earth with refinery cluster highlight for Command Center. */
export function FacilityGlobe({ facility, refineries = [], fleetHealth = null }) {
  const enterprise = isEnterpriseScope(facility);
  const sites = useMemo(
    () => (Array.isArray(refineries) ? refineries : []).filter(
      (row) => row?.lat != null && row?.lng != null,
    ),
    [refineries],
  );

  const focusSite = useMemo(
    () => (enterprise
      ? sites.slice().sort((a, b) => Number(a.fleet_health ?? 100) - Number(b.fleet_health ?? 100))[0]
      : sites.find((row) => row.name === facility) || sites[0]),
    [enterprise, facility, sites],
  );

  const caption = enterprise && sites.length
    ? `${sites.length} facilities worldwide`
    : focusSite?.display_location || 'Location metadata unavailable';

  const reducedMotion = useMemo(
    () => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    [],
  );

  return (
    <div className="facility-globe" aria-label={caption}>
      <DotMatrixGlobe
        sites={sites}
        focusName={focusSite?.name ?? null}
        enterprise={enterprise}
        fleetHealth={fleetHealth == null ? null : round(fleetHealth)}
        caption={caption}
        reducedMotion={reducedMotion}
      />
    </div>
  );
}

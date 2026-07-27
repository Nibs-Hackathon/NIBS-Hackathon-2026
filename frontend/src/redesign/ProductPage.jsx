/* Epic 6 — thin product page: facility scope + lazy workspace views */
import { Suspense, lazy, useEffect } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';
import { useOperations } from '../context/OperationsContext';
import { useObjectContext } from '../context/ObjectContext';
import { filterByFacility, assetLocation, incidentLocation, taskLocation } from '../context/objectNavigation';
import { inferProvenance, useOperatorAudit } from './accountability';
import { PageMotion } from './motion';

const MissionControlOS = lazy(() => import('./views/MissionControlOS').then((m) => ({ default: m.MissionControlOS })));
const AssetConsole = lazy(() => import('./views/AssetConsole').then((m) => ({ default: m.AssetConsole })));
const IncidentManagement = lazy(() => import('./views/IncidentManagement').then((m) => ({ default: m.IncidentManagement })));
const AIInvestigationOS = lazy(() => import('./views/AIInvestigationOS').then((m) => ({ default: m.AIInvestigationOS })));
const MaintenancePlanning = lazy(() => import('./views/MaintenancePlanning').then((m) => ({ default: m.MaintenancePlanning })));
const ForecastTerminal = lazy(() => import('./views/ForecastTerminal').then((m) => ({ default: m.ForecastTerminal })));
const ExecutiveBriefing = lazy(() => import('./views/ExecutiveBriefing').then((m) => ({ default: m.ExecutiveBriefing })));

const config = {
  '/': ['Command center', 'A concise view of facility condition, AI operations, and decisions requiring your attention.'],
  '/assets': ['Critical assets', 'The equipment currently creating the greatest operational and financial exposure.'],
  '/incident-simulator': ['Incident center', 'A traceable record of incidents, AI evidence, and operator decisions.'],
  '/agent-monitor': ['AI investigation', 'Supervise the active reasoning workflow before authorizing a response.'],
  '/maintenance': ['Maintenance', 'Work prioritized by operational risk, asset condition, and AI recommendations.'],
  '/health-prediction': ['Health forecasting', 'A forward-looking view of asset health and intervention timing.'],
  '/reports': ['Executive reports', 'Decision-ready incident outcomes and AI execution records.'],
};

function WorkspaceFallback() {
  return (
    <Box className="e6-workspace-fallback" role="status" aria-live="polite" sx={{ display: 'grid', placeItems: 'center', minHeight: 240, gap: 1.5 }}>
      <CircularProgress size={28} />
      <Typography color="text.secondary">Loading workspace…</Typography>
    </Box>
  );
}

export function ProductPage() {
  const { pathname } = useLocation();
  const { operations, connected, ambient } = useOperations();
  const objectApi = useObjectContext();
  const facility = objectApi.scope?.facility || 'Enterprise view';
  const auditEvents = useOperatorAudit(objectApi, operations);
  const syncAge = ambient?.lastUpdated
    ? Math.round((Date.now() - ambient.lastUpdated) / 1000)
    : (connected ? 0 : 60);
  const dataProvenance = inferProvenance({ connected, syncAge });
  const [title, description] = config[pathname] || config['/'];
  useEffect(() => {
    if (pathname === '/assets' || ['/incident-simulator', '/agent-monitor', '/maintenance', '/health-prediction'].includes(pathname)) {
      document.querySelector('#main-content')?.focus?.({ preventScroll: true });
      return;
    }
    const heading = document.querySelector('.product-hero h1');
    heading?.focus?.({ preventScroll: true });
  }, [pathname]);

  const assetsAll = operations.assets || [];
  const assets = filterByFacility(assetsAll, facility, assetLocation);
  const incidents = filterByFacility(
    operations.critical_incidents || [],
    facility,
    (item) => incidentLocation(item, assetsAll),
  );
  const auditLogs = filterByFacility(
    operations.audit_logs || [],
    facility,
    (item) => incidentLocation(item, assetsAll),
  );
  const tasks = filterByFacility(
    operations.maintenance?.tasks || [],
    facility,
    (item) => taskLocation(item, assetsAll),
  );
  const predicted = filterByFacility(
    operations.predicted_failures || [],
    facility,
    assetLocation,
  );
  const activeInvestigationIncident = auditLogs.find(
    (item) => item.id === operations.investigation?.incident?.id || item.id === objectApi.selection.incidentId,
  ) || operations.investigation?.incident || incidents[0] || auditLogs[0];
  const stages = operations.investigation?.stages || [];
  const telemetry = operations.telemetry || { readings: [] };
  const maintenance = { ...(operations.maintenance || {}), tasks };
  const hideHero = ['/assets', '/incident-simulator', '/agent-monitor', '/maintenance', '/health-prediction'].includes(pathname);
  const opsClass = hideHero ? ' is-ops-os' : '';
  const assetsClass = pathname === '/assets' ? ' is-assets-os' : '';

  return (
    <PageMotion pageKey={pathname}>
      <Box className={`product-page${opsClass}${assetsClass}`}>
        {!hideHero && (
          <Box className="product-hero">
            <Typography className="product-kicker">{facility.toUpperCase()} - LIVE OPERATIONS</Typography>
            <Typography component="h1" tabIndex={-1}>{title}</Typography>
            <Typography>{description}</Typography>
          </Box>
        )}
        <Suspense fallback={<WorkspaceFallback />}>
          {pathname === '/' && (
            <MissionControlOS
              assets={assets}
              incidents={incidents}
              stages={stages}
              dashboard={operations.dashboard || {}}
              projection={operations.revenue_projection}
              refineries={operations.refineries || []}
              telemetry={telemetry}
              maintenance={maintenance}
              facility={facility}
              auditEvents={auditEvents}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/assets' && (
            <AssetConsole
              assets={assets}
              incidents={auditLogs}
              telemetry={telemetry}
              telemetryStreams={operations.critical_asset_telemetry || []}
              maintenance={maintenance}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/incident-simulator' && (
            <IncidentManagement incidents={auditLogs} telemetry={telemetry} provenance={dataProvenance} />
          )}
          {pathname === '/agent-monitor' && (
            <AIInvestigationOS
              stages={stages}
              investigation={operations.investigation || {}}
              incident={activeInvestigationIncident}
              telemetry={telemetry}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/maintenance' && <MaintenancePlanning maintenance={maintenance} />}
          {pathname === '/health-prediction' && (
            <ForecastTerminal
              assets={predicted}
              telemetry={telemetry}
              telemetryStreams={operations.critical_asset_telemetry || []}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/reports' && <ExecutiveBriefing reports={operations.reports || []} />}
        </Suspense>
      </Box>
    </PageMotion>
  );
}

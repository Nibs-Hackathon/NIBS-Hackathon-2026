/* Epic 6 — thin product page: facility scope + lazy workspace views */
import { Suspense, lazy, useEffect, useMemo } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';
import { useOperations } from '../context/OperationsContext';
import { useObjectContext } from '../context/ObjectContext';
import {
  filterByFacility, assetLocation, incidentLocation, taskLocation, reportLocation, activityLocation,
} from '../context/objectNavigation';
import {
  enrichRefineryGeo,
  fleetHealthForScope,
  refineriesForFacility,
  telemetryForFacility,
} from '../api/resourceAdapters';
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
  const { operations, connected } = useOperations();
  const objectApi = useObjectContext();
  const facility = objectApi.scope.facility || 'Enterprise view';
  const enterpriseScope = facility === 'Enterprise view'
    || facility === 'portfolio'
    || facility === 'North Sea Portfolio';
  const auditEvents = useOperatorAudit(objectApi, operations);
  const syncAge = connected ? 0 : 60;
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
  const predictedById = new Map(predicted.map((asset) => [asset.id, asset]));
  const forecastAssets = assets.map((asset) => ({
    ...asset,
    ...(predictedById.get(asset.id) || {}),
  }));
  const currentInvestigationIncident = operations.investigation?.incident;
  const currentInvestigationMatchesScope = enterpriseScope
    || incidentLocation(currentInvestigationIncident, assetsAll) === facility;
  const activeInvestigationIncident = auditLogs.find(
    (item) => item.id === operations.investigation?.incident?.id || item.id === objectApi.selection.incidentId,
  ) || incidents[0] || auditLogs[0] || (currentInvestigationMatchesScope ? currentInvestigationIncident : null);
  const stages = currentInvestigationMatchesScope ? (operations.investigation?.stages || []) : [];
  const scopedInvestigation = currentInvestigationMatchesScope ? (operations.investigation || {}) : {};
  const sourceRefineries = operations.refineries;
  const refineriesAll = useMemo(
    () => enrichRefineryGeo(sourceRefineries || []),
    [sourceRefineries],
  );
  const reports = filterByFacility(
    operations.reports || [],
    facility,
    (item) => reportLocation(item, assetsAll),
  );
  const aiActivity = filterByFacility(
    operations.ai_activity || [],
    facility,
    (item) => activityLocation(item, assetsAll),
  );
  const refineries = refineriesForFacility(refineriesAll, facility);
  const telemetry = telemetryForFacility(operations, facility);
  const dashboard = {
    ...(operations.dashboard || {}),
    fleet_health: fleetHealthForScope(
      { refineries: refineriesAll, assets, dashboard: operations.dashboard || {} },
      facility,
    ),
  };
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
              aiActivity={aiActivity}
              dashboard={dashboard}
              refineries={refineries}
              refineriesAll={refineriesAll}
              telemetry={telemetry}
              maintenance={maintenance}
              simulation={operations.simulation}
              facility={facility}
              auditEvents={auditEvents}
              provenance={dataProvenance}
              connected={connected}
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
            <IncidentManagement
              assets={assets}
              incidents={auditLogs}
              telemetry={telemetry}
              simulation={operations.simulation}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/agent-monitor' && (
            <AIInvestigationOS
              stages={stages}
              investigation={scopedInvestigation}
              incident={activeInvestigationIncident}
              telemetry={telemetry}
              aiActivity={aiActivity}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/maintenance' && <MaintenancePlanning maintenance={maintenance} />}
          {pathname === '/health-prediction' && (
            <ForecastTerminal
              assets={forecastAssets}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/reports' && (
            <ExecutiveBriefing
              reports={reports}
              operatorActions={operations.operator_actions || []}
            />
          )}
        </Suspense>
      </Box>
    </PageMotion>
  );
}

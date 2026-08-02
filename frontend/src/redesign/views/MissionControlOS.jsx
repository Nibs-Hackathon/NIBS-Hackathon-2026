import { useMemo } from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import { BoltOutlined, HubOutlined, PlaceOutlined, ShieldOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { OperationsStrip } from '../../design-system/catalog/shell';
import {
  Grid,
  LiveLine,
  LiveLineChart,
  LiveXAxis,
  LiveYAxis,
} from '@/components/charts';
import { ExportAuditButton } from '../accountability';
import { FacilityGlobe } from './FacilityGlobe';
import { Metric, Status, label, round, safeReasoning, traceLabel } from './shared';
import {
  normalizeAgentActivityRow,
  telemetryToLivePoints,
} from '../../api/resourceAdapters';

/** Part 8 — Command Center with sticky OperationsStrip + cross-nav. */
export function MissionControlOS({
  assets, incidents, stages, dashboard, refineries, refineriesAll, telemetry, maintenance, simulation,
  aiActivity = [],
  facility = null, auditEvents = [], provenance = 'live', connected = false,
}) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const safeAssets = useMemo(
    () => (Array.isArray(assets) ? assets : []),
    [assets],
  );
  const safeIncidents = Array.isArray(incidents) ? incidents : [];
  const safeStages = Array.isArray(stages) ? stages : [];
  const safeRefineries = Array.isArray(refineries) ? refineries : [];
  const globeRefineries = Array.isArray(refineriesAll) && refineriesAll.length
    ? refineriesAll
    : safeRefineries;
  const scopedHealthReadings = useMemo(
    () => safeAssets
      .map((asset) => asset?.health)
      .filter((health) => health != null && health !== '')
      .map(Number)
      .filter(Number.isFinite),
    [safeAssets],
  );
  // Prefer the live scoped asset average; dashboard.fleet_health is the backend fallback.
  const health = scopedHealthReadings.length
    ? round(scopedHealthReadings.reduce((sum, value) => sum + value, 0) / scopedHealthReadings.length)
    : dashboard.fleet_health != null && Number.isFinite(Number(dashboard.fleet_health))
      ? Number(dashboard.fleet_health)
      : null;
  const healthDisplay = health == null ? '—' : `${round(health)}%`;
  const primary = safeIncidents[0];
  const telemetryReadings = telemetry?.readings;
  const sensorReadings = useMemo(
    () => (Array.isArray(telemetryReadings) ? telemetryReadings : []),
    [telemetryReadings],
  );
  const livePoints = useMemo(() => telemetryToLivePoints(sensorReadings), [sensorReadings]);
  const latestValue = livePoints.length ? livePoints[livePoints.length - 1].value : 0;
  const values = useMemo(
    () => sensorReadings.map((item) => item.value).filter((value) => Number.isFinite(Number(value))),
    [sensorReadings],
  );
  const risks = useMemo(
    () => safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health)).slice(0, 4),
    [safeAssets],
  );
  const tasks = Array.isArray(maintenance?.tasks) ? maintenance.tasks : [];
  const activityRows = useMemo(
    () => (Array.isArray(aiActivity) ? aiActivity : [])
      .map(normalizeAgentActivityRow)
      .filter(Boolean),
    [aiActivity],
  );
  const activeFacility = facility || objectApi.scope?.facility || 'Enterprise view';
  const enterpriseScope = !activeFacility
    || activeFacility === 'Enterprise view'
    || activeFacility === 'portfolio'
    || activeFacility === 'North Sea Portfolio';
  const scopeLabel = (
    activeFacility
    || safeRefineries[0]?.name
    || 'Enterprise view'
  ).toUpperCase();
  const focusRefinery = globeRefineries.find((row) => row.name === activeFacility)
    || safeRefineries.find((row) => row.name === activeFacility)
    || globeRefineries[0]
    || safeRefineries[0];
  const agentsLive = safeStages.filter((s) => /running|streaming/i.test(s.state)).length;
  const telemetryLive = values.length > 0;
  const systemsLive = connected && (provenance === 'live' || provenance === 'estimated');
  const pendingDecisions = safeIncidents.filter((item) => {
    const status = String(item.status || '').toLowerCase();
    return !status || !/closed|resolved|complete/.test(status);
  }).length;

  const openInvestigation = () => {
    if (!primary) {
      navigateTo(objectApi, navigate, 'assets');
      return;
    }
    navigateTo(objectApi, navigate, 'investigation', {
      incidentId: primary.id,
      assetId: primary.asset_id || null,
      focusDecisionBar: true,
    });
  };

  return (
    <Box className="mission-os">
      <OperationsStrip
        className="p8-operations-strip"
        metrics={[
          { label: 'Fleet health', value: healthDisplay, detail: health == null ? 'Awaiting asset health' : `${scopedHealthReadings.length} live assets` },
          { label: 'Active incidents', value: String(safeIncidents.length), detail: primary ? label(primary.severity || 'open') : 'Clear' },
          { label: 'Agents live', value: String(safeStages.filter((s) => /running|streaming/i.test(s.state)).length), detail: 'MAO network' },
          { label: 'Work orders', value: String(tasks.length), detail: tasks.length ? 'Planned window' : 'No downtime' },
        ]}
        cta={(
          <Button variant="contained" onClick={openInvestigation}>
            {primary ? 'Review investigation' : 'Open digital twin'}
          </Button>
        )}
      />

      <Paper className={`mission-situation ${primary ? 'attention' : ''}`}>
        <Box>
          <Typography className="product-kicker">{`LIVE SITUATION · ${scopeLabel}`}</Typography>
          <Typography className="mission-situation-title">
            {primary
              ? `${label(primary.incident_type || 'Operating condition')} requires an operator decision.`
              : safeAssets.length
                ? `${safeAssets.length} assets in scope · no open critical incidents.`
                : 'No assets in the current facility scope.'}
          </Typography>
          <Typography>
            {primary
              ? `${primary.asset_name || 'Affected asset'} · ${label(primary.severity || 'active')} severity · evidence is streaming to the investigation record.`
              : `${safeAssets.length} connected assets · monitoring via operations live.`}
          </Typography>
        </Box>
        <Box className="mission-situation-actions">
          <Typography><i />{systemsLive ? 'SYSTEMS LIVE' : provenance === 'stale' ? 'SYSTEMS STALE' : 'SYSTEMS OFFLINE'}</Typography>
          {simulation?.automatic && (
            <Typography title={simulation.next_facility || ''}>
              <i />
              AUTO SCENARIOS · {simulation.incidents_generated || 0} RUN
              {simulation.portfolio_facilities
                ? ` · ${simulation.facilities_covered || 0}/${simulation.portfolio_facilities} SITES`
                : ''}
            </Typography>
          )}
          <ExportAuditButton events={auditEvents} facility={facility} />
          <Button variant="contained" onClick={openInvestigation}>
            {primary ? 'Review investigation' : 'Open digital twin'}
          </Button>
        </Box>
      </Paper>

      <Box className="mission-bento-grid">
        <Paper className="mission-twin mission-bento-globe">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">DIGITAL TWIN OVERVIEW</Typography>
              <Typography>Facility operating map</Typography>
            </Box>
            <Box className="mission-globe-actions">
              <Status state={primary ? 'Attention' : 'Nominal'} />
            </Box>
          </Box>
          <FacilityGlobe
            facility={activeFacility}
            refineries={globeRefineries}
            fleetHealth={health}
          />
          <Box className="mission-twin-footer">
            <Box>
              <PlaceOutlined />
              <span><small>SCOPE</small><b>{enterpriseScope ? 'Global portfolio' : focusRefinery?.display_location || activeFacility}</b></span>
            </Box>
            <Box>
              <HubOutlined />
              <span><small>CONNECTED ASSETS</small><b>{safeAssets.length || 'Awaiting data'}</b></span>
            </Box>
            <Box>
              <BoltOutlined />
              <span><small>HISTORIAN</small><b>{values.length ? `${values.length} samples` : 'Waiting for stream'}</b></span>
            </Box>
            <Box className={primary ? 'is-alert' : 'is-clear'}>
              <ShieldOutlined />
              <span><small>INCIDENT STATE</small><b>{primary ? `${label(primary.severity)} open` : 'No critical incidents'}</b></span>
            </Box>
          </Box>
        </Paper>

        <Paper className="mission-telemetry-panel mission-bento-telemetry">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">LIVE TELEMETRY</Typography>
              <Typography>Operating envelope</Typography>
            </Box>
            <Typography className="mission-live">
              <i />
              {telemetryLive ? 'STREAMING' : 'IDLE'}
            </Typography>
          </Box>
          <Box className="mission-chart-wrap mission-live-chart">
            {livePoints.length ? (
              <LiveLineChart
                data={livePoints}
                value={latestValue}
                window={120}
                nowOffsetUnits={1}
                margin={{ top: 14, right: 66, bottom: 30, left: 34 }}
                style={{ height: '100%' }}
              >
                <Grid horizontal numTicksRows={4} strokeOpacity={0.26} hideHorizontalEdgeLines />
                <LiveLine
                  dataKey="value"
                  stroke="var(--chart-line-primary, #55d6ff)"
                  strokeWidth={1.7}
                  dotSize={3}
                  formatValue={(v) => `${round(v)}${telemetry?.unit ? ` ${telemetry.unit}` : ''}`}
                />
                <LiveXAxis numTicks={4} />
                <LiveYAxis
                  position="left"
                  minGap={42}
                  formatValue={(v) => round(v)}
                />
              </LiveLineChart>
            ) : (
              <Box className="mission-telemetry-standby" role="status" aria-label="Waiting for sensor telemetry">
                <Box className="mission-standby-grid" aria-hidden>
                  <i /><i /><i />
                  <span />
                  <b /><b /><b /><b /><b />
                </Box>
                <Box className="mission-standby-copy">
                  <i aria-hidden />
                  <Typography>Waiting for signal</Typography>
                  <Typography>Chart will start when a sensor stream connects</Typography>
                </Box>
              </Box>
            )}
          </Box>
          {!livePoints.length && (
            <Typography className="mission-empty-copy">
              No sensor telemetry in the current window
            </Typography>
          )}
          <Box className="mission-chart-legend">
            <Typography><i className="normal" />Sensor series</Typography>
            <Typography><i className="watch" />Auto-scaled axis</Typography>
            <Typography><i className="critical" />No invented thresholds</Typography>
          </Box>
          <Box className="mission-production">
            <Metric label="Production" value={dashboard.production_rate ?? '—'} provenance={dashboard.production_rate != null ? 'live' : 'stale'} />
            <Metric label="Energy" value={dashboard.energy_usage ?? '—'} provenance={dashboard.energy_usage != null ? 'live' : 'stale'} />
            <Metric label="Downtime" value={dashboard.downtime ?? '—'} provenance={dashboard.downtime != null ? 'live' : 'stale'} />
          </Box>
        </Paper>

        <Paper className="mission-decisions mission-bento-decisions">
          <Typography className="product-kicker">PENDING DECISIONS</Typography>
          <Typography className="mission-decision-count">{String(pendingDecisions).padStart(2, '0')}</Typography>
          <Typography>
            {primary
              ? primary.ai_recommendation || 'Review the evidence package and approve the recommended response.'
              : 'No operator decision is currently blocking the operating plan.'}
          </Typography>
          <Button
            size="small"
            onClick={() => navigateTo(objectApi, navigate, 'incidents', primary ? { incidentId: primary.id, assetId: primary.asset_id || null } : {})}
          >
            {primary ? 'Open decision record' : 'Review audit trail'}
          </Button>
        </Paper>

        <Box className="mission-bento-lower">
        <Paper className="mission-feed mission-bento-feed">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">LIVE INCIDENT FEED</Typography>
              <Typography>Signals and investigations</Typography>
            </Box>
            <Button size="small" onClick={() => navigateTo(objectApi, navigate, 'incidents')}>View all</Button>
          </Box>
          {safeIncidents.length
            ? safeIncidents.slice(0, 4).map((item, index) => (
              <Box
                key={item.id || index}
                className="mission-feed-row"
                role="button"
                tabIndex={0}
                onClick={() => navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null })}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') {
                    navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null });
                  }
                }}
              >
                <i className={/critical|high/i.test(item.severity || '') ? 'risk' : ''} />
                <Box>
                  <b>{label(item.incident_type || 'Operational event')}</b>
                  <Typography>{item.asset_name || item.asset_id || 'Asset pending'} · {safeReasoning(item.evidence || 'Evidence packet is streaming')}</Typography>
                </Box>
                <Status state={item.severity || item.status} />
              </Box>
            ))
            : <Typography className="mission-empty-copy">No active incidents. The event bus and evidence agents are monitoring the facility.</Typography>}
        </Paper>

        <Paper className="mission-agents mission-bento-agents">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">ACTIVE AI AGENTS</Typography>
              <Typography>Reasoning network</Typography>
            </Box>
            <Typography className="mission-live">
              <i />{safeStages.filter((s) => /running|streaming/i.test(s.state)).length} LIVE
            </Typography>
          </Box>
          <Box className="mission-agent-list">
            {safeStages.length ? safeStages.slice(0, 4).map((stage, index) => {
              const agent = stage.agent;
              const state = stage.state;
              return (
                <Box key={`${stage.id || agent}-${index}`}>
                  <span>{String(agent || '?')[0]}</span>
                  <Typography>
                    <b>{traceLabel(agent, index)}</b>
                    <small>
                      {label(state || 'standing by')}
                      {stage.confidence != null
                        ? ` · ${round(Number(stage.confidence) <= 1 ? Number(stage.confidence) * 100 : Number(stage.confidence))}% confidence`
                        : ''}
                    </small>
                  </Typography>
                  <i className={/running|streaming/i.test(String(state || '')) ? 'active' : ''} />
                </Box>
              );
            }) : activityRows.length ? activityRows.slice(0, 4).map((entry, index) => (
              <Box key={`${entry.agent}-${index}`}>
                <span>{String(entry.agent || '?')[0]}</span>
                <Typography>
                  <b>{entry.agent}</b>
                  <small>
                    {label(entry.state || 'recorded')}
                    {entry.time ? ` · ${new Date(entry.time).toLocaleTimeString()}` : ''}
                  </small>
                </Typography>
                <i className={/running|streaming|completed/i.test(String(entry.state || '')) ? 'active' : ''} />
              </Box>
            )) : (
              <Typography className="mission-empty-copy">
                No agent stages are active. The MAO network will appear here during an investigation.
              </Typography>
            )}
          </Box>
        </Paper>

        <Paper className="mission-risks mission-bento-risks">
          <Typography className="product-kicker">TOP RISKS</Typography>
          {risks.length
            ? risks.map((asset, index) => (
              <Box
                key={asset.id || index}
                role="button"
                tabIndex={0}
                onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id })}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') navigateTo(objectApi, navigate, 'assets', { assetId: asset.id });
                }}
              >
                <Typography><b>{asset.name || `Asset ${index + 1}`}</b><small>{asset.location || asset.zone || '—'}</small></Typography>
                <Box><span style={{ width: `${Math.max(10, 100 - round(asset.health))}%` }} /></Box>
                <b title="Health deficit (100 − health)">{Math.max(0, 100 - round(asset.health))}</b>
              </Box>
            ))
            : <Typography className="mission-empty-copy">Risk model is synchronizing asset condition.</Typography>}
        </Paper>

        <Paper className="mission-shift mission-bento-shift">
          <Typography className="product-kicker">MAINTENANCE WINDOW</Typography>
          <Typography className="mission-shift-title">
            {tasks.length ? `${tasks.length} work orders in plan` : 'No planned downtime'}
          </Typography>
          <Typography><i className="event-dot active" />Agents live <b>{agentsLive}</b></Typography>
          <Typography><i className="event-dot" />Assets in scope <b>{safeAssets.length}</b></Typography>
          <Typography><i className="event-dot risk" />Open incidents <b>{safeIncidents.length}</b></Typography>
          <Button size="small" onClick={() => navigateTo(objectApi, navigate, 'maintenance')}>Open work control</Button>
        </Paper>
        </Box>
      </Box>

      <Paper className="mission-executive">
        <Box>
          <Typography className="product-kicker">EXECUTIVE & FORECAST SUMMARY</Typography>
          <Typography className="mission-executive-title">
            {primary
              ? `${label(primary.incident_type || 'Incident')} on ${primary.asset_name || 'an asset'} needs board visibility.`
              : 'No material incident exposure in the current operating snapshot.'}
          </Typography>
        </Box>
        <Box>
          <Metric label="Portfolio health" value={`${health}%`} provenance="live" />
          <Metric label="Active incidents" value={String(safeIncidents.length)} provenance="live" />
          <Metric label="Work orders" value={String(tasks.length)} provenance="live" />
        </Box>
        <Button onClick={() => navigateTo(objectApi, navigate, 'reports')}>Open board brief</Button>
      </Paper>
    </Box>
  );
}

import { Box, Button, Paper, Typography } from '@mui/material';
import { BoltOutlined, HubOutlined, ShieldOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { OperationsStrip } from '../../design-system/catalog/shell';
import { ExportAuditButton } from '../accountability';
import { Metric, Status, MiniGraph, label, round, averageHealth, safeReasoning, traceLabel } from './shared';
import { normalizeAgentActivityRow } from '../../api/resourceAdapters';

/** Part 8 — Command Center with sticky OperationsStrip + cross-nav. */
export function MissionControlOS({
  assets, incidents, stages, dashboard, refineries, telemetry, maintenance,
  aiActivity = [],
  facility = null, auditEvents = [], provenance = 'live',
}) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const safeAssets = Array.isArray(assets) ? assets : [];
  const safeIncidents = Array.isArray(incidents) ? incidents : [];
  const safeStages = Array.isArray(stages) ? stages : [];
  const safeRefineries = Array.isArray(refineries) ? refineries : [];
  const health = dashboard.fleet_health ?? averageHealth(safeAssets);
  const primary = safeIncidents[0];
  const values = Array.isArray(telemetry?.readings)
    ? telemetry.readings.map((item) => item.value)
    : safeAssets.map((asset) => asset.health);
  const risks = safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health)).slice(0, 4);
  const tasks = Array.isArray(maintenance?.tasks) ? maintenance.tasks : [];
  const activityRows = (Array.isArray(aiActivity) ? aiActivity : [])
    .map(normalizeAgentActivityRow)
    .filter(Boolean);
  const scopeLabel = (
    objectApi.scope?.facility
    || facility
    || safeRefineries[0]?.name
    || 'Enterprise view'
  ).toUpperCase();

  const twinNodes = risks.length
    ? risks.slice(0, 4)
    : safeAssets.slice(0, 4);
  const agentsLive = safeStages.filter((s) => /running|streaming/i.test(s.state)).length;
  const telemetryLive = values.length > 0;

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
          { label: 'Fleet health', value: `${health}%`, detail: provenance },
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
          <Typography><i />SYSTEMS LIVE</Typography>
          <ExportAuditButton events={auditEvents} facility={facility} />
          <Button variant="contained" onClick={openInvestigation}>
            {primary ? 'Review investigation' : 'Open digital twin'}
          </Button>
        </Box>
      </Paper>

      <Box className="mission-command-grid">
        <Paper className="mission-twin">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">DIGITAL TWIN OVERVIEW</Typography>
              <Typography>Facility operating map</Typography>
            </Box>
            <Status state={primary ? 'Attention' : 'Nominal'} />
          </Box>
          <Box className="mission-twin-map">
            <Box className="mission-twin-core"><b>{health}%</b><span>FLEET HEALTH</span></Box>
            {twinNodes.length ? twinNodes.map((asset, index) => (
              <button
                type="button"
                key={asset.id || index}
                className={`mission-twin-node ${Number(asset.health ?? health) < 75 ? 'risk is-pulse' : ''}`}
                onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id || null })}
              >
                <i />
                <span>{asset.name || asset.location || `Asset ${index + 1}`}</span>
                <b>{round(asset.health ?? health)}%</b>
              </button>
            )) : (
              <Typography className="mission-empty-copy" sx={{ position: 'absolute', inset: 0, displayContent: 'center', p: 2 }}>
                No assets available for the twin overview.
              </Typography>
            )}
            <svg viewBox="0 0 600 250"><path d="M86 70H250M350 70H515M86 180H250M350 180H515M300 94V155" /></svg>
          </Box>
          <Box className="mission-twin-footer">
            <Typography><HubOutlined /> {safeAssets.length} assets connected</Typography>
            <Typography><BoltOutlined /> {values.length ? `${values.length} historian samples` : 'No historian samples'}</Typography>
            <Typography>
              <ShieldOutlined />
              {' '}
              {primary ? `${label(primary.severity)} incident open` : 'No critical incidents open'}
            </Typography>
          </Box>
        </Paper>

        <Paper className="mission-telemetry-panel">
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
          <Box className="mission-chart-wrap">
            <MiniGraph
              values={values}
              area
              label={telemetryLive ? 'Process index · live historian feed' : 'No telemetry samples in the current window'}
            />
            {telemetryLive ? (
              <Box className="mission-chart-annotation"><span>Watch threshold</span><i /></Box>
            ) : null}
          </Box>
          <Box className="mission-chart-legend">
            <Typography><i className="normal" />Nominal</Typography>
            <Typography><i className="watch" />Watch ≥ 75%</Typography>
            <Typography><i className="critical" />Critical ≥ 90%</Typography>
          </Box>
          <Box className="mission-production">
            <Metric label="Production" value={dashboard.production_rate ?? '—'} provenance={dashboard.production_rate != null ? 'live' : 'stale'} />
            <Metric label="Energy" value={dashboard.energy_usage ?? '—'} provenance={dashboard.energy_usage != null ? 'live' : 'stale'} />
            <Metric label="Downtime" value={dashboard.downtime ?? '—'} provenance={dashboard.downtime != null ? 'live' : 'stale'} />
          </Box>
        </Paper>

        <Paper className="mission-decisions">
          <Typography className="product-kicker">PENDING DECISIONS</Typography>
          <Typography className="mission-decision-count">{primary ? '01' : '00'}</Typography>
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
      </Box>

      <Box className="mission-lower-grid">
        <Paper className="mission-feed">
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

        <Paper className="mission-agents">
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

        <Paper className="mission-risks">
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
                <Typography><b>{asset.name || `Asset ${index + 1}`}</b><small>{asset.location || asset.zone || 'Process train'}</small></Typography>
                <Box><span style={{ width: `${Math.max(10, 100 - round(asset.health))}%` }} /></Box>
                <b>{Math.max(0, 100 - round(asset.health))}</b>
              </Box>
            ))
            : <Typography className="mission-empty-copy">Risk model is synchronizing asset condition.</Typography>}
        </Paper>

        <Paper className="mission-shift">
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

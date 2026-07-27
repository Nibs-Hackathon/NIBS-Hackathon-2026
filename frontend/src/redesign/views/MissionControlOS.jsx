import { Box, Button, Paper, Typography } from '@mui/material';
import { BoltOutlined, HubOutlined, ShieldOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { OperationsStrip } from '../../design-system/catalog/shell';
import { ExportAuditButton } from '../accountability';
import { Metric, Status, MiniGraph, label, round, averageHealth, safeReasoning, traceLabel } from './shared';

/** Part 8 — Command Center with sticky OperationsStrip + cross-nav. */
export function MissionControlOS({
  assets, incidents, stages, dashboard, projection, refineries, telemetry, maintenance,
  facility = 'Alpha Refinery', auditEvents = [], provenance = 'live',
}) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const safeAssets = Array.isArray(assets) ? assets : [];
  const safeIncidents = Array.isArray(incidents) ? incidents : [];
  const safeStages = Array.isArray(stages) ? stages : [];
  const health = dashboard.fleet_health ?? averageHealth(safeAssets);
  const primary = safeIncidents[0];
  const values = Array.isArray(telemetry?.readings)
    ? telemetry.readings.map((item) => item.value)
    : safeAssets.map((asset) => asset.health);
  const risks = safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health)).slice(0, 4);
  const tasks = Array.isArray(maintenance?.tasks) ? maintenance.tasks : [];
  const scopeLabel = (objectApi.scope?.facility || facility || 'Alpha Refinery').toUpperCase();

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
              : 'All process trains are holding within the operating envelope.'}
          </Typography>
          <Typography>
            {primary
              ? `${primary.asset_name || 'Affected asset'} · ${label(primary.severity || 'active')} severity · evidence is streaming to the investigation record.`
              : `${safeAssets.length} connected assets · network healthy · autonomous monitoring active.`}
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
            {['Crude unit', 'Hydrotreater', 'Utilities', 'Tank farm'].map((name, index) => (
              <button
                type="button"
                key={name}
                className={`mission-twin-node ${Number(safeAssets[index]?.health ?? health) < 75 ? 'risk is-pulse' : ''}`}
                onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: safeAssets[index]?.id || null })}
              >
                <i /><span>{name}</span><b>{round(safeAssets[index]?.health ?? health)}%</b>
              </button>
            ))}
            <svg viewBox="0 0 600 250"><path d="M86 70H250M350 70H515M86 180H250M350 180H515M300 94V155" /></svg>
          </Box>
          <Box className="mission-twin-footer">
            <Typography><HubOutlined /> {safeAssets.length} assets connected</Typography>
            <Typography><BoltOutlined /> {values.length ? `${values.length} historian samples` : 'historian synchronizing'}</Typography>
            <Typography><ShieldOutlined /> safety envelope intact</Typography>
          </Box>
        </Paper>

        <Paper className="mission-telemetry-panel">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">LIVE TELEMETRY</Typography>
              <Typography>Operating envelope</Typography>
            </Box>
            <Typography className="mission-live"><i />STREAMING</Typography>
          </Box>
          <Box className="mission-chart-wrap">
            <MiniGraph values={values} area label="Process index · live historian feed" />
            <Box className="mission-chart-annotation"><span>Watch threshold</span><i /></Box>
          </Box>
          <Box className="mission-chart-legend">
            <Typography><i className="normal" />Nominal</Typography>
            <Typography><i className="watch" />Watch ≥ 75%</Typography>
            <Typography><i className="critical" />Critical ≥ 90%</Typography>
            <Typography><i className="band" />Confidence range</Typography>
          </Box>
          <Box className="mission-production">
            <Metric label="Production" value={dashboard.production_rate ?? 'Awaiting meter'} />
            <Metric label="Energy" value={dashboard.energy_usage ?? 'Awaiting meter'} />
            <Metric label="Downtime" value={dashboard.downtime ?? 'Awaiting event data'} />
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
            }) : (
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
          <Typography className="product-kicker">SHIFT & MAINTENANCE</Typography>
          <Typography className="mission-shift-title">Day shift · 06:00–18:00</Typography>
          <Typography><i className="event-dot active" />Control room <b>staffed</b></Typography>
          <Typography><i className="event-dot" />Network <b>all zones online</b></Typography>
          <Typography><i className="event-dot risk" />Maintenance window <b>{tasks.length ? `${tasks.length} work orders planned` : 'No planned downtime'}</b></Typography>
          <Button size="small" onClick={() => navigateTo(objectApi, navigate, 'maintenance')}>Open work control</Button>
        </Paper>
      </Box>

      <Paper className="mission-executive">
        <Box>
          <Typography className="product-kicker">EXECUTIVE & FORECAST SUMMARY</Typography>
          <Typography className="mission-executive-title">
            {primary
              ? 'Operational exposure is contained; a targeted intervention protects the next production window.'
              : 'The operating plan remains stable with no material exposure in the current forecast.'}
          </Typography>
        </Box>
        <Box>
          <Metric label="Portfolio health" value={`${health}%`} />
          <Metric label="Forecast exposure" value={primary ? 'Moderate' : 'Low'} />
          <Metric label="Knowledge updates" value={String(safeStages.filter((s) => String(s.agent || '').toLowerCase().includes('knowledge')).length)} />
        </Box>
        <Button onClick={() => navigateTo(objectApi, navigate, 'reports')}>Open board brief</Button>
      </Paper>
    </Box>
  );
}

import { useMemo, useState } from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import {
  AccountTreeOutlined, BuildOutlined, DeviceHubOutlined, HistoryOutlined,
  ScienceOutlined, TimelineOutlined, DescriptionOutlined,
} from '@mui/icons-material';
import { MiniGraph, label, round } from './shared';

/**
 * Part F + H — Bottom workspace tabs; controlled focus from twin interactions.
 */
export function AssetBottomWorkspace({
  asset,
  selected,
  stream,
  readings = [],
  statusLabel,
  primaryLabel,
  bottomHeight,
  onCycleHeight,
  onOpenIncident,
  clean,
  workOrders = [],
  activeTab,
  onTabChange,
  focusTag = null,
}) {
  const [internalTab, setInternalTab] = useState('telemetry');
  const tab = activeTab || internalTab;
  const setTab = (next) => {
    onTabChange?.(next);
    setInternalTab(next);
  };

  const incidentCount = selected?.incident ? 1 : 0;
  const projected = Array.isArray(asset?.projected_health)
    ? asset.projected_health.map(Number).filter(Number.isFinite)
    : [];
  const hasForecast = Boolean(
    asset?.forecast_available
    || projected.length > 1
    || asset?.remaining_life_days != null
    || asset?.remaining_life != null
    || asset?.failure_probability != null,
  );
  const assetWOs = useMemo(
    () => workOrders.filter((wo) => wo.assetId === asset?.id || wo.asset_id === asset?.id || wo.asset === asset?.name),
    [workOrders, asset],
  );
  const hasMaint = assetWOs.length > 0;
  const deps = clean?.(asset?.dependencies, '') || asset?.dependencies;
  const tagLabel = focusTag || asset?.tag || asset?.id;

  const tabs = [
    { id: 'telemetry', label: 'Telemetry', icon: <TimelineOutlined fontSize="small" />, show: true },
    { id: 'history', label: 'History', icon: <HistoryOutlined fontSize="small" />, show: true },
    { id: 'incidents', label: `Incidents${incidentCount ? ` (${incidentCount})` : ''}`, icon: <DeviceHubOutlined fontSize="small" />, show: incidentCount > 0 },
    { id: 'forecast', label: 'Forecast', icon: <ScienceOutlined fontSize="small" />, show: true },
    { id: 'maintenance', label: 'Maintenance', icon: <BuildOutlined fontSize="small" />, show: hasMaint },
    { id: 'relationships', label: 'Relationships', icon: <AccountTreeOutlined fontSize="small" />, show: Boolean(deps) },
    { id: 'documents', label: 'Documents', icon: <DescriptionOutlined fontSize="small" />, show: Number(asset?.documents_count) > 0 },
  ].filter((item) => item.show);

  const active = tabs.some((item) => item.id === tab) ? tab : 'telemetry';
  const health = asset?.health != null ? round(asset.health) : null;
  const rull = asset?.remaining_life_days ?? asset?.remaining_life;
  const failure = asset?.failure_probability;

  return (
    <Paper className="twin-bottom assets-bottom">
      <Box className="twin-bottom-tabs">
        {tabs.map((item) => (
          <Button
            key={item.id}
            className={active === item.id ? 'active' : ''}
            startIcon={item.icon}
            onClick={() => setTab(item.id)}
          >
            {item.label}
          </Button>
        ))}
        <Button size="small" sx={{ ml: 'auto' }} onClick={onCycleHeight}>
          Height {bottomHeight}% · Ctrl+B
        </Button>
      </Box>

      <Box className="twin-bottom-body assets-bottom-body" key={`${asset?.id || 'none'}-${active}-${tagLabel || ''}`}>
        {active === 'telemetry' && (
          <>
            <Box>
              <Typography className="product-kicker">TELEMETRY</Typography>
              <Typography className="twin-bottom-title">
                {tagLabel ? `Tag ${tagLabel}` : 'Primary tags'}
                {' · '}
                {clean?.(stream?.sensor_type, 'Condition') || 'Condition'}
                {' · '}
                {clean?.(stream?.unit, 'stream') || 'stream'}
              </Typography>
              <MiniGraph
                values={readings.map((reading) => reading.value)}
                area
                label={readings.length ? `${readings.length} historian samples` : 'No dedicated stream for this asset yet'}
              />
            </Box>
            <Box className="twin-bottom-events">
              <Typography className="product-kicker">DECISION CONTEXT</Typography>
              <Typography><i className="event-dot risk" />Severity <b>{statusLabel}</b></Typography>
              <Typography><i className="event-dot active" />Next action <b>{primaryLabel}</b></Typography>
              {deps ? (
                <Typography><i className="event-dot" />Downstream <b>{deps}</b></Typography>
              ) : (
                <Typography variant="body2" color="text.secondary">No dependency map published for this asset.</Typography>
              )}
            </Box>
          </>
        )}

        {active === 'history' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">STATE HISTORY</Typography>
            {asset?.last_inspection ? (
              <Typography><i className="event-dot" />Last inspection <b>{clean?.(asset.last_inspection, asset.last_inspection)}</b></Typography>
            ) : (
              <Typography variant="body2" color="text.secondary">No inspection history published for this asset yet.</Typography>
            )}
            <Typography><i className="event-dot risk" />Condition band <b>{statusLabel}</b></Typography>
          </Box>
        )}

        {active === 'incidents' && selected?.incident && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">LINKED INCIDENT</Typography>
            <Typography className="twin-bottom-title">{label(selected.incident.incident_type || selected.incident.id)}</Typography>
            <Typography variant="body2" color="text.secondary">
              {selected.incident.evidence || selected.incident.reasoning || 'Evidence packet attached to this asset.'}
            </Typography>
            <Button size="small" sx={{ mt: 1 }} variant="contained" onClick={onOpenIncident}>Open case</Button>
          </Box>
        )}

        {active === 'forecast' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">FORWARD RISK</Typography>
            {hasForecast ? (
              <>
                <Box className="assets-bottom-metrics">
                  <Typography>
                    Failure probability{' '}
                    <b>{failure != null ? `${round(Number(failure) <= 1 ? Number(failure) * 100 : Number(failure))}%` : '—'}</b>
                  </Typography>
                  <Typography>
                    Remaining useful life{' '}
                    <b>{rull != null ? `${round(Number(rull))} days` : '—'}</b>
                  </Typography>
                  <Typography>
                    Health{' '}
                    <b>{health != null ? `${health}%` : '—'}</b>
                  </Typography>
                </Box>
                <MiniGraph
                  values={projected}
                  area
                  label={projected.length > 1 ? 'Projected health curve' : 'No projected health series published'}
                />
              </>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No forecast published for this asset yet. Open Health forecasting for stress scenarios.
              </Typography>
            )}
          </Box>
        )}

        {active === 'maintenance' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">WORK ORDERS</Typography>
            {assetWOs.length
              ? assetWOs.map((wo, index) => (
                <Typography key={wo.id || index}>
                  <i className="event-dot active" />
                  {wo.title || wo.name || `WO ${index + 1}`}
                  <b>{wo.status || wo.Status || 'Backlog'}</b>
                </Typography>
              ))
              : <Typography variant="body2" color="text.secondary">No open work orders for this asset.</Typography>}
          </Box>
        )}

        {active === 'relationships' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">PROCESS RELATIONSHIPS</Typography>
            <Typography><i className="event-dot active" />Selected <b>{asset?.name || '—'}</b></Typography>
            <Typography><i className="event-dot risk" />Downstream <b>{deps}</b></Typography>
          </Box>
        )}

        {active === 'documents' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">DOCUMENTS</Typography>
            <Typography>{clean?.(asset?.documents_count, '0') || '0'} controlled records linked to this asset.</Typography>
          </Box>
        )}
      </Box>
    </Paper>
  );
}

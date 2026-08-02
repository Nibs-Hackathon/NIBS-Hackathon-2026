/** Map backend API payloads to shapes expected by redesign views. */

import { REFINERY_GEO, formatDisplayLocation } from '../data/refineryGeo.js';

const cleanText = (value) => (value == null ? '' : String(value).trim());

export function notificationPresentation(notification = {}) {
  const assetName = cleanText(notification.asset_name);
  const refineryName = cleanText(
    notification.refinery_name
      || notification.refinery
      || notification.facility
      || notification.metadata?.refinery,
  );
  const sourceTitle = cleanText(notification.title);
  const title = [assetName, refineryName].filter(Boolean).join(' · ')
    || sourceTitle
    || 'Operational notification';
  const message = cleanText(notification.message);
  const incidentType = cleanText(notification.incident_type);
  let detail = message && message !== assetName && message !== title
    ? message
    : incidentType;

  if (!detail && sourceTitle !== title) detail = sourceTitle;
  if (!detail) detail = 'Operational update';
  if (notification.type === 'revenue_impact' && detail.startsWith('$')) {
    detail = `Revenue impact: ${detail}`;
  }

  return { title, detail };
}

function parsePercent(value) {
  if (value == null) return null;
  const parsed = parseFloat(String(value).replace('%', '').trim());
  return Number.isFinite(parsed) ? parsed : null;
}

function parseRulDays(value) {
  if (value == null) return null;
  const match = String(value).match(/(\d+(?:\.\d+)?)/);
  return match ? Math.round(Number(match[1])) : null;
}

export function normalizePredictionResponse(data, baseAsset = {}) {
  if (!data) return { ...baseAsset };
  if (!data.data_available) {
    return {
      ...baseAsset,
      forecast_available: false,
      forecast_method: data.forecast_method || 'unavailable',
    };
  }

  const historical = Array.isArray(data.historical?.['Historical health'])
    ? data.historical['Historical health']
    : [];
  const predicted = Array.isArray(data.predicted?.['Predicted health'])
    ? data.predicted['Predicted health']
    : [];
  const projectedHealth = [...historical, ...predicted].map(Number).filter(Number.isFinite);

  return {
    ...baseAsset,
    id: data.asset_id || baseAsset.id,
    health: data.health ?? baseAsset.health,
    remaining_life_days: parseRulDays(data.rul),
    failure_probability: parsePercent(data.failure_probability),
    prediction_confidence: parsePercent(data.confidence),
    forecast_available: projectedHealth.length > 1,
    forecast_method: data.forecast_method,
    projected_health: projectedHealth,
    historical_health: historical.map(Number).filter(Number.isFinite),
    predicted_health: predicted.map(Number).filter(Number.isFinite),
    stress: data.stress ?? 0,
    stress_multiplier: data.stress_multiplier,
    scenario: data.scenario || null,
  };
}

export function normalizeTwinAsset(row) {
  if (!row || typeof row !== 'object') return null;
  return {
    id: row.id,
    name: row.Asset || row.name,
    asset_name: row.Asset || row.name,
    type: row.Category || row.type,
    location: row.Zone || row.location,
    zone: row.Zone || row.zone,
    health: row.Health ?? row.health,
    status: row.Status || row.status,
    temperature: row.Temperature,
    pressure: row.Pressure,
    rpm: row.RPM,
    failure: row.Failure,
    recommendation: row.Recommendation,
    twin_enriched: true,
  };
}

export function mergeAssetsWithTwin(assets, twinRows) {
  const base = Array.isArray(assets) ? assets.filter(Boolean) : [];
  const twins = Array.isArray(twinRows) ? twinRows.map(normalizeTwinAsset).filter(Boolean) : [];
  if (!twins.length) return base;

  const byId = new Map(base.map((asset) => [asset.id, { ...asset }]));
  twins.forEach((twin) => {
    if (!byId.has(twin.id)) return;
    const existing = byId.get(twin.id) || {};
    byId.set(twin.id, { ...existing, ...twin });
  });
  return Array.from(byId.values());
}

export function facilityOptionsFromRefineries(refineries = []) {
  return normalizeRefineryOptions(refineries).map((row) => row.value);
}

function refineryDetail(refinery) {
  if (!refinery) return null;
  if (refinery.display_location) return refinery.display_location;
  const region = [refinery.state, refinery.country].filter(Boolean).join(', ');
  if (region && refinery.sea) return `${region} · ${refinery.sea}`;
  return region || refinery.sea || null;
}

export function normalizeRefineryOptions(refineries = []) {
  const liveRows = (Array.isArray(refineries) ? refineries : []).filter((row) => row?.name);
  // Scope controls expose only facilities confirmed by operations/live.
  // Catalog-only entries may remain visible on the globe, but cannot create
  // an empty application scope before the backend instantiates them.
  const unique = [...new Map(liveRows.map((row) => [row.name, row])).values()];
  return [
    { value: 'Enterprise view', label: 'Enterprise view', detail: 'All facilities in portfolio' },
    ...unique.map((row) => ({
      value: row.name,
      label: row.name,
      detail: refineryDetail(row) || 'Operational site',
    })),
  ];
}

export function enrichRefineryGeo(refineries = []) {
  const liveRows = (Array.isArray(refineries) ? refineries : []).filter((row) => row?.name);
  const byName = new Map(liveRows.map((row) => [row.name, row]));
  Object.entries(REFINERY_GEO).forEach(([name, geo]) => {
    if (!byName.has(name)) byName.set(name, { name, ...geo, catalog_only: true });
  });

  return Array.from(byName.values()).map((row) => {
    const geo = REFINERY_GEO[row?.name] || {};
    return {
      ...row,
      ...geo,
      lat: row.lat ?? geo.lat ?? null,
      lng: row.lng ?? geo.lng ?? null,
      display_location: row.display_location || formatDisplayLocation({ ...geo, ...row }),
    };
  });
}

export function telemetryToLivePoints(readings = []) {
  return (Array.isArray(readings) ? readings : [])
    .map((row, index) => {
      const value = Number(row.value);
      if (!Number.isFinite(value)) return null;
      const stamp = row.timestamp || row.time;
      const time = stamp ? new Date(stamp).getTime() / 1000 : Date.now() / 1000 - (readings.length - index);
      return { time, value };
    })
    .filter(Boolean)
    .slice(-500);
}

export function refineriesForFacility(refineries = [], facility) {
  const list = Array.isArray(refineries) ? refineries : [];
  if (!facility || facility === 'Enterprise view' || facility === 'portfolio' || facility === 'North Sea Portfolio') {
    return list;
  }
  const matched = list.filter((row) => row.name === facility);
  return matched.length ? matched : list;
}

export function telemetryForFacility(operations = {}, facility) {
  const enterprise = !facility || facility === 'Enterprise view' || facility === 'portfolio' || facility === 'North Sea Portfolio';
  if (!enterprise) {
    const row = (operations.telemetry_by_refinery || []).find((item) => item.refinery === facility);
    if (row) {
      return {
        asset_id: row.asset_id,
        asset_name: row.asset_name,
        readings: Array.isArray(row.readings) ? row.readings : [],
      };
    }
  }
  return operations.telemetry || { readings: [] };
}

export function fleetHealthForScope({ refineries = [], assets = [], dashboard = {} }, facility) {
  // The scoped asset collection is the most current source in the live
  // operations snapshot. Average only published numeric readings; treating a
  // missing reading as zero would make a disconnected asset look failed.
  const healthReadings = assets
    .map((asset) => Number(asset?.health))
    .filter(Number.isFinite);
  if (healthReadings.length) {
    const total = healthReadings.reduce((sum, health) => sum + health, 0);
    return Math.round((total / healthReadings.length) * 10) / 10;
  }
  const scoped = refineriesForFacility(refineries, facility);
  if (
    facility
    && facility !== 'Enterprise view'
    && scoped[0]?.fleet_health != null
    && Number.isFinite(Number(scoped[0].fleet_health))
  ) {
    return Number(scoped[0].fleet_health);
  }
  return dashboard.fleet_health != null && Number.isFinite(Number(dashboard.fleet_health))
    ? Number(dashboard.fleet_health)
    : null;
}

export function timelineFromAudit(incident) {
  if (!Array.isArray(incident?.timeline) || !incident.timeline.length) return [];
  return incident.timeline.map((step, index) => ({
    key: step.id || `${step.kind || 'step'}-${index}`,
    title: step.title || step.kind || `Step ${index + 1}`,
    time: step.timestamp,
    detail: step.reasoning || step.output || step.status || 'Recorded in audit trail',
    kind: step.kind || 'event',
  }));
}

/** ISO since/until for incident-scoped telemetry replay (1h before detection through resolution). */
export function incidentTelemetryWindow(incident) {
  if (!incident) return null;
  const start = incident.timestamp || incident.created_at;
  if (!start) return null;
  const since = new Date(new Date(start).getTime() - 60 * 60 * 1000).toISOString();
  const until = incident.resolved_at || new Date().toISOString();
  return { since, until };
}

/** Normalize telemetry API payloads to a flat readings array. */
export function normalizeTelemetryReadings(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.readings)) return payload.readings;
  if (Array.isArray(payload?.history)) {
    return payload.history.map((row) => ({
      timestamp: row.Timestamp || row.timestamp,
      value: row.Value ?? row.value,
      sensor_type: row.Sensor || row.sensor_type,
      unit: row.Unit || row.unit,
    }));
  }
  return [];
}

/** Merge session decisions with persisted operator actions for incident decision history. */
export function decisionEntriesFromIncident(incident, sessionEntries = []) {
  const fromActions = (incident?.operator_actions || []).map((action) => ({
    id: action.id,
    decision: action.decision || action.title || action.action_type,
    what: action.note || action.title || action.action_type,
    who: action.approved_by || action.operator || 'Operator',
    at: action.timestamp,
    rationale: action.note,
  }));
  const seen = new Set();
  return [...sessionEntries, ...fromActions].filter((entry) => {
    const key = entry.id || `${entry.at || entry.when}-${entry.what || entry.decision}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export function normalizeAgentActivityRow(row) {
  if (!row || typeof row !== 'object') return null;
  const confidence = row.confidence;
  const parsedConfidence = typeof confidence === 'string'
    ? parseFloat(confidence.replace('%', ''))
    : confidence;
  return {
    agent: row.agent || row.agent_name || 'Agent',
    action: row.action || row.finding || row.summary || 'Activity recorded',
    state: row.state || (row.success === false ? 'Failed' : row.success ? 'Completed' : 'Recorded'),
    time: row.time || row.timestamp,
    confidence: parsedConfidence,
  };
}

export function normalizeAgentRegistryRow(row) {
  if (!row || typeof row !== 'object') return null;
  return {
    name: row.Agent || row.name || 'Agent',
    specialty: row.Specialty || row.specialty || '',
    state: row.State || row.state || 'Ready',
    confidence: row.Confidence || row.confidence,
    task: row['Current task'] || row.current_task || 'Awaiting task',
  };
}

export function normalizeAgentMetricRow(row) {
  if (!Array.isArray(row) || row.length < 2) return null;
  return { label: row[0], value: row[1], detail: row[2] || '', tone: row[3] || 'cyan' };
}

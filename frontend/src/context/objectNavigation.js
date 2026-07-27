/**
 * Navigation API for ObjectContext — docs/OBJECT_CONTEXT.md
 * Epic 4: product routes use legacy ProductShell paths.
 */

export const WORKSPACE_PATHS = {
  command: '/',
  assets: '/assets',
  incidents: '/incident-simulator',
  investigation: '/agent-monitor',
  maintenance: '/maintenance',
  forecasting: '/health-prediction',
  reports: '/reports',
};

/** Aliases → product paths (canonical Epic 3 names still resolve). */
export const PATH_ALIASES = {
  '/incidents': '/incident-simulator',
  '/investigation': '/agent-monitor',
  '/forecasting': '/health-prediction',
  '/digital-twin': '/assets',
  '/ai-activity': '/agent-monitor',
};

export const WORKSPACE_LABELS = {
  command: 'Command Center',
  assets: 'Assets',
  incidents: 'Incidents',
  investigation: 'Investigation',
  maintenance: 'Maintenance',
  forecasting: 'Forecasting',
  reports: 'Reports',
};

export function pathToWorkspace(pathname) {
  const normalized = PATH_ALIASES[pathname] || pathname;
  const entry = Object.entries(WORKSPACE_PATHS).find(([, path]) => path === normalized);
  return entry ? entry[0] : 'command';
}

/**
 * Apply selection payload then navigate.
 */
export function navigateTo(objectApi, navigate, workspace, options = {}) {
  const path = WORKSPACE_PATHS[workspace];
  if (!path) {
    console.warn(`[RigOS] Unknown workspace: ${workspace}`);
    return;
  }
  objectApi.applyNavigationPayload(options);
  navigate(path);
}

/**
 * Client-side facility scope filter (backend returns full portfolio).
 */
export function filterByFacility(items, facility, getLocation) {
  if (!facility || facility === 'Enterprise view' || facility === 'portfolio' || facility === 'North Sea Portfolio') {
    return items || [];
  }
  const list = Array.isArray(items) ? items : [];
  const matched = list.filter((item) => getLocation(item) === facility);
  return matched.length ? matched : list;
}

export function assetLocation(asset) {
  return asset?.location || asset?.zone || asset?.refinery || null;
}

export function incidentLocation(item, assets = []) {
  if (item?.refinery || item?.location) return item.refinery || item.location;
  const asset = assets.find((a) => a.id === item?.asset_id);
  return assetLocation(asset);
}

export function taskLocation(task, assets = []) {
  if (task?.refinery || task?.location) return task.refinery || task.location;
  const asset = assets.find((a) => a.id === task?.asset_id);
  return assetLocation(asset);
}

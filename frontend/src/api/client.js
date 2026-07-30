import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';
const errorLogTimes = new Map();
const ERROR_LOG_WINDOW_MS = 30000;

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const endpoint = error.config?.url || 'unknown endpoint';
    const now = Date.now();
    const lastLogged = errorLogTimes.get(endpoint) || 0;
    if (import.meta.env.DEV && now - lastLogged >= ERROR_LOG_WINDOW_MS) {
      errorLogTimes.set(endpoint, now);
      console.warn(`API unavailable [${endpoint}]: ${error.message}`);
    }
    return Promise.reject(error);
  },
);

// ============================================
// ASSETS
// ============================================
/** Prefer `getOperationsLive()` for the full asset list; standalone refresh helper. */
export const getAssets = () => api.get('/assets');
export const getAssetHealth = (assetId) => api.get(`/assets/${encodeURIComponent(assetId)}`);
export const getAssetNotes = (assetId) => api.get(`/assets/${encodeURIComponent(assetId)}/notes`);
export const saveAssetNote = (assetId, note, operator = 'Control operator') =>
  api.post(`/assets/${encodeURIComponent(assetId)}/notes`, { note, operator });

// ============================================
// TELEMETRY
// ============================================
export const getTelemetry = (assetId, { limit = 30, since = null, until = null } = {}) => {
  const params = new URLSearchParams({ limit: String(limit) });
  if (since) params.set('since', since);
  if (until) params.set('until', until);
  return api.get(`/telemetry/${encodeURIComponent(assetId)}?${params.toString()}`);
};

// ============================================
// INCIDENTS
// ============================================
/** Runtime event list; incident center uses `operations.audit_logs` from live snapshot. */
export const getIncidents = () => api.get('/incidents');
/** Inject a simulator fault (pressure spike, gas leak, etc.) for demos. */
export const triggerIncident = (type, assetId = null) =>
  api.post(
    `/incidents/${encodeURIComponent(type)}`,
    null,
    { params: assetId ? { asset_id: assetId } : undefined },
  );

// ============================================
// AGENTS
// ============================================
export const getAgents = () => api.get('/agents');
export const getAgentMetrics = () => api.get('/agent-metrics');
export const getAgentActivity = () => api.get('/agent-activity');

// ============================================
// MAINTENANCE
// ============================================
export const getMaintenancePlan = () => api.get('/maintenance');
export const createWorkOrder = (payload) => api.post('/maintenance/work-orders', payload);
export const approveWorkOrder = (workOrderId, payload = {}) =>
  api.post(`/maintenance/work-orders/${encodeURIComponent(workOrderId)}/approve`, payload);
export const transitionWorkOrder = (workOrderId, payload) =>
  api.post(`/maintenance/work-orders/${encodeURIComponent(workOrderId)}/status`, payload);

// ============================================
// PREDICTIONS
// ============================================
export const getPredictions = (assetId, horizon = 14, stress = 0) => {
  const params = new URLSearchParams({ horizon: String(horizon), stress: String(stress ?? 0) });
  return api.get(`/predictions/${encodeURIComponent(assetId)}?${params.toString()}`);
};

// ============================================
// DASHBOARD
// ============================================
/** Prefer `getOperationsLive().dashboard`; standalone summary endpoint. */
export const getDashboard = () => api.get('/dashboard');
export const getOperationsLive = () => api.get('/operations/live');

// ============================================
// OPERATIONS AUDIT
// ============================================
/** List audit records; views use live `audit_logs` or `getIncidentAuditDetail`. */
export const getIncidentAudit = (limit = 100) => api.get(`/incidents/audit?limit=${limit}`);
export const getIncidentAuditDetail = (incidentId) =>
  api.get(`/incidents/audit/${encodeURIComponent(incidentId)}`);

// ============================================
// GLOBAL AI ASSISTANT / KNOWLEDGE
// ============================================
// Knowledge retrieval can legitimately take longer than telemetry/dashboard calls.
export const askAssistant = (question, context = {}) => api.post(
  '/assistant/query',
  {
    question,
    asset_id: context.asset_id || context.assetId || null,
    incident_id: context.incident_id || context.incidentId || null,
    facility: context.facility || null,
    history: Array.isArray(context.history) ? context.history.slice(-8) : [],
  },
  { timeout: 60000 },
);
export const searchKnowledge = (query) =>
  api.get(`/knowledge/search?q=${encodeURIComponent(query || '')}`, { timeout: 30000 });
export const getKnowledgeDocuments = () =>
  api.get('/knowledge/documents');

// Persistent operator supervision; this records a decision but does not command equipment.
export const recordOperatorAction = (payload) => api.post('/operator-actions', payload);
export const getOperatorActions = ({ limit = 50, incidentId = null, assetId = null } = {}) => {
  const params = new URLSearchParams({ limit: String(limit) });
  if (incidentId) params.set('incident_id', incidentId);
  if (assetId) params.set('asset_id', assetId);
  return api.get(`/operator-actions?${params.toString()}`);
};
/** Capability contract for demos; facilities come from `operations.refineries`. */
export const getPlatformMetadata = () => api.get('/metadata');
export const markNotificationsRead = (payload) => api.post('/notifications/read', payload);

// ============================================
// REPORTS
// ============================================
export const getReports = () => api.get('/reports');
export const exportReport = (reportId, format = 'markdown') =>
  api.get(`/reports/${encodeURIComponent(reportId)}/export?format=${encodeURIComponent(format)}`);

// ============================================
// DIGITAL TWIN
// ============================================
export const getTwinAssets = () => api.get('/twin-assets');

export default api;


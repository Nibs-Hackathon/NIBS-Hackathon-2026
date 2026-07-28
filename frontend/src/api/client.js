import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response [${response.config.url}]:`, response.data);
    return response;
  },
  (error) => {
    console.error(`❌ API Error [${error.config?.url}]:`, error.message);
    return Promise.reject(error);
  }
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
export const triggerIncident = (type) =>
  api.post(`/incidents/${encodeURIComponent(type)}`);

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
  },
  { timeout: 60000 },
);
export const searchKnowledge = (query) =>
  api.get(`/knowledge/search?q=${encodeURIComponent(query || '')}`, { timeout: 30000 });

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


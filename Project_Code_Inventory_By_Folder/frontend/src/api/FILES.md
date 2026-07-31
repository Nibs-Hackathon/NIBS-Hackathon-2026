# Folder: frontend/src/api Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/api`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/api/client.js

**Folder path:** `frontend/src/api`

**File path:** `frontend/src/api/client.js`

```javascript
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
export const getAssets = () => api.get('/assets');
export const getAssetHealth = (assetId) => api.get(`/assets/${assetId}`);

// ============================================
// TELEMETRY
// ============================================
export const getTelemetry = (assetId, limit = 30) =>
  api.get(`/telemetry/${assetId}?limit=${limit}`);

// ============================================
// INCIDENTS
// ============================================
export const getIncidents = () => api.get('/incidents');
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

// ============================================
// PREDICTIONS
// ============================================
export const getPredictions = (assetId, horizon = 14) =>
  api.get(`/predictions/${assetId}?horizon=${horizon}`);

// ============================================
// DASHBOARD
// ============================================
export const getDashboard = () => api.get('/dashboard');
export const getOperationsLive = () => api.get('/operations/live');

// ============================================
// OPERATIONS AUDIT
// ============================================
export const getIncidentAudit = (limit = 100) => api.get(`/incidents/audit?limit=${limit}`);
export const getIncidentAuditDetail = (incidentId) =>
  api.get(`/incidents/audit/${encodeURIComponent(incidentId)}`);

// ============================================
// GLOBAL AI ASSISTANT
// ============================================
// Knowledge retrieval can legitimately take longer than telemetry/dashboard calls.
export const askAssistant = (question) => api.post('/assistant/query', { question }, { timeout: 60000 });

// Persistent operator supervision; this records a decision but does not command equipment.
export const recordOperatorAction = (payload) => api.post('/operator-actions', payload);
export const getPlatformMetadata = () => api.get('/metadata');
export const markNotificationsRead = (payload) => api.post('/notifications/read', payload);

// ============================================
// REPORTS
// ============================================
export const getReports = () => api.get('/reports');

// ============================================
// DIGITAL TWIN
// ============================================
export const getTwinAssets = () => api.get('/twin-assets');

export default api;
```

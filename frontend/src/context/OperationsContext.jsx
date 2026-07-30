import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { getOperationsLive } from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';

const OperationsContext = createContext(null);
const POLL_CONNECTED_MS = 60000;
const POLL_DISCONNECTED_MS = 15000;
const POLL_MAX_BACKOFF_MS = 120000;
let initialOperationsRequest = null;

const emptySnapshot = {
  dashboard: {}, assets: [], refineries: [], telemetry_by_refinery: [], critical_incidents: [], audit_logs: [],
  operator_actions: [],
  investigation: { status: 'waiting', stages: [] }, ai_activity: [],
  maintenance: { tasks: [] }, predicted_failures: [], notifications: [], reports: [],
  telemetry: { readings: [] }, critical_asset_telemetry: [],
  simulation: { automatic: false, state: 'offline' },
};

const collectionKeys = ['assets', 'refineries', 'telemetry_by_refinery', 'critical_incidents', 'audit_logs', 'operator_actions', 'ai_activity', 'predicted_failures', 'notifications', 'reports', 'critical_asset_telemetry'];
const objectKeys = ['dashboard', 'investigation', 'maintenance', 'telemetry', 'simulation'];

function mergeOperations(current, incoming) {
  if (!incoming || typeof incoming !== 'object') return current;
  const next = { ...current, ...incoming };
  objectKeys.forEach((key) => {
    if (incoming[key] && typeof incoming[key] === 'object' && !Array.isArray(incoming[key])) next[key] = { ...(current[key] || {}), ...incoming[key] };
  });
  collectionKeys.forEach((key) => {
    if (!Array.isArray(incoming[key])) next[key] = current[key] || [];
  });
  return next;
}

export function OperationsProvider({ children }) {
  const [initialOperations, setInitialOperations] = useState(emptySnapshot);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const notifiedIds = useRef(new Set());
  const refreshInFlight = useRef(null);
  const { connected, data: socketSnapshot } = useWebSocket();

  const refresh = useCallback(async ({ background = false } = {}) => {
    if (refreshInFlight.current) return refreshInFlight.current;
    if (!background) setLoading(true);

    const request = getOperationsLive()
      .then((response) => {
        setInitialOperations((current) => mergeOperations(current, response.data));
        setLastUpdated(Date.now());
        setError(null);
        return true;
      })
      .catch((requestError) => {
        setError(requestError);
        return false;
      })
      .finally(() => {
        if (!background) setLoading(false);
        refreshInFlight.current = null;
      });
    refreshInFlight.current = request;
    return request;
  }, []);

  useEffect(() => {
    let active = true;
    if (!initialOperationsRequest) {
      initialOperationsRequest = getOperationsLive()
        .finally(() => { initialOperationsRequest = null; });
    }
    initialOperationsRequest
      .then((response) => {
        if (!active) return;
        setInitialOperations((current) => mergeOperations(current, response.data));
        setLastUpdated(Date.now());
        setError(null);
      })
      .catch((requestError) => active && setError(requestError))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  // The REST snapshot is an independent safety net for the live socket. It
  // keeps pages populated during deploys, sleep/wake, or a temporary WS drop.
  useEffect(() => {
    let stopped = false;
    let timeout = null;
    let failureCount = 0;

    const schedule = (delay) => {
      if (stopped) return;
      timeout = window.setTimeout(poll, delay);
    };
    const poll = async () => {
      if (document.visibilityState !== 'visible') {
        schedule(POLL_MAX_BACKOFF_MS);
        return;
      }
      const succeeded = await refresh({ background: true });
      failureCount = succeeded ? 0 : failureCount + 1;
      const healthyDelay = connected ? POLL_CONNECTED_MS : POLL_DISCONNECTED_MS;
      const retryDelay = Math.min(
        POLL_DISCONNECTED_MS * (2 ** Math.max(0, failureCount - 1)),
        POLL_MAX_BACKOFF_MS,
      );
      schedule(succeeded ? healthyDelay : retryDelay);
    };

    schedule(connected ? POLL_CONNECTED_MS : POLL_DISCONNECTED_MS);
    return () => {
      stopped = true;
      if (timeout) window.clearTimeout(timeout);
    };
  }, [connected, refresh]);

  useEffect(() => {
    if (!socketSnapshot) return;
    (socketSnapshot.notifications || []).filter((notification) => !notification.read).slice(0, 5).forEach((notification) => {
      if (notifiedIds.current.has(notification.id)) return;
      notifiedIds.current.add(notification.id);
      toast(notification.title, {
        duration: 4000,
        icon: notification.severity === 'critical' ? '🔴' : notification.severity === 'warning' ? '🟠' : '🔵',
      });
    });
  }, [socketSnapshot]);

  const value = useMemo(() => {
    const operations = socketSnapshot
      ? mergeOperations(initialOperations, socketSnapshot)
      : initialOperations;
    const socketGeneratedAt = socketSnapshot?.generated_at
      ? Date.parse(socketSnapshot.generated_at)
      : null;
    const effectiveLastUpdated = Number.isFinite(socketGeneratedAt)
      ? socketGeneratedAt
      : lastUpdated;
    const telemetryReadings = operations.telemetry?.readings || [];
    const currentValue = Number(telemetryReadings.at?.(-1)?.value);
    const agents = (operations.investigation?.stages || []).map((stage) => ({ name: stage.agent, state: stage.state || 'waiting', confidence: stage.confidence, duration: stage.duration_seconds }));
    const ambient = { lastUpdated: effectiveLastUpdated, telemetry: { value: currentValue, delta: 0, unit: operations.telemetry?.unit || '' }, agents, incidentCount: Number(operations.dashboard?.active_incidents || operations.critical_incidents?.length || 0) };
    return { operations, ambient, connected, loading: socketSnapshot ? false : loading, error: socketSnapshot ? null : error, refresh };
  }, [initialOperations, connected, loading, error, socketSnapshot, refresh, lastUpdated]);
  return <OperationsContext.Provider value={value}>{children}</OperationsContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useOperations() {
  const context = useContext(OperationsContext);
  if (!context) throw new Error('useOperations must be used inside OperationsProvider');
  return context;
}

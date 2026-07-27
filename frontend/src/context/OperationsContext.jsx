import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { getOperationsLive } from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';

const OperationsContext = createContext(null);

const emptySnapshot = {
  dashboard: {}, assets: [], refineries: [], telemetry_by_refinery: [], critical_incidents: [], audit_logs: [],
  investigation: { status: 'waiting', stages: [] }, ai_activity: [],
  maintenance: { tasks: [] }, predicted_failures: [], notifications: [], reports: [],
  telemetry: { readings: [] }, critical_asset_telemetry: [],
};

const collectionKeys = ['assets', 'refineries', 'telemetry_by_refinery', 'critical_incidents', 'audit_logs', 'ai_activity', 'predicted_failures', 'notifications', 'reports', 'critical_asset_telemetry'];
const objectKeys = ['dashboard', 'investigation', 'maintenance', 'telemetry'];

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
  const { connected, data: socketSnapshot } = useWebSocket();

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await getOperationsLive();
      setInitialOperations((current) => mergeOperations(current, response.data));
      setLastUpdated(Date.now());
      setError(null);
    } catch (requestError) {
      setError(requestError);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    getOperationsLive()
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
    const interval = setInterval(() => { refresh(); }, 10000);
    return () => clearInterval(interval);
  }, [refresh]);

  useEffect(() => {
    if (!socketSnapshot) return;
    setInitialOperations((current) => mergeOperations(current, socketSnapshot));
    setLastUpdated(Date.now());
    (socketSnapshot.notifications || []).forEach((notification) => {
      if (notifiedIds.current.has(notification.id)) return;
      notifiedIds.current.add(notification.id);
      toast(notification.title, {
        duration: 4000,
        icon: notification.severity === 'critical' ? '🔴' : notification.severity === 'warning' ? '🟠' : '🔵',
      });
    });
  }, [socketSnapshot]);

  const value = useMemo(() => {
    const operations = initialOperations;
    const telemetryReadings = operations.telemetry?.readings || [];
    const currentValue = Number(telemetryReadings.at?.(-1)?.value);
    const agents = (operations.investigation?.stages || []).map((stage) => ({ name: stage.agent, state: stage.state || 'waiting', confidence: stage.confidence, duration: stage.duration_seconds }));
    const ambient = { lastUpdated, telemetry: { value: currentValue, delta: 0, unit: operations.telemetry?.unit || '' }, agents, incidentCount: Number(operations.dashboard?.active_incidents || operations.critical_incidents?.length || 0) };
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

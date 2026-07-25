import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { getOperationsLive } from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';

const OperationsContext = createContext(null);

const emptySnapshot = {
  dashboard: {}, assets: [], refineries: [], telemetry_by_refinery: [], critical_incidents: [], audit_logs: [],
  investigation: { status: 'waiting', stages: [] }, ai_activity: [],
  maintenance: { tasks: [] }, predicted_failures: [], notifications: [], reports: [],
  telemetry: { readings: [] },
};

export function OperationsProvider({ children }) {
  const [initialOperations, setInitialOperations] = useState(emptySnapshot);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const notifiedIds = useRef(new Set());
  const { connected, data: socketSnapshot } = useWebSocket();

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await getOperationsLive();
      setInitialOperations({ ...emptySnapshot, ...response.data });
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
        setInitialOperations({ ...emptySnapshot, ...response.data });
        setError(null);
      })
      .catch((requestError) => active && setError(requestError))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!socketSnapshot) return;
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
    const operations = socketSnapshot ? { ...emptySnapshot, ...socketSnapshot } : initialOperations;
    return { operations, connected, loading: socketSnapshot ? false : loading, error: socketSnapshot ? null : error, refresh };
  }, [initialOperations, connected, loading, error, socketSnapshot, refresh]);
  return <OperationsContext.Provider value={value}>{children}</OperationsContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useOperations() {
  const context = useContext(OperationsContext);
  if (!context) throw new Error('useOperations must be used inside OperationsProvider');
  return context;
}

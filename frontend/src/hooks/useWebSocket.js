import { useEffect, useRef, useState } from 'react';
import { toast } from 'react-hot-toast';

/**
 * Prefer same-origin /ws (Vite proxies to backend). Fall back to local API.
 * Absolute VITE_WS_URL wins when set.
 */
function resolveWsUrl() {
  if (import.meta.env.VITE_WS_URL) return import.meta.env.VITE_WS_URL;
  if (typeof window !== 'undefined') {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${proto}//${window.location.host}/ws`;
  }
  return 'ws://localhost:8080/ws';
}

const RECONNECT_MIN_DELAY = 3000;
const RECONNECT_MAX_DELAY = 120000;
const STRICT_MODE_CONNECT_DELAY = 75;

/**
 * Keeps the most recently verified snapshot on screen while the connection
 * recovers. A dropped socket is a transport issue, never evidence that the
 * facility suddenly has no assets, incidents, or audit history.
 */
export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const [data, setData] = useState(null);
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const disposedRef = useRef(false);
  const attemptsRef = useRef(0);

  useEffect(() => {
    disposedRef.current = false;

    const scheduleReconnect = () => {
      if (disposedRef.current) return;
      if (reconnectTimeoutRef.current) window.clearTimeout(reconnectTimeoutRef.current);
      const baseDelay = Math.min(
        RECONNECT_MIN_DELAY * (2 ** attemptsRef.current),
        RECONNECT_MAX_DELAY,
      );
      const delay = Math.round(baseDelay * (0.85 + Math.random() * 0.3));
      attemptsRef.current += 1;
      reconnectTimeoutRef.current = window.setTimeout(() => {
        reconnectTimeoutRef.current = null;
        connect();
      }, delay);
    };

    const connect = () => {
      if (disposedRef.current) return;
      const existing = socketRef.current;
      if (existing && (existing.readyState === WebSocket.OPEN || existing.readyState === WebSocket.CONNECTING)) {
        return;
      }

      try {
        const socket = new WebSocket(resolveWsUrl());
        socketRef.current = socket;

        socket.onopen = () => {
          if (disposedRef.current) {
            socket.close();
            return;
          }
          const wasReconnecting = attemptsRef.current > 0;
          attemptsRef.current = 0;
          setConnected(true);
          if (wasReconnecting) toast.success('Live operations connection restored', { duration: 2200 });
        };

        socket.onmessage = (event) => {
          try {
            const payload = JSON.parse(event.data);
            if (payload.type === 'update' && payload.data) setData(payload.data);
          } catch (error) {
            console.error('WebSocket payload parse error:', error);
          }
        };

        // Browser transport owns the close transition; onclose schedules retry.
        socket.onerror = () => {};
        socket.onclose = () => {
          if (socketRef.current === socket) socketRef.current = null;
          if (disposedRef.current) return;
          setConnected(false);
          scheduleReconnect();
        };
      } catch (error) {
        console.error('WebSocket setup error:', error);
        setConnected(false);
        scheduleReconnect();
      }
    };

    // Avoid opening then immediately closing the first socket during React
    // StrictMode's development-only effect probe.
    const initialConnectTimeout = window.setTimeout(connect, STRICT_MODE_CONNECT_DELAY);
    const onVisibilityChange = () => {
      if (document.visibilityState !== 'visible') return;
      if (!socketRef.current && !reconnectTimeoutRef.current) scheduleReconnect();
    };
    document.addEventListener('visibilitychange', onVisibilityChange);

    return () => {
      disposedRef.current = true;
      window.clearTimeout(initialConnectTimeout);
      if (reconnectTimeoutRef.current) window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
      document.removeEventListener('visibilitychange', onVisibilityChange);
      const socket = socketRef.current;
      socketRef.current = null;
      if (socket) {
        socket.onopen = null;
        socket.onmessage = null;
        socket.onerror = null;
        socket.onclose = null;
        if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
          try { socket.close(1000, 'unmount'); } catch { /* ignore */ }
        }
      }
    };
  }, []);

  return { connected, data };
}

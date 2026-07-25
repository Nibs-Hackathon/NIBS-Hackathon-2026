import { useEffect, useRef, useState } from 'react';
import { toast } from 'react-hot-toast';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8080/ws';
const RECONNECT_MIN_DELAY = 1500;
const RECONNECT_MAX_DELAY = 15000;

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
      const delay = Math.min(
        RECONNECT_MIN_DELAY * (2 ** attemptsRef.current),
        RECONNECT_MAX_DELAY,
      );
      attemptsRef.current += 1;
      reconnectTimeoutRef.current = window.setTimeout(connect, delay);
    };

    const connect = () => {
      if (disposedRef.current || socketRef.current?.readyState === WebSocket.OPEN) return;

      try {
        const socket = new WebSocket(WS_URL);
        socketRef.current = socket;

        socket.onopen = () => {
          if (disposedRef.current) return;
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

        socket.onerror = () => socket.close();
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

    connect();
    return () => {
      disposedRef.current = true;
      if (reconnectTimeoutRef.current) window.clearTimeout(reconnectTimeoutRef.current);
      socketRef.current?.close();
      socketRef.current = null;
    };
  }, []);

  return { connected, data };
}

# Folder: frontend/src/hooks Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/hooks`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/hooks/useWebSocket.js

**Folder path:** `frontend/src/hooks`

**File path:** `frontend/src/hooks/useWebSocket.js`

```javascript
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
      if (reconnectTimeoutRef.current) window.clearTimeout(reconnectTimeoutRef.current);
      const delay = Math.min(
        RECONNECT_MIN_DELAY * (2 ** attemptsRef.current),
        RECONNECT_MAX_DELAY,
      );
      attemptsRef.current += 1;
      reconnectTimeoutRef.current = window.setTimeout(connect, delay);
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

        socket.onerror = () => {
          // Let onclose own reconnect; closing here avoids half-open proxies.
          if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
            try { socket.close(1000, 'error'); } catch { /* already closing */ }
          }
        };
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
      reconnectTimeoutRef.current = null;
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
```

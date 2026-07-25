import { useEffect, useState, useRef } from 'react';
import { toast } from 'react-hot-toast';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const [data, setData] = useState(null);
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      socketRef.current = new WebSocket(WS_URL);

      socketRef.current.onopen = () => {
        console.log('✅ WebSocket connected');
        setConnected(true);
        toast.success('Connected to RigOS', { duration: 2000 });
      };

      socketRef.current.onclose = () => {
        console.log('❌ WebSocket disconnected');
        setConnected(false);
        // Fall back to the REST snapshot while the replacement socket opens.
        setData(null);
        // Attempt reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      };

      socketRef.current.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'update') {
            setData(payload.data);
          }
        } catch (e) {
          console.error('WebSocket parse error:', e);
        }
      };
    };

    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  return { connected, data };
}

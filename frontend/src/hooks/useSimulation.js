import { useCallback, useEffect, useRef, useState } from 'react';

const getWsUrl = () => {
  const host = window.location.hostname || '127.0.0.1';
  return `ws://${host}:8000/ws/simulation`;
};

export function useSimulation() {
  const wsRef = useRef(null);
  const [status, setStatus] = useState('disconnected'); // disconnected | idle | loading | running | paused | error
  const [gridState, setGridState] = useState(null);
  const [episodeHistory, setEpisodeHistory] = useState([]); // [{episode, reward}]
  const [checkpoints, setCheckpoints] = useState([]);
  const [selectedCheckpoint, setSelectedCheckpoint] = useState(50000);
  const [speed, setSpeed] = useState(300); // ms between steps
  const [errorMsg, setErrorMsg] = useState('');

  // Fetch available checkpoints on mount
  useEffect(() => {
    fetch('/api/training/checkpoints')
      .then(r => r.json())
      .then(data => {
        if (data.checkpoints?.length) {
          setCheckpoints(data.checkpoints);
          // Default to middle checkpoint
          const mid = data.checkpoints[Math.floor(data.checkpoints.length / 2)];
          setSelectedCheckpoint(mid);
        }
      })
      .catch(() => {});
  }, []);

  // Connect WebSocket on mount
  const connect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.onmessage = null;
      wsRef.current.onclose = null;
      wsRef.current.close();
    }

    const ws = new WebSocket(getWsUrl());

    ws.onopen = () => {
      setStatus('idle');
      setErrorMsg('');
    };

    ws.onmessage = (evt) => {
      const msg = JSON.parse(evt.data);

      if (msg.type === 'state') {
        const data = msg.data;
        setGridState(data);
        // When episode ends, record it for the chart
        if (data.is_done) {
          setEpisodeHistory(prev => [
            ...prev,
            { episode: data.episode, reward: data.reward },
          ]);
        }
      } else if (msg.type === 'status') {
        setStatus(msg.status);
      } else if (msg.type === 'error') {
        setErrorMsg(msg.message);
        setStatus('error');
      }
    };

    ws.onclose = () => setStatus('disconnected');
    ws.onerror = () => setStatus('error');

    wsRef.current = ws;
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, [connect]);

  // Send helper
  const send = useCallback((msg) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg));
    }
  }, []);

  const start = useCallback(() => {
    send({ action: 'start', checkpoint: selectedCheckpoint, speed });
  }, [send, selectedCheckpoint, speed]);

  const pause = useCallback(() => send({ action: 'pause' }), [send]);
  const resume = useCallback(() => send({ action: 'resume' }), [send]);

  const reset = useCallback(() => {
    setEpisodeHistory([]);
    setGridState(null);
    send({ action: 'reset' });
  }, [send]);

  const newEnv = useCallback(() => send({ action: 'new_env' }), [send]);

  const updateSpeed = useCallback((ms) => {
    setSpeed(ms);
    send({ action: 'set_speed', speed: ms });
  }, [send]);

  return {
    status,
    gridState,
    episodeHistory,
    checkpoints,
    selectedCheckpoint,
    setSelectedCheckpoint,
    speed,
    updateSpeed,
    errorMsg,
    start,
    pause,
    resume,
    reset,
    newEnv,
  };
}

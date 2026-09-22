import { useCallback, useEffect, useRef, useState } from 'react';

export function useTraining() {
  const [isReplaying, setIsReplaying] = useState(false);
  const [isDone, setIsDone] = useState(false);
  const [progress, setProgress] = useState(0);   // 0-100
  const [total, setTotal] = useState(49);
  const [current, setCurrent] = useState(0);     // entries received so far
  const [logLines, setLogLines] = useState([]);  // displayed log strings
  const [latestEntry, setLatestEntry] = useState(null);
  const [chartData, setChartData] = useState([]); // [{timestep, mean_reward, success_rate}]
  const esRef = useRef(null);

  const startReplay = useCallback((speed = 0.12) => {
    // Close any existing stream
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
    }

    setIsReplaying(true);
    setIsDone(false);
    setProgress(0);
    setCurrent(0);
    setLogLines([]);
    setLatestEntry(null);
    setChartData([]);

    const es = new EventSource(`/api/training/replay?speed=${speed}`);
    esRef.current = es;

    es.onmessage = (evt) => {
      const msg = JSON.parse(evt.data);

      if (msg.type === 'start') {
        setTotal(msg.total);
      } else if (msg.type === 'update') {
        const d = msg.data;
        setCurrent(prev => prev + 1);
        setTotal(t => t);
        setProgress(Math.round((d.n_updates / 49) * 100));
        setLatestEntry(d);

        // Build a PPO-style log line
        const line = [
          `| rollout/            |`,
          `  ep_rew_mean: ${d.mean_reward.toFixed(4).padStart(8)}`,
          `  success_rate: ${d.success_rate.toFixed(1).padStart(5)}%`,
          `| time/               |`,
          `  fps: ${String(d.fps).padStart(5)}`,
          `  n_updates: ${String(d.n_updates).padStart(4)}`,
          `  total_timesteps: ${String(d.timestep).padStart(7)}`,
          `| train/              |`,
          `  entropy_loss: ${d.entropy_loss.toFixed(4)}`,
          `  value_loss: ${d.value_loss.toFixed(4)}`,
          `  policy_gradient_loss: ${d.policy_gradient_loss.toFixed(6)}`,
          `${'─'.repeat(38)}`,
        ].join('\n');

        setLogLines(prev => [...prev, line].slice(-80)); // keep last 80 lines
        setChartData(prev => [
          ...prev,
          { timestep: d.timestep, mean_reward: d.mean_reward, success_rate: d.success_rate },
        ]);
      } else if (msg.type === 'done') {
        setIsReplaying(false);
        setIsDone(true);
        setProgress(100);
        es.close();
        esRef.current = null;
      }
    };

    es.onerror = () => {
      setIsReplaying(false);
      es.close();
      esRef.current = null;
    };
  }, []);

  const stopReplay = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
    }
    setIsReplaying(false);
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (esRef.current) esRef.current.close();
    };
  }, []);

  return { isReplaying, isDone, progress, logLines, latestEntry, chartData, startReplay, stopReplay };
}

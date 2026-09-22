import { useEffect, useRef } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import styles from './TrainingPanel.module.css';

export default function TrainingPanel({ training, onStartReplay, onStopReplay }) {
  const { isReplaying, isDone, progress, logLines, latestEntry, chartData } = training;
  const logRef = useRef(null);

  // Auto-scroll log
  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [logLines]);

  return (
    <div className={`card ${styles.panel}`}>
      <div className={styles.header}>
        <span className="section-label">Training Progress — PPO Replay</span>
        <div className={styles.headerRight}>
          {isDone && <span className={`badge badge-running`}>Complete</span>}
          {!isReplaying && !isDone && (
            <button className="btn btn-primary" id="btn-replay" onClick={() => onStartReplay(0.12)}>
              ▶ Replay Training
            </button>
          )}
          {isReplaying && (
            <button className="btn" id="btn-stop-replay" onClick={onStopReplay}>
              ⏹ Stop
            </button>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <div className={styles.progressWrap}>
        <div className={styles.progressTrack}>
          <div className={styles.progressFill} style={{ width: `${progress}%` }} />
        </div>
        <span className={styles.progressLabel}>
          {latestEntry
            ? `${latestEntry.timestep.toLocaleString()} / 100,000 timesteps`
            : 'Press "Replay Training" to simulate the training run'}
        </span>
      </div>

      {/* Live stats row */}
      {latestEntry && (
        <div className={styles.liveStats}>
          <LiveStat label="Mean Reward" value={latestEntry.mean_reward.toFixed(4)} color="cyan" />
          <LiveStat label="Success Rate" value={`${latestEntry.success_rate.toFixed(1)}%`} color="green" />
          <LiveStat label="FPS" value={latestEntry.fps} color="purple" />
          <LiveStat label="Entropy" value={latestEntry.entropy_loss.toFixed(4)} color="amber" />
          <LiveStat label="Updates" value={latestEntry.n_updates} color="default" />
        </div>
      )}

      <div className={styles.body}>
        {/* Reward + Success chart */}
        <div className={styles.chartWrap}>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={chartData} margin={{ top: 4, right: 16, left: -24, bottom: 4 }}>
                <defs>
                  <linearGradient id="trainRewardGrad" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%"   stopColor="#00d4ff" />
                    <stop offset="100%" stopColor="#7c3aed" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                <XAxis
                  dataKey="timestep"
                  tickFormatter={v => `${(v/1000).toFixed(0)}K`}
                  tick={{ fill: 'rgba(232,232,255,0.35)', fontSize: 9 }}
                  axisLine={false} tickLine={false}
                />
                <YAxis yAxisId="left"
                  tick={{ fill: 'rgba(232,232,255,0.35)', fontSize: 9 }}
                  axisLine={false} tickLine={false}
                  domain={[-0.2, 1.0]}
                />
                <YAxis yAxisId="right" orientation="right"
                  tick={{ fill: 'rgba(232,232,255,0.35)', fontSize: 9 }}
                  axisLine={false} tickLine={false}
                  domain={[0, 100]}
                  tickFormatter={v => `${v}%`}
                />
                <Tooltip
                  contentStyle={{ background:'rgba(13,13,40,0.95)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:8, fontSize:11 }}
                  labelFormatter={v => `Timestep: ${v.toLocaleString()}`}
                />
                <Legend
                  wrapperStyle={{ fontSize: 10, color: 'rgba(232,232,255,0.5)', paddingTop: 4 }}
                />
                <Line yAxisId="left" type="monotone" dataKey="mean_reward"
                  name="Mean Reward" stroke="url(#trainRewardGrad)"
                  strokeWidth={2} dot={false} isAnimationActive={false}
                />
                <Line yAxisId="right" type="monotone" dataKey="success_rate"
                  name="Success %" stroke="#10b981"
                  strokeWidth={1.5} dot={false} strokeDasharray="4 2" isAnimationActive={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className={styles.emptyChart}>Training chart will appear here during replay</div>
          )}
        </div>

        {/* Log console */}
        <div ref={logRef} className={styles.log}>
          {logLines.length === 0 ? (
            <span className={styles.logEmpty}>— stdout will stream here —</span>
          ) : (
            logLines.map((line, i) => (
              <pre key={i} className={styles.logLine}>{line}</pre>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

function LiveStat({ label, value, color }) {
  const colorMap = {
    cyan: 'var(--cyan)', green: 'var(--green)',
    purple: 'var(--purple)', amber: 'var(--amber)',
    default: 'var(--text-primary)',
  };
  return (
    <div className={styles.liveStat}>
      <span className={styles.liveVal} style={{ color: colorMap[color] }}>{value}</span>
      <span className={styles.liveLabel}>{label}</span>
    </div>
  );
}

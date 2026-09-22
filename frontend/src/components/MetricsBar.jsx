import styles from './MetricsBar.module.css';

export default function MetricsBar({ gridState, selectedCheckpoint }) {
  const m = gridState?.metrics;

  return (
    <div className={`card ${styles.bar}`}>
      <Metric
        label="Success Rate"
        value={m ? `${m.success_rate}%` : '—'}
        color="green"
        icon="✓"
      />
      <div className={styles.sep} />
      <Metric
        label="Avg Reward"
        value={m ? m.avg_reward.toFixed(3) : '—'}
        color="cyan"
        icon="◈"
      />
      <div className={styles.sep} />
      <Metric
        label="Avg Steps"
        value={m ? m.avg_steps.toFixed(1) : '—'}
        color="purple"
        icon="⟳"
      />
      <div className={styles.sep} />
      <Metric
        label="Timesteps"
        value={selectedCheckpoint ? selectedCheckpoint.toLocaleString() : '—'}
        color="amber"
        icon="⏱"
      />
    </div>
  );
}

function Metric({ label, value, color, icon }) {
  const colorMap = {
    green:  'var(--green)',
    cyan:   'var(--cyan)',
    purple: 'var(--purple)',
    amber:  'var(--amber)',
  };
  return (
    <div className={styles.metric}>
      <span className={styles.icon} style={{ color: colorMap[color] }}>{icon}</span>
      <span className={styles.value} style={{ color: colorMap[color] }}>{value}</span>
      <span className={styles.label}>{label}</span>
    </div>
  );
}

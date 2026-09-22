import styles from './NPCStatus.module.css';

const STATUS_LABEL = {
  disconnected: 'Disconnected',
  idle:         'Idle',
  loading:      'Loading Model…',
  running:      'Running',
  paused:       'Paused',
  error:        'Error',
};

export default function NPCStatus({ status, gridState, selectedCheckpoint, errorMsg }) {
  const m = gridState?.metrics;

  return (
    <div className={`card ${styles.panel}`}>
      <div className={styles.panelHeader}>
        <span className="section-label">NPC Status</span>
        <span className={`badge badge-${status}`}>
          <span className={`pulse-dot ${status}`} />
          {STATUS_LABEL[status] ?? status}
        </span>
      </div>

      <div className={styles.rows}>
        <Row label="Model" value="PPO (MlpPolicy)" highlight />
        <Row label="Checkpoint" value={selectedCheckpoint ? `${selectedCheckpoint.toLocaleString()} steps` : '—'} />
        <Row label="Episode" value={gridState?.episode ?? '—'} />
        <Row label="Step" value={gridState?.step ?? '—'} />
        <Row
          label="Reward"
          value={gridState ? gridState.reward.toFixed(4) : '—'}
          color={gridState?.reward > 0 ? 'green' : gridState?.reward < 0 ? 'red' : undefined}
        />
        <Row label="Done" value={gridState ? (gridState.is_done ? 'Yes ✓' : 'No') : '—'} />
      </div>

      {errorMsg && (
        <div className={styles.error}>{errorMsg}</div>
      )}

      <div className={styles.divider} />

      <div className={styles.miniMetrics}>
        <MiniStat label="Success Rate" value={m ? `${m.success_rate}%` : '—'} />
        <MiniStat label="Avg Reward" value={m ? m.avg_reward.toFixed(3) : '—'} />
        <MiniStat label="Avg Steps" value={m ? m.avg_steps.toFixed(1) : '—'} />
        <MiniStat label="Episodes" value={m ? m.total_episodes : '—'} />
      </div>
    </div>
  );
}

function Row({ label, value, highlight, color }) {
  return (
    <div className={styles.row}>
      <span className={styles.rowLabel}>{label}</span>
      <span
        className={styles.rowValue}
        style={{
          color: highlight ? 'var(--cyan)' : color === 'green' ? 'var(--green)' : color === 'red' ? 'var(--red)' : undefined,
          fontWeight: highlight ? 700 : 500,
        }}
      >
        {value}
      </span>
    </div>
  );
}

function MiniStat({ label, value }) {
  return (
    <div className={styles.miniStat}>
      <span className={styles.miniValue}>{value}</span>
      <span className={styles.miniLabel}>{label}</span>
    </div>
  );
}

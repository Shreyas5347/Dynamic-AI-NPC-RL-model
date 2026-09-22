import styles from './TrainingControls.module.css';

export default function TrainingControls({
  status,
  checkpoints,
  selectedCheckpoint,
  setSelectedCheckpoint,
  speed,
  updateSpeed,
  onStart,
  onPause,
  onResume,
  onReset,
  onNewEnv,
}) {
  const isIdle         = status === 'idle' || status === 'disconnected';
  const isRunning      = status === 'running';
  const isPaused       = status === 'paused';
  const isLoading      = status === 'loading';
  const canControl     = isRunning || isPaused;

  return (
    <div className={`card ${styles.panel}`}>
      {/* Checkpoint + speed selectors */}
      <div className={styles.selectors}>
        <label className={styles.selectWrap}>
          <span className="section-label">Checkpoint</span>
          <select
            className={styles.select}
            value={selectedCheckpoint}
            onChange={e => setSelectedCheckpoint(Number(e.target.value))}
            disabled={isRunning || isLoading}
          >
            {checkpoints.map(ck => (
              <option key={ck} value={ck}>{ck.toLocaleString()} steps</option>
            ))}
          </select>
        </label>

        <label className={styles.selectWrap}>
          <span className="section-label">Speed — {speed} ms/step</span>
          <input
            type="range"
            min={50}
            max={800}
            step={50}
            value={speed}
            onChange={e => updateSpeed(Number(e.target.value))}
            className={styles.slider}
          />
        </label>
      </div>

      {/* Buttons */}
      <div className={styles.buttons}>
        {(isIdle || isLoading) && (
          <button
            id="btn-start"
            className="btn btn-primary"
            onClick={onStart}
            disabled={isLoading || !checkpoints.length}
          >
            {isLoading ? (
              <><span className={styles.spinner} /> Loading…</>
            ) : (
              <><span>▶</span> START</>
            )}
          </button>
        )}

        {isRunning && (
          <button id="btn-pause" className="btn" onClick={onPause}>
            ⏸ PAUSE
          </button>
        )}

        {isPaused && (
          <button id="btn-resume" className="btn btn-primary" onClick={onResume}>
            ▶ RESUME
          </button>
        )}

        {canControl && (
          <>
            <button id="btn-new-env" className="btn" onClick={onNewEnv}>
              ⟳ NEW ENV
            </button>
            <button id="btn-reset" className="btn btn-danger" onClick={onReset}>
              ✕ RESET
            </button>
          </>
        )}
      </div>
    </div>
  );
}

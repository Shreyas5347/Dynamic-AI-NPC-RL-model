import { useSimulation } from './hooks/useSimulation.js';
import { useTraining } from './hooks/useTraining.js';
import Header from './components/Header.jsx';
import GridCanvas from './components/GridCanvas.jsx';
import NPCStatus from './components/NPCStatus.jsx';
import TrainingControls from './components/TrainingControls.jsx';
import RewardChart from './components/RewardChart.jsx';
import MetricsBar from './components/MetricsBar.jsx';
import TrainingPanel from './components/TrainingPanel.jsx';
import styles from './App.module.css';

export default function App() {
  const sim = useSimulation();
  const training = useTraining();

  return (
    <div className={styles.app}>
      <Header />

      <main className={styles.main}>
        {/* ── TOP SECTION: Grid + Status ── */}
        <section className={styles.topSection}>
          {/* Left: Grid + Controls */}
          <div className={styles.leftCol}>
            <GridCanvas gridState={sim.gridState} />

            <TrainingControls
              status={sim.status}
              checkpoints={sim.checkpoints}
              selectedCheckpoint={sim.selectedCheckpoint}
              setSelectedCheckpoint={sim.setSelectedCheckpoint}
              speed={sim.speed}
              updateSpeed={sim.updateSpeed}
              onStart={sim.start}
              onPause={sim.pause}
              onResume={sim.resume}
              onReset={sim.reset}
              onNewEnv={sim.newEnv}
            />
          </div>

          {/* Right: Status + Reward Chart */}
          <div className={styles.rightCol}>
            <NPCStatus
              status={sim.status}
              gridState={sim.gridState}
              selectedCheckpoint={sim.selectedCheckpoint}
              errorMsg={sim.errorMsg}
            />
            <RewardChart episodeHistory={sim.episodeHistory} />
          </div>
        </section>

        {/* ── TRAINING PANEL ── */}
        <section>
          <TrainingPanel
            training={training}
            onStartReplay={training.startReplay}
            onStopReplay={training.stopReplay}
          />
        </section>

        {/* ── METRICS BAR ── */}
        <section>
          <MetricsBar
            gridState={sim.gridState}
            selectedCheckpoint={sim.selectedCheckpoint}
          />
        </section>
      </main>
    </div>
  );
}

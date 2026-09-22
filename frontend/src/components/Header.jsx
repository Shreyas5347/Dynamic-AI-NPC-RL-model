import styles from './Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>⬡</span>
          <div>
            <h1 className={styles.title}>DYNAMIC NPC AI</h1>
            <span className={styles.subtitle}>RL SIMULATOR</span>
          </div>
        </div>
        <div className={styles.tags}>
          <span className={styles.tag}>PPO</span>
          <span className={styles.tag}>MiniGrid</span>
          <span className={styles.tag}>8 × 8</span>
          <span className={styles.tag}>stable-baselines3</span>
        </div>
      </div>
    </header>
  );
}

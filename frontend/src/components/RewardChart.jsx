import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';
import styles from './RewardChart.module.css';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className={styles.tooltip}>
      <p className={styles.tooltipLabel}>Episode {label}</p>
      <p className={styles.tooltipValue}>
        Reward: <strong>{payload[0].value.toFixed(4)}</strong>
      </p>
    </div>
  );
};

export default function RewardChart({ episodeHistory }) {
  const data = episodeHistory.map((h, i) => ({
    episode: h.episode ?? i + 1,
    reward: h.reward,
  }));

  const isEmpty = data.length === 0;

  return (
    <div className={`card ${styles.panel}`}>
      <div className={styles.header}>
        <span className="section-label">Episode Rewards</span>
        {data.length > 0 && (
          <span className={styles.count}>{data.length} episodes</span>
        )}
      </div>

      {isEmpty ? (
        <div className={styles.empty}>
          <span>Chart will populate as the NPC completes episodes</span>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={160}>
          <LineChart data={data} margin={{ top: 8, right: 16, left: -20, bottom: 4 }}>
            <defs>
              <linearGradient id="rewardGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%"   stopColor="#00d4ff" />
                <stop offset="100%" stopColor="#7c3aed" />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis
              dataKey="episode"
              tick={{ fill: 'rgba(232,232,255,0.4)', fontSize: 10 }}
              axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
              tickLine={false}
              label={{ value: 'Episode', position: 'insideBottomRight', offset: -4, fill: 'rgba(232,232,255,0.3)', fontSize: 10 }}
            />
            <YAxis
              tick={{ fill: 'rgba(232,232,255,0.4)', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              domain={['auto', 'auto']}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine y={0} stroke="rgba(255,255,255,0.15)" strokeDasharray="4 4" />
            <Line
              type="monotone"
              dataKey="reward"
              stroke="url(#rewardGrad)"
              strokeWidth={2}
              dot={data.length < 30 ? { r: 3, fill: '#00d4ff', strokeWidth: 0 } : false}
              activeDot={{ r: 5, fill: '#00d4ff', strokeWidth: 2, stroke: '#fff' }}
              isAnimationActive={true}
              animationDuration={400}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

import { useEffect, useRef } from 'react';
import styles from './GridCanvas.module.css';

const CELL = 50;        // px per cell
const GRID_SIZE = 8;
const CANVAS_SIZE = CELL * GRID_SIZE;

// Direction → angle (radians). MiniGrid: 0=right,1=down,2=left,3=up
const DIR_ANGLE = [0, Math.PI / 2, Math.PI, -Math.PI / 2];

function drawCell(ctx, x, y, type) {
  const px = x * CELL;
  const py = y * CELL;

  switch (type) {
    case 'wall': {
      const g = ctx.createLinearGradient(px, py, px + CELL, py + CELL);
      g.addColorStop(0, '#22204a');
      g.addColorStop(1, '#16143a');
      ctx.fillStyle = g;
      ctx.fillRect(px, py, CELL, CELL);
      ctx.strokeStyle = 'rgba(140, 100, 255, 0.18)';
      ctx.lineWidth = 1;
      ctx.strokeRect(px + 0.5, py + 0.5, CELL - 1, CELL - 1);
      // Corner accents
      ctx.strokeStyle = 'rgba(140, 100, 255, 0.35)';
      ctx.lineWidth = 2;
      const a = 6;
      ctx.beginPath();
      ctx.moveTo(px + a, py + 1); ctx.lineTo(px + 1, py + 1); ctx.lineTo(px + 1, py + a);
      ctx.moveTo(px + CELL - a, py + 1); ctx.lineTo(px + CELL - 1, py + 1); ctx.lineTo(px + CELL - 1, py + a);
      ctx.moveTo(px + 1, py + CELL - a); ctx.lineTo(px + 1, py + CELL - 1); ctx.lineTo(px + a, py + CELL - 1);
      ctx.moveTo(px + CELL - 1, py + CELL - a); ctx.lineTo(px + CELL - 1, py + CELL - 1); ctx.lineTo(px + CELL - a, py + CELL - 1);
      ctx.stroke();
      break;
    }
    case 'goal': {
      ctx.fillStyle = '#060f0a';
      ctx.fillRect(px, py, CELL, CELL);
      // Outer glow rings
      const cx = px + CELL / 2, cy = py + CELL / 2;
      const radii = [22, 16, 10];
      const alphas = [0.08, 0.14, 0.22];
      radii.forEach((r, i) => {
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(16, 185, 129, ${alphas[i]})`;
        ctx.fill();
      });
      // Core gem shape
      ctx.save();
      ctx.shadowBlur = 20;
      ctx.shadowColor = '#10b981';
      ctx.fillStyle = '#10b981';
      ctx.beginPath();
      ctx.arc(cx, cy, 8, 0, Math.PI * 2);
      ctx.fill();
      // Highlight
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      ctx.beginPath();
      ctx.arc(cx - 2, cy - 2, 2.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
      break;
    }
    default: {
      ctx.fillStyle = '#09091e';
      ctx.fillRect(px, py, CELL, CELL);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.025)';
      ctx.lineWidth = 0.5;
      ctx.strokeRect(px + 0.5, py + 0.5, CELL - 1, CELL - 1);
    }
  }
}

function drawAgent(ctx, ax, ay, dir) {
  const cx = ax * CELL + CELL / 2;
  const cy = ay * CELL + CELL / 2;
  const angle = DIR_ANGLE[dir] ?? 0;
  const R = 14, r = 8;

  // Outer glow halo
  const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R + 10);
  grad.addColorStop(0, 'rgba(0, 212, 255, 0.22)');
  grad.addColorStop(1, 'rgba(0, 212, 255, 0)');
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(cx, cy, R + 10, 0, Math.PI * 2);
  ctx.fill();

  // Body circle
  ctx.save();
  ctx.shadowBlur = 18;
  ctx.shadowColor = '#00d4ff';
  ctx.fillStyle = '#0a2030';
  ctx.strokeStyle = '#00d4ff';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Direction triangle
  const tip = { x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle) };
  const left = { x: cx + r * Math.cos(angle + 2.356), y: cy + r * Math.sin(angle + 2.356) };
  const right = { x: cx + r * Math.cos(angle - 2.356), y: cy + r * Math.sin(angle - 2.356) };
  ctx.fillStyle = '#00d4ff';
  ctx.shadowBlur = 10;
  ctx.beginPath();
  ctx.moveTo(tip.x, tip.y);
  ctx.lineTo(left.x, left.y);
  ctx.lineTo(right.x, right.y);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

export default function GridCanvas({ gridState }) {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const prevAgentRef = useRef(null);
  const animProgressRef = useRef(1);
  const prevGridStateRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const render = (interpX, interpY) => {
      ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

      // Background
      ctx.fillStyle = '#07071a';
      ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

      if (!gridState) {
        // Placeholder grid lines
        for (let x = 0; x < GRID_SIZE; x++) {
          for (let y = 0; y < GRID_SIZE; y++) {
            ctx.strokeStyle = 'rgba(255,255,255,0.04)';
            ctx.lineWidth = 0.5;
            ctx.strokeRect(x * CELL + 0.5, y * CELL + 0.5, CELL - 1, CELL - 1);
          }
        }
        // "Waiting" text
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.font = '500 14px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Select checkpoint and click START', CANVAS_SIZE / 2, CANVAS_SIZE / 2);
        return;
      }

      // Draw cells
      gridState.cells.forEach(cell => drawCell(ctx, cell.x, cell.y, cell.type));

      // Draw agent (interpolated or final position)
      const ax = interpX !== undefined ? interpX : gridState.agent.x;
      const ay = interpY !== undefined ? interpY : gridState.agent.y;
      drawAgent(ctx, ax, ay, gridState.agent.dir);
    };

    // Detect agent movement → animate
    const prev = prevAgentRef.current;
    const curr = gridState?.agent;

    if (
      curr && prev &&
      (prev.x !== curr.x || prev.y !== curr.y) &&
      prevGridStateRef.current
    ) {
      // Cancel any ongoing animation
      if (animRef.current) cancelAnimationFrame(animRef.current);
      animProgressRef.current = 0;

      const startX = prev.x, startY = prev.y;
      const endX = curr.x, endY = curr.y;

      const animate = () => {
        animProgressRef.current = Math.min(1, animProgressRef.current + 0.15);
        const t = animProgressRef.current;
        const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // ease-in-out
        render(startX + (endX - startX) * ease, startY + (endY - startY) * ease);
        if (animProgressRef.current < 1) {
          animRef.current = requestAnimationFrame(animate);
        }
      };
      animRef.current = requestAnimationFrame(animate);
    } else {
      render();
    }

    prevAgentRef.current = curr ? { ...curr } : null;
    prevGridStateRef.current = gridState;

    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, [gridState]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.label}>
        <span>8 × 8 GRID</span>
        {gridState && (
          <span className={styles.coords}>
            Agent ({gridState.agent.x}, {gridState.agent.y}) → Goal ({gridState.goal.x}, {gridState.goal.y})
          </span>
        )}
      </div>
      <div className={styles.canvasFrame}>
        <canvas
          ref={canvasRef}
          width={CANVAS_SIZE}
          height={CANVAS_SIZE}
          className={styles.canvas}
        />
      </div>
    </div>
  );
}

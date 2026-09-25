import { useRef, type FC, type PointerEvent } from 'react';
import { motion, useMotionValue, useReducedMotion, useSpring, type Variants } from 'framer-motion';
import {
  ArrowRight,
  ExternalLink,
  Compass,
} from 'lucide-react';
import { PulseScannerIcon, StatusBeacon } from './icons';

interface BentoHeroProps {
  onOpenTelegramModal: () => void;
  onOpenAuthModal: () => void;
  onScrollToSandbox: () => void;
}

/* ── Bento Card Data ────────────────────────────────────────────────────── */

const skillPills = [
  'DevOps & CI/CD',
  'Engineering',
  'Machine Learning',
  'Computations',
  'User Experience',
  'Data Engineering',
];

const matchScoreRows = [
  { label: 'Relevant Candidate Qualifications', score: '89/60' },
  { label: 'Candidate Competency Analysis', score: '89/80' },
  { label: 'Relevant Domain Qualifications', score: '82/5' },
];

/* ── Stagger Variants ───────────────────────────────────────────────────── */

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.07,
      delayChildren: 0.1,
    },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 20, scale: 0.98 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      duration: 0.55,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

export const BentoHero: FC<BentoHeroProps> = ({
  onOpenTelegramModal,
  onOpenAuthModal,
  onScrollToSandbox,
}) => {
  const dashboardRef = useRef<HTMLDivElement>(null);

  const reduceMotion = useReducedMotion();
  const rotateX = useSpring(useMotionValue(0), { stiffness: 120, damping: 20, mass: 0.5 });
  const rotateY = useSpring(useMotionValue(0), { stiffness: 120, damping: 20, mass: 0.5 });

  const resetTilt = () => {
    rotateX.set(0);
    rotateY.set(0);
  };

  const handleTilt = (e: PointerEvent<HTMLDivElement>) => {
    if (reduceMotion || e.pointerType === 'touch') return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    rotateX.set(y * -3);
    rotateY.set(x * 4);
  };

  return (
    <section className="nexus-hero">
      {/* ── Hero Copy & Actions ─────────────────────────────────── */}
      <div className="nexus-hero-copy">
        <motion.div
          className="nexus-pill"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{ marginBottom: '22px' }}
        >
          <span className="pulse-dot" />
          <span>HYBRID CAREER INTELLIGENCE · WEB HQ & TELEGRAM AGENT</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
        >
          Autonomous Career Headquarters <span className="hero-accent">& Pro Telegram Agent.</span>
        </motion.h1>

        <motion.p
          className="nexus-hero-subtitle"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.12, ease: [0.16, 1, 0.3, 1] }}
        >
          Evaluate your resume against any target job description completely free.
          Sign in to unlock a <strong>7-Day All-Access Pass</strong> to our Power BI application cockpit,
          live startup funding radar, and 24/7 autonomous Telegram partner.
        </motion.p>

        <motion.div
          className="nexus-hero-actions"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.18, ease: [0.16, 1, 0.3, 1] }}
        >
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onScrollToSandbox}
            className="btn-primary"
          >
            <PulseScannerIcon size={16} className="scanner-animated" color="var(--accent-light)" />
            <span>Test Free ATS Checker</span>
            <ArrowRight size={16} />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onOpenAuthModal}
            className="btn-secondary"
            style={{
              background: 'rgba(255, 255, 255, 0.9)',
              borderColor: 'var(--accent)',
              color: 'var(--text-primary)',
            }}
          >
            <Compass size={15} color="var(--primary)" />
            <span>Start 7-Day All-Access Pass</span>
          </motion.button>
        </motion.div>

        {/* Micro Trust Banner */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.25 }}
          style={{
            marginTop: '16px',
            fontSize: '0.80rem',
            color: 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
            <StatusBeacon size={6} color="#16a34a" />
            <span>Free ATS checks require zero login</span>
          </span>
          <span>·</span>
          <span>7-Day full Pro trial on sign in</span>
          <span>·</span>
          <span>Zero credit card required</span>
        </motion.div>
      </div>

      {/* ── Signature Bento Cockpit Grid ─────────────────────────── */}
      <motion.div
        className="nexus-grid"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Card 1 */}
        <motion.div
          className="surface-card nexus-col-6"
          variants={cardVariants}
          ref={dashboardRef}
          onPointerMove={handleTilt}
          onPointerLeave={resetTilt}
          style={{ rotateX, rotateY, transformPerspective: 1200 }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
            <h3 className="ats-header" style={{ marginBottom: 0 }}>ATS score card</h3>
            <span className="nexus-pill nexus-pill-dark">CALIBRATED</span>
          </div>

          <div className="ats-ring-area">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
              {skillPills.slice(0, 3).map((skill) => (
                <span className="skill-tag" key={skill}>{skill}</span>
              ))}
            </div>

            <div className="ats-ring">
              <svg viewBox="0 0 120 120" aria-label="89% ATS match score">
                <circle cx="60" cy="60" r="52" className="ats-ring-track" />
                <circle cx="60" cy="60" r="52" className="ats-ring-value" />
              </svg>
              <div className="ats-ring-label">
                <strong>89%</strong>
                <span>match</span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1, alignItems: 'flex-end' }}>
              {skillPills.slice(3).map((skill) => (
                <span className="skill-tag" key={skill}>{skill}</span>
              ))}
            </div>
          </div>

          <table className="score-table">
            <thead>
              <tr>
                <th>Matched Skill Tags</th>
                <th>Match Score</th>
              </tr>
            </thead>
            <tbody>
              {matchScoreRows.map((row) => (
                <tr key={row.label}>
                  <td>{row.label}</td>
                  <td>{row.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>

        {/* Card 2 */}
        <motion.div
          className="surface-card nexus-col-3"
          variants={cardVariants}
          style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
        >
          <div className="briefing-block">
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '10px' }}>
              <svg width="34" height="34" viewBox="0 0 34 34" fill="none">
                <circle cx="17" cy="17" r="15" stroke="rgba(161, 184, 135, 0.25)" strokeWidth="1" strokeDasharray="3 3" />
                <circle cx="17" cy="17" r="10" stroke="rgba(161, 184, 135, 0.45)" strokeWidth="1" />
                <path d="M12 17 L17 12 L22 17 M17 12 L17 22" stroke="var(--accent-light)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <div className="briefing-time">7:00 PM</div>
            <div className="briefing-meta">Batch: 3<br />Matched High-Signal Roles</div>
            <div className="briefing-badge">Automated Job<br />evening update</div>
          </div>
        </motion.div>

        {/* Card 3 */}
        <motion.div
          className="surface-card nexus-col-3"
          variants={cardVariants}
          style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
              <span className="nexus-pill nexus-pill-dark" style={{ fontSize: '0.62rem' }}>RADAR ACTIVE</span>
              <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="8" stroke="rgba(161, 184, 135, 0.3)" strokeWidth="1" />
                <circle cx="10" cy="10" r="4" stroke="rgba(161, 184, 135, 0.5)" strokeWidth="1" />
                <line x1="10" y1="10" x2="16" y2="4" stroke="var(--accent-light)" strokeWidth="1.5" strokeLinecap="round" className="radar-sweep-arm" />
                <circle cx="10" cy="10" r="2" fill="var(--accent-light)" />
              </svg>
            </div>
            <h4 className="funding-title">Startup Funding Radar</h4>
            <p className="funding-desc">Direct founder LinkedIn links from newly funded seed &amp; series A companies.</p>
            <button className="btn-surface" type="button" onClick={onScrollToSandbox} style={{ width: '100%', marginBottom: '16px' }}>
              <span>Founder LinkedIn</span>
              <ExternalLink size={13} />
            </button>
          </div>

          <div style={{ paddingTop: '16px', borderTop: '1px solid var(--border-surface)' }}>
            <h4 className="funding-title" style={{ fontSize: '0.98rem' }}>Venture Intelligence</h4>
            <button
              className="btn-surface"
              type="button"
              onClick={onOpenTelegramModal}
              style={{
                width: '100%',
                background: 'rgba(161, 184, 135, 0.20)',
                color: '#FAF7F2',
                border: '1px solid rgba(161, 184, 135, 0.40)',
                boxShadow: 'none',
                fontWeight: '600',
              }}
            >
              <span>Connect Telegram</span>
            </button>
          </div>
        </motion.div>

        {/* Row 2: Metric Cards with authentic SVG instruments */}
        <motion.div className="surface-card nexus-col-4" variants={cardVariants}>
          <div className="metric-card">
            <div className="telemetry-instrument">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="rgba(161, 184, 135, 0.25)" strokeWidth="1" />
                <path d="M5 12 C7 8, 9 16, 12 12 C15 8, 17 16, 19 12" stroke="var(--accent-light)" strokeWidth="1.8" strokeLinecap="round" className="wave-path-active" />
              </svg>
            </div>
            <div>
              <div className="metric-label">32ms Vector Computation</div>
              <div className="metric-sublabel">Sub-second cosine distance across 1,536 embeddings</div>
            </div>
          </div>
        </motion.div>

        <motion.div className="surface-card nexus-col-4" variants={cardVariants}>
          <div className="metric-card">
            <div className="telemetry-instrument">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="5" width="18" height="14" rx="3" stroke="rgba(217, 119, 6, 0.35)" strokeWidth="1.2" />
                <line x1="7" y1="10" x2="17" y2="10" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round" />
                <line x1="7" y1="14" x2="13" y2="14" stroke="var(--accent-light)" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            </div>
            <div>
              <div className="metric-label">Two-Tier Calibration</div>
              <div className="metric-sublabel">Vector cosine math + ModernBERT System-1 calibration</div>
            </div>
          </div>
        </motion.div>

        <motion.div className="surface-card nexus-col-4" variants={cardVariants}>
          <div className="metric-card">
            <div className="telemetry-instrument">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="rgba(22, 163, 74, 0.25)" strokeWidth="1" />
                <path d="M8 12.5 L11 15.5 L16.5 9" stroke="var(--positive)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <div>
              <div className="metric-label">Google-XYZ Rewrites</div>
              <div className="metric-sublabel">Automated impact metric bullets ready for submission</div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

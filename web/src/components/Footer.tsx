import type { FC } from 'react';
import { Shield } from 'lucide-react';

export const Footer: FC = () => {
  return (
    <footer
      style={{
        borderTop: '1px solid var(--border-warm)',
        padding: '48px 24px',
        maxWidth: '1280px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '20px',
        position: 'relative',
        zIndex: 10,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div
          style={{
            width: '30px',
            height: '30px',
            borderRadius: '9px',
            background: 'var(--primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 600,
            fontFamily: 'var(--font-display)',
            fontSize: '1.05rem',
            color: 'var(--accent-light)',
            boxShadow: '0 2px 8px rgba(46, 58, 47, 0.25)',
          }}
        >
          N
        </div>
        <span style={{ fontFamily: 'var(--font-display)', fontWeight: 500, fontSize: '1.08rem', color: 'var(--text-primary)' }}>
          Neera AI
        </span>
        <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
          • Organic Editorial Precision
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
        <span>Two-Tier ATS Engine</span>
        <span>•</span>
        <span>6–8 PM Evening Briefings</span>
        <span>•</span>
        <span>Startup Funding Radar</span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
        <Shield size={14} color="var(--positive)" />
        <span style={{ fontFamily: 'var(--font-mono)' }}>Enterprise Zero-IDOR Architecture</span>
      </div>
    </footer>
  );
};

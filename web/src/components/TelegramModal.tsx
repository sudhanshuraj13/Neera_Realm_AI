import { useState, useEffect, type FC } from 'react';
import {
  Send,
  X,
  CheckCircle2,
  Copy,
  ExternalLink,
  ShieldCheck,
} from 'lucide-react';

interface TelegramModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TelegramModal: FC<TelegramModalProps> = ({ isOpen, onClose }) => {
  const [copied, setCopied] = useState(false);
  const sampleCode = 'NEERA-7892';

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(`/link ${sampleCode}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'rgba(28, 18, 11, 0.65)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        zIndex: 100,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
      }}
      onClick={onClose}
    >
      <div
        className="surface-card"
        role="dialog"
        aria-modal="true"
        aria-label="Connect Telegram AI Companion"
        style={{
          width: '100%',
          maxWidth: '520px',
          padding: '34px',
          position: 'relative',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'var(--surface-light)',
            border: '1px solid var(--border-surface)',
            borderRadius: 'var(--radius-pill)',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text-on-surface-muted)',
            cursor: 'pointer',
            transition: 'color 0.2s',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = '#ffffff')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-on-surface-muted)')}
        >
          <X size={16} />
        </button>

        {/* Modal Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '18px' }}>
          <div
            style={{
              width: '42px',
              height: '42px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(161, 184, 135, 0.15)',
              border: '1px solid rgba(161, 184, 135, 0.35)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Send size={20} color="var(--accent-light)" />
          </div>
          <div>
            <h3 style={{ fontSize: '1.28rem', fontWeight: '700', color: 'var(--text-on-surface)', letterSpacing: '-0.01em' }}>
              Connect Your Telegram Bot
            </h3>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-on-surface-muted)' }}>
              Pocket agent for 6–8 PM evening batches &amp; startup radar
            </span>
          </div>
        </div>

        <p style={{ fontSize: '0.9rem', color: 'var(--text-on-surface-muted)', marginBottom: '24px', lineHeight: '1.6' }}>
          Pairing your Web Console with Telegram allows Neera to dispatch your phone once every evening with
          verified ≥75% ATS match jobs and flash funding alerts.
        </p>

        {/* 2-Step Pairing Instructions */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '26px' }}>
          <div style={{ background: 'var(--surface-light)', padding: '16px 20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-surface)' }}>
            <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--accent-light)', marginBottom: '10px', fontFamily: 'var(--font-mono)', letterSpacing: '0.05em' }}>
              STEP 1: OPEN NEERA BOT
            </div>
            <a
              href="https://t.me/NeeraCareerBot"
              target="_blank"
              rel="noreferrer"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                background: 'rgba(161, 184, 135, 0.18)',
                color: '#FAF7F2',
                border: '1px solid rgba(161, 184, 135, 0.40)',
                padding: '9px 18px',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.86rem',
                fontWeight: '600',
                textDecoration: 'none',
                transition: 'background 0.2s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(161, 184, 135, 0.28)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'rgba(161, 184, 135, 0.18)')}
            >
              <Send size={14} color="var(--accent-light)" />
              <span>@NeeraCareerBot on Telegram</span>
              <ExternalLink size={12} color="var(--accent-light)" />
            </a>
          </div>

          <div style={{ background: 'var(--surface-light)', padding: '16px 20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-surface)' }}>
            <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--accent-light)', marginBottom: '10px', fontFamily: 'var(--font-mono)', letterSpacing: '0.05em' }}>
              STEP 2: SEND PAIRING CODE
            </div>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: 'rgba(0, 0, 0, 0.45)',
                padding: '12px 16px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-surface)',
              }}
            >
              <code style={{ color: '#FBBF24', fontFamily: 'var(--font-mono)', fontSize: '0.95rem', fontWeight: '700', letterSpacing: '0.04em' }}>
                /link {sampleCode}
              </code>

              <button
                onClick={handleCopy}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: copied ? 'var(--positive)' : 'var(--text-on-surface-muted)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  fontSize: '0.80rem',
                  fontWeight: '600',
                }}
              >
                {copied ? <CheckCircle2 size={14} /> : <Copy size={14} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-on-surface-muted)', marginTop: '6px', fontFamily: 'var(--font-mono)' }}>
              Expires in 15 minutes • Single-use cryptographic token
            </div>
          </div>
        </div>

        {/* Security & Multi-Channel Notice */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.76rem', color: 'var(--text-on-surface-muted)' }}>
          <ShieldCheck size={16} color="var(--positive)" />
          <span>Zero-Trust: Isolated and encrypted on Supabase PostgreSQL.</span>
        </div>
      </div>
    </div>
  );
};

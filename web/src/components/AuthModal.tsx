import { useState, useEffect, type FC } from 'react';
import {
  X,
  CheckCircle2,
  ShieldCheck,
  Mail,
  ArrowRight,
} from 'lucide-react';
import { StatusBeacon } from './icons';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const AuthModal: FC<AuthModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) return;
    setIsSubmitted(true);
    setTimeout(() => {
      if (onSuccess) onSuccess();
    }, 1500);
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'rgba(25, 28, 33, 0.70)',
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
        aria-label="7-Day All-Access Pass Activation"
        style={{
          width: '100%',
          maxWidth: '500px',
          padding: '36px',
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

        {!isSubmitted ? (
          <div>
            {/* Badge */}
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '4px 12px',
                borderRadius: 'var(--radius-pill)',
                background: 'rgba(161, 184, 135, 0.18)',
                border: '1px solid rgba(161, 184, 135, 0.35)',
                color: 'var(--accent-light)',
                fontSize: '0.74rem',
                fontWeight: 700,
                fontFamily: 'var(--font-mono)',
                textTransform: 'uppercase',
                marginBottom: '16px',
              }}
            >
              <StatusBeacon size={6} color="var(--accent-light)" />
              <span>7-Day All-Access Pass</span>
            </div>

            <h3
              style={{
                fontSize: '1.75rem',
                fontFamily: 'var(--font-display)',
                color: 'var(--text-on-surface)',
                marginBottom: '8px',
                lineHeight: 1.15,
              }}
            >
              Unlock Web Headquarters & Telegram AI Agent
            </h3>

            <p
              style={{
                fontSize: '0.88rem',
                color: 'var(--text-on-surface-muted)',
                lineHeight: 1.55,
                marginBottom: '24px',
              }}
            >
              Sign in to activate 7 days of full Pro access. Monitor applications in the Power BI
              cockpit, connect your Telegram bot, and receive venture radar alerts.
            </p>

            {/* Trial Benefits */}
            <div
              style={{
                background: 'var(--surface-light)',
                borderRadius: '14px',
                border: '1px solid var(--border-surface)',
                padding: '14px 16px',
                marginBottom: '24px',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
              }}
            >
              {[
                'Full access to Web Headquarters & Application Ledger',
                '24/7 Telegram Autonomous Career Agent pairing',
                'Live Startup Funding Radar & founder email assistant',
                'Zero credit card required · Free ATS remains free forever',
              ].map((item, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.80rem', color: 'var(--text-on-surface)' }}>
                  <CheckCircle2 size={14} color="var(--accent-light)" style={{ flexShrink: 0 }} />
                  <span>{item}</span>
                </div>
              ))}
            </div>

            {/* Google Sign In Button */}
            <button
              onClick={() => {
                setIsSubmitted(true);
                setTimeout(() => {
                  if (onSuccess) onSuccess();
                }, 1500);
              }}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: 'var(--radius-pill)',
                background: '#FFFFFF',
                color: '#1F1B16',
                border: 'none',
                fontWeight: 600,
                fontSize: '0.90rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '10px',
                cursor: 'pointer',
                marginBottom: '16px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                transition: 'opacity 0.2s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.opacity = '0.92')}
              onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
            >
              <svg width="18" height="18" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"
                />
                <path
                  fill="#34A853"
                  d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.36 24 12 24z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.16 0 9.97 0 12s.45 3.84 1.25 5.42l4.03-3.15z"
                />
                <path
                  fill="#EA4335"
                  d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.36 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.93 6.72-4.93z"
                />
              </svg>
              <span>Continue with Google</span>
            </button>

            {/* Divider */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                margin: '18px 0',
                gap: '12px',
                color: 'var(--text-on-surface-muted)',
                fontSize: '0.75rem',
              }}
            >
              <div style={{ flex: 1, height: '1px', background: 'var(--border-surface)' }} />
              <span>OR WITH WORK EMAIL</span>
              <div style={{ flex: 1, height: '1px', background: 'var(--border-surface)' }} />
            </div>

            {/* Email Form */}
            <form onSubmit={handleSubmit}>
              <div style={{ position: 'relative', marginBottom: '14px' }}>
                <Mail
                  size={16}
                  style={{
                    position: 'absolute',
                    left: '16px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: 'var(--text-on-surface-muted)',
                  }}
                />
                <input
                  type="email"
                  placeholder="name@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '12px 16px 12px 42px',
                    borderRadius: 'var(--radius-pill)',
                    background: 'var(--surface-light)',
                    border: '1px solid var(--border-surface)',
                    color: 'var(--text-on-surface)',
                    fontSize: '0.88rem',
                    outline: 'none',
                  }}
                />
              </div>

              <button
                type="submit"
                className="btn-cta-pill"
                style={{
                  width: '100%',
                  justifyContent: 'center',
                  padding: '12px',
                }}
              >
                <span>Activate Free 7-Day Access</span>
                <ArrowRight size={14} />
              </button>
            </form>

            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px',
                marginTop: '16px',
                fontSize: '0.74rem',
                color: 'var(--text-on-surface-muted)',
              }}
            >
              <ShieldCheck size={14} color="var(--accent-light)" />
              <span>No credit card required. Encrypted authentication.</span>
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <div
              style={{
                width: '56px',
                height: '56px',
                borderRadius: '50%',
                background: 'rgba(161, 184, 135, 0.2)',
                border: '1px solid rgba(161, 184, 135, 0.4)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 18px',
              }}
            >
              <CheckCircle2 size={32} color="var(--accent-light)" />
            </div>

            <h3
              style={{
                fontSize: '1.6rem',
                fontFamily: 'var(--font-display)',
                color: 'var(--text-on-surface)',
                marginBottom: '8px',
              }}
            >
              Trial Activated!
            </h3>

            <p style={{ fontSize: '0.88rem', color: 'var(--text-on-surface-muted)', lineHeight: 1.55, maxWidth: '340px', margin: '0 auto 20px' }}>
              We've activated your 7-Day All-Access Pass. Your Web Headquarters is ready, and your
              Telegram pairing link has been dispatched.
            </p>

            <button
              onClick={onClose}
              className="btn-cta-pill"
              style={{ padding: '10px 24px' }}
            >
              <span>Enter Headquarters</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

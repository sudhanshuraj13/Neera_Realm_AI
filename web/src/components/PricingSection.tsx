import { useState, type FC } from 'react';
import {
  Check,
  ShieldCheck,
  Clock,
  ArrowRight,
} from 'lucide-react';
import { PulseScannerIcon, StatusBeacon } from './icons';

interface PricingSectionProps {
  onOpenAuthModal: () => void;
  onScrollToSandbox: () => void;
}

export const PricingSection: FC<PricingSectionProps> = ({
  onOpenAuthModal,
  onScrollToSandbox,
}) => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  const proPrice = billingCycle === 'monthly' ? 19 : 14;
  const billingPeriodLabel = billingCycle === 'monthly' ? '/month' : '/mo, billed annually';

  return (
    <section id="pricing" className="nexus-section" style={{ paddingBottom: '90px' }}>
      {/* Section Header */}
      <div className="nexus-section-header" style={{ textAlign: 'center', marginBottom: '36px' }}>
        <div className="nexus-pill" style={{ marginBottom: '14px', display: 'inline-flex', alignItems: 'center', gap: '7px' }}>
          <StatusBeacon size={6} color="var(--primary)" />
          <span>TRANSPARENT VALUE ARCHITECTURE · ACCESS TIERS</span>
        </div>

        <h2 style={{ maxWidth: '850px', margin: '0 auto 16px' }}>
          Start Free, Experience Everything, Upgrade for Momentum
        </h2>

        <p style={{ maxWidth: '720px', margin: '0 auto 28px' }}>
          Test your resume against any job description completely free. Sign in to activate your
          7-Day All-Access Pass with zero credit card required, then select flexible monthly or annual
          membership to keep your autonomous career agent running.
        </p>

        {/* Billing Switch */}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '14px' }}>
          <div className="pricing-toggle">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`pricing-toggle-btn ${billingCycle === 'monthly' ? 'active' : ''}`}
            >
              Monthly Billing
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`pricing-toggle-btn ${billingCycle === 'yearly' ? 'active' : ''}`}
            >
              Annual Billing
            </button>
          </div>

          {billingCycle === 'yearly' && (
            <span
              style={{
                background: 'rgba(161, 184, 135, 0.22)',
                color: 'var(--accent-light)',
                border: '1px solid rgba(161, 184, 135, 0.45)',
                padding: '4px 12px',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.76rem',
                fontWeight: 700,
                fontFamily: 'var(--font-mono)',
              }}
            >
              SAVE 26% + 2 MONTHS FREE
            </span>
          )}
        </div>
      </div>

      {/* 3 Pricing Cards Grid */}
      <div className="pricing-grid">
        {/* Tier 1: Free Public Utility */}
        <div className="pricing-card pricing-card-free">
          <div style={{ marginBottom: '16px' }}>
            <span
              style={{
                fontSize: '0.78rem',
                fontWeight: 700,
                color: 'var(--text-secondary)',
                textTransform: 'uppercase',
                fontFamily: 'var(--font-mono)',
                letterSpacing: '0.05em',
              }}
            >
              Public Utility
            </span>
            <h3
              style={{
                fontSize: '1.65rem',
                fontFamily: 'var(--font-display)',
                color: 'var(--text-primary)',
                marginTop: '4px',
                marginBottom: '8px',
              }}
            >
              Free Forever
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              Immediate, objective ATS resume audit against any target job description.
            </p>
          </div>

          <div style={{ margin: '14px 0 24px', display: 'flex', alignItems: 'baseline', gap: '4px' }}>
            <span style={{ fontSize: '2.8rem', fontWeight: 700, fontFamily: 'var(--font-display)', color: 'var(--text-primary)' }}>
              $0
            </span>
            <span style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>forever, no sign-in</span>
          </div>

          <button
            onClick={onScrollToSandbox}
            className="btn-secondary"
            style={{
              width: '100%',
              justifyContent: 'center',
              marginBottom: '26px',
            }}
          >
            <span>Test ATS Check Now</span>
            <ArrowRight size={14} />
          </button>

          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-primary)', textTransform: 'uppercase', marginBottom: '12px', letterSpacing: '0.04em' }}>
            What’s Included:
          </div>

          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', padding: 0, margin: 0 }}>
            {[
              'Instant Resume vs JD ATS evaluation',
              '30ms vector cosine semantic match score',
              'Detected missing keywords & competencies',
              'Google-XYZ bullet point rewrite advice',
              'Zero login or credit card required',
            ].map((feature, i) => (
              <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
                <Check size={16} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Tier 2: 7-Day All-Access Pass (On Sign-Up / Login) */}
        <div className="pricing-card pricing-card-trial">
          <div
            style={{
              position: 'absolute',
              top: '-13px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'var(--primary)',
              color: 'var(--accent-light)',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.72rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              padding: '4px 14px',
              borderRadius: 'var(--radius-pill)',
              boxShadow: '0 4px 12px rgba(46, 58, 47, 0.25)',
              border: '1px solid rgba(161, 184, 135, 0.4)',
              whiteSpace: 'nowrap',
            }}
          >
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
              <StatusBeacon size={6} color="var(--accent-light)" />
              <span>INCLUDED UPON SIGN IN</span>
            </span>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <span
              style={{
                fontSize: '0.78rem',
                fontWeight: 700,
                color: 'var(--primary)',
                textTransform: 'uppercase',
                fontFamily: 'var(--font-mono)',
                letterSpacing: '0.05em',
              }}
            >
              Account Activation
            </span>
            <h3
              style={{
                fontSize: '1.65rem',
                fontFamily: 'var(--font-display)',
                color: 'var(--text-primary)',
                marginTop: '4px',
                marginBottom: '8px',
              }}
            >
              7-Day All-Access Pass
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              Full, unrestricted access to the Web Headquarters & Telegram AI Agent.
            </p>
          </div>

          <div style={{ margin: '14px 0 24px', display: 'flex', alignItems: 'baseline', gap: '4px' }}>
            <span style={{ fontSize: '2.8rem', fontWeight: 700, fontFamily: 'var(--font-display)', color: 'var(--text-primary)' }}>
              $0
            </span>
            <span style={{ fontSize: '0.88rem', color: 'var(--primary)', fontWeight: 600 }}>for 7 full days</span>
          </div>

          <button
            onClick={onOpenAuthModal}
            className="btn-primary"
            style={{
              width: '100%',
              justifyContent: 'center',
              marginBottom: '26px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <span>Claim 7-Day Free Pass</span>
            <ArrowRight size={15} />
          </button>

          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-primary)', textTransform: 'uppercase', marginBottom: '12px', letterSpacing: '0.04em' }}>
            Everything in Free, Plus:
          </div>

          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', padding: 0, margin: 0 }}>
            {[
              'Full Power BI application tracking ledger',
              'Historical ATS review & submission archive',
              'Telegram 24/7 AI Career Agent bot access',
              'Timed evening job batches (6:00–8:00 PM)',
              'Live Startup Funding Radar (Seed to Series B)',
              'Founder LinkedIn intel & email draft assistant',
              'Zero credit card required to start',
            ].map((feature, i) => (
              <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
                <Check size={16} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span style={{ fontWeight: i === 0 || i === 2 ? 600 : 400 }}>{feature}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Tier 3: Pro Membership (Monthly or Yearly) */}
        <div className="pricing-card pricing-card-pro">
          <div className="pricing-badge-popular">
            RECOMMENDED FOR ACTIVE JOB HUNTERS
          </div>

          <div style={{ marginBottom: '16px' }}>
            <span
              style={{
                fontSize: '0.78rem',
                fontWeight: 700,
                color: 'var(--accent-light)',
                textTransform: 'uppercase',
                fontFamily: 'var(--font-mono)',
                letterSpacing: '0.05em',
              }}
            >
              Continuous Acceleration
            </span>
            <h3
              style={{
                fontSize: '1.65rem',
                fontFamily: 'var(--font-display)',
                color: 'var(--text-on-surface)',
                marginTop: '4px',
                marginBottom: '8px',
              }}
            >
              Pro Membership
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-on-surface-muted)', lineHeight: 1.5 }}>
              Continuous, autonomous career intelligence, background scrapers, and outreach.
            </p>
          </div>

          <div style={{ margin: '14px 0 24px', display: 'flex', alignItems: 'baseline', gap: '4px' }}>
            <span style={{ fontSize: '2.8rem', fontWeight: 700, fontFamily: 'var(--font-display)', color: 'var(--text-on-surface)' }}>
              ${proPrice}
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-on-surface-muted)' }}>{billingPeriodLabel}</span>
          </div>

          <button
            onClick={onOpenAuthModal}
            className="btn-cta-pill"
            style={{
              width: '100%',
              justifyContent: 'center',
              marginBottom: '26px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <PulseScannerIcon size={16} className="scanner-animated" color="var(--primary)" />
            <span>Upgrade to Pro</span>
          </button>

          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--accent-light)', textTransform: 'uppercase', marginBottom: '12px', letterSpacing: '0.04em' }}>
            Complete Career Operating System:
          </div>

          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', padding: 0, margin: 0 }}>
            {[
              'Continuous Web Headquarters telemetry & export',
              '24/7 background job matching & priority alerts',
              'Real-time venture rounds & verified founder emails',
              'Autonomous founder cold outreach dispatch',
              'Unlimited deep multi-resume ATS audits',
              'Direct Telegram conversation with AI Career Agent',
              'Cancel or pause anytime with 1-click',
            ].map((feature, i) => (
              <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.86rem', color: 'var(--text-on-surface)' }}>
                <Check size={16} color="var(--accent-light)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Trust & Guarantee Banner */}
      <div
        style={{
          maxWidth: '850px',
          margin: '40px auto 0',
          padding: '16px 24px',
          borderRadius: 'var(--radius-pill)',
          background: 'rgba(255, 255, 255, 0.5)',
          border: '1px solid var(--border-warm)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-around',
          flexWrap: 'wrap',
          gap: '16px',
          fontSize: '0.82rem',
          color: 'var(--text-secondary)',
          boxShadow: '0 4px 20px rgba(31, 27, 22, 0.04)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <ShieldCheck size={16} color="var(--primary)" />
          <span>Zero Credit Card Required for 7-Day Trial</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Clock size={16} color="var(--primary)" />
          <span>Instant Activation in 30 Seconds</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Check size={16} color="var(--primary)" />
          <span>Cancel Anytime · Free ATS Always Free</span>
        </div>
      </div>
    </section>
  );
};

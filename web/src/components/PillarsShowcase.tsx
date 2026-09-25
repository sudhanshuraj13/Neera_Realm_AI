import { useState, type FC } from 'react';
import { motion } from 'framer-motion';
import {
  Clock,
  Send,
  TrendingUp,
  ExternalLink,
  Bot,
  Mail,
  CheckCircle,
  Layers,
} from 'lucide-react';
import { LinkedinIcon } from './icons';

interface PillarsShowcaseProps {
  onOpenTelegramModal: () => void;
}

const SAMPLE_FUNDED_STARTUPS = [
  {
    company: 'Vitalis Health',
    domain: 'HealthTech AI',
    raised: '$18M Series A',
    investors: 'General Catalyst & Khosla',
    summary: 'Autonomous AI documentation and clinical diagnostics engine for ICU care teams.',
    founderLinkedin: 'https://www.linkedin.com/search/results/people/?keywords=Vitalis%20Health%20founder',
    companyLinkedin: 'https://www.linkedin.com/company/vitalis-health',
  },
  {
    company: 'Nexus Ledger',
    domain: 'FinTech Infrastructure',
    raised: '$12M Seed',
    investors: 'a16z Crypto & Founders Fund',
    summary: 'Cross-border real-time stablecoin settlement engine for B2B global supply chains.',
    founderLinkedin: 'https://www.linkedin.com/search/results/people/?keywords=Nexus%20Ledger%20founder',
    companyLinkedin: 'https://www.linkedin.com/company/nexus-ledger',
  },
  {
    company: 'Synthetica AI',
    domain: 'AI / LLM Infrastructure',
    raised: '$24M Series A',
    investors: 'Lightspeed & Benchmark',
    summary: 'High-throughput synthetic data generation platform for multimodal frontier models.',
    founderLinkedin: 'https://www.linkedin.com/search/results/people/?keywords=Synthetica%20AI%20founder',
    companyLinkedin: 'https://www.linkedin.com/company/synthetica-ai',
  },
];

export const PillarsShowcase: FC<PillarsShowcaseProps> = ({ onOpenTelegramModal }) => {
  const [activeDomainTab, setActiveDomainTab] = useState<'All' | 'HealthTech' | 'FinTech' | 'AI'>('All');
  const [briefingHour, setBriefingHour] = useState('19:00');

  const filteredStartups = SAMPLE_FUNDED_STARTUPS.filter((s) => {
    if (activeDomainTab === 'All') return true;
    return s.domain.toLowerCase().includes(activeDomainTab.toLowerCase());
  });

  return (
    <motion.section
      id="features"
      className="nexus-section"
      initial={{ opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.08 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Section Headline */}
      <div className="nexus-section-header" style={{ textAlign: 'center' }}>
        <div className="nexus-pill" style={{ marginBottom: '14px' }}>
          <Layers size={14} />
          <span>PRO TELEGRAM AGENT · INCLUDED IN 7-DAY TRIAL & PRO MEMBERSHIP</span>
        </div>

        <h2 style={{ maxWidth: '850px', margin: '0 auto 14px' }}>
          Autonomous Pro Career Agent on Telegram
        </h2>

        <p style={{ margin: '0 auto', maxWidth: '750px' }}>
          While your Web Headquarters provides the central command and historical analytics,
          your paired Telegram bot acts as your 24/7 autonomous career partner—delivering timed job
          briefings, live venture capital intelligence, and direct founder email drafting.
        </p>
      </div>

      {/* ─── PILLAR 1: Timed 6:00–8:00 PM Job Dispatches ─────────────────── */}
          <div className="pillar-card-v1">
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                <div
                  style={{
                    width: '34px',
                    height: '34px',
                    borderRadius: '10px',
                    background: 'rgba(161, 184, 135, 0.15)',
                    border: '1px solid rgba(161, 184, 135, 0.30)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <Clock size={18} color="var(--accent-light)" />
                </div>
                <span style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--accent-light)', textTransform: 'uppercase', letterSpacing: '0.05em', fontFamily: 'var(--font-mono)' }}>
                  Pillar 1: Evening Briefing Engine
                </span>
                <span className="nexus-pill nexus-pill-live" style={{ fontSize: '0.72rem', padding: '4px 12px', marginLeft: 'auto' }}>
                  TELEGRAM SYNCED
                </span>
              </div>

              <h3 style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--text-on-surface)', marginBottom: '14px', letterSpacing: '-0.02em', lineHeight: 1.25 }}>
                Zero-Spam Evening Job Batches (6:00 – 8:00 PM)
              </h3>

              <p style={{ fontSize: '0.94rem', color: 'var(--text-on-surface-muted)', marginBottom: '22px', lineHeight: '1.65' }}>
                Instead of distracting you with continuous ping alerts throughout the workday, Neera compiles your
                top matches into a single high-signal batch delivered to your phone when you actually have time to apply.
              </p>

              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '26px' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: 'var(--text-on-surface)' }}>
                  <CheckCircle size={16} color="var(--accent-light)" style={{ flexShrink: 0 }} />
                  <span>Strict <b>≥75% ATS Match Gate</b> — only verified high-fit listings dispatched.</span>
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: 'var(--text-on-surface)' }}>
                  <CheckCircle size={16} color="var(--accent-light)" style={{ flexShrink: 0 }} />
                  <span>Symmetric matrix for both <b>Freshers / Interns</b> and <b>Senior Engineers</b>.</span>
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: 'var(--text-on-surface)' }}>
                  <CheckCircle size={16} color="var(--accent-light)" style={{ flexShrink: 0 }} />
                  <span>Configure time on the <b>Web Console</b> or directly via Telegram: <code>/briefing 19:00</code>.</span>
                </li>
              </ul>

              <button
                onClick={onOpenTelegramModal}
                className="btn-cta-pill"
                style={{
                  padding: '12px 26px',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                <Send size={15} />
                <span>Configure Telegram Briefing</span>
              </button>
            </div>

            {/* Precision Interactive Widget */}
            <div
              style={{
                background: 'var(--surface-light)',
                border: '1px solid var(--border-surface)',
                borderRadius: 'var(--radius-card)',
                padding: '28px',
                boxShadow: 'inset 0 1px 0 rgba(255, 255, 255, 0.06)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
                <span style={{ fontSize: '0.86rem', fontWeight: '600', color: 'var(--text-on-surface)' }}>
                  Scheduled Dispatch Window:
                </span>
                <span className="nexus-pill nexus-pill-live" style={{ padding: '4px 12px', fontSize: '0.72rem' }}>
                  {briefingHour} (Active)
                </span>
              </div>

              <div style={{ display: 'flex', gap: '8px', marginBottom: '22px', flexWrap: 'wrap' }}>
                {['18:00', '18:30', '19:00', '19:30', '20:00'].map((time) => (
                  <button
                    key={time}
                    onClick={() => setBriefingHour(time)}
                    className="dispatch-time-btn"
                    style={{
                      background: briefingHour === time ? 'var(--accent)' : 'rgba(255, 255, 255, 0.06)',
                      color: briefingHour === time ? '#191C21' : '#FAF7F2',
                      border: briefingHour === time ? '1px solid var(--accent)' : '1px solid var(--border-surface)',
                      boxShadow: briefingHour === time ? '0 4px 14px -3px rgba(161, 184, 135, 0.5)' : 'none',
                      fontWeight: '600',
                      cursor: 'pointer',
                    }}
                  >
                    {time}
                  </button>
                ))}
              </div>

              <div className="dispatch-preview-box">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', color: 'var(--accent-light)', fontWeight: '600', fontFamily: 'var(--font-mono)' }}>
                    <Send size={13} />
                    <span>TELEGRAM DISPATCH · {briefingHour}</span>
                  </div>
                  <span style={{ fontSize: '0.70rem', color: 'var(--text-on-surface-muted)', fontFamily: 'var(--font-mono)' }}>VERIFIED BATCH</span>
                </div>
                <div style={{ fontSize: '0.84rem', color: 'var(--text-on-surface)', lineHeight: '1.55', marginBottom: '12px' }}>
                  "🔔 <b>Neera Evening Briefing ({briefingHour})</b><br />
                  Found 3 verified roles matching your profile with ATS &gt; 80% at <b>Stripe, OpenAI, and Notion</b>."
                </div>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '0.70rem', background: 'rgba(255, 255, 255, 0.08)', padding: '3px 8px', borderRadius: '4px', color: 'var(--text-on-surface)' }}>Stripe · Staff</span>
                  <span style={{ fontSize: '0.70rem', background: 'rgba(255, 255, 255, 0.08)', padding: '3px 8px', borderRadius: '4px', color: 'var(--text-on-surface)' }}>OpenAI · Research</span>
                  <span style={{ fontSize: '0.70rem', background: 'rgba(161, 184, 135, 0.18)', border: '1px solid rgba(161, 184, 135, 0.35)', color: 'var(--accent-light)', padding: '3px 8px', borderRadius: '4px', fontWeight: 600 }}>ATS 89% Match</span>
                </div>
              </div>
            </div>
          </div>

      {/* ─── PILLAR 2: Startup Funding Radar & Founder Outreach ──────────── */}
      <div
        id="funding-radar"
        className="surface-card"
        style={{ marginBottom: '32px' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '28px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <div
                style={{
                  width: '34px',
                  height: '34px',
                  borderRadius: '10px',
                  background: 'rgba(217, 119, 6, 0.12)',
                  border: '1px solid rgba(217, 119, 6, 0.25)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <TrendingUp size={18} color="var(--accent)" />
              </div>
              <span style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.05em', fontFamily: 'var(--font-mono)' }}>
                Pillar 2: Venture Capital Intelligence
              </span>
            </div>

            <h3 style={{ fontSize: '1.7rem', fontWeight: '700', color: 'var(--text-on-surface)', letterSpacing: '-0.02em', marginBottom: '6px' }}>
              Startup Funding Radar &amp; Founder Outreach
            </h3>
            <p style={{ fontSize: '0.92rem', color: 'var(--text-on-surface-muted)' }}>
              Follow the capital. When a startup gets funded in your domain, reach founders directly on LinkedIn before jobs are posted publicly.
            </p>
          </div>

          {/* Domain Filter Pills */}
          <div style={{ display: 'flex', gap: '8px' }}>
            {(['All', 'HealthTech', 'FinTech', 'AI'] as const).map((domain) => (
              <button
                key={domain}
                onClick={() => setActiveDomainTab(domain)}
                style={{
                  background: activeDomainTab === domain ? 'var(--accent)' : 'var(--surface-light)',
                  color: activeDomainTab === domain ? '#191C21' : 'var(--text-on-surface-muted)',
                  border: activeDomainTab === domain ? 'none' : '1px solid var(--border-surface)',
                  borderRadius: 'var(--radius-pill)',
                  padding: '7px 16px',
                  fontSize: '0.82rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  boxShadow: activeDomainTab === domain ? '0 4px 12px -2px rgba(161, 184, 135, 0.4)' : 'none',
                }}
              >
                {domain}
              </button>
            ))}
          </div>
        </div>

        {/* Live Startups Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
          {filteredStartups.map((startup) => (
            <div
              key={startup.company}
              style={{
                background: 'var(--surface-light)',
                border: '1px solid var(--border-surface)',
                borderRadius: 'var(--radius-card)',
                padding: '24px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                  <span style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-on-surface)' }}>
                    {startup.company}
                  </span>
                  <span className="nexus-pill nexus-pill-dark" style={{ fontSize: '0.74rem', padding: '3px 10px' }}>
                    {startup.domain}
                  </span>
                </div>

                <div style={{ fontSize: '0.88rem', color: '#FBBF24', fontWeight: '700', marginBottom: '8px', fontFamily: 'var(--font-mono)' }}>
                  {startup.raised} • {startup.investors}
                </div>

                <p style={{ fontSize: '0.84rem', color: 'var(--text-on-surface-muted)', lineHeight: '1.55', marginBottom: '20px' }}>
                  {startup.summary}
                </p>
              </div>

              {/* Action Links: Founder LinkedIn & Company */}
              <div style={{ display: 'flex', gap: '10px' }}>
                <a
                  href={startup.founderLinkedin}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    flex: 1,
                    background: 'var(--accent)',
                    color: '#191C21',
                    textDecoration: 'none',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-control)',
                    fontSize: '0.80rem',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    boxShadow: '0 4px 14px -3px rgba(161, 184, 135, 0.35)',
                  }}
                >
                  <LinkedinIcon size={14} />
                  <span>Founder LinkedIn</span>
                  <ExternalLink size={12} />
                </a>

                <a
                  href={startup.companyLinkedin}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    color: 'var(--text-on-surface)',
                    textDecoration: 'none',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-control)',
                    fontSize: '0.80rem',
                    fontWeight: '600',
                    border: '1px solid var(--border-surface)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                  }}
                >
                  <span>Company Page</span>
                  <ExternalLink size={12} />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ─── PILLAR 3: Autonomous Application & Cold Outreach ─────────── */}
      <div className="surface-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div
              style={{
                width: '34px',
                height: '34px',
                borderRadius: '10px',
                background: 'rgba(161, 184, 135, 0.15)',
                border: '1px solid rgba(161, 184, 135, 0.30)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Bot size={18} color="var(--accent-light)" />
            </div>
            <span style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--accent-light)', textTransform: 'uppercase', letterSpacing: '0.05em', fontFamily: 'var(--font-mono)' }}>
              Pillar 3: Autonomous Application Agent (Phase 4 Roadmap)
            </span>
          </div>

          <span className="nexus-pill nexus-pill-dark">
            IN ACTIVE DEVELOPMENT
          </span>
        </div>

        <h3 style={{ fontSize: '1.7rem', fontWeight: '700', color: 'var(--text-on-surface)', letterSpacing: '-0.02em', marginBottom: '12px' }}>
          Autonomous Form Auto-Filling &amp; Executive Cold Outreach
        </h3>

        <p style={{ fontSize: '0.94rem', color: 'var(--text-on-surface-muted)', maxWidth: '780px', marginBottom: '26px', lineHeight: '1.65' }}>
          Once you review a matched job or funded venture, our AI agent will autonomously parse external application
          forms (Greenhouse, Lever, Ashby), autofill candidate fields with calibrated context, and draft hyper-personalized
          cold emails to founders referencing their recent funding round and your matching projects.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
          <div style={{ background: 'var(--surface-light)', padding: '22px', borderRadius: 'var(--radius-card)', border: '1px solid var(--border-surface)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Bot size={16} color="var(--primary)" />
              <span style={{ fontWeight: '600', fontSize: '0.94rem', color: 'var(--text-on-surface)' }}>
                1-Click Application Form Fill
              </span>
            </div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-on-surface-muted)', lineHeight: '1.55' }}>
              Autonomously extracts required essays and fields from employer portals, drafting tailored responses for your final 1-click confirmation.
            </p>
          </div>

          <div style={{ background: 'var(--surface-light)', padding: '22px', borderRadius: 'var(--radius-card)', border: '1px solid var(--border-surface)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Mail size={16} color="var(--accent)" />
              <span style={{ fontWeight: '600', fontSize: '0.94rem', color: 'var(--text-on-surface)' }}>
                Contextual Cold Outreach to Founders
              </span>
            </div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-on-surface-muted)', lineHeight: '1.55' }}>
              Crafts highly tailored emails referencing the company's recent funding announcement and mapping 2 exact projects from your resume that solve their immediate engineering priorities.
            </p>
          </div>
        </div>
      </div>
    </motion.section>
  );
};

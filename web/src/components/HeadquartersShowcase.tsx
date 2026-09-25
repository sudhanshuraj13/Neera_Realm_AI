import { useState, type FC } from 'react';
import {
  BarChart3,
  TrendingUp,
  Sliders,
  ShieldCheck,
  Filter,
  Bot,
  Send,
  CheckCircle2,
  ChevronRight,
  Eye,
  Lock,
} from 'lucide-react';
import { StatusBeacon, CalibratedShieldIcon } from './icons';

interface HeadquartersShowcaseProps {
  onOpenAuthModal: () => void;
  onOpenTelegramModal: () => void;
}

interface ApplicationRecord {
  id: string;
  company: string;
  role: string;
  domain: string;
  date: string;
  score: number;
  status: 'Offer' | 'Interview' | 'Screening' | 'Applied';
  channel: 'Telegram Dispatch' | 'Web Submission';
  feedback: string;
  missingKeywords: string[];
}

const SAMPLE_APPLICATIONS: ApplicationRecord[] = [
  {
    id: 'APP-9021',
    company: 'Stripe',
    role: 'Staff Infrastructure Engineer',
    domain: 'FinTech / Systems',
    date: '2026-09-18',
    score: 94,
    status: 'Offer',
    channel: 'Telegram Dispatch',
    feedback: 'Exceptional alignment on distributed consensus, idempotent API design, and latency budgets.',
    missingKeywords: ['eBPF', 'Kafka partitioning'],
  },
  {
    id: 'APP-8942',
    company: 'Anthropic',
    role: 'Full Stack Systems Engineer',
    domain: 'AI / Frontier Models',
    date: '2026-09-15',
    score: 91,
    status: 'Interview',
    channel: 'Telegram Dispatch',
    feedback: 'High semantic match on TypeScript, streaming evaluation pipelines, and vector cosine ranking.',
    missingKeywords: ['Triton server', 'CUDA profiling'],
  },
  {
    id: 'APP-8711',
    company: 'Vercel',
    role: 'Senior Edge Platform Architect',
    domain: 'Cloud / Developer Tools',
    date: '2026-09-12',
    score: 88,
    status: 'Screening',
    channel: 'Web Submission',
    feedback: 'Strong proof on serverless execution models, Edge runtime cold-starts, and bundle optimization.',
    missingKeywords: ['Rust Wasm', 'Turbopack internal plugins'],
  },
  {
    id: 'APP-8604',
    company: 'Datadog',
    role: 'Distributed Observability Engineer',
    domain: 'Enterprise DevOps',
    date: '2026-09-08',
    score: 85,
    status: 'Applied',
    channel: 'Telegram Dispatch',
    feedback: 'Solid qualifications in high-cardinality metrics processing and Prometheus integrations.',
    missingKeywords: ['OpenTelemetry collector', 'Vector aggregations'],
  },
];

export const HeadquartersShowcase: FC<HeadquartersShowcaseProps> = ({
  onOpenAuthModal,
  onOpenTelegramModal,
}) => {
  const [filterStatus, setFilterStatus] = useState<string>('All');
  const [selectedApp, setSelectedApp] = useState<ApplicationRecord>(SAMPLE_APPLICATIONS[0]);
  const [telegramHour, setTelegramHour] = useState<string>('19:00');
  const [minMatchScore, setMinMatchScore] = useState<number>(85);
  const [autoEmailFounders, setAutoEmailFounders] = useState<boolean>(true);

  const filteredApps = SAMPLE_APPLICATIONS.filter((app) => {
    if (filterStatus === 'All') return true;
    return app.status === filterStatus;
  });

  const getStatusColor = (status: ApplicationRecord['status']) => {
    switch (status) {
      case 'Offer':
        return { bg: 'rgba(161, 184, 135, 0.22)', text: '#B6CC9D', border: 'rgba(161, 184, 135, 0.45)' };
      case 'Interview':
        return { bg: 'rgba(217, 119, 6, 0.18)', text: '#FBBF24', border: 'rgba(217, 119, 6, 0.40)' };
      case 'Screening':
        return { bg: 'rgba(59, 130, 246, 0.16)', text: '#93C5FD', border: 'rgba(59, 130, 246, 0.35)' };
      default:
        return { bg: 'rgba(255, 255, 255, 0.08)', text: '#D1D5DB', border: 'rgba(255, 255, 255, 0.15)' };
    }
  };

  return (
    <section id="hq-platform" className="nexus-section" style={{ paddingBottom: '90px' }}>
      {/* Header */}
      <div className="nexus-section-header" style={{ textAlign: 'center', marginBottom: '42px' }}>
        <div className="nexus-pill" style={{ marginBottom: '14px' }}>
          <BarChart3 size={14} />
          <span>TIER 2 & PRO · WEB HEADQUARTERS PLATFORM</span>
        </div>

        <h2 style={{ maxWidth: '880px', margin: '0 auto 16px' }}>
          Power BI-Grade Career Intelligence Cockpit
        </h2>

        <p style={{ maxWidth: '760px', margin: '0 auto' }}>
          When you sign in, unlock an executive telemetry suite. Monitor every tracked application,
          inspect historical ATS evaluations, analyze conversion velocity, and configure your
          Telegram AI agent directly from your central web dashboard.
        </p>

        {/* Trial Badge */}
        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center' }}>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 16px',
              borderRadius: 'var(--radius-pill)',
              background: 'rgba(161, 184, 135, 0.15)',
              border: '1px solid rgba(161, 184, 135, 0.35)',
              color: 'var(--accent-light)',
              fontSize: '0.84rem',
              fontWeight: 600,
              fontFamily: 'var(--font-mono)',
            }}
          >
            <StatusBeacon size={6} color="var(--accent-light)" />
            <span>Included Free for 7 Days Upon Sign In · No Credit Card Required</span>
          </div>
        </div>
      </div>

      {/* Main Cockpit Container */}
      <div className="cockpit-container">
        {/* Cockpit Toolbar */}
        <div className="cockpit-toolbar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="pulse-dot" />
              <span
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.84rem',
                  fontWeight: 700,
                  color: 'var(--text-on-surface)',
                  letterSpacing: '0.04em',
                }}
              >
                NEERA REALM HQ v5.2
              </span>
            </div>
            <span
              style={{
                fontSize: '0.75rem',
                color: 'var(--text-on-surface-muted)',
                background: 'rgba(255, 255, 255, 0.05)',
                padding: '3px 8px',
                borderRadius: '6px',
                fontFamily: 'var(--font-mono)',
              }}
            >
              CANDIDATE TELEMETRY STREAM
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button
              onClick={onOpenAuthModal}
              className="btn-surface"
              style={{
                fontSize: '0.82rem',
                padding: '7px 16px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <Lock size={13} />
              <span>Sign In to Sync</span>
            </button>

            <button
              onClick={onOpenTelegramModal}
              className="btn-cta-pill"
              style={{
                fontSize: '0.82rem',
                padding: '7px 16px',
              }}
            >
              <Send size={13} />
              <span>Link Telegram Bot</span>
            </button>
          </div>
        </div>

        {/* 4 KPI Metric Tiles */}
        <div className="cockpit-kpi-grid">
          <div className="kpi-tile">
            <div className="kpi-tile-label">
              <span>Tracked Applications</span>
              <Filter size={13} />
            </div>
            <div className="kpi-tile-value">42</div>
            <div className="kpi-tile-trend" style={{ color: '#B6CC9D' }}>
              <TrendingUp size={13} />
              <span>+12 this week across 8 sectors</span>
            </div>
          </div>

          <div className="kpi-tile">
            <div className="kpi-tile-label">
              <span>Average ATS Score</span>
              <ShieldCheck size={13} />
            </div>
            <div className="kpi-tile-value">89.4%</div>
            <div className="kpi-tile-trend" style={{ color: '#B6CC9D' }}>
              <CalibratedShieldIcon size={13} color="var(--accent-light)" />
              <span>Top 4% Candidate Percentile</span>
            </div>
          </div>

          <div className="kpi-tile">
            <div className="kpi-tile-label">
              <span>Interview Conversion</span>
              <BarChart3 size={13} />
            </div>
            <div className="kpi-tile-value">23.8%</div>
            <div className="kpi-tile-trend" style={{ color: '#FBBF24' }}>
              <TrendingUp size={13} />
              <span>3.4× Industry Benchmark</span>
            </div>
          </div>

          <div className="kpi-tile">
            <div className="kpi-tile-label">
              <span>Telegram Bot Link</span>
              <Bot size={13} />
            </div>
            <div className="kpi-tile-value" style={{ fontSize: '1.35rem', color: '#B6CC9D' }}>
              {telegramHour} BATCH
            </div>
            <div className="kpi-tile-trend" style={{ color: 'var(--text-on-surface-muted)' }}>
              <CheckCircle2 size={13} color="#B6CC9D" />
              <span>Scheduled Daily Digest</span>
            </div>
          </div>
        </div>

        {/* Main Content: Split View Table + Detail Drawer */}
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.6fr) minmax(0, 1fr)', background: 'var(--surface)' }}>
          {/* Left Column: Historical Table */}
          <div style={{ borderRight: '1px solid var(--border-surface)', overflowX: 'auto' }}>
            <div
              style={{
                padding: '14px 20px',
                background: 'rgba(25, 28, 33, 0.7)',
                borderBottom: '1px solid var(--border-surface)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '10px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-on-surface)' }}>
                  Application Pipeline Ledger
                </span>
                <span
                  style={{
                    fontSize: '0.72rem',
                    padding: '2px 8px',
                    borderRadius: '10px',
                    background: 'rgba(255, 255, 255, 0.08)',
                    fontFamily: 'var(--font-mono)',
                    color: 'var(--text-on-surface-muted)',
                  }}
                >
                  {filteredApps.length} records
                </span>
              </div>

              {/* Status Filter Chips */}
              <div style={{ display: 'flex', gap: '6px' }}>
                {['All', 'Offer', 'Interview', 'Screening'].map((status) => (
                  <button
                    key={status}
                    onClick={() => setFilterStatus(status)}
                    style={{
                      padding: '4px 10px',
                      borderRadius: 'var(--radius-pill)',
                      border: '1px solid',
                      borderColor: filterStatus === status ? 'var(--accent)' : 'rgba(255, 255, 255, 0.1)',
                      background: filterStatus === status ? 'rgba(161, 184, 135, 0.18)' : 'transparent',
                      color: filterStatus === status ? 'var(--accent-light)' : 'var(--text-on-surface-muted)',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                      transition: 'all 0.18s ease',
                    }}
                  >
                    {status}
                  </button>
                ))}
              </div>
            </div>

            <table className="powerbi-table">
              <thead>
                <tr>
                  <th>Role & Company</th>
                  <th>ATS Match</th>
                  <th>Status</th>
                  <th>Channel</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredApps.length === 0 ? (
                  <tr>
                    <td
                      colSpan={5}
                      style={{
                        textAlign: 'center',
                        padding: '36px 16px',
                        color: 'var(--text-on-surface-muted)',
                        fontSize: '0.86rem',
                        fontFamily: 'var(--font-mono)',
                      }}
                    >
                      No applications found matching status &ldquo;{filterStatus}&rdquo;.
                    </td>
                  </tr>
                ) : (
                  filteredApps.map((app) => {
                    const isSelected = selectedApp.id === app.id;
                    const statusStyle = getStatusColor(app.status);

                    return (
                      <tr
                        key={app.id}
                        onClick={() => setSelectedApp(app)}
                        style={{
                          cursor: 'pointer',
                          background: isSelected ? 'rgba(161, 184, 135, 0.07)' : 'transparent',
                        }}
                      >
                        <td>
                          <div style={{ fontWeight: 600, color: 'var(--text-on-surface)', fontSize: '0.90rem' }}>
                            {app.company}
                          </div>
                          <div style={{ fontSize: '0.78rem', color: 'var(--text-on-surface-muted)', marginTop: '2px' }}>
                            {app.role} · {app.domain}
                          </div>
                        </td>

                        <td>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div
                              style={{
                                width: '38px',
                                height: '5px',
                                background: 'rgba(255, 255, 255, 0.1)',
                                borderRadius: '4px',
                                overflow: 'hidden',
                              }}
                            >
                              <div
                                style={{
                                  width: `${app.score}%`,
                                  height: '100%',
                                  background: app.score >= 90 ? 'var(--accent-light)' : '#FBBF24',
                                }}
                              />
                            </div>
                            <span
                              style={{
                                fontSize: '0.80rem',
                                fontWeight: 700,
                                fontFamily: 'var(--font-mono)',
                                color: app.score >= 90 ? 'var(--accent-light)' : '#FBBF24',
                              }}
                            >
                              {app.score}%
                            </span>
                          </div>
                        </td>

                        <td>
                          <span
                            style={{
                              display: 'inline-block',
                              padding: '3px 10px',
                              borderRadius: '12px',
                              fontSize: '0.72rem',
                              fontWeight: 700,
                              fontFamily: 'var(--font-mono)',
                              background: statusStyle.bg,
                              color: statusStyle.text,
                              border: `1px solid ${statusStyle.border}`,
                            }}
                          >
                            {app.status}
                          </span>
                        </td>

                        <td>
                          <span style={{ fontSize: '0.78rem', color: 'var(--text-on-surface-muted)' }}>
                            {app.channel}
                          </span>
                        </td>

                        <td>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedApp(app);
                            }}
                            style={{
                              background: 'transparent',
                              border: 'none',
                              color: isSelected ? 'var(--accent-light)' : 'var(--text-on-surface-muted)',
                              cursor: 'pointer',
                              padding: '4px',
                            }}
                            title="Inspect ATS Feedback"
                          >
                            <ChevronRight size={16} />
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* Right Column: Historical ATS Review & Telegram Command Center */}
          <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '22px' }}>
            {/* Active Selected Card Detail */}
            <div
              style={{
                background: 'var(--surface-light)',
                border: '1px solid var(--border-surface)',
                borderRadius: '18px',
                padding: '20px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Eye size={15} color="var(--accent-light)" />
                  <span
                    style={{
                      fontSize: '0.76rem',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 700,
                      color: 'var(--accent-light)',
                      textTransform: 'uppercase',
                    }}
                  >
                    Historical ATS Audit · {selectedApp.id}
                  </span>
                </div>
                <span
                  style={{
                    fontSize: '0.72rem',
                    color: 'var(--text-on-surface-muted)',
                    fontFamily: 'var(--font-mono)',
                  }}
                >
                  {selectedApp.date}
                </span>
              </div>

              <div style={{ fontSize: '1.15rem', fontWeight: 600, color: 'var(--text-on-surface)', marginBottom: '4px' }}>
                {selectedApp.company} — {selectedApp.role}
              </div>

              <p style={{ fontSize: '0.85rem', color: 'var(--text-on-surface-muted)', lineHeight: 1.55, marginBottom: '14px' }}>
                {selectedApp.feedback}
              </p>

              <div>
                <div style={{ fontSize: '0.74rem', fontWeight: 600, color: 'var(--text-on-surface-muted)', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Key Detected Missing Signals:
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {selectedApp.missingKeywords.map((kw) => (
                    <span
                      key={kw}
                      style={{
                        padding: '3px 9px',
                        borderRadius: '6px',
                        background: 'rgba(217, 119, 6, 0.14)',
                        border: '1px solid rgba(217, 119, 6, 0.30)',
                        color: '#FBBF24',
                        fontSize: '0.72rem',
                        fontFamily: 'var(--font-mono)',
                      }}
                    >
                      +{kw}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Telegram Bot Remote Configurator */}
            <div
              style={{
                background: 'rgba(46, 58, 47, 0.25)',
                border: '1px solid rgba(161, 184, 135, 0.25)',
                borderRadius: '18px',
                padding: '20px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                <Sliders size={16} color="var(--accent-light)" />
                <span
                  style={{
                    fontSize: '0.82rem',
                    fontWeight: 700,
                    fontFamily: 'var(--font-mono)',
                    color: 'var(--text-on-surface)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em',
                  }}
                >
                  Remote Telegram Bot Settings
                </span>
              </div>

              {/* Setting 1: Evening Briefing Hour */}
              <div style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', color: 'var(--text-on-surface-muted)', marginBottom: '6px' }}>
                  <span>Evening Digest Window:</span>
                  <span style={{ color: 'var(--accent-light)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                    {telegramHour} Local
                  </span>
                </div>
                <input
                  type="range"
                  min="18"
                  max="21"
                  step="0.5"
                  value={parseFloat(telegramHour.split(':')[0]) + (telegramHour.endsWith(':30') ? 0.5 : 0)}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value);
                    const h = Math.floor(val);
                    const m = val % 1 === 0 ? '00' : '30';
                    setTelegramHour(`${h}:${m}`);
                  }}
                  style={{ width: '100%', accentColor: 'var(--accent)' }}
                />
              </div>

              {/* Setting 2: Minimum ATS Match Threshold */}
              <div style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', color: 'var(--text-on-surface-muted)', marginBottom: '6px' }}>
                  <span>Minimum Match Threshold:</span>
                  <span style={{ color: 'var(--accent-light)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                    {minMatchScore}% Cosine Match
                  </span>
                </div>
                <input
                  type="range"
                  min="70"
                  max="95"
                  step="5"
                  value={minMatchScore}
                  onChange={(e) => setMinMatchScore(parseInt(e.target.value))}
                  style={{ width: '100%', accentColor: 'var(--accent)' }}
                />
              </div>

              {/* Setting 3: Auto Draft Founder Outreach */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '8px', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
                <div>
                  <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-on-surface)' }}>
                    Founder Cold Outreach Assistant
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-on-surface-muted)' }}>
                    Draft personalized email in Telegram when startup is funded
                  </div>
                </div>

                <button
                  onClick={() => setAutoEmailFounders(!autoEmailFounders)}
                  style={{
                    width: '42px',
                    height: '24px',
                    borderRadius: '12px',
                    background: autoEmailFounders ? 'var(--accent)' : 'rgba(255, 255, 255, 0.15)',
                    border: 'none',
                    position: 'relative',
                    cursor: 'pointer',
                    transition: 'background 0.2s ease',
                  }}
                >
                  <div
                    style={{
                      width: '18px',
                      height: '18px',
                      borderRadius: '50%',
                      background: '#191C21',
                      position: 'absolute',
                      top: '3px',
                      left: autoEmailFounders ? '21px' : '3px',
                      transition: 'left 0.2s cubic-bezier(0.16, 1, 0.3, 1)',
                    }}
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

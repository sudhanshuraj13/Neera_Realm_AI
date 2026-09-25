import { useState, useEffect, type FC } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, ArrowRight, Menu, X, Sparkles } from 'lucide-react';

interface NavbarProps {
  onOpenTelegramModal: () => void;
  onOpenAuthModal: () => void;
  onScrollToSandbox: () => void;
}

export const Navbar: FC<NavbarProps> = ({
  onOpenTelegramModal,
  onOpenAuthModal,
  onScrollToSandbox,
}) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState<string>('');

  // Scroll detection for capsule elevation
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Active section tracking via IntersectionObserver
  useEffect(() => {
    const sections = ['ats-sandbox', 'hq-platform', 'features', 'pricing'];
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { rootMargin: '-25% 0px -55% 0px' }
    );

    sections.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  // Close mobile menu on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  const handleNavClick = (sectionId: string, customAction?: () => void) => {
    setMobileMenuOpen(false);
    if (customAction) {
      customAction();
      return;
    }
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <motion.header
      className={`navbar-wrapper ${isScrolled ? 'scrolled' : ''}`}
      initial={{ y: -24, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      <nav className="navbar-capsule" aria-label="Main Navigation">
        {/* ─── Left: Brand Identity & Live Engine Beacon ────────────────── */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            type="button"
            onClick={() => {
              window.scrollTo({ top: 0, behavior: 'smooth' });
              setMobileMenuOpen(false);
            }}
            className="navbar-brand-btn"
            aria-label="Neera AI - Back to top"
          >
            <div className="navbar-brand-glyph" aria-hidden="true">
              N
            </div>
            <span className="navbar-brand-text">Neera AI</span>
          </button>

          <div className="navbar-live-beacon" title="Semantic Decision Engine operational">
            <span className="navbar-pulse-dot" />
            <span>NextGen ATS · Live</span>
          </div>
        </div>

        {/* ─── Center: Editorial Nav Links (Desktop) ────────────────────── */}
        <div className="desktop-nav-links" role="menubar">
          <a
            href="#ats-sandbox"
            role="menuitem"
            className={`nav-link-pill ${activeSection === 'ats-sandbox' ? 'active' : ''}`}
            onClick={(e) => {
              e.preventDefault();
              handleNavClick('ats-sandbox', onScrollToSandbox);
            }}
          >
            <span>ATS Diagnostic</span>
            <span className="nav-link-tag">Free</span>
          </a>

          <a
            href="#hq-platform"
            role="menuitem"
            className={`nav-link-pill ${activeSection === 'hq-platform' ? 'active' : ''}`}
            onClick={(e) => {
              e.preventDefault();
              handleNavClick('hq-platform');
            }}
          >
            <span>HQ Cockpit</span>
          </a>

          <a
            href="#features"
            role="menuitem"
            className={`nav-link-pill ${activeSection === 'features' ? 'active' : ''}`}
            onClick={(e) => {
              e.preventDefault();
              handleNavClick('features');
            }}
          >
            <span>Venture Radar</span>
          </a>

          <a
            href="#pricing"
            role="menuitem"
            className={`nav-link-pill ${activeSection === 'pricing' ? 'active' : ''}`}
            onClick={(e) => {
              e.preventDefault();
              handleNavClick('pricing');
            }}
          >
            <span>Pricing &amp; Trial</span>
          </a>
        </div>

        {/* ─── Right: High-Intent Actions ───────────────────────────────── */}
        <div className="navbar-actions">
          {/* Telegram Companion Quick Link */}
          <button
            type="button"
            onClick={onOpenTelegramModal}
            className="navbar-btn-telegram"
            title="Pair with 24/7 Telegram Assistant"
            aria-label="Link Telegram Bot"
          >
            <Send size={13} color="var(--primary)" />
            <span>Bot Link</span>
          </button>

          {/* Primary Sign-In & 7-Day Pass Trigger */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="button"
            onClick={onOpenAuthModal}
            className="navbar-btn-primary"
            aria-label="Sign in to claim 7-Day All-Access Pass"
          >
            <span>Sign In</span>
            <span className="pass-text">· 7-Day Pass</span>
            <ArrowRight size={13} className="cta-arrow" />
          </motion.button>

          {/* Mobile Menu Toggle Button */}
          <button
            type="button"
            className="mobile-nav-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label={mobileMenuOpen ? 'Close menu' : 'Open navigation menu'}
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* ─── Mobile Dropdown Menu (AnimatePresence) ────────────────────── */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              className="mobile-nav-drawer"
              initial={{ opacity: 0, y: -12, scale: 0.97 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.97 }}
              transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '4px 12px 10px',
                  borderBottom: '1px solid rgba(200, 196, 188, 0.4)',
                }}
              >
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.72rem',
                    color: 'var(--text-muted)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em',
                  }}
                >
                  Navigation Index
                </span>
                <span className="navbar-live-beacon" style={{ display: 'inline-flex' }}>
                  <span className="navbar-pulse-dot" />
                  <span>v5.2 Online</span>
                </span>
              </div>

              <a
                href="#ats-sandbox"
                className={`mobile-nav-link ${activeSection === 'ats-sandbox' ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick('ats-sandbox', onScrollToSandbox);
                }}
              >
                <span>Free ATS Diagnostic Sandbox</span>
                <span className="nav-link-tag">100% Free</span>
              </a>

              <a
                href="#hq-platform"
                className={`mobile-nav-link ${activeSection === 'hq-platform' ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick('hq-platform');
                }}
              >
                <span>Web Headquarters Cockpit</span>
              </a>

              <a
                href="#features"
                className={`mobile-nav-link ${activeSection === 'features' ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick('features');
                }}
              >
                <span>Venture Capital Radar</span>
              </a>

              <a
                href="#pricing"
                className={`mobile-nav-link ${activeSection === 'pricing' ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick('pricing');
                }}
              >
                <span>Pricing &amp; 7-Day All-Access Pass</span>
              </a>

              <div className="mobile-nav-divider" />

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', paddingTop: '4px' }}>
                <button
                  type="button"
                  onClick={() => {
                    setMobileMenuOpen(false);
                    onOpenTelegramModal();
                  }}
                  className="navbar-btn-telegram"
                  style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
                >
                  <Send size={14} color="var(--primary)" />
                  <span style={{ display: 'inline' }}>Pair Telegram Bot Assistant</span>
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setMobileMenuOpen(false);
                    onOpenAuthModal();
                  }}
                  className="navbar-btn-primary"
                  style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
                >
                  <Sparkles size={14} />
                  <span>Start 7-Day All-Access Pass</span>
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </motion.header>
  );
};

export default Navbar;

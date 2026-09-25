import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { BentoHero } from './components/BentoHero';
import { InteractiveATSSection } from './components/InteractiveATSSection';
import { HeadquartersShowcase } from './components/HeadquartersShowcase';
import { PillarsShowcase } from './components/PillarsShowcase';
import { PricingSection } from './components/PricingSection';
import { TelegramModal } from './components/TelegramModal';
import { AuthModal } from './components/AuthModal';
import { Footer } from './components/Footer';
import { ErrorBoundary } from './components/ErrorBoundary';

export function App() {
  const [isTelegramModalOpen, setIsTelegramModalOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  const handleScrollToSandbox = () => {
    const el = document.getElementById('ats-sandbox');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div style={{ position: 'relative', minHeight: '100vh', background: 'var(--bg-canvas)' }}>
      {/* ─── Ambient Atmospheric Glow (Sage & Amber Orbs) ──────────────── */}
      <div className="atmos-container">
        <div className="atmos-orb-primary" />
        <div className="atmos-orb-secondary" />
      </div>

      {/* ─── Navigation Header ─────────────────────────────────────────── */}
      <Navbar
        onOpenTelegramModal={() => setIsTelegramModalOpen(true)}
        onOpenAuthModal={() => setIsAuthModalOpen(true)}
        onScrollToSandbox={handleScrollToSandbox}
      />

      {/* ─── Main Landing Page Content ─────────────────────────────────── */}
      <main>
        {/* Bento Grid Hero with Integrated 3D Machine Video (Matching Reference) */}
        <BentoHero
          onOpenTelegramModal={() => setIsTelegramModalOpen(true)}
          onOpenAuthModal={() => setIsAuthModalOpen(true)}
          onScrollToSandbox={handleScrollToSandbox}
        />

        {/* Tier 1: 100% Free Interactive ATS Sandbox (Live Resume vs JD Test) */}
        <ErrorBoundary fallbackTitle="Interactive ATS Diagnostic Sandbox">
          <InteractiveATSSection />
        </ErrorBoundary>

        {/* Tier 2 & Pro: Web Headquarters Cockpit (Power BI Analytics & Telegram Sync) */}
        <HeadquartersShowcase
          onOpenAuthModal={() => setIsAuthModalOpen(true)}
          onOpenTelegramModal={() => setIsTelegramModalOpen(true)}
        />

        {/* Pro Telegram Agent: The 3 Pillars (Evening Jobs, Venture Radar, Auto-Outreach) */}
        <PillarsShowcase
          onOpenTelegramModal={() => setIsTelegramModalOpen(true)}
        />

        {/* Value Architecture: Free vs 7-Day Sign-in Pass vs Pro (Monthly/Yearly) */}
        <PricingSection
          onOpenAuthModal={() => setIsAuthModalOpen(true)}
          onScrollToSandbox={handleScrollToSandbox}
        />
      </main>

      {/* ─── Footer ────────────────────────────────────────────────────── */}
      <Footer />

      {/* ─── Telegram Pairing Modal ────────────────────────────────────── */}
      <TelegramModal
        isOpen={isTelegramModalOpen}
        onClose={() => setIsTelegramModalOpen(false)}
      />

      {/* ─── 7-Day All-Access Trial & Auth Modal ───────────────────────── */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={() => {
          setIsAuthModalOpen(false);
          // Smooth scroll to the HQ cockpit as reward
          document.getElementById('hq-platform')?.scrollIntoView({ behavior: 'smooth' });
        }}
      />
    </div>
  );
}

export default App;

import { useState, useRef, type FC } from 'react';
import { motion } from 'framer-motion';
import { Volume2, VolumeX, Play, Pause, Maximize2 } from 'lucide-react';

interface CinematicVideoBannerProps {
  videoUrl?: string;
}

const DEFAULT_VIDEO_URL =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260518_003132_8b7edcb6-c64d-4a52-a9ca-879942e122ad.mp4';

export const CinematicVideoBanner: FC<CinematicVideoBannerProps> = ({
  videoUrl = DEFAULT_VIDEO_URL,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isMuted, setIsMuted] = useState(true);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isHovered, setIsHovered] = useState(false);

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
        setIsPlaying(false);
      } else {
        videoRef.current.play();
        setIsPlaying(true);
      }
    }
  };

  const toggleFullscreen = () => {
    if (videoRef.current) {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else {
        videoRef.current.requestFullscreen();
      }
    }
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.15 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      style={{
        width: '100%',
        maxWidth: '1280px',
        margin: '0 auto 60px auto',
        padding: '0 24px',
        position: 'relative',
        zIndex: 10,
      }}
    >
      {/* ── Outer Bezel / Canvas Frame ─────────────────────────────────── */}
      <div
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{
          position: 'relative',
          width: '100%',
          aspectRatio: '19 / 6',
          minHeight: '220px',
          borderRadius: 'var(--radius-card, 32px)',
          overflow: 'hidden',
          background: 'var(--surface, #191C21)',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          boxShadow:
            '0 24px 60px -16px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.15)',
        }}
      >
        {/* ── HTML5 Video Element with 19:6 Ratio ───────────────────────── */}
        <video
          ref={videoRef}
          src={videoUrl}
          autoPlay
          loop
          muted={isMuted}
          playsInline
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            display: 'block',
          }}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
        />

        {/* ── Ambient Gradient Vignette ─────────────────────────────────── */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            pointerEvents: 'none',
            background:
              'linear-gradient(180deg, rgba(0, 0, 0, 0.3) 0%, transparent 40%, rgba(0, 0, 0, 0.5) 100%)',
          }}
        />

        {/* ── Top-Left HUD Telemetry Badge ──────────────────────────────── */}
        <div
          style={{
            position: 'absolute',
            top: '18px',
            left: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            zIndex: 2,
          }}
        >
          <div
            className="nexus-pill nexus-pill-dark"
            style={{
              backdropFilter: 'blur(12px)',
              WebkitBackdropFilter: 'blur(12px)',
              background: 'rgba(25, 28, 33, 0.75)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#FAF7F2',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '9999px',
              fontFamily: 'var(--font-mono, JetBrains Mono)',
              fontSize: '0.72rem',
              fontWeight: 600,
              letterSpacing: '0.04em',
            }}
          >
            <span className="pulse-dot" />
            <span>NEERA CINEMATIC REEL · 19:6 ULTRA-WIDE</span>
          </div>
        </div>

        {/* ── Bottom Floating Controls ──────────────────────────────────── */}
        <motion.div
          animate={{ opacity: isHovered ? 1 : 0.75 }}
          transition={{ duration: 0.2 }}
          style={{
            position: 'absolute',
            bottom: '18px',
            right: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            zIndex: 2,
          }}
        >
          {/* Play/Pause Button */}
          <button
            onClick={togglePlay}
            aria-label={isPlaying ? 'Pause video' : 'Play video'}
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'rgba(25, 28, 33, 0.75)',
              backdropFilter: 'blur(12px)',
              WebkitBackdropFilter: 'blur(12px)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#FAF7F2',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(25, 28, 33, 0.95)';
              e.currentTarget.style.transform = 'scale(1.06)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(25, 28, 33, 0.75)';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            {isPlaying ? <Pause size={15} /> : <Play size={15} style={{ marginLeft: '2px' }} />}
          </button>

          {/* Sound Mute/Unmute Button */}
          <button
            onClick={toggleMute}
            aria-label={isMuted ? 'Unmute video' : 'Mute video'}
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'rgba(25, 28, 33, 0.75)',
              backdropFilter: 'blur(12px)',
              WebkitBackdropFilter: 'blur(12px)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#FAF7F2',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(25, 28, 33, 0.95)';
              e.currentTarget.style.transform = 'scale(1.06)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(25, 28, 33, 0.75)';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            {isMuted ? <VolumeX size={15} /> : <Volume2 size={15} />}
          </button>

          {/* Fullscreen Button */}
          <button
            onClick={toggleFullscreen}
            aria-label="Toggle Fullscreen"
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'rgba(25, 28, 33, 0.75)',
              backdropFilter: 'blur(12px)',
              WebkitBackdropFilter: 'blur(12px)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#FAF7F2',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(25, 28, 33, 0.95)';
              e.currentTarget.style.transform = 'scale(1.06)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(25, 28, 33, 0.75)';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            <Maximize2 size={15} />
          </button>
        </motion.div>
      </div>
    </motion.section>
  );
};

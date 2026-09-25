import type { FC, SVGProps } from 'react';

interface IconProps extends SVGProps<SVGSVGElement> {
  size?: number;
  color?: string;
  className?: string;
}

/**
 * Animated Pulse Scanner / Radar Reticle.
 * Authentic developer-grade scanning telemetry icon replacing generic 'Zap' and AI emojis.
 */
export const PulseScannerIcon: FC<IconProps> = ({
  size = 18,
  color = 'currentColor',
  className = '',
  ...props
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    className={className}
    {...props}
  >
    <circle
      cx="12"
      cy="12"
      r="9"
      stroke={color}
      strokeWidth="1.5"
      strokeDasharray="2 2"
      opacity="0.5"
    />
    <circle cx="12" cy="12" r="5" stroke={color} strokeWidth="1.5" opacity="0.8" />
    <circle cx="12" cy="12" r="2" fill={color} />
    {/* Dynamic scanning crosshair ticks */}
    <line x1="12" y1="1" x2="12" y2="4" stroke={color} strokeWidth="1.5" strokeLinecap="round" />
    <line x1="12" y1="20" x2="12" y2="23" stroke={color} strokeWidth="1.5" strokeLinecap="round" />
    <line x1="1" y1="12" x2="4" y2="12" stroke={color} strokeWidth="1.5" strokeLinecap="round" />
    <line x1="20" y1="12" x2="23" y2="12" stroke={color} strokeWidth="1.5" strokeLinecap="round" />
  </svg>
);

/**
 * Cosine Vector Waveform Icon.
 * Visual representation of 30ms vector cosine distance embeddings math.
 */
export const VectorWaveIcon: FC<IconProps> = ({
  size = 18,
  color = 'currentColor',
  className = '',
  ...props
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    className={className}
    {...props}
  >
    <path
      d="M2 12 C5 4, 8 20, 12 12 C16 4, 19 20, 22 12"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx="6" cy="9.3" r="1.5" fill={color} />
    <circle cx="12" cy="12" r="1.5" fill={color} />
    <circle cx="18" cy="14.7" r="1.5" fill={color} />
  </svg>
);

/**
 * Calibrated Quality Shield.
 * Used for Match Tier badges, replacing unicode '★' star glyphs.
 */
export const CalibratedShieldIcon: FC<IconProps> = ({
  size = 16,
  color = 'currentColor',
  className = '',
  ...props
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    className={className}
    {...props}
  >
    <path
      d="M12 2L4 5.5V11.5C4 16.5 7.5 21 12 22C16.5 21 20 16.5 20 11.5V5.5L12 2Z"
      stroke={color}
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M9 12L11 14L15 10"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

/**
 * Git Branch / Rewrite Transformation Node Icon.
 * Replaces unicode '↳' for Google-XYZ formula rewrites.
 */
export const BranchTransformIcon: FC<IconProps> = ({
  size = 15,
  color = 'currentColor',
  className = '',
  ...props
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    className={className}
    {...props}
  >
    <circle cx="6" cy="6" r="3" stroke={color} strokeWidth="1.75" />
    <circle cx="18" cy="18" r="3" stroke={color} strokeWidth="1.75" />
    <path
      d="M6 9V14C6 16.2 7.8 18 10 18H15"
      stroke={color}
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M13 15L16 18L13 21"
      stroke={color}
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

/**
 * Live Status Beacon Dot with Animated Pulse Wave.
 */
export const StatusBeacon: FC<{ color?: string; size?: number }> = ({
  color = '#4ade80',
  size = 8,
}) => (
  <span
    style={{
      position: 'relative',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: `${size + 6}px`,
      height: `${size + 6}px`,
    }}
  >
    <span
      style={{
        position: 'absolute',
        width: `${size + 4}px`,
        height: `${size + 4}px`,
        borderRadius: '50%',
        backgroundColor: color,
        opacity: 0.45,
        animation: 'beaconPing 2s cubic-bezier(0, 0, 0.2, 1) infinite',
      }}
    />
    <span
      style={{
        width: `${size}px`,
        height: `${size}px`,
        borderRadius: '50%',
        backgroundColor: color,
        display: 'inline-block',
      }}
    />
  </span>
);

/**
 * Professional LinkedIn Icon.
 */
export const LinkedinIcon: FC<IconProps> = ({
  size = 16,
  color = 'currentColor',
  className = '',
  ...props
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
    <rect x="2" y="9" width="4" height="12" />
    <circle cx="4" cy="4" r="2" />
  </svg>
);

/**
 * Target Requisition Crosshair Icon.
 */
export const TargetCrosshairIcon: FC<IconProps> = ({
  size = 16,
  color = 'currentColor',
  className = '',
  ...props
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    className={className}
    {...props}
  >
    <circle cx="12" cy="12" r="8" stroke={color} strokeWidth="1.75" />
    <circle cx="12" cy="12" r="3" stroke={color} strokeWidth="1.5" />
    <line x1="12" y1="2" x2="12" y2="5" stroke={color} strokeWidth="1.75" strokeLinecap="round" />
    <line x1="12" y1="19" x2="12" y2="22" stroke={color} strokeWidth="1.75" strokeLinecap="round" />
    <line x1="2" y1="12" x2="5" y2="12" stroke={color} strokeWidth="1.75" strokeLinecap="round" />
    <line x1="19" y1="12" x2="22" y2="12" stroke={color} strokeWidth="1.75" strokeLinecap="round" />
  </svg>
);

// Minimal inline icon set (stroke-based, currentColor). Keeps us free of an
// icon-library dependency while staying crisp at any size.

const base = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 2,
  strokeLinecap: "round",
  strokeLinejoin: "round",
};

export const ThermometerIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M14 14.76V5a2 2 0 0 0-4 0v9.76a4 4 0 1 0 4 0Z" />
    <path d="M12 11v5" />
  </svg>
);

export const RefreshIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M21 12a9 9 0 1 1-2.64-6.36" />
    <path d="M21 4v5h-5" />
  </svg>
);

export const WifiIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M5 12.55a11 11 0 0 1 14 0" />
    <path d="M8.5 16.1a6 6 0 0 1 7 0" />
    <path d="M2 8.82a16 16 0 0 1 20 0" />
    <line x1="12" y1="20" x2="12.01" y2="20" />
  </svg>
);

export const WifiOffIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M8.5 16.1a6 6 0 0 1 7 0" />
    <path d="M2 8.82a16 16 0 0 1 5.55-3.39" />
    <path d="M10.5 5.07A16 16 0 0 1 22 8.82" />
    <path d="M5 12.55a11 11 0 0 1 4.07-2.6" />
    <line x1="12" y1="20" x2="12.01" y2="20" />
    <line x1="2" y1="2" x2="22" y2="22" />
  </svg>
);

export const AlertIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
);

export const InboxIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M22 12h-6l-2 3h-4l-2-3H2" />
    <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11Z" />
  </svg>
);

export const MenuIcon = (p) => (
  <svg {...base} {...p}>
    <line x1="4" y1="7" x2="20" y2="7" />
    <line x1="4" y1="12" x2="20" y2="12" />
    <line x1="4" y1="17" x2="20" y2="17" />
  </svg>
);

export const ArrowUpRight = (p) => (
  <svg {...base} {...p}>
    <line x1="7" y1="17" x2="17" y2="7" />
    <polyline points="7 7 17 7 17 17" />
  </svg>
);

export const TrendUp = (p) => (
  <svg {...base} {...p}>
    <polyline points="3 17 9 11 13 15 21 7" />
    <polyline points="21 12 21 7 16 7" />
  </svg>
);

export const TrendDown = (p) => (
  <svg {...base} {...p}>
    <polyline points="3 7 9 13 13 9 21 17" />
    <polyline points="21 12 21 17 16 17" />
  </svg>
);

export const SparkIcon = (p) => (
  <svg {...base} {...p}>
    <path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1" />
  </svg>
);

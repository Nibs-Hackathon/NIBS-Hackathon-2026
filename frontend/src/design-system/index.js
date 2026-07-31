// Public surface for RigOS design system.
// Epic 1 catalog is canonical for new work. Legacy primitives kept as aliases.

export { createRigOSV2Theme } from './RigOSV2Theme';
export { rigosV2Tokens, semanticTone, statusColors, resolveTone } from './tokens';

// Legacy V2* components (prefixed — no name clashes)
export * from './components';

// Legacy primitives — aliases where names overlap the catalog
export {
  RigCard,
  RigProgress,
  TelemetryChart,
  RigDrawer,
  RigModal,
  Toast,
  NotificationItem,
  RigSearch,
  FloatingPanel,
  PageHeader,
  RigToolbar,
  CommandPalette,
  AIAgentCard,
  TimelineCard,
  MetricCard as LegacyMetricCard,
  StatusBadge as LegacyStatusBadge,
  EmptyState as LegacyEmptyState,
  SectionHeader as LegacySectionHeader,
} from './primitives';

// Epic 1 catalog (canonical)
export * from './catalog';

// Epic 2 layouts + ApplicationShell
export * from './layouts';

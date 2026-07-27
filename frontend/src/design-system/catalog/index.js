/**
 * Epic 1 catalog public surface.
 * Prefer these names over legacy primitives / V2* components for new work.
 */

export {
  StatusBadge, RiskBadge, ProvenanceBadge, ConfidenceMeter, normalizeStatus,
} from './status';

export {
  MetricCard, SignalCard, HealthRing, Sparkline, ForecastChart, ThresholdLegend, EmptyState,
} from './data';

export {
  WorkspaceHeader, OperationsStrip, CommandBar, ScopeSwitcher, SyncIndicator,
  AuditSpine, Dock, Toolbar, UnitRiskMap, DecisionQueue,
} from './shell';

export {
  ObjectRow, IncidentQueueItem, WorkOrderCard, AssetTreeNode, TwinNode, ReportIndexItem,
} from './objects';

export {
  Timeline, IncidentTimeline, EventMarker, AuditEvent,
} from './time';

export {
  AgentPipeline, AgentStageCard, TracePanel, EvidencePanel, EvidenceGraph, RecommendationPanel,
} from './investigation';

export {
  ProcessSchematic, TagOverlay, GaugeCluster, SignalPanel,
} from './twin';

export {
  ObjectInspector, CaseDossier, DecisionRail, DecisionBar, DecisionSurface,
  WorkspacePanel, SectionHeader, SplitPaneHandle,
} from './panels';

export { NotificationInbox } from './panels-notifications';

export {
  PrimaryCTA, DecisionButtonGroup, RationaleField, ScenarioSlider, FilterChipBar,
} from './actions';

export {
  BriefDocument, ApprovalStamp, EvidenceAppendixLink,
} from './executive';

/**
 * Isolated design-system preview — Epic 1 exit criterion.
 * Not a product page. Route: /__catalog
 */
import { useState } from 'react';
import { Box, CssBaseline, Divider, Stack, ThemeProvider, Typography } from '@mui/material';
import { useColorMode } from '../context/ColorModeContext';
import { createRigOSV2Theme } from './RigOSV2Theme';
import './catalog.css';
import './motion.css';
import {
  AgentPipeline, ApprovalStamp, AssetTreeNode, AuditSpine, BriefDocument, CaseDossier,
  CommandBar, ConfidenceMeter, DecisionBar, DecisionQueue, Dock, EmptyState,
  EvidenceAppendixLink, EvidenceGraph, EvidencePanel, FilterChipBar, ForecastChart,
  GaugeCluster, HealthRing, IncidentQueueItem, MetricCard, ObjectInspector, ObjectRow,
  OperationsStrip, PrimaryCTA, ProcessSchematic, ProvenanceBadge, RecommendationPanel,
  ReportIndexItem, RiskBadge, ScenarioSlider, ScopeSwitcher, SectionHeader, SignalCard,
  SignalPanel, Sparkline, StatusBadge, SyncIndicator, Timeline, Toolbar, TracePanel,
  UnitRiskMap, WorkOrderCard, WorkspaceHeader, WorkspacePanel,
} from './catalog';

function Section({ title, children }) {
  return (
    <Box sx={{ mb: 4 }}>
      <Typography className="rig-label" sx={{ mb: 1.5 }}>{title}</Typography>
      {children}
    </Box>
  );
}

function CatalogBody() {
  const { mode, toggle } = useColorMode();
  const [commandOpen, setCommandOpen] = useState(false);
  const [panelOpen, setPanelOpen] = useState(false);
  const [rationale, setRationale] = useState('');
  const [scenario, setScenario] = useState(2);
  const [selectedStage, setSelectedStage] = useState('sensor');

  const stages = [
    { id: 'sensor', name: 'Sensor', state: 'complete', duration: 1.2, confidence: 92, reasoning: 'Vibration spike correlated with tag PI-101.' },
    { id: 'diagnostic', name: 'Diagnostic', state: 'running', duration: 0.8, confidence: 74, reasoning: 'Evaluating bearing wear hypothesis.' },
    { id: 'maintenance', name: 'Maintenance', state: 'queued', confidence: 0 },
  ];

  return (
    <ThemeProvider theme={createRigOSV2Theme(mode)}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', color: 'text.primary', p: 3, maxWidth: 1200, mx: 'auto' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
          <Box>
            <Typography className="rig-label">RigOS design system</Typography>
            <Typography component="h1" sx={{ fontSize: '1.75rem', fontWeight: 600 }}>Component catalog</Typography>
            <Typography variant="body2" color="text.secondary">Epic 1 isolated preview · not a product workspace</Typography>
          </Box>
          <PrimaryCTA onClick={toggle}>{mode === 'dark' ? 'Light mode' : 'Dark mode'}</PrimaryCTA>
        </Stack>

        <Section title="Shell">
          <WorkspaceHeader
            title="Command Center"
            breadcrumbs={[
              { label: 'Alpha Refinery' },
              { label: 'Command Center' },
            ]}
            scope="Alpha Refinery"
            facilities={['Alpha Refinery', 'Enterprise view']}
            connected
            syncAge={2}
            actions={<PrimaryCTA onClick={() => setCommandOpen(true)}>Open CommandBar</PrimaryCTA>}
          />
          <OperationsStrip
            metrics={[
              { label: 'Fleet health', value: '86%', detail: 'Within envelope' },
              { label: 'Open incidents', value: '2', detail: '1 critical' },
              { label: 'Assets online', value: '48' },
              { label: 'Agents active', value: '1' },
            ]}
            cta={<PrimaryCTA>Review investigation</PrimaryCTA>}
            sx={{ mt: 2 }}
          />
          <Toolbar sx={{ mt: 2 }}>
            <ScopeSwitcher value="Alpha Refinery" options={['Alpha Refinery', 'Enterprise view']} />
            <SyncIndicator connected syncAge={3} />
            <FilterChipBar chips={[{ label: 'Critical', onRemove: () => {} }]} onClear={() => {}} />
          </Toolbar>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 2 }}>
            <UnitRiskMap
              units={[
                { id: 'u1', name: 'Crude unit', health: 88 },
                { id: 'u2', name: 'Hydrotreater', health: 62, status: 'attention' },
                { id: 'u3', name: 'Utilities', health: 91 },
                { id: 'u4', name: 'Tank farm', health: 44, status: 'critical' },
              ]}
              sx={{ flex: 1 }}
            />
            <DecisionQueue
              items={[
                { id: 'i1', kind: 'incident', title: 'Pump vibration high', severity: 'critical', assetName: 'P-101', age: '12m' },
                { id: 'i2', title: 'Schedule seal inspection', status: 'Ready' },
              ]}
              sx={{ flex: 1, border: '1px solid', borderColor: 'divider', borderRadius: 1, p: 1 }}
            />
          </Stack>
          <AuditSpine
            events={[
              { who: 'A. Rao', what: 'Accepted recommendation', when: '14:02', objectLabel: 'INC-2847' },
              { who: 'System', what: 'Investigation started', when: '13:51', objectLabel: 'P-101' },
            ]}
            sx={{ mt: 2 }}
          />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Data display">
          <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
            <MetricCard label="Fleet health" value="86%" delta="+1.2" provenance="live" tone="nominal" sx={{ width: 200 }} />
            <SignalCard name="PI-101" value={4.2} unit="mm/s" threshold={5} provenance="live" sx={{ width: 200 }} />
            <HealthRing value={72} />
            <Box sx={{ width: 160 }}>
              <Sparkline values={[70, 72, 68, 74, 71, 69, 66]} label="Health trend" />
              <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                <StatusBadge status="critical" label="Critical" live />
                <RiskBadge value={78} />
                <ProvenanceBadge value="estimated" />
              </Stack>
            </Box>
          </Stack>
          <ForecastChart
            series={[90, 88, 85, 82, 78, 74, 70]}
            band={{ high: [92, 90, 88, 86, 84, 82, 80], low: [88, 85, 82, 78, 72, 68, 62] }}
            threshold={65}
            provenance="estimated"
            sx={{ mt: 2, maxWidth: 480 }}
          />
          <ConfidenceMeter value={81} sx={{ mt: 2, maxWidth: 320 }} />
          <EmptyState title="No assets match" description="Adjust scope or wait for telemetry sync." sx={{ mt: 2 }} />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Objects & lists">
          <ObjectRow name="P-101 Crude Pump" secondaryId="AST-1021" status="attention" selected />
          <IncidentQueueItem id="INC-2847" title="Bearing vibration anomaly" severity="critical" assetName="P-101" age="8m" />
          <WorkOrderCard title="Replace bearing assembly" priority="P1" asset="P-101" cost={18500} window="6h" sx={{ mt: 1, maxWidth: 280 }} />
          <AssetTreeNode name="Crude unit" health={88} expanded>
            <AssetTreeNode name="P-101" health={62} depth={1} selected />
          </AssetTreeNode>
          <ReportIndexItem title="Alpha weekly brief" date="2026-07-26" approvalState="Awaiting" />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Twin">
          <ProcessSchematic
            nodes={[
              { id: 'n1', label: 'Feed', x: 40, y: 70 },
              { id: 'n2', label: 'P-101', x: 190, y: 70, risk: true },
              { id: 'n3', label: 'HX-2', x: 340, y: 70 },
            ]}
            selectedId="n2"
            overlays={[{ label: 'Vibration', value: '4.2', unit: 'mm/s', x: 200, y: 20 }]}
          />
          <GaugeCluster gauges={[{ label: 'Vib', value: 72 }, { label: 'Temp', value: 54 }, { label: 'Flow', value: 88 }]} sx={{ mt: 2 }} />
          <SignalPanel
            signals={[
              { name: 'Vibration', value: 4.2, unit: 'mm/s', values: [3, 3.2, 3.8, 4.2] },
              { name: 'Temp', value: 82, unit: '°C', values: [78, 79, 81, 82] },
            ]}
            sx={{ mt: 2 }}
          />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Investigation">
          <AgentPipeline stages={stages} selectedId={selectedStage} onSelect={(s) => setSelectedStage(s.id)} />
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 2 }}>
            <TracePanel stages={stages} selectedId={selectedStage} onSelect={(s) => setSelectedStage(s.id)} sx={{ flex: 1 }} />
            <EvidencePanel items={[{ title: 'Telemetry spike', source: 'PI-101', detail: '4.2 mm/s at 13:48' }]} sx={{ flex: 1 }} />
          </Stack>
          <EvidenceGraph nodes={[{ type: 'sensor', label: 'PI-101' }, { type: 'event', label: 'Spike' }, { type: 'asset', label: 'P-101' }]} sx={{ mt: 2 }} />
          <RecommendationPanel recommendation="Reduce load 8% and schedule bearing inspection within 48h." confidence={81} sx={{ mt: 2 }} />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Time & panels">
          <Timeline
            variant="incident"
            items={[
              { title: 'Detection', time: '13:48', detail: 'Vibration exceeded advisory band', status: 'attention' },
              { title: 'AI recommendation', time: '13:55', detail: 'Reduce load and inspect', decision: 'pending', status: 'ai-active' },
            ]}
          />
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 2 }}>
            <ObjectInspector
              title="P-101 Crude Pump"
              subtitle="Identity"
              sections={[
                { title: 'State', content: <Stack direction="row" spacing={1}><StatusBadge status="attention" label="Attention" /><RiskBadge value={62} /></Stack> },
                { title: 'Signals', content: <Sparkline values={[70, 68, 65, 62]} /> },
              ]}
              sx={{ flex: 1 }}
            />
            <CaseDossier
              evidence={[{ title: 'Audit trail', source: 'MAO' }]}
              recommendation="Approve temporary derate"
              confidence={78}
              sx={{ flex: 1 }}
            />
          </Stack>
          <DecisionBar
            recommendation="Approve temporary derate"
            rationale={rationale}
            onRationaleChange={setRationale}
            onAccept={() => {}}
            onModify={() => {}}
            onReject={() => {}}
            sx={{ mt: 2 }}
          />
          <ScenarioSlider value={scenario} onChange={setScenario} sx={{ mt: 2, maxWidth: 360 }} />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Executive">
          <BriefDocument
            title="Alpha refinery operating brief"
            summary="One critical asset requires operator decision within this shift."
            metrics={[{ label: 'Confidence', value: '81%' }, { label: 'Exposure', value: 'P1' }]}
            sections={[{ title: 'Ask', body: 'Approve temporary derate and maintenance window.' }]}
          />
          <ApprovalStamp signatory="Plant Manager" timestamp="2026-07-26 14:00" status="Awaiting approval" sx={{ mt: 2, maxWidth: 320 }} />
          <EvidenceAppendixLink sx={{ mt: 1 }} />
          <SectionHeader eyebrow="Section" title="Panel title" description="Supporting copy for section headers." sx={{ mt: 2 }} />
        </Section>

        <CommandBar
          open={commandOpen}
          onClose={() => setCommandOpen(false)}
          commands={[
            { label: 'Go to Assets', description: 'Digital twin workspace', onSelect: () => setCommandOpen(false) },
            { label: 'Toggle theme', onSelect: toggle },
          ]}
        />
        <WorkspacePanel
          open={panelOpen}
          onClose={() => setPanelOpen(false)}
          notifications={[{ id: 1, title: 'Critical vibration', message: 'P-101 exceeded band', severity: 'critical', unread: true, time: '13:48' }]}
          auditContent={<Typography variant="body2">Read-only audit slice for preview.</Typography>}
        />
        <Dock
          onCommand={() => setCommandOpen(true)}
          onCopilot={() => {}}
          onWorkspacePanel={() => setPanelOpen(true)}
          onPin={() => {}}
        />
      </Box>
    </ThemeProvider>
  );
}

export function CatalogPreview() {
  return <CatalogBody />;
}

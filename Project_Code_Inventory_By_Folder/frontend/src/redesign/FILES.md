# Folder: frontend/src/redesign Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/redesign`

Contains 28 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/redesign/accountability.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/accountability.css`

```css
/* Epic 5 — AI accountability chrome */

.e5-audit-spine {
  position: sticky;
  bottom: 0;
  z-index: 12;
  min-height: 36px;
  padding: 6px 16px;
  border-top: 1px solid rgba(148, 163, 184, 0.16);
  background: rgba(9, 11, 15, 0.94);
  backdrop-filter: blur(10px);
}

.e5-audit-spine:focus {
  outline: 2px solid #4f8cff;
  outline-offset: -2px;
}

.e5-decision-bar {
  position: sticky;
  bottom: 36px;
  z-index: 11;
  margin-top: 16px;
  border-radius: 12px 12px 0 0;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: #111722 !important;
}

.e5-evidence-lineage {
  margin-top: 12px;
  padding: 12px;
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 10px;
  background: rgba(15, 20, 28, 0.55);
}

.e5-lineage-chip {
  background: rgba(79, 140, 255, 0.12) !important;
  border: 1px solid rgba(79, 140, 255, 0.28) !important;
}

.e5-decision-history {
  margin-top: 12px;
}

.e5-decision-row {
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.12);
  background: rgba(17, 20, 24, 0.7);
}

.e5-metric .rig-provenance {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.58rem;
  font-weight: 800;
}

.e5-trace-wrap {
  margin-top: 8px;
}

.os-stage {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.os-stage > main {
  flex: 1;
  padding-bottom: 48px;
}

.workspace-dock {
  bottom: 48px !important;
}

.e6-skip-link {
  position: absolute;
  left: -9999px;
  top: 8px;
  z-index: 100;
  padding: 8px 14px;
  border-radius: 8px;
  background: #4f8cff;
  color: #fff;
  font-weight: 700;
  text-decoration: none;
}

.e6-skip-link:focus {
  left: 12px;
}

.e6-workspace-fallback {
  color: #94a3b8;
}

html[data-rigos-theme='light'] .e5-audit-spine,
html[data-rigos-theme='light'] .e5-decision-bar {
  background: rgba(255, 255, 255, 0.96) !important;
  border-color: rgba(15, 23, 42, 0.12);
}

html[data-rigos-theme='light'] .e5-evidence-lineage,
html[data-rigos-theme='light'] .e5-decision-row {
  background: #f8fafc;
  border-color: rgba(15, 23, 42, 0.1);
}
```

## frontend/src/redesign/accountability.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/accountability.jsx`

```javascript
/**
 * Epic 5 — AI accountability surface for ProductShell / ProductPage.
 * Reuses design-system catalog; enforces rationale ≥ 20 on operator decisions.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Box, Button, Chip, Stack, Typography } from '@mui/material';
import toast from 'react-hot-toast';
import { DecisionBar } from '../design-system/catalog/panels';
import { TracePanel } from '../design-system/catalog/investigation';
import { AuditSpine } from '../design-system/catalog/shell';
import { ProvenanceBadge } from '../design-system/catalog/status';
import { ApprovalStamp } from '../design-system/catalog/executive';
import { recordOperatorAction } from '../api/client';
import './accountability.css';

export const RATIONALE_MIN = 20;

export { ProvenanceBadge, ApprovalStamp, TracePanel, AuditSpine };

/** Infer Live / Estimated / Stale from connection + age. */
export function inferProvenance({ connected = false, syncAge = 0, explicit } = {}) {
  if (explicit) return explicit;
  if (!connected) return 'stale';
  if (syncAge > 30) return 'stale';
  if (syncAge > 12) return 'estimated';
  return 'live';
}

export function normalizeTraceStages(stages = [], investigation = {}) {
  return (Array.isArray(stages) ? stages : []).map((stage, index) => {
    const name = stage.agent || stage.name || `Stage ${index + 1}`;
    const confidence = stage.confidence != null
      ? (Number(stage.confidence) <= 1 ? Number(stage.confidence) * 100 : Number(stage.confidence))
      : null;
    return {
      id: stage.id || `${name}-${index}`,
      name,
      agent: name,
      state: stage.state || 'queued',
      reasoning: stage.reasoning || stage.finding || stage.summary || null,
      inputs: stage.inputs || stage.evidence || (stage.input ? JSON.stringify(stage.input) : `telemetry + case context · step ${index + 1}`),
      outputs: stage.outputs || stage.output || stage.recommendation || (confidence != null ? `${Math.round(confidence)}% confidence finding` : null),
      modelId: stage.model_id || stage.modelId || investigation.model_id || 'gemini-flash · MAO',
      duration: stage.duration_seconds != null ? `${stage.duration_seconds}s` : stage.duration || null,
      confidence,
    };
  });
}

/** Palantir-style linked evidence facts for a case / investigation. */
export function EvidenceLineage({ facts = [], className = '' }) {
  return (
    <Box className={`e5-evidence-lineage ${className}`} role="list" aria-label="Evidence lineage">
      <Typography className="product-kicker">EVIDENCE LINEAGE</Typography>
      <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mt: 1 }}>
        {facts.length
          ? facts.map((fact, index) => (
            <Chip
              key={fact.id || index}
              role="listitem"
              size="small"
              className="e5-lineage-chip"
              label={`${fact.type || 'fact'}: ${fact.label || fact.detail || 'linked'}`}
              title={fact.detail || fact.source || ''}
            />
          ))
          : <Typography variant="caption" color="text.secondary">No linked facts yet — agents are assembling the packet.</Typography>}
      </Stack>
    </Box>
  );
}

export function buildEvidenceFacts({ incident, stages = [], investigation } = {}) {
  const facts = [];
  if (incident?.id) facts.push({ id: 'case', type: 'case', label: String(incident.id).slice(0, 10), detail: incident.incident_type });
  if (incident?.asset_id || incident?.asset_name) {
    facts.push({ id: 'asset', type: 'asset', label: incident.asset_name || incident.asset_id, detail: 'affected equipment' });
  }
  if (incident?.evidence) facts.push({ id: 'sensor', type: 'sensor', label: 'snapshot', detail: String(incident.evidence).slice(0, 80) });
  (stages || []).slice(0, 4).forEach((stage, index) => {
    facts.push({
      id: `stage-${index}`,
      type: 'agent',
      label: stage.agent || stage.name || `agent ${index + 1}`,
      detail: stage.state || 'queued',
    });
  });
  if (investigation?.confidence != null) {
    const conf = Number(investigation.confidence) <= 1 ? Number(investigation.confidence) * 100 : Number(investigation.confidence);
    facts.push({ id: 'conf', type: 'model', label: `${Math.round(conf)}% confidence`, detail: 'investigation aggregate' });
  }
  return facts;
}

export function mapAuditEvents({ sessionDecisions = [], auditLogs = [], operatorActions = [] } = {}) {
  const fromSession = (sessionDecisions || []).map((entry, index) => ({
    id: entry.id || `session-${index}`,
    who: entry.operator || entry.who || 'Control operator',
    what: entry.decision || entry.what || 'Decision recorded',
    when: entry.at ? new Date(entry.at).toLocaleTimeString() : entry.when,
    objectLabel: entry.objectLabel || entry.incidentId || entry.action_type,
  }));
  const fromActions = (operatorActions || []).map((action, index) => ({
    id: action.id || `action-${index}`,
    who: action.approved_by || action.operator || 'Operator',
    what: action.title || action.action_type || action.status || 'Operator action',
    when: action.timestamp ? new Date(action.timestamp).toLocaleTimeString() : null,
    objectLabel: action.incident_id || action.asset_id,
  }));
  const fromLogs = (auditLogs || []).slice(0, 5).map((item, index) => ({
    id: item.id || `log-${index}`,
    who: item.operator || 'System',
    what: item.incident_type || item.action_type || 'Operational event',
    when: item.timestamp || item.created_at
      ? new Date(item.timestamp || item.created_at).toLocaleTimeString()
      : null,
    objectLabel: item.asset_name || item.asset_id,
  }));
  return [...fromSession, ...fromActions, ...fromLogs].slice(0, 8);
}

export function exportAuditLog({ events = [], facility = 'Facility', filename } = {}) {
  const rows = [
    ['when', 'who', 'what', 'object', 'facility'],
    ...events.map((event) => [
      event.when || event.at || '',
      event.who || '',
      event.what || '',
      event.objectLabel || '',
      facility,
    ]),
  ];
  const csv = rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename || `rigos-audit-${new Date().toISOString().slice(0, 10)}.csv`;
  anchor.click();
  URL.revokeObjectURL(url);
  toast.success('Audit log exported');
}

/**
 * Sticky DecisionBar with mandatory rationale + API persistence + session audit push.
 * Part 8: Ctrl/⌘ Enter accepts; focusDecisionBar focuses rationale field.
 */
export function OperatorDecisionBar({
  incident,
  recommendation,
  objectApi,
  onRecorded,
  className = '',
}) {
  const [rationale, setRationale] = useState('');
  const [busy, setBusy] = useState(false);
  const rationaleRef = useRef(null);
  const rec = recommendation
    || incident?.ai_recommendation
    || 'Review the evidence package and authorize the recommended response.';

  useEffect(() => {
    if (!objectApi?.ui?.focusDecisionBar) return undefined;
    const timer = requestAnimationFrame(() => {
      rationaleRef.current?.focus?.();
      objectApi.setFocusDecisionBar?.(false);
    });
    return () => cancelAnimationFrame(timer);
  }, [objectApi?.ui?.focusDecisionBar, objectApi, incident?.id]);

  const submit = useCallback(async (decision) => {
    const note = String(rationale || '').trim();
    if (note.length < RATIONALE_MIN) {
      toast.error(`Rationale must be at least ${RATIONALE_MIN} characters`);
      return;
    }
    setBusy(true);
    try {
      const response = await recordOperatorAction({
        incident_id: incident?.id || null,
        asset_id: incident?.asset_id || null,
        action_type: String(rec).slice(0, 80) || 'operator_decision',
        decision,
        risk_level: incident?.severity || 'MEDIUM',
        note,
        operator: 'Control operator',
      });
      const entry = {
        id: response?.data?.id || `local-${Date.now()}`,
        decision,
        what: `${decision.replace(/_/g, ' ')} — ${note.slice(0, 48)}`,
        operator: 'Control operator',
        who: 'Control operator',
        at: new Date().toISOString(),
        incidentId: incident?.id,
        objectLabel: incident?.asset_name || incident?.id,
        rationale: note,
      };
      objectApi?.pushAuditDecision?.(entry);
      setRationale('');
      toast.success(`Decision recorded: ${decision.replace(/_/g, ' ')}`);
      onRecorded?.(entry, response?.data);
    } catch (error) {
      const detail = error.response?.data?.detail;
      const message = typeof detail === 'string'
        ? detail
        : detail?.message || (Array.isArray(detail) ? detail.map((d) => d.msg).join('; ') : null);
      toast.error(message || 'Decision could not be persisted.');
    } finally {
      setBusy(false);
    }
  }, [rationale, incident, rec, objectApi, onRecorded]);

  if (!incident) return null;

  return (
    <DecisionBar
      className={`e5-decision-bar ${className}`}
      recommendation={rec}
      rationale={rationale}
      onRationaleChange={setRationale}
      minRationale={RATIONALE_MIN}
      busy={busy}
      rationaleInputRef={rationaleRef}
      onAccept={() => submit('approved')}
      onModify={() => submit('escalated')}
      onReject={() => submit('rejected')}
    />
  );
}

/** Compact decision history for inspectors / dossiers. */
export function DecisionHistory({ entries = [], className = '' }) {
  return (
    <Box className={`e5-decision-history ${className}`}>
      <Typography className="product-kicker">DECISION HISTORY</Typography>
      <Stack spacing={0.75} sx={{ mt: 1 }}>
        {entries.length
          ? entries.map((entry, index) => (
            <Box key={entry.id || index} className="e5-decision-row">
              <Typography fontWeight={700}>{entry.decision || entry.what}</Typography>
              <Typography variant="caption" color="text.secondary">
                {entry.who || entry.operator || 'Operator'}
                {entry.at || entry.when ? ` · ${entry.at ? new Date(entry.at).toLocaleString() : entry.when}` : ''}
              </Typography>
              {entry.rationale && <Typography variant="body2">{entry.rationale}</Typography>}
            </Box>
          ))
          : <Typography variant="caption" color="text.secondary">No operator decisions recorded for this case yet.</Typography>}
      </Stack>
    </Box>
  );
}

export function MetricWithProvenance({ label, value, provenance = 'estimated', className = '' }) {
  return (
    <Box className={`metric e5-metric ${className}`}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
        <Typography>{label}</Typography>
        <ProvenanceBadge value={provenance} />
      </Stack>
      <Typography>{String(value)}</Typography>
    </Box>
  );
}

export function useOperatorAudit(objectApi, operations = {}) {
  return useMemo(() => {
    const session = objectApi?.audit?.recentDecisions || [];
    const actions = [];
    (operations.audit_logs || []).forEach((log) => {
      (log.operator_actions || []).forEach((action) => actions.push({ ...action, incident_id: log.id }));
    });
    if (Array.isArray(operations.operator_actions)) actions.push(...operations.operator_actions);
    return mapAuditEvents({
      sessionDecisions: session,
      auditLogs: operations.audit_logs || [],
      operatorActions: actions,
    });
  }, [objectApi?.audit?.recentDecisions, operations.audit_logs, operations.operator_actions]);
}

export function ExportAuditButton({ events, facility, variant = 'outlined', size = 'small' }) {
  return (
    <Button
      size={size}
      variant={variant}
      onClick={() => exportAuditLog({ events, facility })}
    >
      Export audit log
    </Button>
  );
}
```

## frontend/src/redesign/ai-investigation.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/ai-investigation.css`

```css
.ai-flagship{display:grid;gap:14px}.ai-flagship-head{display:flex;justify-content:space-between;align-items:end;gap:20px;padding:3px 2px}.ai-flagship-title{margin:5px 0 5px!important;font-size:1.55rem!important;font-weight:850!important;letter-spacing:-.055em}.ai-flagship-head>div:first-child>p:last-child{color:#92a4bb;font-size:.75rem}.ai-flagship-live{display:grid;gap:4px;padding:9px 11px;border:1px solid rgba(98,161,255,.25);border-radius:9px;background:rgba(79,140,255,.07);color:#a9caff;font:.65rem 'DM Mono',monospace}.ai-flagship-live i{width:6px;height:6px;border-radius:50%;background:#4bd09e;box-shadow:0 0 0 4px rgba(75,208,158,.1);animation:ai-live 1.5s ease infinite}.ai-flagship-live small{color:#7f99bb;font-size:.56rem}.ai-flagship-grid{display:grid;grid-template-columns:280px minmax(360px,1fr) 290px;gap:12px;min-height:555px}.ai-pipeline,.ai-reasoning,.ai-evidence,.ai-bottom{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:14px!important;box-shadow:none!important}.ai-pipeline,.ai-reasoning,.ai-evidence{padding:14px!important;overflow:auto}.ai-panel-head{display:flex;align-items:start;justify-content:space-between;gap:8px}.ai-panel-head>div>p:last-child{margin-top:4px;color:#c5d1df;font-size:.74rem}.ai-panel-head .MuiButton-root{color:#9ec4fb;font-size:.6rem!important;text-transform:none}.ai-panel-head .MuiChip-root{height:22px;color:#8fd6ba;font-size:.58rem}.ai-pipeline-list{display:grid;gap:5px;margin-top:14px}.ai-stage{position:relative;display:grid;grid-template-columns:26px 1fr auto;gap:8px;width:100%;padding:9px;border:1px solid transparent;border-radius:9px;background:#0c1016;color:#dbe6f5;cursor:pointer;text-align:left}.ai-stage:hover,.ai-stage.expanded{border-color:rgba(99,162,255,.34);background:#111b28}.ai-stage-index{display:grid;place-items:center;width:23px;height:23px;border:1px solid rgba(99,162,255,.35);border-radius:50%;color:#9cc4ff;font:700 .58rem 'DM Mono',monospace}.ai-stage>div:nth-child(2)>p:first-child{font-size:.7rem;font-weight:800}.ai-stage>div:nth-child(2)>p:nth-child(2){margin-top:2px;color:#8092a9;font-size:.56rem}.ai-stage>div:nth-child(2)>i{display:block;width:100%;height:3px;margin-top:7px;border-radius:99px;background:rgba(148,163,184,.14);overflow:hidden}.ai-stage>div:nth-child(2)>i span{display:block;height:100%;border-radius:99px;background:#5f9eff;transition:width .6s ease}.ai-stage.running>div:nth-child(2)>i span,.ai-stage.streaming>div:nth-child(2)>i span{background:#48cc9b;animation:ai-progress 1.8s ease infinite}.ai-stage-state{display:grid;align-content:center;text-align:right}.ai-stage-state b{color:#b9d5ff;font:.62rem 'DM Mono',monospace}.ai-stage-state small{margin-top:2px;color:#8193ab;font-size:.52rem}.ai-stage>em{position:absolute;left:20px;top:100%;height:6px;border-left:1px dashed rgba(110,162,237,.55)}.ai-stage-expanded{grid-column:2/-1;margin-top:3px;padding:7px;border-top:1px solid rgba(148,163,184,.1);color:#b8c7d9;font-size:.61rem;line-height:1.45}.ai-stage-expanded>div{display:flex;gap:8px;margin-top:7px}.ai-stage-expanded span{color:#8da5c2;font:600 .53rem 'DM Mono',monospace}.reasoning-tree{display:grid;gap:9px;margin-top:16px}.reasoning-root{padding:10px;border:1px solid rgba(239,159,91,.35);border-radius:9px;background:rgba(239,159,91,.07)}.reasoning-root b{font-size:.68rem}.reasoning-root p{margin-top:4px;color:#c8ae95;font-size:.62rem}.reasoning-branches{display:grid;gap:6px;margin-left:17px;padding-left:13px;border-left:1px dashed rgba(104,159,238,.45)}.reasoning-branches>div{display:flex;gap:8px;padding:7px;border-radius:8px;background:#0c1016}.reasoning-branches>div>span{color:#86b5f7;font:700 .58rem 'DM Mono',monospace}.reasoning-branches p{display:grid;gap:2px;color:#cbd7e5;font-size:.62rem}.reasoning-branches small{color:#7e91aa;font-size:.54rem}.evidence-graph{margin-top:15px;padding:10px;border:1px solid rgba(148,163,184,.1);border-radius:10px;background:#0c1016}.evidence-graph svg{width:100%;margin:5px 0}.evidence-graph path{fill:none;stroke:rgba(103,160,246,.5);stroke-width:2}.evidence-graph circle{fill:#142033;stroke:#75adff;stroke-width:2}.evidence-graph circle:last-child{stroke:#f0a15f}.evidence-graph>div{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}.evidence-graph span,.evidence-graph strong{color:#8397b0;font-size:.51rem;text-align:center}.evidence-graph strong{color:#edba88}.ai-telemetry{margin-top:14px;padding:10px;border:1px solid rgba(148,163,184,.1);border-radius:9px;background:#0c1016}.ai-telemetry .mini-graph{margin:8px 0 0}.ai-documents,.ai-artifacts{display:grid;gap:5px;margin-top:14px}.ai-documents>p:not(:first-child){display:flex;align-items:center;gap:7px;padding:7px 0;border-bottom:1px solid rgba(148,163,184,.09)}.ai-documents svg{color:#88b6fa;font-size:.85rem}.ai-documents span{display:grid;gap:2px;min-width:0;flex:1;color:#c5d2e1;font-size:.61rem}.ai-documents small{color:#7d90a8;font-size:.52rem}.ai-documents b{color:#91bdfd;font:600 .56rem 'DM Mono',monospace}.ai-artifacts{padding:10px;border-left:2px solid #5e9fff;border-radius:0 8px 8px 0;background:rgba(79,140,255,.055)}.ai-artifacts>p:not(:first-child){display:flex;align-items:center;gap:6px;color:#b7c8dc;font-size:.61rem}.ai-artifacts i{width:5px;height:5px;border-radius:50%;background:#4bd09e}.ai-bottom{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;padding:14px!important}.ai-confidence>div{display:flex;align-items:end;gap:8px;height:58px;margin:9px 0;border-bottom:1px solid rgba(148,163,184,.14)}.ai-confidence span{position:relative;flex:1;min-height:8px;border-radius:4px 4px 0 0;background:linear-gradient(#68a5ff,#38649e)}.ai-confidence small{position:absolute;top:-13px;color:#9fc5ff;font-size:.49rem}.ai-confidence>p:last-child{color:#7e90a8;font-size:.56rem}.ai-execution{display:grid;align-content:start;gap:7px}.ai-execution>p:not(:first-child){display:flex;gap:6px;color:#a2b3c6;font-size:.61rem}.ai-execution i{width:6px;height:6px;margin-top:3px;border-radius:50%;background:#54cc9d}.ai-execution b{margin-left:auto;color:#d3dfed;font-size:.54rem}.ai-decisions>p:nth-child(2){margin:6px 0 9px;color:#9fafc2;font-size:.63rem;line-height:1.4}.ai-decisions .MuiButton-root{font-size:.6rem!important;text-transform:none}@keyframes ai-live{50%{opacity:.35;box-shadow:0 0 0 7px rgba(75,208,158,.04)}}@keyframes ai-progress{50%{filter:brightness(1.4)}}@media(max-width:1200px){.ai-flagship-grid{grid-template-columns:250px minmax(360px,1fr)}.ai-evidence{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr}.ai-evidence .ai-panel-head{grid-column:1/-1}.ai-artifacts{grid-column:span 2}}@media(max-width:820px){.ai-flagship-grid{grid-template-columns:1fr}.ai-evidence{grid-column:auto}.ai-bottom{grid-template-columns:1fr}.ai-flagship-head{align-items:start;flex-direction:column}}@media(max-width:520px){.ai-evidence{grid-template-columns:1fr}.ai-artifacts{grid-column:auto}.evidence-graph>div{grid-template-columns:1fr 1fr}.ai-flagship-head{gap:10px}}
```

## frontend/src/redesign/ambient.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/ambient.css`

```css
.os-ambient{display:grid;gap:1px;padding:0 8px;text-align:right}.os-ambient p:first-child{color:#d5e1f0;font:600 .67rem "DM Mono",monospace}.os-ambient p:last-child{color:#7e91aa;font-size:.56rem;letter-spacing:.04em}@media(max-width:1080px){.os-ambient{display:none}}
```

## frontend/src/redesign/AssistantPanel.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/AssistantPanel.jsx`

```javascript
import { useState } from 'react';
import { Box, Button, CircularProgress, IconButton, Stack, TextField, Typography } from '@mui/material';
import { CloseOutlined, SendOutlined, SmartToyOutlined } from '@mui/icons-material';
import { askAssistant } from '../api/client';

const prompts = ['What needs my attention?', 'Explain the active investigation', 'Summarize current asset risk'];

export function AssistantPanel({ onClose }) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const send = async (value = question) => {
    const text = value.trim(); if (!text || busy) return;
    setMessages((items) => [...items, { role: 'operator', text }]); setQuestion(''); setBusy(true);
    try { const response = await askAssistant(text); setMessages((items) => [...items, { role: 'assistant', text: response.data.answer || 'No response was returned.' }]); }
    catch (error) {
      const unavailable = !error.response;
      setMessages((items) => [...items, { role: 'assistant', text: unavailable ? 'RigOS cannot reach the AI service. Check the deployed backend connection, then try again.' : (error.response?.data?.detail || 'The AI service could not complete that request. Please try again.') }]);
    }
    finally { setBusy(false); }
  };
  return <Box className="assistant-panel"><Stack direction="row" justifyContent="space-between" alignItems="start"><Box><Typography className="product-dialog-label">RIGOS AI</Typography><Typography variant="h6">Operations copilot</Typography><Typography variant="body2" color="text.secondary">Ask about assets, incidents, evidence, and recommended next actions.</Typography></Box><IconButton onClick={onClose}><CloseOutlined /></IconButton></Stack><Stack direction="row" flexWrap="wrap" gap={.7} sx={{ mt: 2 }}>{prompts.map((prompt) => <Button key={prompt} size="small" variant="outlined" onClick={() => send(prompt)}>{prompt}</Button>)}</Stack><Box className="assistant-history">{messages.length ? <Stack spacing={1.2}>{messages.map((message, index) => <Box key={index} className={`assistant-message ${message.role}`}><Typography variant="body2">{message.text}</Typography></Box>)}{busy && <CircularProgress size={20} />}</Stack> : <Box className="assistant-empty"><SmartToyOutlined/><Typography fontWeight={750}>How can I help?</Typography><Typography variant="body2" color="text.secondary">I use the existing RigOS knowledge service and live operational context.</Typography></Box>}</Box><Stack direction="row" spacing={1}><TextField fullWidth value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask RigOS⬦" onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); send(); } }} /><Button variant="contained" onClick={() => send()} disabled={!question.trim() || busy}><SendOutlined /></Button></Stack></Box>;
}
```

## frontend/src/redesign/copilot.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/copilot.css`

```css
.copilot-dock{position:fixed;z-index:1400;top:78px;right:18px;bottom:18px;width:min(440px,calc(100vw - 36px));border:1px solid rgba(148,163,184,.18);border-radius:16px;background:#111722;box-shadow:-18px 20px 60px rgba(0,0,0,.34);overflow:hidden}.copilot-dock .assistant-panel{display:grid;grid-template-rows:auto auto 1fr auto;height:100%;padding:20px}.copilot-dock .assistant-history{min-height:0;max-height:none}@media(max-width:680px){.copilot-dock{top:66px;right:0;bottom:0;width:100%;border-radius:0}}
```

## frontend/src/redesign/executive-briefing.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/executive-briefing.css`

```css
.executive-briefing{display:grid;gap:16px}.briefing-head{display:flex;align-items:end;justify-content:space-between;gap:16px}.briefing-title{margin:5px 0!important;font-family:Georgia,'Times New Roman',serif!important;font-size:1.85rem!important;font-weight:700!important;letter-spacing:-.05em}.briefing-head>div>p:last-child{color:#93a5bb;font-size:.72rem}.briefing-layout{display:grid;grid-template-columns:225px minmax(450px,1fr) 270px;gap:14px}.briefing-index,.briefing-document,.briefing-rail{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:14px!important;box-shadow:none!important}.briefing-index{display:grid;align-content:start;gap:6px;padding:14px!important}.briefing-index-title{margin:-6px 0 7px!important;font-size:1.05rem!important;font-weight:800!important}.briefing-index button{display:flex;gap:8px;width:100%;padding:9px;border:1px solid transparent;border-radius:8px;background:transparent;color:#cdd9e8;cursor:pointer;text-align:left}.briefing-index button:hover,.briefing-index button.selected{border-color:rgba(98,161,255,.35);background:rgba(79,140,255,.09)}.briefing-index button>span{color:#7890ad;font:600 .57rem 'DM Mono',monospace}.briefing-index button>div{display:grid;gap:3px;min-width:0}.briefing-index b{overflow:hidden;font-size:.65rem;white-space:nowrap;text-overflow:ellipsis}.briefing-index small{overflow:hidden;color:#8093aa;font-size:.54rem;white-space:nowrap;text-overflow:ellipsis}.briefing-index-audit{display:grid;gap:7px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(148,163,184,.1)}.briefing-index-audit>p:not(:first-child){display:flex;align-items:center;gap:5px;color:#8fa1b7;font-size:.6rem}.briefing-index-audit i,.briefing-approvals i{width:6px;height:6px;border-radius:50%;background:#f0a25e}.briefing-index-audit i{background:#4dcc9b}.briefing-document{padding:27px 34px!important}.briefing-document-top{display:flex;justify-content:space-between;gap:10px;padding-bottom:16px;border-bottom:1px solid rgba(148,163,184,.12)}.briefing-document-top>p{color:#7e91a9;font-size:.56rem!important;font-weight:800!important;letter-spacing:.1em}.briefing-document-top>p:last-child{letter-spacing:0;font-weight:500!important}.briefing-document-top b{color:#a5c5ee}.briefing-document-title{margin:25px 0 10px!important;font-family:Georgia,'Times New Roman',serif!important;font-size:2.1rem!important;font-weight:700!important;letter-spacing:-.055em}.briefing-lede{max-width:700px;color:#c2cede;font-family:Georgia,'Times New Roman',serif!important;font-size:1rem!important;line-height:1.6!important}.briefing-numbers{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:23px 0}.briefing-numbers .metric{padding:9px 0;border-top:2px solid #5f9eff}.briefing-section{margin-top:22px}.briefing-section>p:last-child{margin-top:7px;color:#b7c5d6;font-size:.72rem;line-height:1.6}.briefing-timeline{display:grid;gap:0;margin-top:22px}.briefing-timeline>div{display:grid;grid-template-columns:18px 1fr auto;gap:8px;padding:7px 0}.briefing-timeline i{width:8px;height:8px;margin-top:5px;border-radius:50%;background:#5f9eff;box-shadow:0 0 0 4px rgba(95,158,255,.08)}.briefing-timeline>div:not(:last-child){border-bottom:1px solid rgba(148,163,184,.08)}.briefing-timeline p{display:grid;gap:2px;font-size:.66rem}.briefing-timeline small{color:#8294aa;font-size:.57rem}.briefing-timeline span{color:#8294aa;font:600 .53rem 'DM Mono',monospace}.briefing-section.recommendation{padding:12px;border-left:2px solid #4dce9e;border-radius:0 9px 9px 0;background:rgba(75,208,158,.05)}.briefing-rail{display:grid;align-content:start;gap:15px;padding:15px!important}.briefing-confidence{padding:10px;border-radius:9px;background:#0c1016}.briefing-confidence p{color:#8295ad;font-size:.61rem}.briefing-confidence b{display:block;margin:4px 0;color:#b7d4ff;font:700 1.2rem 'DM Mono',monospace}.briefing-confidence i{display:block;height:4px;border-radius:99px;background:rgba(148,163,184,.15);overflow:hidden}.briefing-confidence i span{display:block;height:100%;border-radius:99px;background:#5f9eff}.briefing-evidence,.briefing-approvals{display:grid;gap:8px}.briefing-evidence>p:not(:first-child){display:flex;align-items:center;gap:6px;color:#aebfd2;font-size:.6rem}.briefing-evidence svg{color:#85b5f7;font-size:.8rem}.briefing-evidence b{margin-left:auto;color:#82d5b3;font:600 .52rem 'DM Mono',monospace}.briefing-approvals{padding-top:12px;border-top:1px solid rgba(148,163,184,.1)}.briefing-approvals>p:not(:first-child){display:flex;align-items:center;gap:6px;color:#a4b4c7;font-size:.6rem}.briefing-approvals i.done{background:#4dce9e}.briefing-approvals b{margin-left:auto;color:#c9d6e5;font-size:.54rem}.briefing-rail .MuiButton-root{font-size:.65rem!important;text-transform:none}.executive-briefing.presentation .briefing-index,.executive-briefing.presentation .briefing-rail{display:none}.executive-briefing.presentation .briefing-layout{grid-template-columns:minmax(0,920px);justify-content:center}.executive-briefing.presentation .briefing-document{padding:48px 68px!important}.executive-briefing.presentation .briefing-document-title{font-size:2.7rem!important}@media(max-width:1100px){.briefing-layout{grid-template-columns:210px 1fr}.briefing-rail{grid-column:1/-1;grid-template-columns:repeat(3,1fr)}.briefing-rail>.product-kicker{grid-column:1/-1}.briefing-rail .MuiStack-root{grid-column:span 2}}@media(max-width:720px){.briefing-layout{grid-template-columns:1fr}.briefing-index{max-height:260px}.briefing-rail{grid-column:auto;grid-template-columns:1fr}.briefing-rail>.product-kicker,.briefing-rail .MuiStack-root{grid-column:auto}.briefing-document{padding:22px!important}.briefing-document-title{font-size:1.75rem!important}.briefing-numbers{grid-template-columns:1fr 1fr}.briefing-head{align-items:start;flex-direction:column}}@media(max-width:460px){.briefing-numbers{grid-template-columns:1fr}.briefing-document-top{align-items:start;flex-direction:column}}
```

## frontend/src/redesign/final-polish.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/final-polish.css`

```css
/* Final product-quality layer: shared density, controls, state, and accessibility contract. */
:root{--rig-surface:#10151c;--rig-surface-raised:#141b25;--rig-inset:#0c1016;--rig-line:rgba(148,163,184,.14);--rig-line-strong:rgba(148,163,184,.24);--rig-text:#e7eef8;--rig-muted:#8d9eb3;--rig-blue:#6aa6ff;--rig-radius:12px;--rig-radius-sm:8px;--rig-shadow:0 10px 28px rgba(0,0,0,.14);--rig-fast:150ms;--rig-standard:220ms;--rig-ease:cubic-bezier(.2,.8,.2,1)}
.product-page{max-width:none!important}.product-page :where(.MuiTypography-root){text-wrap:pretty}.product-page :where(.MuiPaper-root){box-shadow:none}.product-page :where(.MuiButton-root){min-height:30px;letter-spacing:0}.product-page :where(.MuiButton-contained){box-shadow:0 4px 12px rgba(43,105,200,.2)!important}.product-page :where(.MuiOutlinedInput-root){min-height:34px;border-radius:var(--rig-radius-sm)}.product-page :where(.MuiInputBase-input){font-size:.72rem}.product-page :where(.MuiSelect-select){font-size:.7rem}.product-page :where(.MuiChip-root){height:22px;border-radius:6px;font-size:.6rem;font-weight:750}.product-page :where(.MuiIconButton-root){border-radius:8px}.product-page :where(.MuiDivider-root){border-color:rgba(148,163,184,.1)}
.product-page button,.product-page [role=button]{-webkit-tap-highlight-color:transparent}.product-page button:not(:disabled),.product-page [role=button]{transition:transform var(--rig-fast) var(--rig-ease),background-color var(--rig-fast) ease,border-color var(--rig-fast) ease,box-shadow var(--rig-fast) ease}.product-page button:not(:disabled):hover{transform:translateY(-1px)}.product-page button:not(:disabled):active{transform:translateY(0) scale(.985)}.product-page button:focus-visible,.product-page a:focus-visible,.product-page input:focus-visible{outline:2px solid #8ab7ff!important;outline-offset:2px}.product-page button:disabled{opacity:.52;cursor:not-allowed}
.product-page :where(.mission-twin,.mission-telemetry-panel,.mission-decisions,.mission-feed,.mission-agents,.mission-risks,.mission-shift,.mission-executive,.asset-explorer,.twin-canvas,.twin-inspector,.twin-bottom,.incident-queue,.investigation-timeline,.incident-evidence,.incident-bottom,.maintenance-board,.maintenance-inspector,.maintenance-bottom,.ai-pipeline,.ai-reasoning,.ai-evidence,.ai-bottom,.terminal-watchlist,.terminal-chart,.terminal-scenario,.terminal-bottom,.briefing-index,.briefing-document,.briefing-rail){border-color:var(--rig-line)!important}.product-page :where(.mission-twin,.mission-telemetry-panel,.mission-decisions,.mission-feed,.mission-agents,.mission-risks,.mission-shift,.asset-explorer,.twin-canvas,.twin-inspector,.incident-queue,.investigation-timeline,.incident-evidence,.maintenance-board,.maintenance-inspector,.ai-pipeline,.ai-reasoning,.ai-evidence,.terminal-watchlist,.terminal-chart,.terminal-scenario,.briefing-index,.briefing-rail){transition:border-color var(--rig-standard) ease,background-color var(--rig-standard) ease,box-shadow var(--rig-standard) ease}.product-page :where(.mission-twin,.mission-telemetry-panel,.mission-decisions,.mission-feed,.mission-agents,.mission-risks,.mission-shift,.asset-explorer,.twin-canvas,.twin-inspector,.incident-queue,.investigation-timeline,.incident-evidence,.maintenance-board,.maintenance-inspector,.ai-pipeline,.ai-reasoning,.ai-evidence,.terminal-watchlist,.terminal-chart,.terminal-scenario,.briefing-index,.briefing-rail):hover{border-color:var(--rig-line-strong)!important;box-shadow:var(--rig-shadow)!important}
.product-kicker{color:#7890ad!important;font-size:.57rem!important;letter-spacing:.115em!important}.product-page :where(.metric)>p:first-child{color:#7e90a7!important;font-size:.55rem!important;letter-spacing:.065em}.product-page :where(.metric)>p:last-child{color:var(--rig-text)!important;font-size:.72rem!important;font-weight:760!important}.mini-graph{border-radius:var(--rig-radius-sm);overflow:hidden}.mini-graph>p{color:#7f91a8!important;font-size:.56rem!important}.mini-graph svg{filter:drop-shadow(0 5px 8px rgba(61,130,240,.08))}
.mission-command-grid,.mission-lower-grid,.twin-workspace-grid,.incident-os-grid,.maintenance-layout,.ai-flagship-grid,.forecast-terminal-grid,.briefing-layout{align-items:stretch}.mission-lower-grid>*,.maintenance-layout>*,.ai-flagship-grid>*,.forecast-terminal-grid>*,.briefing-layout>*{min-width:0}.asset-tree,.incident-queue-list,.mission-feed,.mission-agent-list,.briefing-index{scrollbar-width:thin;scrollbar-color:rgba(132,160,196,.35) transparent}.asset-tree::-webkit-scrollbar,.incident-queue-list::-webkit-scrollbar{width:5px}.asset-tree::-webkit-scrollbar-thumb,.incident-queue-list::-webkit-scrollbar-thumb{border-radius:9px;background:rgba(132,160,196,.35)}
.product-page :where(.twin-empty,.product-empty-state){min-height:220px;border-radius:var(--rig-radius)!important}.product-page :where(.twin-empty,.product-empty-state) :is(p,h1,h2,h3){max-width:480px}.product-page :where(.MuiSkeleton-root){background:linear-gradient(90deg,rgba(148,163,184,.06),rgba(148,163,184,.13),rgba(148,163,184,.06));background-size:200% 100%;animation:rig-skeleton 1.4s ease infinite}
@keyframes rig-skeleton{to{background-position:-200% 0}}@media(max-width:900px){.product-page{padding-bottom:38px}.mission-situation,.briefing-head,.forecast-terminal-head,.ai-flagship-head{gap:10px}.product-page :where(.MuiButton-root){min-height:32px}}@media(max-width:520px){.product-page :where(.MuiButton-root){font-size:.65rem!important}.product-page :where(.MuiIconButton-root){padding:6px}.product-kicker{font-size:.54rem!important}}@media(prefers-reduced-motion:reduce){.product-page *, .product-page *:before,.product-page *:after{scroll-behavior:auto!important;animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}

/* Remove redundant hero whitespace now that each operating surface owns its context. */
.os-stage main{padding-top:20px!important}.product-page>.product-hero{max-width:760px!important;margin-bottom:24px!important}.product-hero h1{margin:7px 0 10px!important;font-size:clamp(2.5rem,4.2vw,4.5rem)!important;line-height:.95!important}.product-hero>p:last-child{font-size:.88rem!important;line-height:1.55!important}.os-crumb{margin-bottom:12px!important}.twin-process-map>svg{z-index:1!important;display:block!important}.twin-grid-lines{z-index:0!important}.twin-map-node{z-index:3!important;display:flex!important}.twin-map-legend{z-index:4!important}.map-pipe{stroke:rgba(119,173,255,.42)!important}.map-flow{stroke:#6ea9ff!important}.twin-process-map{background:radial-gradient(circle at 52% 45%,rgba(77,141,255,.18),transparent 40%),#0b1017!important}
```

## frontend/src/redesign/forecast-terminal.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/forecast-terminal.css`

```css
.forecast-terminal{display:grid;gap:14px}.forecast-terminal-head{display:flex;justify-content:space-between;align-items:end;gap:12px}.forecast-terminal-title{margin-top:4px!important;font-size:1.35rem!important;font-weight:830!important;letter-spacing:-.05em}.forecast-terminal-grid{display:grid;grid-template-columns:230px minmax(430px,1fr) 260px;gap:12px}.terminal-watchlist,.terminal-chart,.terminal-scenario,.terminal-bottom{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:14px!important;box-shadow:none!important}.terminal-watchlist{display:grid;align-content:start;gap:5px;padding:14px!important;overflow:auto}.terminal-watchlist-sub{margin-bottom:7px!important;color:#8092a9;font-size:.61rem!important}.terminal-watchlist button{display:flex;align-items:center;gap:7px;width:100%;padding:8px;border:1px solid transparent;border-radius:8px;background:transparent;color:#d4dfed;cursor:pointer;text-align:left}.terminal-watchlist button:hover,.terminal-watchlist button.selected{border-color:rgba(94,157,255,.3);background:rgba(79,140,255,.1)}.terminal-watchlist button>span{color:#72859e;font:600 .58rem 'DM Mono',monospace}.terminal-watchlist button>div{display:grid;gap:2px;min-width:0;flex:1}.terminal-watchlist b{overflow:hidden;font-size:.65rem;white-space:nowrap;text-overflow:ellipsis}.terminal-watchlist small{overflow:hidden;color:#8295ad;font-size:.54rem;white-space:nowrap;text-overflow:ellipsis}.terminal-watchlist em{color:#ed9b75;font:700 .6rem 'DM Mono',monospace;font-style:normal}.terminal-chart{padding:15px!important;overflow:hidden}.terminal-chart-head{display:flex;justify-content:space-between;gap:10px}.terminal-chart-head>div:first-child>p:last-child{margin-top:4px;color:#b8c7d8;font-size:.68rem}.terminal-chart-legend{display:flex;gap:8px;align-items:start;flex-wrap:wrap}.terminal-chart-legend span{display:flex;gap:4px;align-items:center;color:#7d90a8;font-size:.54rem}.terminal-chart-legend i{width:6px;height:6px;border-radius:50%;background:#5f9eff}.terminal-chart-legend .observed{background:#48ce9c}.terminal-chart-legend .band{background:rgba(95,158,255,.5)}.terminal-graph{position:relative;margin-top:13px}.terminal-graph svg{display:block;width:100%;height:267px}.terminal-graph line{stroke:rgba(148,163,184,.14);stroke-width:1}.terminal-watch-zone{fill:rgba(238,171,79,.08)}.terminal-critical-zone{fill:rgba(237,115,104,.08)}.terminal-line{fill:none;stroke:#68a5ff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1000;animation:forecast-line 1.2s ease forwards}.terminal-marker{stroke:#eca35e!important;stroke-dasharray:4 4}.terminal-graph text{fill:#d7aa75;font-size:11px}.terminal-axis{display:flex;justify-content:space-between;margin-top:-8px;color:#8092a9;font:600 .56rem 'DM Mono',monospace}.terminal-brush{height:12px;margin-top:12px;border:1px solid rgba(148,163,184,.15);border-radius:6px;background:#0c1016}.terminal-brush span{position:relative;display:block;height:100%;border:1px solid rgba(105,164,255,.6);border-radius:5px;background:rgba(79,140,255,.2)}.terminal-brush span:before,.terminal-brush span:after{position:absolute;top:-3px;bottom:-3px;width:3px;border-radius:2px;background:#85b5ff;content:''}.terminal-brush span:before{left:-2px}.terminal-brush span:after{right:-2px}.terminal-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:14px}.terminal-stats .metric{padding:8px;border-top:1px solid rgba(148,163,184,.1)}.terminal-scenario{display:grid;align-content:start;gap:12px;padding:14px!important}.terminal-scenario-title{margin-top:-8px!important;font-size:1.05rem!important;font-weight:810!important}.terminal-scenario>p:nth-child(3){color:#93a5ba;font-size:.65rem;line-height:1.45}.scenario-control{padding:10px;border-radius:9px;background:#0c1016}.scenario-control>p{color:#889ab0;font-size:.6rem}.scenario-control>div{justify-content:space-between;align-items:center;margin-top:8px}.scenario-control b{color:#afd0ff;font:700 .85rem 'DM Mono',monospace}.scenario-control .MuiButton-root{min-width:27px!important;padding:3px!important;color:#a8c8fb}.scenario-outcomes{display:grid;gap:8px}.scenario-outcomes .metric{padding:8px;border-bottom:1px solid rgba(148,163,184,.1)}.terminal-recommendation{padding:10px;border-left:2px solid #619fff;border-radius:0 8px 8px 0;background:rgba(79,140,255,.06)}.terminal-recommendation>p:last-child{margin-top:6px;color:#b7c8dc;font-size:.64rem;line-height:1.45}.terminal-bottom{display:grid;grid-template-columns:1.25fr 1fr;gap:18px;padding:14px!important}.terminal-bottom>div{min-width:0}.terminal-bottom>div>p:nth-child(2){margin:5px 0;color:#98aac0;font-size:.65rem}.terminal-bottom b{color:#f0ba83}.terminal-bottom .mini-graph{margin:7px 0 0}.sensitivity-bars{display:grid;gap:8px;margin-top:10px}.sensitivity-bars p{display:grid;grid-template-columns:92px 1fr 45px;gap:7px;align-items:center;color:#94a6bc;font-size:.6rem}.sensitivity-bars i{height:5px;border-radius:99px;background:rgba(148,163,184,.14);overflow:hidden}.sensitivity-bars i b{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#5e9eff,#ef9c66)}.sensitivity-bars em{color:#aec2dc;font-style:normal;font:600 .53rem 'DM Mono',monospace}@keyframes forecast-line{to{stroke-dashoffset:0}}@media(max-width:1120px){.forecast-terminal-grid{grid-template-columns:210px 1fr}.terminal-scenario{grid-column:1/-1;grid-template-columns:repeat(3,1fr)}.terminal-scenario>.product-kicker,.terminal-scenario-title,.terminal-scenario>p:nth-child(3){grid-column:1/-1}.terminal-recommendation{grid-column:span 2}}@media(max-width:760px){.forecast-terminal-grid{grid-template-columns:1fr}.terminal-watchlist{max-height:270px}.terminal-scenario{grid-column:auto;grid-template-columns:1fr}.terminal-recommendation{grid-column:auto}.terminal-bottom{grid-template-columns:1fr}.terminal-stats{grid-template-columns:1fr 1fr}.forecast-terminal-head{align-items:start;flex-direction:column}}@media(prefers-reduced-motion:reduce){.terminal-line{animation:none}}
```

## frontend/src/redesign/incident-management.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/incident-management.css`

```css
.incident-os{display:grid;gap:14px}.incident-os-head{display:flex;align-items:end;justify-content:space-between;gap:14px}.incident-os-title{margin-top:4px!important;font-size:1.35rem!important;font-weight:820!important;letter-spacing:-.045em}.incident-os-grid{display:grid;grid-template-columns:250px minmax(420px,1fr) 285px;gap:12px;min-height:590px}.incident-queue,.investigation-timeline,.incident-evidence,.incident-bottom{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;box-shadow:none!important;border-radius:14px!important}.incident-queue{display:grid;align-content:start;gap:10px;padding:14px!important;overflow:auto}.incident-queue-head,.investigation-head,.incident-evidence-head{display:flex;align-items:start;justify-content:space-between;gap:8px}.incident-queue-head>div>p:last-child,.incident-evidence-head>div>p:last-child{margin-top:4px;color:#c4d0df;font-size:.75rem}.incident-queue .MuiOutlinedInput-root{background:#0c1016;border-radius:9px}.incident-queue .MuiInputBase-input{font-size:.7rem}.incident-queue-list{display:grid;gap:6px}.incident-queue-item{display:grid;gap:7px;width:100%;padding:10px;border:1px solid transparent;border-radius:10px;background:#0c1016;color:#d7e1ee;cursor:pointer;text-align:left}.incident-queue-item:hover{border-color:rgba(148,163,184,.2)}.incident-queue-item.selected{border-color:rgba(94,157,255,.45);background:rgba(79,140,255,.1);box-shadow:inset 2px 0 #67a5ff}.incident-queue-item>div:first-child,.incident-queue-item>div:last-child{display:flex;justify-content:space-between;align-items:center;gap:7px}.incident-queue-item>div:first-child>p{color:#72839b;font-size:.57rem}.incident-queue-item>b{font-size:.71rem;line-height:1.25}.incident-queue-item>p{overflow:hidden;color:#8fa0b7;font-size:.61rem;white-space:nowrap;text-overflow:ellipsis}.incident-queue-item>div:last-child span{color:#91a7c5;font:600 .55rem 'DM Mono',monospace}.investigation-timeline{padding:16px!important;overflow:auto}.investigation-title{margin:5px 0 2px!important;font-size:1.25rem!important;font-weight:840!important;letter-spacing:-.045em}.investigation-head .MuiTypography-caption{color:#8192a9;font-size:.62rem}.incident-summary-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:16px 0;padding:10px;border:1px solid rgba(148,163,184,.1);border-radius:10px;background:#0c1016}.incident-summary-strip>div{min-width:0}.incident-summary-strip p{color:#7c8da5;font-size:.55rem!important;font-weight:800!important;letter-spacing:.06em;text-transform:uppercase}.incident-summary-strip b{display:block;margin-top:5px;overflow:hidden;color:#dbe6f4;font-size:.7rem;white-space:nowrap;text-overflow:ellipsis}.incident-timeline{display:grid;gap:0}.incident-event{position:relative;display:grid;grid-template-columns:28px 1fr;gap:10px;padding:0 0 18px}.incident-event:not(:last-child):before{position:absolute;top:27px;bottom:0;left:13px;width:1px;background:rgba(148,163,184,.18);content:''}.incident-event>span{z-index:1;display:grid;place-items:center;width:27px;height:27px;border:1px solid rgba(92,157,255,.42);border-radius:50%;background:#142033;color:#a9caff;font:700 .62rem 'DM Mono',monospace}.incident-event.alert>span{border-color:rgba(239,126,112,.48);color:#ef9a8f}.incident-event.agent>span{border-color:rgba(172,132,239,.48);color:#c6a6ff}.incident-event>div>p:first-child{display:flex;align-items:center;gap:8px;color:#dce7f4;font-size:.73rem;font-weight:800}.incident-event small{color:#73859e;font-size:.55rem;font-weight:600}.incident-event>div>p:nth-child(2){margin-top:5px;color:#aebdce;font-size:.67rem;line-height:1.48}.incident-event .MuiButton-root{margin-top:6px;padding:2px 0!important;color:#9ac4ff;font-size:.61rem!important;text-transform:none}.incident-reasoning{margin-top:7px;padding:8px;border-left:2px solid #9f80e6;border-radius:0 7px 7px 0;background:rgba(169,132,239,.07);color:#c5b4e6;font-size:.63rem;line-height:1.45}.dependency-graph{padding:12px;border:1px solid rgba(148,163,184,.11);border-radius:10px;background:#0c1016}.dependency-graph>div{display:flex;align-items:center;justify-content:space-between;gap:7px;margin:10px 0}.dependency-graph span,.dependency-graph strong{padding:6px 7px;border:1px solid rgba(148,163,184,.16);border-radius:7px;color:#9aacc1;font-size:.58rem;text-align:center}.dependency-graph strong{border-color:rgba(239,156,95,.42);color:#f5c08b}.dependency-graph i{flex:1;height:1px;background:linear-gradient(90deg,#5e9dff,#f1a15e)}.dependency-graph .MuiTypography-caption{color:#7789a1;font-size:.57rem}.incident-evidence{display:grid;align-content:start;gap:13px;padding:14px!important;overflow:auto}.incident-evidence-head .MuiButton-root{color:#a7caff;font-size:.6rem!important;text-transform:none}.evidence-snapshot{padding:11px;border:1px solid rgba(148,163,184,.11);border-radius:10px;background:#0c1016}.evidence-snapshot>div:first-child{display:flex;justify-content:space-between;gap:8px}.evidence-snapshot>div:first-child>p:last-child{color:#88a7cf;font-size:.58rem}.evidence-snapshot .mini-graph{margin:10px 0 0}.evidence-list{display:grid;gap:5px}.evidence-list>div{display:flex;align-items:center;gap:8px;padding:7px 2px;border-bottom:1px solid rgba(148,163,184,.09)}.evidence-list>div>span{display:grid;place-items:center;width:25px;height:25px;border-radius:7px;background:rgba(79,140,255,.1);color:#94bdff}.evidence-list>div>span svg{font-size:.83rem}.evidence-list>div>p{display:grid;gap:2px;min-width:0}.evidence-list b{font-size:.65rem}.evidence-list small{overflow:hidden;color:#8192a9;font-size:.56rem;white-space:nowrap;text-overflow:ellipsis}.evidence-list>div>svg{margin-left:auto;color:#71839a}.root-cause{padding:10px;border-left:2px solid #e89c63;border-radius:0 8px 8px 0;background:rgba(239,155,91,.06)}.root-cause>p:last-child{margin-top:6px;color:#cbb59e;font-size:.65rem;line-height:1.45}.incident-bottom{overflow:hidden}.incident-bottom-tabs{display:flex;gap:3px;overflow:auto;padding:4px 9px;border-bottom:1px solid rgba(148,163,184,.1)}.incident-bottom-tabs .MuiButton-root{min-width:max-content;padding:8px 9px!important;color:#8496ad!important;font-size:.62rem!important;text-transform:none!important}.incident-bottom-tabs .MuiButton-root.active{color:#cfe2ff!important;border-bottom:2px solid #67a5ff;border-radius:0}.incident-bottom-body{display:grid;grid-template-columns:1.35fr 1fr;gap:18px;padding:14px}.operator-note{max-width:560px;margin:6px 0 8px!important;color:#9caec2;font-size:.67rem!important;line-height:1.45}.incident-bottom-body .MuiButton-root{padding:2px 0!important;color:#9ac4ff;font-size:.62rem!important;text-transform:none}.decision-track{display:grid;align-content:start;gap:7px}.decision-track>p:not(:first-child){display:flex;align-items:center;gap:6px;color:#9bacbf;font-size:.63rem}.decision-track i{width:6px;height:6px;border-radius:50%;background:#60a0ff}.decision-track p:last-child i{background:#f0a05f}.decision-track b{margin-left:auto;color:#ced9e8;font-size:.57rem}@media(max-width:1220px){.incident-os-grid{grid-template-columns:230px minmax(360px,1fr)}.incident-evidence{grid-column:1/-1;grid-template-columns:1fr 1fr}.incident-evidence-head{grid-column:1/-1}.root-cause{grid-column:span 2}}@media(max-width:850px){.incident-os-grid{grid-template-columns:1fr}.incident-queue{max-height:340px}.incident-evidence{grid-column:auto}.incident-bottom-body{grid-template-columns:1fr}.incident-os-head{align-items:start;flex-direction:column}}@media(max-width:540px){.incident-summary-strip{grid-template-columns:1fr 1fr}.incident-evidence{grid-template-columns:1fr}.root-cause{grid-column:auto}.dependency-graph>div{gap:3px}.dependency-graph span,.dependency-graph strong{padding:5px;font-size:.5rem}}
```

## frontend/src/redesign/incidents.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/incidents.css`

```css
.incident-workspace-v2{display:grid;grid-template-columns:340px minmax(0,1fr);gap:16px}.incident-index-v2,.incident-detail-v2{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:15px!important;box-shadow:none!important}.incident-index-v2{padding:17px!important}.incident-index-v2 .MuiOutlinedInput-root{background:#0d1117;border-radius:8px}.incident-case-list{display:grid;gap:7px;margin-top:16px}.incident-case{display:grid;gap:7px;padding:12px;border:1px solid transparent;border-radius:10px;cursor:pointer}.incident-case:hover{background:#151c26}.incident-case.selected{border-color:rgba(96,156,255,.3);background:rgba(79,140,255,.09)}.incident-case-time{color:#8191a8;font:500 .58rem "DM Mono",monospace!important}.incident-case>p:nth-of-type(1){font-size:.82rem}.incident-case-evidence{padding-top:7px;border-top:1px solid rgba(148,163,184,.1);color:#aebace;font-size:.68rem;line-height:1.45}.incident-expand{justify-content:flex-start!important;min-height:21px!important;padding:0!important;color:#91a5c0!important;font-size:.62rem!important;text-transform:none!important}.incident-detail-v2{padding:23px!important}.incident-facts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:20px 0}.incident-facts .metric{min-height:72px;padding:11px;border-radius:9px;background:#0c1016}.incident-timeline-v2{display:grid;gap:0;margin-top:16px}.incident-timeline-entry{display:grid;grid-template-columns:18px minmax(0,1fr);gap:11px;min-height:84px}.incident-timeline-rail{position:relative;display:flex;justify-content:center}.incident-timeline-rail:after{content:'';position:absolute;top:13px;bottom:-5px;width:1px;background:rgba(148,163,184,.17)}.incident-timeline-entry:last-child .incident-timeline-rail:after{display:none}.incident-timeline-rail i{position:relative;z-index:1;width:9px;height:9px;margin-top:5px;border-radius:50%;background:#63a4ff;box-shadow:0 0 0 4px rgba(99,164,255,.08)}.incident-timeline-entry.violet .incident-timeline-rail i{background:#a887ff}.incident-timeline-entry.warning .incident-timeline-rail i{background:#f2aa48}.incident-timeline-entry>div:last-child>p{margin-top:5px;max-width:760px;line-height:1.55}.incident-operator-bar{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:6px;padding:14px;border:1px solid rgba(148,163,184,.13);border-radius:11px;background:#0c1016}.incident-operator-bar .MuiButton-root{text-transform:none!important;font-size:.7rem!important}@media(max-width:860px){.incident-workspace-v2{grid-template-columns:1fr}.incident-case-list{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.incident-case-list,.incident-facts{grid-template-columns:1fr}.incident-operator-bar{align-items:stretch;flex-direction:column}.incident-operator-bar>.MuiStack-root{flex-wrap:wrap}.incident-detail-v2{padding:17px!important}}
```

## frontend/src/redesign/interaction.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/interaction.css`

```css
/* Part 8 — Interaction Model: sticky chrome + allowed animation timings */

:root {
  --p8-select: 120ms;
  --p8-crossfade: 200ms;
  --p8-page: 120ms;
  --p8-pulse: 400ms;
  --p8-stage: 120ms;
}

/* Sticky: Mission Control OperationsStrip */
.mission-os .rig-operations-strip,
.p8-operations-strip {
  position: sticky;
  top: 0;
  z-index: 8;
  margin-bottom: 14px;
}

/* Sticky: Explorer / Kanban / Forecast / Executive toolbars & headers */
.twin-workspace-head,
.maintenance-planner-head,
.maintenance-board-head,
.terminal-watchlist .product-kicker,
.briefing-index .product-kicker,
.incident-queue-head,
.ai-pipeline .ai-panel-head {
  position: sticky;
  top: 0;
  z-index: 6;
  background: inherit;
}

.twin-workspace-head,
.maintenance-planner-head,
.incident-os-head,
.forecast-terminal-head,
.ai-flagship-head,
.briefing-head {
  position: sticky;
  top: 0;
  z-index: 7;
  padding-bottom: 8px;
  background: linear-gradient(180deg, #090b0f 70%, transparent);
}

.incident-queue-head {
  background: #11161e;
  padding-bottom: 8px;
}

.ai-pipeline {
  position: relative;
}

.ai-pipeline .ai-panel-head {
  background: #11161e;
  padding-top: 4px;
  padding-bottom: 8px;
}

.terminal-watchlist > .product-kicker,
.terminal-watchlist > .terminal-watchlist-sub {
  position: sticky;
  top: 0;
  z-index: 5;
  background: #11161e;
}

.briefing-index > .product-kicker,
.briefing-index > .briefing-index-title {
  position: sticky;
  top: 0;
  z-index: 5;
  background: #11161e;
}

/* Selection highlight 120ms */
.asset-tree-item,
.incident-queue-item,
.work-order,
.terminal-watchlist button,
.briefing-index button,
.mission-feed-row {
  transition:
    background-color var(--p8-select) ease,
    box-shadow var(--p8-select) ease,
    border-color var(--p8-select) ease,
    transform var(--p8-select) ease !important;
}

/* Inspector / dossier crossfade 200ms */
.twin-inspector,
.incident-evidence,
.maintenance-inspector,
.p8-inspector-swap {
  animation: p8-crossfade var(--p8-crossfade) ease;
}

@keyframes p8-crossfade {
  from { opacity: 0.55; }
  to { opacity: 1; }
}

/* Map / twin node pulse */
.twin-map-node.selected,
.mission-twin-node.is-pulse {
  animation: p8-node-pulse var(--p8-crossfade) ease;
}

.twin-map-node.critical i,
.asset-tree-dot.critical,
.rig-status-badge.is-pulse i {
  animation: p8-status-pulse var(--p8-pulse) ease infinite;
}

@keyframes p8-node-pulse {
  0% { box-shadow: 0 0 0 0 rgba(79, 140, 255, 0.45); }
  100% { box-shadow: 0 0 0 8px rgba(79, 140, 255, 0); }
}

@keyframes p8-status-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(0.85); }
}

/* Pipeline stage enlarge 120ms */
.ai-stage {
  transition: transform var(--p8-stage) ease, background-color var(--p8-stage) ease !important;
}

.ai-stage.expanded {
  transform: scale(1.02);
  transform-origin: left center;
}

/* Value crossfade on live metrics */
.e5-metric > p:last-child,
.rig-kpi,
.metric > p:last-child {
  transition: opacity var(--p8-crossfade) ease;
}

/* Forbidden: bounce/spring on operational panels — prefer linear fades */
.workspace-inspector,
.copilot-dock,
.product-page :where(.mission-twin, .asset-explorer, .incident-queue, .ai-pipeline, .maintenance-board) {
  transition: opacity var(--p8-page) ease, border-color var(--p8-select) ease !important;
}

.product-page :where(.interactive-card, .pulse-card, .refinery-card, .maintenance-refinery, .work-order):hover {
  transform: none !important;
}

/* Asset inspector section stack */
.p8-inspector-section {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid rgba(148, 163, 184, 0.12);
}

.p8-inspector-section:first-of-type {
  margin-top: 0;
  padding-top: 0;
  border-top: 0;
}

.p8-inspector-signals {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.p8-inspector-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.p8-inspector-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.p8-inspector-state {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* Focus trap shell */
.workspace-inspector.is-open {
  outline: none;
}

.workspace-inspector[data-focus-trap='true'] {
  box-shadow: -12px 0 40px rgba(0, 0, 0, 0.35);
}

/* Primary nav roving focus */
.os-nav a:focus-visible {
  outline: 2px solid #4f8cff;
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .twin-inspector,
  .p8-inspector-swap,
  .twin-map-node.selected,
  .mission-twin-node.is-pulse,
  .ai-stage.expanded {
    animation: none !important;
    transition: none !important;
    transform: none !important;
  }
}
```

## frontend/src/redesign/investigation.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/investigation.css`

```css
.ai-showcase{display:grid;gap:16px}.ai-showcase-header{display:flex;justify-content:space-between;align-items:start;gap:20px;padding:24px!important;background:radial-gradient(circle at 85% 25%,rgba(110,103,255,.12),transparent 28%),#10151c!important;border:1px solid rgba(148,163,184,.15)!important;border-radius:15px!important;box-shadow:none!important}.ai-showcase-title{max-width:680px;margin:8px 0!important;font-size:clamp(1.7rem,3vw,2.7rem)!important;font-weight:850!important;line-height:1.02!important;letter-spacing:-.065em!important}.ai-showcase-live{display:flex;align-items:center;gap:8px;white-space:nowrap;padding:8px 10px;border-radius:999px;background:rgba(123,103,255,.11);color:#b9adff;font-size:.65rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.ai-showcase-live i{width:6px;height:6px;border-radius:50%;background:#a997ff}.ai-workflow-map{display:flex;align-items:center;justify-content:space-between;gap:4px;overflow-x:auto;padding:13px 16px;border:1px solid rgba(148,163,184,.13);border-radius:14px;background:#0d1117}.ai-workflow-node{display:flex;align-items:center;gap:5px;color:#74849b}.ai-workflow-node>div{min-width:105px;padding:9px;border:1px solid rgba(148,163,184,.12);border-radius:9px;background:#111823}.ai-workflow-node p:first-child{color:#dbe6f4;font-size:.68rem;font-weight:800}.ai-workflow-node p:last-child{margin-top:3px;color:#8da3c2;font-size:.58rem;text-transform:uppercase;letter-spacing:.08em}.ai-workflow-node svg{width:20px;min-width:20px;color:#6a98dd}.investigation-console{margin-top:0}.trace-stage{overflow:hidden}.trace-stage-summary{transition:background-color .16s ease!important}.trace-stage-summary:hover{background:rgba(98,140,255,.055)!important}.trace-stage-detail{border-left:1px solid rgba(104,151,227,.27)}@media(max-width:700px){.ai-showcase-header{flex-direction:column}.ai-workflow-map{justify-content:flex-start}}
```

## frontend/src/redesign/magic.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/magic.jsx`

```javascript
import { useEffect, useState } from 'react';
import { motion, useReducedMotion } from 'motion/react';

// Compact local adaptations of Magic UI primitives, kept intentionally neutral for RigOS.
export function NumberTicker({ value, prefix = '', suffix = '' }) {
  const reduced = useReducedMotion();
  const target = Number(value) || 0;
  const [display, setDisplay] = useState(reduced ? target : 0);

  useEffect(() => {
    if (reduced) return undefined;
    let frame;
    const origin = display;
    const started = performance.now();
    const update = (time) => {
      const progress = Math.min((time - started) / 220, 1);
      setDisplay(origin + ((target - origin) * (1 - ((1 - progress) ** 3))));
      if (progress < 1) frame = requestAnimationFrame(update);
    };
    frame = requestAnimationFrame(update);
    return () => cancelAnimationFrame(frame);
  // This intentionally starts from the rendered value when live telemetry changes.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, reduced]);

  return <>{prefix}{Math.round(reduced ? target : display).toLocaleString()}{suffix}</>;
}

export function AnimatedBorder({ children, className = '' }) {
  const reduced = useReducedMotion();
  return <div className={`animated-border ${className}`}><motion.span aria-hidden="true" className="animated-border-runner" initial={false} animate={reduced ? { x: '0%' } : { x: ['-105%', '205%'] }} transition={{ duration: 2.8, ease: 'linear', repeat: Infinity, repeatDelay: 3.5 }} />{children}</div>;
}
```

## frontend/src/redesign/maintenance-planning.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/maintenance-planning.css`

```css
.maintenance-planner{display:grid;gap:14px}.maintenance-planner-head{display:flex;align-items:end;justify-content:space-between;gap:12px}.maintenance-planner-title{margin-top:4px!important;font-size:1.35rem!important;font-weight:820!important;letter-spacing:-.045em}.maintenance-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.maintenance-kpis .metric,.maintenance-board,.maintenance-inspector,.maintenance-bottom{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:14px!important;box-shadow:none!important}.maintenance-kpis .metric{padding:13px}.maintenance-layout{display:grid;grid-template-columns:minmax(550px,1fr) 292px;gap:12px}.maintenance-board{min-width:0;overflow:hidden}.maintenance-board-head{display:flex;justify-content:space-between;align-items:center;padding:10px 13px;border-bottom:1px solid rgba(148,163,184,.1)}.maintenance-view-tabs{display:flex;gap:2px}.maintenance-view-tabs .MuiButton-root{min-width:0;padding:7px 9px!important;color:#8496ad!important;font-size:.62rem!important;text-transform:capitalize!important}.maintenance-view-tabs .MuiButton-root.active{color:#d7e8ff!important;border-bottom:2px solid #67a5ff;border-radius:0}.maintenance-board-head>.MuiButton-root{color:#9dbff2;font-size:.62rem!important;text-transform:none}.maintenance-kanban{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:9px;min-height:445px;padding:11px;overflow:auto}.maintenance-column{display:grid;align-content:start;gap:8px;min-width:155px}.maintenance-column>p{display:flex;justify-content:space-between;padding:2px 3px;color:#9fb0c6;font-size:.65rem;font-weight:800}.maintenance-column>p b{color:#71849d;font:600 .58rem 'DM Mono',monospace}.work-order{display:grid;gap:8px;padding:10px;border:1px solid rgba(148,163,184,.11);border-radius:10px;background:#0c1016;color:#d9e4f2;cursor:grab;text-align:left}.work-order:hover,.work-order.selected{border-color:rgba(101,163,255,.45);background:#111b28}.work-order>div:first-child,.work-order>div:last-of-type{display:flex;align-items:center;justify-content:space-between}.work-order>div:first-child svg{color:#71849a}.priority{padding:3px 5px;border-radius:5px;background:rgba(236,122,111,.13);color:#f0a096;font:800 .53rem 'DM Mono',monospace}.priority.p2{background:rgba(239,172,75,.12);color:#eec16f}.priority.p3{background:rgba(75,202,156,.1);color:#84d9b7}.work-order>b{font-size:.68rem;line-height:1.35}.work-order>p{color:#8799b0;font-size:.59rem}.work-order>div:last-of-type span{color:#9caec5;font:600 .54rem 'DM Mono',monospace}.work-order>i{height:3px;border-radius:99px;background:rgba(148,163,184,.15);overflow:hidden}.work-order>i span{display:block;height:100%;border-radius:99px;background:#62a1ff;transition:width .4s ease}.maintenance-inspector{display:grid;align-content:start;gap:13px;padding:15px!important}.maintenance-work-title{margin-top:-8px!important;font-size:1.08rem!important;font-weight:830!important;letter-spacing:-.04em}.maintenance-inspector>.state{justify-self:start}.maintenance-facts{display:grid;grid-template-columns:1fr 1fr;gap:7px}.maintenance-facts .metric{padding:8px;border-bottom:1px solid rgba(148,163,184,.1)}.maintenance-ai,.maintenance-checklist{padding:10px;border-radius:9px;background:#0c1016}.maintenance-ai{border-left:2px solid #639fff;background:rgba(79,140,255,.06)}.maintenance-ai>p:last-child{margin-top:6px;color:#b8c8da;font-size:.65rem;line-height:1.45}.maintenance-checklist{display:grid;gap:8px}.maintenance-checklist>p:not(:first-child){display:flex;align-items:center;gap:5px;color:#a1b1c4;font-size:.62rem}.maintenance-checklist i{width:6px;height:6px;border-radius:50%;background:#f1aa5d}.maintenance-checklist p:last-child i{background:#4dce9e}.maintenance-checklist b{margin-left:auto;color:#d6e1ee;font-size:.58rem}.maintenance-inspector>.MuiButton-root{font-size:.68rem!important}.maintenance-bottom{display:grid;grid-template-columns:1fr 1fr;gap:25px;padding:14px!important}.maintenance-bottom>div{display:grid;gap:8px}.maintenance-bottom>div>p:not(:first-child){display:flex;gap:6px;color:#9fafc3;font-size:.64rem}.maintenance-bottom b{margin-left:auto;color:#d4dfec;font-size:.59rem}.maintenance-schedule-grid{position:relative;min-height:445px;padding:14px;background:linear-gradient(rgba(148,163,184,.06) 1px,transparent 1px);background-size:100% 62px}.maintenance-days{display:grid;grid-template-columns:repeat(7,1fr);gap:5px}.maintenance-days p{padding:6px;color:#8da0b9;font-size:.6rem;font-weight:800;text-align:center}.schedule-work{display:grid;grid-column:var(--start)/span var(--span);gap:4px;margin:15px 4px 0;padding:9px;border:1px solid rgba(95,157,255,.32);border-radius:8px;background:rgba(79,140,255,.12);color:#dbe9fb;cursor:pointer;text-align:left}.schedule-work:nth-of-type(3n){border-color:rgba(239,171,79,.35);background:rgba(239,171,79,.09)}.schedule-work b{font-size:.65rem}.schedule-work span{color:#9eb5d2;font-size:.56rem}@media(max-width:1050px){.maintenance-layout{grid-template-columns:1fr}.maintenance-inspector{grid-template-columns:repeat(3,1fr)}.maintenance-inspector>.product-kicker,.maintenance-work-title,.maintenance-inspector>.state{grid-column:1/-1}.maintenance-ai{grid-column:span 2}}@media(max-width:720px){.maintenance-kpis{grid-template-columns:1fr 1fr}.maintenance-planner-head{align-items:start;flex-direction:column}.maintenance-bottom{grid-template-columns:1fr}.maintenance-inspector{grid-template-columns:1fr}.maintenance-ai{grid-column:auto}}@media(max-width:480px){.maintenance-kpis{grid-template-columns:1fr}.maintenance-view-tabs{overflow:auto;max-width:240px}.maintenance-board-head{gap:5px}.maintenance-kanban{min-height:380px}}
```

## frontend/src/redesign/mission-control-os.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/mission-control-os.css`

```css
.mission-os{display:grid;gap:13px}.mission-situation{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:17px 19px!important;border:1px solid rgba(76,205,156,.25)!important;border-radius:14px!important;background:linear-gradient(100deg,rgba(61,201,153,.08),rgba(17,21,28,.96) 45%)!important;box-shadow:none!important}.mission-situation.attention{border-color:rgba(240,166,88,.36)!important;background:linear-gradient(100deg,rgba(240,156,88,.1),rgba(17,21,28,.96) 45%)!important}.mission-situation-title{margin:5px 0!important;font-size:1.12rem!important;font-weight:830!important;letter-spacing:-.04em}.mission-situation>div:first-child>p:last-child{color:#a9bacd;font-size:.69rem}.mission-situation-actions{display:flex;align-items:center;gap:13px}.mission-situation-actions>p{display:flex;align-items:center;gap:6px;color:#8ccfb4;font:700 .58rem 'DM Mono',monospace}.mission-situation-actions i,.mission-live i{width:6px;height:6px;border-radius:50%;background:#4ed09f;box-shadow:0 0 0 4px rgba(78,208,159,.1);animation:mission-live 1.6s ease infinite}.mission-situation-actions .MuiButton-root{font-size:.67rem!important}.mission-command-grid{display:grid;grid-template-columns:1.05fr .95fr 235px;gap:12px}.mission-twin,.mission-telemetry-panel,.mission-decisions,.mission-feed,.mission-agents,.mission-risks,.mission-shift,.mission-executive{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:14px!important;box-shadow:none!important}.mission-twin,.mission-telemetry-panel,.mission-decisions{min-height:310px;padding:15px!important}.mission-panel-head{display:flex;justify-content:space-between;align-items:start;gap:8px}.mission-panel-head>div>p:last-child{margin-top:4px;color:#cad5e2;font-size:.74rem}.mission-panel-head .MuiButton-root{color:#9fc5fb;font-size:.6rem!important;text-transform:none}.mission-twin-map{position:relative;height:205px;margin-top:12px;overflow:hidden;border:1px solid rgba(148,163,184,.1);border-radius:11px;background:radial-gradient(circle at 50% 50%,rgba(79,140,255,.15),transparent 34%),#0c1016}.mission-twin-map svg{position:absolute;inset:0;width:100%;height:100%}.mission-twin-map path{fill:none;stroke:rgba(117,169,247,.26);stroke-width:8;stroke-linecap:round}.mission-twin-core{position:absolute;z-index:2;left:50%;top:50%;display:grid;place-items:center;width:73px;height:73px;border:1px solid rgba(111,173,255,.52);border-radius:50%;background:#142033;transform:translate(-50%,-50%);box-shadow:0 0 0 9px rgba(79,140,255,.05)}.mission-twin-core b{font-size:1.1rem;letter-spacing:-.06em}.mission-twin-core span{color:#8ea5c4;font-size:.48rem;font-weight:800}.mission-twin-node{position:absolute;z-index:3;display:flex;align-items:center;gap:4px;padding:5px 7px;border:1px solid rgba(101,164,255,.27);border-radius:7px;background:#141d2a;color:#d8e6f8;cursor:pointer}.mission-twin-node i{width:6px;height:6px;border-radius:50%;background:#4dce9e}.mission-twin-node.risk i{background:#ef9d6c}.mission-twin-node span{font-size:.56rem;font-weight:750}.mission-twin-node b{color:#9dc5ff;font:700 .55rem 'DM Mono',monospace}.mission-twin-node:nth-of-type(2){left:7%;top:21%}.mission-twin-node:nth-of-type(3){right:8%;top:20%}.mission-twin-node:nth-of-type(4){left:9%;bottom:18%}.mission-twin-node:nth-of-type(5){right:7%;bottom:19%}.mission-twin-footer{display:flex;gap:12px;margin-top:10px;overflow:auto}.mission-twin-footer p{display:flex;align-items:center;gap:4px;white-space:nowrap;color:#8194ad;font-size:.56rem}.mission-twin-footer svg{font-size:.75rem;color:#80b2fa}.mission-live{display:flex;align-items:center;gap:5px;color:#8fd6b9;font:700 .56rem 'DM Mono',monospace}.mission-chart-wrap{position:relative;margin-top:16px}.mission-chart-wrap .mini-graph{margin:0}.mission-chart-annotation{position:absolute;right:10px;top:28%;display:flex;align-items:center;gap:5px;color:#e4b16f;font-size:.52rem}.mission-chart-annotation i{width:44px;border-top:1px dashed #e4b16f}.mission-chart-legend{display:flex;gap:11px;flex-wrap:wrap;margin-top:9px}.mission-chart-legend p{display:flex;align-items:center;gap:4px;color:#8294aa;font-size:.54rem}.mission-chart-legend i{width:5px;height:5px;border-radius:50%;background:#4dce9e}.mission-chart-legend .watch{background:#f0ad5d}.mission-chart-legend .critical{background:#ec8580}.mission-chart-legend .band{background:#6aa6ff}.mission-production{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:10px}.mission-production .metric{padding-top:7px;border-top:1px solid rgba(148,163,184,.1)}.mission-decisions{display:grid;align-content:start}.mission-decision-count{margin:10px 0!important;color:#f0b072;font:700 2.3rem 'DM Mono',monospace!important;letter-spacing:-.1em}.mission-decisions>p:nth-child(3){color:#adbdce;font-size:.67rem;line-height:1.5}.mission-decisions .MuiButton-root{justify-self:start;margin-top:13px;padding:3px 0!important;color:#a5c9ff;font-size:.62rem!important;text-transform:none}.mission-lower-grid{display:grid;grid-template-columns:1.1fr .9fr .85fr .85fr;gap:12px}.mission-feed,.mission-agents,.mission-risks,.mission-shift{padding:14px!important}.mission-feed-row{display:grid;grid-template-columns:7px 1fr auto;gap:8px;align-items:start;padding:9px 0;border-bottom:1px solid rgba(148,163,184,.09)}.mission-feed-row>i{width:6px;height:6px;margin-top:5px;border-radius:50%;background:#56cfa1}.mission-feed-row>i.risk{background:#ed8d77}.mission-feed-row b{font-size:.65rem}.mission-feed-row p{margin-top:3px;color:#8395ac;font-size:.57rem;line-height:1.35}.mission-feed-row .MuiChip-root{font-size:.52rem}.mission-empty-copy{margin-top:12px!important;color:#8597ae;font-size:.63rem!important;line-height:1.45}.mission-agent-list{display:grid;gap:6px;margin-top:12px}.mission-agent-list>div{display:flex;align-items:center;gap:7px;padding:6px;border-radius:7px;background:#0c1016}.mission-agent-list>div>span{display:grid;place-items:center;width:22px;height:22px;border-radius:6px;background:rgba(79,140,255,.14);color:#a9caff;font-size:.58rem;font-weight:800}.mission-agent-list p{display:grid;gap:2px;min-width:0;flex:1}.mission-agent-list b{font-size:.61rem}.mission-agent-list small{overflow:hidden;color:#8193a9;font-size:.52rem;white-space:nowrap;text-overflow:ellipsis}.mission-agent-list>div>i{width:6px;height:6px;border-radius:50%;background:#596a80}.mission-agent-list>div>i.active{background:#4bd09e;animation:mission-live 1.6s ease infinite}.mission-risks>div:not(:first-child){display:grid;grid-template-columns:1fr 52px 23px;gap:6px;align-items:center;padding:9px 0;border-bottom:1px solid rgba(148,163,184,.09)}.mission-risks p{display:grid;gap:2px}.mission-risks p b{font-size:.61rem}.mission-risks small{color:#8193aa;font-size:.52rem}.mission-risks>div>div{height:4px;border-radius:99px;background:rgba(148,163,184,.14);overflow:hidden}.mission-risks>div>div span{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#eaaa61,#ec7776)}.mission-risks>div>b{color:#f0ae76;font:700 .57rem 'DM Mono',monospace}.mission-shift{display:grid;align-content:start;gap:9px}.mission-shift-title{margin-top:-8px!important;font-size:.92rem!important;font-weight:800!important}.mission-shift>p:not(:first-child){display:flex;align-items:center;gap:6px;color:#a0b0c2;font-size:.6rem}.mission-shift b{margin-left:auto;color:#d7e2ee;font-size:.55rem}.mission-shift .MuiButton-root{justify-self:start;padding:2px 0!important;color:#a2c8ff;font-size:.6rem!important;text-transform:none}.mission-executive{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px!important;background:linear-gradient(100deg,rgba(79,140,255,.1),#10151c 45%)!important}.mission-executive-title{max-width:570px;margin-top:5px!important;font-family:Georgia,serif!important;font-size:1.05rem!important;line-height:1.35!important}.mission-executive>div:nth-child(2){display:grid;grid-template-columns:repeat(3,1fr);gap:15px;min-width:360px}.mission-executive .metric{padding-left:10px;border-left:1px solid rgba(148,163,184,.13)}.mission-executive .MuiButton-root{font-size:.64rem!important;text-transform:none}@keyframes mission-live{50%{opacity:.35;box-shadow:0 0 0 7px rgba(78,208,159,.04)}}@media(max-width:1200px){.mission-command-grid{grid-template-columns:1fr 1fr}.mission-decisions{grid-column:1/-1;min-height:unset}.mission-lower-grid{grid-template-columns:1fr 1fr}.mission-executive>div:nth-child(2){min-width:300px}}@media(max-width:760px){.mission-situation,.mission-executive{align-items:start;flex-direction:column}.mission-command-grid,.mission-lower-grid{grid-template-columns:1fr}.mission-decisions{grid-column:auto}.mission-executive>div:nth-child(2){width:100%;min-width:0}.mission-situation-actions{width:100%;justify-content:space-between}}@media(max-width:480px){.mission-production,.mission-executive>div:nth-child(2){grid-template-columns:1fr}.mission-twin-footer{gap:8px}.mission-situation{padding:14px!important}}
```

## frontend/src/redesign/mission-control.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/mission-control.css`

```css
.situation-banner{display:block;padding:14px 17px!important;margin-bottom:14px;border:1px solid rgba(72,203,154,.24)!important;border-radius:14px!important;background:linear-gradient(90deg,rgba(51,191,139,.09),rgba(16,21,28,.96) 42%)!important;box-shadow:none!important}.situation-banner.attention{border-color:rgba(242,169,73,.34)!important;background:linear-gradient(90deg,rgba(242,169,73,.11),rgba(16,21,28,.96) 42%)!important}.situation-banner>div>div:first-child>i{width:8px;height:8px;border-radius:50%;background:#42cc9b;box-shadow:0 0 0 5px rgba(66,204,155,.08)}.situation-banner.attention>div>div:first-child>i{background:#f2a949;box-shadow:0 0 0 5px rgba(242,169,73,.1)}.situation-banner .MuiTypography-caption{display:block;margin-top:4px;color:#91a2b8}.situation-metric{color:#91a2b8;font-size:.66rem;white-space:nowrap}.situation-metric b{color:#d9e5f4;font:700 .85rem "DM Mono",monospace}@media(max-width:600px){.situation-banner .MuiStack-root:last-child{justify-content:space-between;flex-wrap:wrap}}
```

## frontend/src/redesign/motion.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/motion.jsx`

```javascript
import { forwardRef, useEffect, useState } from 'react';
import { motion, useReducedMotion } from 'motion/react';

/** Part 8 — page transition is 120ms fade only (no layout bounce). */
const enter = { duration: 0.12, ease: 'easeOut' };

export function PageMotion({ children, pageKey }) {
  const reduced = useReducedMotion();
  return <motion.div key={pageKey} initial={reduced ? false : { opacity: 0 }} animate={{ opacity: 1 }} transition={enter}>{children}</motion.div>;
}

export function Reveal({ children, delay = 0, className }) {
  const reduced = useReducedMotion();
  return <motion.div className={className} initial={reduced ? false : { opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.15 }} transition={{ ...enter, delay }}>{children}</motion.div>;
}

export function AnimatedNumber({ value, prefix = '', suffix = '' }) {
  const reduced = useReducedMotion();
  const number = Number(value) || 0;
  const [shown, setShown] = useState(reduced ? number : 0);

  useEffect(() => {
    if (reduced) return undefined;
    let frame;
    const initial = shown;
    const start = performance.now();
    const duration = 220;
    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - (1 - progress) ** 3;
      setShown(initial + ((number - initial) * eased));
      if (progress < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  // `shown` deliberately does not restart the count while an animation runs.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [number, reduced]);

  return <>{prefix}{Math.round(reduced ? number : shown).toLocaleString()}{suffix}</>;
}

export const DialogMotion = forwardRef(function DialogMotion(props, ref) {
  const { children, in: open, onEnter, onExited, ...rest } = props;
  const reduced = useReducedMotion();
  useEffect(() => { if (open) onEnter?.(); else onExited?.(); }, [open, onEnter, onExited]);
  return <motion.div ref={ref} {...rest} initial={false} animate={open ? { opacity: 1, scale: 1 } : { opacity: 0, scale: reduced ? 1 : 0.98 }} transition={{ duration: reduced ? 0 : 0.18, ease: [0.16, 1, 0.3, 1] }}>{children}</motion.div>;
});
```

## frontend/src/redesign/operations-v2.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/operations-v2.css`

```css
.forecast-v2,.reports-v2{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:16px}.forecast-hero,.forecast-queue,.report-preview-v2{padding:22px!important;background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:15px!important;box-shadow:none!important}.forecast-canvas{position:relative;overflow:hidden;height:250px;margin:18px 0;border:1px solid rgba(148,163,184,.12);border-radius:12px;background:#0c1016}.forecast-canvas .mini-graph{position:absolute;z-index:2;inset:44px 0 0;margin:0}.forecast-risk-zone{position:absolute;left:0;right:0;z-index:1;height:32%;padding:7px 10px;color:#7c8ca2;font-size:.58rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.forecast-risk-zone.critical{bottom:0;background:rgba(237,103,103,.07);border-top:1px dashed rgba(237,103,103,.25)}.forecast-risk-zone.watch{bottom:32%;background:rgba(242,169,73,.055);border-top:1px dashed rgba(242,169,73,.22)}.forecast-markers{position:absolute;z-index:3;bottom:22px;left:6%;right:5%;display:flex;justify-content:space-between}.forecast-markers i{position:relative;width:1px;background:rgba(163,193,232,.35)}.forecast-markers span{position:absolute;top:100%;left:50%;margin-top:4px;color:#8292a9;font:500 .56rem "DM Mono",monospace;transform:translateX(-50%)}.forecast-confidence{display:grid;grid-template-columns:110px 1fr 34px;gap:10px;align-items:center;color:#93a2b8;font-size:.68rem}.forecast-confidence>i{height:5px;border-radius:9px;background:#679fff}.forecast-queue{display:grid;align-content:start;gap:5px}.forecast-queue>button{display:grid;grid-template-columns:24px 1fr 74px;gap:8px;align-items:center;padding:10px;border:1px solid transparent;border-radius:9px;background:transparent;color:#e4edf8;text-align:left;cursor:pointer}.forecast-queue>button:hover,.forecast-queue>button.selected{border-color:rgba(94,153,255,.28);background:rgba(79,140,255,.08)}.forecast-queue>button>p:first-child{color:#8495ac;font:500 .66rem "DM Mono",monospace}.planning-workspace{display:grid;gap:18px}.planning-lanes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.planning-lane{display:grid;align-content:start;gap:9px;min-height:330px;padding:14px;border:1px solid rgba(148,163,184,.13);border-radius:14px;background:#0d1117}.planning-order{display:grid;gap:8px;padding:12px;border:1px solid rgba(148,163,184,.12);border-radius:10px;background:#121923}.planning-order>p:nth-of-type(1){font-size:.78rem}.planning-expand{justify-content:flex-start!important;min-height:21px!important;padding:0!important;color:#96acd0!important;font-size:.62rem!important;text-transform:none!important}.planning-detail{display:grid;gap:5px;padding-top:8px;border-top:1px solid rgba(148,163,184,.11);color:#aebdce;font-size:.66rem}.planning-empty{padding:18px;border:1px dashed rgba(148,163,184,.18);border-radius:9px;color:#7d8da3;font-size:.68rem;text-align:center}.reports-v2{grid-template-columns:minmax(0,1fr) minmax(360px,.9fr)}.report-card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.report-card-v2{display:grid;align-content:start;gap:10px;min-height:190px;padding:16px;border:1px solid rgba(148,163,184,.13);border-radius:13px;background:#10151c;cursor:pointer}.report-card-v2:hover,.report-card-v2.selected{border-color:rgba(111,162,255,.34);background:#121a25}.report-card-v2>p:nth-of-type(1){font-size:.9rem;line-height:1.3}.report-card-v2>div:last-child{display:flex;align-items:center;justify-content:space-between;margin-top:auto}.report-card-v2>div:last-child>p{color:#8495ac;font-size:.59rem}.report-preview-v2{display:grid;align-content:start;gap:16px}.report-loading-lines{display:grid;gap:7px;padding:14px;border-radius:10px;background:#0c1016}.report-loading-lines i{display:block;height:6px;border-radius:99px;background:linear-gradient(90deg,#5f98f5,#9a81f5)}.report-summary-v2{color:#b8c5d6;line-height:1.65}.report-chart-v2{padding:12px;border:1px solid rgba(148,163,184,.1);border-radius:11px;background:#0c1016}.report-preview-v2 .MuiButton-root{text-transform:none!important}@media(max-width:900px){.forecast-v2,.reports-v2{grid-template-columns:1fr}.planning-lanes{grid-template-columns:1fr}.forecast-queue{grid-template-columns:repeat(2,minmax(0,1fr))}.forecast-queue>.product-kicker{grid-column:1/-1}.report-card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:600px){.forecast-queue,.report-card-grid{grid-template-columns:1fr}.forecast-confidence{grid-template-columns:1fr}.forecast-confidence>i{width:100%}}
```

## frontend/src/redesign/polish.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/polish.css`

```css
/* Global interaction contract: every movement reports state, focus, or progress. */
:root{--rig-ease:cubic-bezier(.2,.8,.2,1)}.product-app button,.os-app button,.rig-card,[role=button]{transition:transform .16s var(--rig-ease),background-color .16s ease,border-color .16s ease,box-shadow .16s ease!important}.product-app button:not(:disabled):hover,.os-app button:not(:disabled):hover{transform:translateY(-1px)}.product-app button:active,.os-app button:active{transform:translateY(0) scale(.985)}.MuiButtonBase-root:focus-visible{outline:2px solid #82b1ff!important;outline-offset:2px!important}.product-stage main,.os-stage main{scroll-behavior:smooth}.MuiDialog-container .MuiPaper-root,.MuiDrawer-paper{animation:rig-overlay-in .2s var(--rig-ease)}.mini-graph polyline{stroke-dasharray:1200;stroke-dashoffset:1200;animation:rig-draw-line 1.1s var(--rig-ease) forwards}.mini-graph line{animation:rig-grid-in .4s ease both}.mini-graph line:nth-child(2){animation-delay:.06s}.mini-graph line:nth-child(3){animation-delay:.12s}.health i,.confidence i{transition:width .65s var(--rig-ease)}.product-dialog .MuiOutlinedInput-root:focus-within,.rig-search .MuiOutlinedInput-root:focus-within{box-shadow:0 0 0 3px rgba(100,160,255,.11)}.product-page{animation:rig-page-in .28s var(--rig-ease)}.product-feature,.product-map,.product-section,.product-collection,.pulse-card{transition:border-color .18s ease,transform .18s var(--rig-ease),background-color .18s ease}.product-feature:hover,.product-map:hover,.product-section:hover,.product-collection:hover,.pulse-card:hover{border-color:rgba(132,177,242,.24)!important}.product-empty-state,.twin-empty,.mission-portfolio-empty{background-image:linear-gradient(90deg,transparent,rgba(93,156,255,.035),transparent);background-size:200% 100%;animation:rig-scan 4s linear infinite}@keyframes rig-page-in{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}@keyframes rig-overlay-in{from{opacity:0;transform:translateY(6px) scale(.99)}to{opacity:1;transform:translateY(0) scale(1)}}@keyframes rig-draw-line{to{stroke-dashoffset:0}}@keyframes rig-grid-in{from{opacity:0}to{opacity:1}}@keyframes rig-scan{from{background-position:160% 0}to{background-position:-80% 0}}@media(prefers-reduced-motion:reduce){.MuiDialog-container .MuiPaper-root,.MuiDrawer-paper,.product-page,.mini-graph polyline,.mini-graph line,.product-empty-state,.twin-empty,.mission-portfolio-empty{animation:none!important}.product-app button,.os-app button,.rig-card,[role=button]{transition:none!important}}
```

## frontend/src/redesign/product.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/product.css`

```css
.product-app{min-height:100vh;background:#090b0f;color:#f8fafc;display:flex}.product-nav{position:fixed;width:68px;inset:0 auto 0 0;z-index:3;background:#0e1014;border-right:1px solid rgba(255,255,255,.08);padding:16px 10px;display:flex;flex-direction:column;transition:width .22s ease;overflow:hidden}.product-nav:hover{width:228px}.product-logo{height:42px;display:flex;align-items:center;gap:10px;margin-bottom:24px;white-space:nowrap}.product-logo>div{width:30px;height:30px;display:grid;place-items:center;background:#f8fafc;color:#111418;border-radius:9px;font-weight:850}.product-logo p{font-weight:800;letter-spacing:-.05em;opacity:0;transition:opacity .12s}.product-nav:hover .product-logo p{opacity:1}.product-nav-stack{gap:5px}.product-nav a{height:42px;padding:0 13px;border-radius:10px;display:flex;align-items:center;gap:14px;color:#94a3b8;text-decoration:none;white-space:nowrap;font-weight:650;font-size:.88rem}.product-nav a:hover{background:#171b21;color:#f8fafc}.product-nav a.active{background:rgba(79,140,255,.14);color:#f8fafc}.product-nav a.active:before{content:'';position:absolute;left:0;width:3px;height:19px;border-radius:99px;background:#4f8cff}.product-nav a span{opacity:0;transition:opacity .12s}.product-nav:hover a span{opacity:1}.product-settings{margin-top:auto}.product-stage{width:calc(100% - 68px);margin-left:68px}.product-top{height:70px;padding:0 42px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:space-between}.product-search{height:38px;width:360px;padding:0 12px;display:flex;align-items:center;gap:10px;background:#151922;border-radius:10px;color:#94a3b8}.product-search input{width:100%;border:0;outline:0;background:transparent;color:#f8fafc;font:inherit}.product-search kbd{font-size:.68rem;color:#94a3b8}.product-live{padding:7px 11px;border-radius:999px;font-size:.67rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em}.product-live i{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:6px}.product-live.ok{color:#22c55e;background:rgba(34,197,94,.12)}.product-live.ok i{background:#22c55e}.product-live.warn{color:#f59e0b;background:rgba(245,158,11,.12)}.product-live.warn i{background:#f59e0b}.product-stage main{max-width:1520px;margin:auto;padding:28px 52px 64px}.product-crumb{display:flex;justify-content:space-between;margin-bottom:20px}.product-crumb p{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#94a3b8}.product-page>.product-hero{max-width:820px;margin-bottom:48px}.product-kicker{font-size:.68rem!important;font-weight:800!important;color:#94a3b8;letter-spacing:.14em;text-transform:uppercase}.product-hero h1{font-size:clamp(3.1rem,6vw,6rem);line-height:.91;letter-spacing:-.075em;margin:11px 0 18px;font-weight:800}.product-hero>p:last-child{color:#94a3b8;line-height:1.7;max-width:650px}.product-stats{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.08);margin-bottom:36px}.product-stats>div{padding:22px 26px;border-right:1px solid rgba(255,255,255,.08)}.product-stats p:first-child{color:#94a3b8;font-size:.7rem;text-transform:uppercase;font-weight:800;letter-spacing:.1em}.product-stats p:last-child{font-size:2.5rem;font-weight:800;letter-spacing:-.07em;margin-top:7px}.product-home-grid{display:grid;grid-template-columns:.85fr 1.5fr;gap:22px}.product-feature,.product-map,.product-section,.product-collection{padding:28px!important;background:#111418!important;border:1px solid rgba(255,255,255,.08);box-shadow:none!important;border-radius:16px!important}.product-feature{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:16px}.product-feature-title{font-size:2rem!important;line-height:1.03!important;font-weight:780!important;letter-spacing:-.05em}.product-map-canvas{height:330px;margin-top:20px;position:relative;border-radius:12px;background:#0c0f14;overflow:hidden}.product-map-canvas:before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:40px 40px}.product-node{position:absolute;z-index:1;font-size:.7rem;color:#cbd5e1;transform:translate(-50%,-50%)}.product-node i{display:block;width:14px;height:14px;margin:0 auto 7px;border-radius:50%;background:#22c55e;box-shadow:0 0 0 5px rgba(34,197,94,.1)}.product-node.risk i{background:#ef4444;box-shadow:0 0 0 5px rgba(239,68,68,.1)}.product-section{margin-top:24px}.product-section-title{font-size:1.45rem!important;font-weight:750!important;margin-bottom:16px!important}.product-row{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:16px 0}.product-row>p{font-size:.75rem;color:#94a3b8}.product-toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;color:#94a3b8}.product-empty{min-height:260px;display:grid;place-items:center;color:#94a3b8}@media(max-width:900px){.product-top{padding:0 22px}.product-search{width:240px}.product-stage main{padding:25px 24px}.product-home-grid{grid-template-columns:1fr}.product-stats{grid-template-columns:repeat(2,1fr)}.product-stats>div:nth-child(2){border-right:0}}@media(max-width:580px){.product-top{padding:0 14px}.product-search{width:42px;padding:0 11px}.product-search input,.product-search kbd,.product-live{display:none}.product-stage main{padding:20px 16px}.product-stats{grid-template-columns:1fr}.product-stats>div{border-right:0;border-bottom:1px solid rgba(255,255,255,.08)}}
.product-search{width:380px!important;justify-content:space-between!important;padding:0 13px!important;text-transform:none!important;font-weight:500!important}.product-dialog{background:#111418!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:16px!important}.product-command,.product-inbox{padding:18px}.product-command .MuiOutlinedInput-root{background:#171b21;border-radius:10px}.product-dialog-label{display:block;margin:20px 0 8px;color:#94a3b8;font-size:.68rem!important;font-weight:800!important;letter-spacing:.12em}.product-command-item{width:100%;justify-content:flex-start!important;padding:11px 12px!important;color:#f8fafc!important;text-transform:none!important}.product-command-item:hover,.product-command-item.is-active{background:#171b21!important}.product-dialog-empty{padding:28px 0;text-align:center;color:#94a3b8}.product-notification{padding:13px 0;border-bottom:1px solid rgba(255,255,255,.08)}.product-notification .MuiTypography-caption{display:block;margin-top:6px}.product-inbox-empty{min-height:210px;display:grid;place-content:center;gap:8px;text-align:center}.product-inbox-empty svg{justify-self:center;color:#4f8cff;font-size:30px}html[data-rigos-theme='light'] .product-app{background:#f6f7f9;color:#111827}html[data-rigos-theme='light'] .product-nav,html[data-rigos-theme='light'] .product-feature,html[data-rigos-theme='light'] .product-map,html[data-rigos-theme='light'] .product-section,html[data-rigos-theme='light'] .product-collection,html[data-rigos-theme='light'] .product-dialog{background:#fff!important;border-color:#e5e7eb!important}html[data-rigos-theme='light'] .product-top{background:rgba(255,255,255,.9);border-color:#e5e7eb}html[data-rigos-theme='light'] .product-search,html[data-rigos-theme='light'] .product-command .MuiOutlinedInput-root{background:#f1f5f9!important;color:#64748b!important}html[data-rigos-theme='light'] .product-nav a{color:#64748b}html[data-rigos-theme='light'] .product-nav a:hover{background:#f1f5f9;color:#111827}html[data-rigos-theme='light'] .product-map-canvas{background:#f8fafc}@media(max-width:580px){.product-search{width:42px!important;font-size:0!important}.product-search .MuiButton-endIcon{display:none!important}}
.product-settings{justify-content:flex-start!important;margin-top:auto!important;color:#94a3b8!important;text-transform:none!important;white-space:nowrap!important}.assistant-panel{padding:22px}.assistant-history{min-height:300px;max-height:390px;overflow:auto;margin:20px 0;padding-right:4px}.assistant-empty{min-height:280px;display:grid;place-content:center;gap:9px;text-align:center}.assistant-empty svg{justify-self:center;color:#4f8cff;font-size:34px}.assistant-message{max-width:88%;padding:11px 13px;border-radius:12px;white-space:pre-wrap}.assistant-message.operator{margin-left:auto;background:#4f8cff;color:#fff}.assistant-message.assistant{background:#171b21}.assistant-panel .MuiOutlinedInput-root{background:#171b21;border-radius:10px}html[data-rigos-theme='light'] .assistant-message.assistant,html[data-rigos-theme='light'] .assistant-panel .MuiOutlinedInput-root{background:#f1f5f9}
.product-revenue{padding:28px!important}.product-chart-title{margin-top:6px!important;font-size:1.2rem!important;font-weight:750!important;letter-spacing:-.035em}.product-chart-number{font-size:1.7rem!important;font-weight:800!important;letter-spacing:-.06em}.product-chart{height:220px;margin:20px 0 10px;border-radius:12px;background:#0c0f14;overflow:hidden}.product-chart svg{width:100%;height:100%}.facility-layout{display:grid;grid-template-columns:1.05fr .95fr;gap:22px}.facility-toolbar{justify-content:flex-start!important;gap:10px}.facility-toolbar .MuiOutlinedInput-root{background:#111418}.product-map-caption{position:absolute;left:16px;bottom:14px;color:#94a3b8;font-size:.75rem!important}html[data-rigos-theme='light'] .product-chart,html[data-rigos-theme='light'] .facility-toolbar .MuiOutlinedInput-root{background:#f8fafc}@media(max-width:900px){.facility-layout{grid-template-columns:1fr}}
.product-stage main{max-width:1440px!important;padding:34px 56px 72px!important}.product-page>.product-hero{max-width:900px!important;margin-bottom:52px!important}.product-home-grid{grid-template-columns:minmax(330px,.82fr) minmax(560px,1.55fr)!important}.product-feature,.product-map{min-height:330px}.product-feature{padding:32px!important}.product-summary-signal{display:flex;align-items:center;gap:7px;margin-top:2px;color:#94a3b8}.product-summary-signal i{width:7px;height:7px;border-radius:50%;background:#22c55e}.product-summary-signal i.risk{background:#ef4444}.product-revenue{padding:30px!important}.product-chart{height:205px!important;background:linear-gradient(180deg,#0c0f14,rgba(12,15,20,.68))!important}.product-chart svg line{vector-effect:non-scaling-stroke}.product-section{padding:30px!important}.product-row{padding:18px 0!important}.product-row>div:first-child{min-width:0}.product-row .MuiTypography-body2{max-width:850px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}@media(max-width:900px){.product-stage main{padding:28px 28px 60px!important}.product-home-grid{grid-template-columns:1fr!important}.product-feature,.product-map{min-height:unset}}@media(max-width:580px){.product-stage main{padding:22px 16px 50px!important}.product-row .MuiTypography-body2{white-space:normal}.product-feature{padding:24px!important}}
.product-decision{padding:28px!important;margin-bottom:24px;background:#111418!important;border:1px solid rgba(79,140,255,.28)!important;border-radius:16px!important;box-shadow:none!important}html[data-rigos-theme='light'] .product-decision{background:#fff!important;border-color:#bfdbfe!important}
.product-stage main{max-width:none!important;width:calc(100% - 168px)!important;margin-left:84px!important;margin-right:0!important;padding:42px 0 80px!important}.product-page{max-width:1380px}.product-crumb{margin-bottom:28px!important}.product-crumb p,.product-kicker,.product-dialog-label{font-size:.72rem!important;letter-spacing:.13em!important}.product-hero h1{font-size:clamp(3.7rem,5vw,6.4rem)!important}.product-hero>p:last-child{font-size:1.05rem!important}.product-stats{margin-bottom:42px!important}.product-stats>div{padding:26px 30px!important}.product-stats p:first-child{font-size:.72rem!important}.product-stats p:last-child{font-size:2.7rem!important}.product-home-grid{gap:26px!important}.product-feature,.product-map{min-height:348px!important;border-radius:18px!important}.product-feature-title{font-size:2.25rem!important}.product-summary-signal{margin-top:6px!important}.product-chart-head{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:start}.product-chart-head>div:last-child{text-align:right}.product-chart-number{font-size:2rem!important;line-height:1!important}.product-chart-caption,.product-chart-footer{font-size:.74rem;color:#94a3b8}.product-chart{height:220px!important;margin-top:24px!important}.product-chart-footer{display:flex;justify-content:space-between;gap:20px;margin-top:10px}.product-section{margin-top:28px!important;border-radius:18px!important}.product-section-title{margin-bottom:0!important;font-size:1.65rem!important}.product-section-meta{font-size:.78rem!important;color:#94a3b8}.product-row{padding:20px 0!important}.product-row .MuiTypography-root:first-child{font-size:.95rem}.product-nav{width:76px!important}.product-stage{width:calc(100% - 76px)!important;margin-left:76px!important}.product-nav:hover{width:244px!important}.product-nav a{height:46px!important}.product-logo{margin-bottom:32px!important}.product-top{height:76px!important;padding:0 36px!important}@media(max-width:1050px){.product-stage main{width:auto!important;margin:0 36px!important;padding:34px 0 64px!important}.product-page{max-width:none}.product-hero h1{font-size:clamp(3.2rem,7vw,5rem)!important}}@media(max-width:700px){.product-stage main{margin:0 20px!important}.product-hero h1{font-size:3.2rem!important}.product-chart-footer{flex-direction:column;gap:4px}.product-home-grid{gap:16px!important}}

/* Route-specific operational workspaces: data is grouped by decisions, not raw records. */
.product-toolbar-title,.product-panel-title{font-size:1.28rem!important;font-weight:780!important;letter-spacing:-.035em}.product-toolbar>div>p:last-child{margin-top:5px;color:#94a3b8}.asset-workspace,.incident-workspace,.investigation-workspace,.reports-workspace{display:grid;grid-template-columns:minmax(330px,.78fr) minmax(500px,1.42fr);gap:24px;align-items:start}.asset-list,.incident-list,.report-index{padding:12px!important}.asset-row,.incident-row,.report-index-item,.forecast-row{width:100%;display:flex!important;justify-content:space-between!important;align-items:center!important;text-align:left!important;text-transform:none!important;color:#f8fafc!important;padding:18px!important;border-radius:13px!important}.asset-row:hover,.incident-row:hover,.report-index-item:hover,.forecast-row:hover{background:#171b21!important}.asset-row.selected,.incident-row.selected,.report-index-item.selected,.forecast-row.selected{background:rgba(79,140,255,.13)!important;box-shadow:inset 3px 0 #4f8cff}.asset-row>div:last-child{text-align:right;min-width:88px}.health{display:flex;align-items:center;justify-content:flex-end;gap:9px}.health>div{height:6px;width:64px;background:#272d37;border-radius:99px;overflow:hidden}.health i{display:block;height:100%;background:#22c55e;border-radius:inherit}.health:has(i[style^="width: 0"] ) i,.health:has(i[style^="width: 1"] ) i,.health:has(i[style^="width: 2"] ) i,.health:has(i[style^="width: 3"] ) i,.health:has(i[style^="width: 4"] ) i,.health:has(i[style^="width: 5"] ) i{background:#ef4444}.health>p{font-size:.75rem!important;font-weight:800!important}.health.large{margin:22px 0;justify-content:flex-start}.health.large>div{width:200px;height:9px}.asset-brief,.incident-detail,.investigation-context,.reasoning-panel,.forecast-focus,.forecast-chart,.report-reader{background:#111418!important;border:1px solid rgba(255,255,255,.08)!important;box-shadow:none!important;border-radius:18px!important;padding:30px!important}.asset-brief>.MuiDivider-root,.incident-detail>.MuiDivider-root,.investigation-context>.MuiDivider-root,.reasoning-panel>.MuiDivider-root,.report-reader>.MuiDivider-root{margin:24px 0}.metric{padding:14px 0;border-bottom:1px solid rgba(255,255,255,.07)}.metric:last-of-type{border-bottom:0}.metric>p:first-child{color:#94a3b8;font-size:.7rem!important;text-transform:uppercase;font-weight:800;letter-spacing:.1em}.metric>p:last-child{margin-top:5px;font-size:.94rem!important;line-height:1.5}.mini-graph{height:196px;margin-top:22px;padding:14px 0 0;background:#0c0f14;border-radius:12px;overflow:hidden}.mini-graph svg{width:100%;height:160px}.mini-graph>p{padding:0 14px;color:#94a3b8;font-size:.72rem!important}.mini-graph.empty{display:grid;place-content:center;background:#0c0f14}.mini-graph.empty>p{text-align:center}.incident-list>div:first-child,.report-index>div:first-child{padding:7px 8px 16px}.incident-list>.MuiDivider-root,.report-index>.MuiDivider-root{margin:0 8px 8px}.incident-row{gap:14px!important}.incident-row>div:first-child{display:grid;grid-template-columns:auto 1fr;column-gap:10px;align-items:center}.incident-row>div:first-child>.MuiChip-root{grid-row:span 2}.severity{font-weight:800!important;text-transform:uppercase!important;font-size:.62rem!important}.severity.critical{background:rgba(239,68,68,.16)!important;color:#fca5a5!important}.severity.high{background:rgba(245,158,11,.15)!important;color:#fcd34d!important}.severity.medium{background:rgba(79,140,255,.15)!important;color:#93c5fd!important}.state{background:#1b2430!important;color:#a5b4c7!important;font-size:.64rem!important;text-transform:capitalize!important}.incident-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:20px 0}.audit-timeline{display:grid;gap:20px;margin-top:20px}.audit-timeline>div,.reasoning-timeline>div{position:relative;display:grid;grid-template-columns:18px 1fr;gap:14px}.audit-timeline>div:not(:last-child):after,.reasoning-timeline>div:not(:last-child):after{content:'';position:absolute;left:8px;top:20px;bottom:-20px;width:1px;background:rgba(79,140,255,.28)}.audit-timeline i{width:17px;height:17px;border-radius:50%;background:#4f8cff;box-shadow:0 0 0 5px rgba(79,140,255,.13);z-index:1}.audit-timeline .MuiTypography-caption{display:block;color:#94a3b8;margin:3px 0}.investigation-context{position:sticky;top:96px}.investigation-context .MuiStack-root:last-of-type{margin:22px 0 12px}.reasoning-panel{min-height:620px}.reasoning-timeline{display:grid;gap:25px;margin:25px 0}.agent-dot{width:28px;height:28px;background:#1a2230;border-radius:50%;display:grid;place-items:center;color:#93c5fd;font-size:.72rem;font-weight:800;z-index:1}.confidence{display:flex;align-items:center;gap:8px;margin-top:10px}.confidence>div{height:5px;width:110px;background:#273141;border-radius:99px;overflow:hidden}.confidence i{height:100%;display:block;background:#4f8cff;border-radius:inherit}.maintenance-board{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.maintenance-lane{min-height:400px;padding:18px;border-radius:16px;background:#0e1116;border:1px solid rgba(255,255,255,.06)}.maintenance-lane>.product-kicker{display:block;margin:3px 3px 16px}.work-order{padding:17px!important;border-radius:13px!important;margin-bottom:12px;background:#171b21!important;border:1px solid rgba(255,255,255,.07)!important;box-shadow:none!important}.work-order>p{margin-top:15px}.work-order>.MuiStack{margin-top:12px}.priority{font-weight:800!important;font-size:.63rem!important}.priority.p1{background:rgba(239,68,68,.16)!important;color:#fca5a5!important}.priority.p2{background:rgba(245,158,11,.14)!important;color:#fcd34d!important}.lane-empty{height:160px;display:grid;place-items:center;color:#64748b;font-size:.83rem}.forecast-grid{display:grid;grid-template-columns:.7fr 1.3fr;gap:24px}.forecast-focus .health{justify-content:flex-start}.forecast-chart .mini-graph{height:250px}.forecast-chart .mini-graph svg{height:212px}.forecast-row{gap:20px!important;border-bottom:1px solid rgba(255,255,255,.07);border-radius:0!important;padding:18px 0!important}.forecast-row.selected{box-shadow:none!important;padding-left:12px!important;border-radius:10px!important}.forecast-rank{font-size:1.1rem!important;color:#64748b;min-width:32px}.forecast-row>div:nth-child(2){flex:1}.report-index-item{justify-content:flex-start!important}.report-index-item>div{display:grid;gap:4px}.report-reader{min-height:590px}.report-note{margin-top:24px;padding:20px;border-radius:13px;background:#171b21}.report-note>p:last-child{margin-top:8px;color:#cbd5e1;line-height:1.55}.product-dialog{color:#f8fafc!important}.product-dialog .MuiInputBase-input,.product-dialog .MuiInputLabel-root{color:#f8fafc!important}.product-dialog .MuiSvgIcon-root{color:inherit!important}html[data-rigos-theme='light'] .product-dialog{color:#0f172a!important}html[data-rigos-theme='light'] .product-dialog .MuiInputBase-input,html[data-rigos-theme='light'] .product-dialog .MuiInputLabel-root{color:#0f172a!important}html[data-rigos-theme='light'] .asset-row,html[data-rigos-theme='light'] .incident-row,html[data-rigos-theme='light'] .report-index-item,html[data-rigos-theme='light'] .forecast-row{color:#0f172a!important}html[data-rigos-theme='light'] .asset-row:hover,html[data-rigos-theme='light'] .incident-row:hover,html[data-rigos-theme='light'] .report-index-item:hover,html[data-rigos-theme='light'] .forecast-row:hover,html[data-rigos-theme='light'] .work-order,html[data-rigos-theme='light'] .report-note{background:#f1f5f9!important}html[data-rigos-theme='light'] .asset-brief,html[data-rigos-theme='light'] .incident-detail,html[data-rigos-theme='light'] .investigation-context,html[data-rigos-theme='light'] .reasoning-panel,html[data-rigos-theme='light'] .forecast-focus,html[data-rigos-theme='light'] .forecast-chart,html[data-rigos-theme='light'] .report-reader{background:#fff!important;border-color:#e5e7eb!important}html[data-rigos-theme='light'] .maintenance-lane,html[data-rigos-theme='light'] .mini-graph{background:#f8fafc!important}@media(max-width:1040px){.asset-workspace,.incident-workspace,.investigation-workspace,.reports-workspace,.forecast-grid{grid-template-columns:1fr}.investigation-context{position:static}.maintenance-board{grid-template-columns:1fr}.maintenance-lane{min-height:unset}.incident-metrics{grid-template-columns:1fr}.forecast-chart .mini-graph{height:205px}.forecast-chart .mini-graph svg{height:165px}}@media(max-width:650px){.asset-row,.incident-row,.forecast-row{padding:14px!important}.asset-workspace,.incident-workspace,.investigation-workspace,.reports-workspace,.forecast-grid{gap:16px}.asset-brief,.incident-detail,.investigation-context,.reasoning-panel,.forecast-focus,.forecast-chart,.report-reader{padding:22px!important}.incident-metrics{gap:4px}.product-toolbar{align-items:flex-start;gap:12px}.product-toolbar .MuiTextField-root{min-width:135px}.product-toolbar-title{font-size:1.1rem!important}}

.company-pulse{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:28px}.pulse-card{min-height:270px;padding:26px!important;background:#111418!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:18px!important;box-shadow:none!important}.donut{width:148px;height:148px;margin:20px auto 14px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--donut-color) 0 var(--donut),#252c36 var(--donut) 360deg);position:relative}.donut:after{content:'';position:absolute;inset:13px;border-radius:50%;background:#111418}.donut>div{position:relative;z-index:1;text-align:center}.donut p:first-child{font-size:1.65rem!important;font-weight:820!important;letter-spacing:-.06em}.donut p:last-child{max-width:72px;margin:2px auto 0;color:#94a3b8;font-size:.65rem!important;line-height:1.2}.pulse-copy{text-align:center;color:#94a3b8;font-size:.77rem!important}.agent-pulse{display:flex;flex-direction:column}.agent-number{font-size:2.8rem!important;font-weight:820!important;letter-spacing:-.07em}.agent-statuses{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}.agent-statuses>div{padding:9px;border-radius:9px;background:#171b21;display:grid;grid-template-columns:7px 1fr;column-gap:6px;align-items:center}.agent-statuses i{width:6px;height:6px;border-radius:50%;background:#475569}.agent-statuses i.active{background:#22c55e;box-shadow:0 0 0 4px rgba(34,197,94,.12);animation:agent-pulse 1.5s ease infinite}.agent-statuses i.done{background:#4f8cff}.agent-statuses p{font-size:.64rem!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.agent-statuses .MuiTypography-caption{grid-column:2;color:#94a3b8;font-size:.59rem!important}@keyframes agent-pulse{50%{box-shadow:0 0 0 7px rgba(34,197,94,0)}}html[data-rigos-theme='light'] .pulse-card{background:#fff!important;border-color:#e5e7eb!important}html[data-rigos-theme='light'] .donut:after{background:#fff}html[data-rigos-theme='light'] .agent-statuses>div{background:#f1f5f9}@media(max-width:1040px){.company-pulse{grid-template-columns:1fr}.pulse-card{min-height:unset}.agent-statuses{grid-template-columns:repeat(3,1fr)}}

.refinery-portfolio{margin-top:28px!important}.refinery-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:24px}.refinery-card{padding:18px;border-radius:14px;background:#0d1015;border:1px solid rgba(255,255,255,.06)}.refinery-card .health{min-width:105px}.refinery-card .mini-graph{height:108px;margin-top:13px}.refinery-card .mini-graph svg{height:80px}.refinery-card .mini-graph>p{font-size:.62rem!important}.refinery-metrics{display:flex;gap:18px;margin:16px 0 0;color:#94a3b8}.refinery-metrics p{font-size:.72rem!important}.refinery-metrics b{color:#f8fafc;font-size:1rem}@media(max-width:760px){.refinery-grid{grid-template-columns:1fr}}html[data-rigos-theme='light'] .refinery-card{background:#f8fafc;border-color:#e5e7eb}html[data-rigos-theme='light'] .refinery-metrics b{color:#0f172a}

.product-notification-dialog{max-height:min(78vh,760px)!important}.product-notification-dialog .product-inbox{padding:26px!important}.product-notification{padding:18px 0!important;display:grid;gap:8px}.product-notification>p:last-child{line-height:1.5}.notification-severity{font-size:.63rem!important;font-weight:800!important;letter-spacing:.08em;text-transform:uppercase;color:#93c5fd}.notification-severity.critical{color:#fca5a5}.notification-severity.warning{color:#fcd34d}.notification-severity.success{color:#86efac}

.maintenance-by-refinery{display:grid;gap:18px}.maintenance-refinery{padding:24px!important;background:#111418!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:17px!important;box-shadow:none!important}.maintenance-refinery>.MuiDivider-root{margin:20px 0}.maintenance-plan-row{display:grid;grid-template-columns:54px minmax(200px,1fr) 130px 130px auto;align-items:center;gap:18px;padding:16px 0;border-bottom:1px solid rgba(255,255,255,.07)}.maintenance-plan-row:last-child{border-bottom:0}.maintenance-plan-row>div:nth-child(3) p:first-child,.maintenance-plan-row>div:nth-child(4) p:first-child{font-size:.65rem!important;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8}.maintenance-plan-row>div:nth-child(3) p:last-child,.maintenance-plan-row>div:nth-child(4) p:last-child{margin-top:3px;font-size:.78rem!important}@media(max-width:920px){.maintenance-plan-row{grid-template-columns:54px 1fr auto}.maintenance-plan-row>div:nth-child(3),.maintenance-plan-row>div:nth-child(4){grid-column:2}.maintenance-plan-row>.MuiChip-root:last-child{grid-column:3;grid-row:1}}@media(max-width:600px){.maintenance-refinery{padding:18px!important}.maintenance-plan-row{gap:10px}.maintenance-plan-row>div:nth-child(3),.maintenance-plan-row>div:nth-child(4){display:none}}html[data-rigos-theme='light'] .maintenance-refinery{background:#fff!important;border-color:#e5e7eb!important}

/* The investigation is an evidence flow. A generic sensor chart obscures that
   flow and can be unrelated to the incident under review. */
.reasoning-panel>.mini-graph{display:none}

/* Compact shell alignment: the mark and system state remain intentional when
   the navigation is collapsed. */
.product-nav:not(:hover) .product-logo{justify-content:center}.product-nav:not(:hover) .product-logo>div{margin:0!important}.product-nav:not(:hover) .product-settings{width:46px!important;min-width:46px!important;padding:0!important;justify-content:center!important}.product-nav:not(:hover) .product-settings .MuiButton-startIcon{margin:0!important}.product-top .product-live{height:32px;display:flex;align-items:center;justify-content:center;white-space:nowrap}.product-top .product-live i{flex:none}

/* Interaction polish: operational surfaces respond, but never compete with live data. */
.product-nav a,.product-settings,.product-search,.product-top .MuiIconButton-root,.product-top .MuiAvatar-root,.product-dialog .MuiButton-root,.product-page .MuiButton-root,.product-page .MuiChip-root,.interactive-card,.pulse-card,.refinery-card,.maintenance-refinery,.asset-brief,.incident-detail,.investigation-context,.reasoning-panel,.forecast-focus,.forecast-chart,.report-reader,.work-order{transition:transform .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s cubic-bezier(.2,.8,.2,1),background-color .18s ease,border-color .18s ease,color .18s ease!important}
.product-top .MuiIconButton-root:hover,.product-top .MuiAvatar-root:hover{transform:translateY(-1px);background-color:rgba(79,140,255,.12)}
.product-nav a:hover,.product-settings:hover,.product-search:hover{transform:translateX(2px)}
.product-search:hover{border-color:rgba(79,140,255,.35);box-shadow:0 0 0 3px rgba(79,140,255,.07)}
.product-page .MuiButton-root:not(:disabled):hover{transform:translateY(-1px)}
.interactive-card:hover,.pulse-card:hover,.refinery-card:hover,.maintenance-refinery:hover,.asset-brief:hover,.incident-detail:hover,.investigation-context:hover,.reasoning-panel:hover,.forecast-focus:hover,.forecast-chart:hover,.report-reader:hover,.work-order:hover{transform:translateY(-2px);border-color:rgba(148,163,184,.2)!important;box-shadow:0 12px 26px rgba(0,0,0,.16)!important}
.product-dialog{transform-origin:center center}.MuiDialog-container .product-dialog{animation:rigos-dialog-in .18s cubic-bezier(.16,1,.3,1)}
.product-live i{animation:rigos-pulse 2.4s var(--rigos-ease) infinite}
.product-stats>div{position:relative;overflow:hidden}.product-stats>div:after{content:'';position:absolute;inset:auto 18px 0;height:1px;background:linear-gradient(90deg,transparent,rgba(79,140,255,.72),transparent);opacity:0;transition:opacity .18s ease}.product-stats>div:hover:after{opacity:1}
@keyframes rigos-dialog-in{from{opacity:0;transform:scale(.98)}to{opacity:1;transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.MuiDialog-container .product-dialog{animation:none}.product-live i{animation:none}}

/* Command Center: a calm, high-information mission-control surface. */
.mission-status-grid{gap:12px;border:0!important;margin-bottom:28px!important}.mission-status-grid>div{padding:0!important;border:0!important;overflow:visible!important}.mission-status-grid>div:after{display:none!important}.animated-border{position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.09);border-radius:14px;background:#111418}.animated-border-runner{position:absolute;top:0;left:0;width:34%;height:1px;background:#64748b;opacity:.8}.mission-stat{height:100%;min-height:142px}.mission-stat>div{height:100%;padding:20px 21px;display:flex;flex-direction:column}.mission-stat .product-kicker{color:#9aa6b8!important}.mission-stat-value{margin-top:16px;font-size:2.35rem!important;line-height:1!important;font-weight:820!important;letter-spacing:-.07em}.mission-stat-detail{margin-top:auto;padding-top:14px;color:#94a3b8;font-size:.74rem!important}.mission-status-dot{width:7px;height:7px;border-radius:50%;background:#64748b}.mission-stat.healthy .mission-status-dot{background:#22c55e;animation:rigos-pulse 2.2s ease infinite}.mission-stat.attention .mission-status-dot{background:#f59e0b;animation:rigos-pulse 1.8s ease infinite}.mission-stat:hover{border-color:rgba(148,163,184,.24)}
.mission-primary-grid{grid-template-columns:minmax(340px,.85fr) minmax(480px,1.45fr)!important}.mission-decision-card{position:relative;overflow:hidden}.mission-decision-card:before{content:'';position:absolute;inset:0;pointer-events:none;opacity:.42;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28'%3E%3Cpath d='M0 .5H28M.5 0V28' fill='none' stroke='%2394a3b8' stroke-opacity='.10'/%3E%3C/svg%3E")}
.mission-decision-card>*{position:relative}.product-page .product-chart{position:relative;background:#0c0f14!important}.product-page .product-chart:before{content:'';position:absolute;inset:0;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='36' height='36'%3E%3Cpath d='M0 .5H36M.5 0V36' fill='none' stroke='%2394a3b8' stroke-opacity='.075'/%3E%3C/svg%3E")}.product-page .product-chart svg{position:relative}.product-page .product-chart svg defs{display:none}.product-page .product-chart svg polyline[fill]{fill:none}.product-page .product-chart svg polyline:last-of-type{stroke-dasharray:560;stroke-dashoffset:560;animation:mission-chart-draw .55s cubic-bezier(.16,1,.3,1) .08s forwards}
.mission-bento{grid-template-columns:.82fr .82fr 1.45fr!important;gap:14px!important}.mission-bento .pulse-card{min-height:294px;border-radius:15px!important}.mission-workforce{border-radius:15px}.mission-workforce .pulse-card{height:100%;border:0!important;border-radius:14px!important}.mission-workforce-title{margin-top:6px;font-size:1.12rem!important;font-weight:760!important;letter-spacing:-.035em}.mission-live-label{display:flex;align-items:center;gap:6px;color:#94a3b8;font-size:.65rem;font-weight:800;letter-spacing:.08em}.mission-live-label i{width:6px;height:6px;border-radius:50%;background:#22c55e;animation:rigos-pulse 2s ease infinite}.mission-bento .agent-statuses{margin:18px 0 12px}.mission-bento .agent-statuses>div{transition:background-color .18s ease,transform .18s ease}.mission-bento .agent-statuses>div:hover{background:#202732;transform:translateY(-1px)}
.refinery-portfolio .product-empty{min-height:180px;border:1px dashed rgba(148,163,184,.24);border-radius:14px;margin-top:20px;background:#0d1015}.refinery-portfolio .product-empty:before{content:'○';display:block;text-align:center;font-size:1.6rem;color:#64748b;margin-bottom:10px}
@keyframes mission-chart-draw{to{stroke-dashoffset:0}}
@media(max-width:1040px){.mission-primary-grid,.mission-bento{grid-template-columns:1fr!important}.mission-bento .pulse-card{min-height:unset}.mission-status-grid{grid-template-columns:repeat(2,1fr)!important}}
@media(max-width:650px){.mission-status-grid{grid-template-columns:1fr!important}.mission-stat{min-height:126px}.mission-primary-grid{gap:16px!important}}
@media(prefers-reduced-motion:reduce){.animated-border-runner,.mission-status-dot,.mission-live-label i{animation:none!important}.product-page .product-chart svg polyline:last-of-type{animation:none;stroke-dashoffset:0}}

/* AI Investigation: a trace console for evidence, timing, and operator review. */
.investigation-console{display:grid;grid-template-columns:minmax(300px,.67fr) minmax(580px,1.55fr);gap:24px;align-items:start}.trace-context{position:sticky;top:96px}.trace-console{padding:0!important;overflow:hidden;background:#0d1015!important;border:1px solid rgba(148,163,184,.15)!important}.trace-console-header{padding:28px 30px 24px;border-bottom:1px solid rgba(148,163,184,.12)}.trace-live{display:flex;align-items:center;gap:7px;padding:7px 10px;border:1px solid rgba(148,163,184,.16);border-radius:999px;color:#94a3b8;font-size:.66rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em}.trace-live i,.trace-state i{width:6px;height:6px;border-radius:50%;background:#64748b}.trace-live.running i,.trace-stage.running .trace-state i{background:#22c55e;animation:rigos-pulse 1.8s ease infinite}.reactbits-timeline{padding:8px 30px 28px}.trace-stage{position:relative;padding-top:18px}.trace-rail{position:absolute;top:16px;bottom:-18px;left:17px;width:1px;background:#29313d}.trace-stage:last-child .trace-rail{bottom:29px}.trace-rail i{position:absolute;top:0;left:-3px;width:7px;height:7px;border:1px solid #64748b;border-radius:50%;background:#0d1015}.trace-stage.completed .trace-rail i,.trace-stage.success .trace-rail i{border-color:#4f8cff;background:#4f8cff}.trace-stage.running .trace-rail i{border-color:#22c55e;background:#22c55e;box-shadow:0 0 0 4px rgba(34,197,94,.1)}.trace-stage-summary{width:100%;display:grid!important;grid-template-columns:36px minmax(0,1fr) auto;align-items:center;gap:12px;padding:12px!important;text-align:left!important;color:#f8fafc!important;text-transform:none!important;border:1px solid transparent!important;border-radius:12px!important}.trace-stage-summary:hover{background:#151a21!important;border-color:rgba(148,163,184,.13)!important;transform:none!important}.trace-agent-mark{width:34px;height:34px;display:grid;place-items:center;border:1px solid rgba(148,163,184,.18);border-radius:9px;background:#171b21;color:#cbd5e1;font-size:.75rem;font-weight:850}.trace-stage-title{min-width:0}.trace-stage-title .MuiTypography-caption{display:block;margin-top:2px;color:#94a3b8}.trace-chevron{width:24px;color:#94a3b8;font-size:1.1rem;text-align:center}.trace-state{display:flex;align-items:center;gap:7px;grid-column:3;grid-row:1;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:#94a3b8}.trace-stage.running .trace-state{color:#86efac}.trace-stage.queued .trace-state{color:#94a3b8}.trace-stage-detail{margin:0 0 2px 48px;padding:4px 12px 18px;border-left:1px solid rgba(148,163,184,.13);overflow:hidden}.trace-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0 14px}.trace-metrics>div{padding:10px;border:1px solid rgba(148,163,184,.1);border-radius:9px;background:#111418}.trace-metrics p:first-child{font-size:.6rem!important;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8}.trace-metrics p:last-child{margin-top:4px;font-size:.77rem!important;font-weight:750}.trace-reasoning,.trace-documents{padding:12px 0}.trace-reasoning>p:last-child{margin-top:7px;color:#cbd5e1;line-height:1.55}.trace-documents{display:grid;gap:6px}.trace-documents .MuiTypography-caption{display:block;padding:8px 10px;border-left:2px solid #475569;background:#111418;color:#cbd5e1}.trace-console .product-kicker{font-size:.66rem!important}.trace-console:hover{transform:none!important;box-shadow:none!important}
@media(max-width:1040px){.investigation-console{grid-template-columns:1fr}.trace-context{position:static}.trace-console{min-height:auto!important}}@media(max-width:650px){.trace-console-header,.reactbits-timeline{padding-left:18px;padding-right:18px}.trace-console-header{gap:12px;flex-direction:column}.trace-stage-summary{grid-template-columns:32px minmax(0,1fr)!important}.trace-state{grid-column:2;grid-row:2;justify-self:start}.trace-stage-detail{margin-left:43px}.trace-metrics{grid-template-columns:repeat(2,1fr)}}

/* Assets: dense industrial condition cards with a clear path to operating detail. */
.asset-console-toolbar{margin-bottom:24px!important}.asset-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.asset-condition-motion{min-width:0}.asset-condition-card{height:100%;padding:20px!important;background:#111418!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:15px!important;box-shadow:none!important;overflow:hidden;transition:border-color .18s ease,box-shadow .18s ease!important}.asset-condition-card:hover{border-color:rgba(148,163,184,.28)!important;box-shadow:0 14px 24px rgba(0,0,0,.16)!important}.asset-condition-card.critical{border-left:3px solid #ef4444!important}.asset-card-heading{display:flex;justify-content:space-between;gap:14px}.asset-card-name{margin-top:6px;font-size:1.17rem!important;font-weight:800!important;letter-spacing:-.035em}.asset-card-heading .MuiTypography-caption{color:#94a3b8}.asset-card-priority{height:28px;min-width:34px;display:grid;place-items:center;border-radius:8px;background:#1b2430;color:#cbd5e1;font-size:.66rem;font-weight:850}.asset-card-priority.p1{background:rgba(239,68,68,.13);color:#fca5a5}.asset-card-priority.p2{background:rgba(245,158,11,.12);color:#fcd34d}.asset-card-health{display:flex;align-items:end;justify-content:space-between;gap:16px;margin:22px 0 17px}.asset-card-health>div:first-child>p:last-child{margin-top:5px;font-size:2rem!important;font-weight:840!important;line-height:1;letter-spacing:-.07em}.asset-card-health .health{display:grid;justify-items:end;gap:6px}.asset-card-health .health>div{width:96px}.asset-card-readings{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}.asset-card-readings>div{min-width:0;padding:10px 9px;border:1px solid rgba(148,163,184,.1);border-radius:9px;background:#0d1015}.asset-card-readings p:first-child{font-size:.59rem!important;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#94a3b8}.asset-card-readings p:last-child{margin-top:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:.75rem!important;font-weight:760}.asset-card-status{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:17px 0 10px;color:#94a3b8}.asset-card-status>div{display:flex;align-items:center;gap:7px;min-width:0}.asset-card-status i{width:6px;height:6px;border-radius:50%;background:#f59e0b}.asset-condition-card.critical .asset-card-status i{background:#ef4444;animation:rigos-pulse 1.8s ease infinite}.asset-card-status p{font-size:.68rem!important;font-weight:750;text-transform:uppercase;letter-spacing:.06em}.asset-card-status .MuiTypography-caption{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.asset-expand{width:100%;justify-content:space-between!important;padding:8px 0!important;color:#94a3b8!important;font-size:.72rem!important;text-transform:none!important}.asset-expand:hover{color:#f8fafc!important;background:transparent!important;transform:none!important}.asset-card-expanded{overflow:hidden}.asset-card-expanded>.MuiDivider-root{margin:5px 0 14px}.asset-card-expanded>p:last-of-type{margin-top:7px;color:#cbd5e1;line-height:1.5}.asset-expanded-meta{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}.asset-expanded-meta p{display:grid;gap:4px;padding:9px;border-radius:8px;background:#0d1015;color:#cbd5e1;font-size:.7rem!important}.asset-expanded-meta b{color:#94a3b8;font-size:.6rem;text-transform:uppercase;letter-spacing:.06em}.asset-console-empty{min-height:330px;display:grid;place-content:center;gap:10px;padding:30px;border:1px dashed rgba(148,163,184,.25);border-radius:16px;background:#0d1015;text-align:center}.asset-console-empty>p:last-child{max-width:400px;color:#94a3b8}.asset-console-empty:before{content:'□';font-size:2rem;color:#64748b}@media(max-width:1100px){.asset-card-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.asset-card-grid{grid-template-columns:1fr}.asset-card-readings{grid-template-columns:repeat(3,1fr)}.asset-console-toolbar{align-items:flex-start!important;gap:12px;flex-direction:column}.asset-card-status{align-items:flex-start;flex-direction:column}}
/* Navigation: fast, quiet, and deliberate. */
.product-nav{transition:width .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s ease!important}.product-nav:hover{box-shadow:12px 0 30px rgba(0,0,0,.14)}.product-nav a{position:relative;isolation:isolate;outline:none;transition:color .16s ease,background-color .16s ease,transform .16s ease!important}.product-nav a:before{display:none!important}.product-nav a.active{background:transparent!important}.product-nav a:hover{background:#171b21!important;transform:translateX(1px)}.product-nav a:focus-visible,.product-settings:focus-visible,.product-search:focus-visible,.product-top .MuiIconButton-root:focus-visible{outline:2px solid #7aa7ff;outline-offset:2px}.product-nav-indicator{position:absolute;z-index:-1;inset:0;border:1px solid rgba(79,140,255,.28);border-radius:10px;background:rgba(79,140,255,.12)}.product-nav-icon{width:20px;height:20px;display:grid;place-items:center;flex:none}.product-nav-icon svg{transition:transform .16s ease,color .16s ease}.product-nav a:hover .product-nav-icon svg{transform:scale(1.04)}.product-nav a span:last-child{transition:opacity .14s ease,transform .16s ease}.product-nav:hover a span:last-child{transform:translateX(0)}.product-nav:not(:hover) a span:last-child{transform:translateX(-4px)}
.product-search{border:1px solid transparent!important;transition:width .18s cubic-bezier(.2,.8,.2,1),border-color .16s ease,box-shadow .16s ease,background-color .16s ease!important}.product-search:hover{transform:none!important;background:#181e28!important}.product-top .MuiIconButton-root{transition:transform .16s ease,background-color .16s ease,color .16s ease!important}.product-top .MuiIconButton-root:hover{transform:translateY(-1px) scale(1.03)}.product-dialog{box-shadow:0 22px 60px rgba(0,0,0,.35)!important}.product-command{padding:14px!important}.product-command .MuiOutlinedInput-root{border:1px solid rgba(148,163,184,.14)!important}.product-dialog-label{margin:16px 8px 7px!important}.product-command-item{border-radius:9px!important;transition:background-color .14s ease,transform .14s ease!important}.product-command-item:hover{transform:translateX(2px)!important;background:#1a202a!important}.product-command-item .MuiButton-startIcon{color:#94a3b8}.product-notification-dialog{border-left:2px solid rgba(79,140,255,.38)!important}.product-notification{position:relative;padding:17px 0 17px 14px!important;transition:background-color .16s ease,transform .16s ease}.product-notification:before{content:'';position:absolute;left:0;top:20px;bottom:20px;width:2px;border-radius:99px;background:#475569}.product-notification:hover{transform:translateX(2px);background:#151a21}.product-notification:hover:before{background:#4f8cff}.assistant-panel{background:#111418}.assistant-panel .MuiButton-outlined{border-color:rgba(148,163,184,.2);color:#cbd5e1;transition:background-color .16s ease,border-color .16s ease,transform .16s ease}.assistant-panel .MuiButton-outlined:hover{background:#171d27;border-color:rgba(148,163,184,.38);transform:translateY(-1px)}.assistant-history{scroll-behavior:smooth;border-top:1px solid rgba(148,163,184,.1);border-bottom:1px solid rgba(148,163,184,.1);padding:15px 2px}.assistant-message{border:1px solid transparent;animation:assistant-message-in .18s cubic-bezier(.2,.8,.2,1)}.assistant-message.assistant{border-color:rgba(148,163,184,.1)}.assistant-panel .MuiOutlinedInput-root:focus-within{box-shadow:0 0 0 3px rgba(79,140,255,.1);border-color:rgba(79,140,255,.45)}@keyframes assistant-message-in{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.product-nav,.product-nav a,.product-nav-icon svg,.product-search,.product-top .MuiIconButton-root,.product-command-item,.product-notification,.assistant-message{transition:none!important;animation:none!important}}
/* Keep navigation glyphs visible while only labels collapse. */
.product-nav a .product-nav-icon{opacity:1!important;transform:none!important}
/* Contextual empty states: a calm operational handoff, never a dead end. */
.product-empty{display:block!important;min-height:unset!important}.product-empty-state{min-height:250px;display:grid;place-content:center;justify-items:center;gap:9px;padding:30px;border:1px dashed rgba(148,163,184,.22);border-radius:14px;background:#0d1015;text-align:center}.empty-state-mark{width:46px;height:46px;display:grid;place-items:center;border:1px solid rgba(148,163,184,.18);border-radius:13px;color:#a5b4c7;animation:empty-state-breathe 3.4s ease-in-out infinite}.empty-state-mark svg{font-size:23px}.empty-state-title{margin-top:5px;font-weight:800!important;letter-spacing:-.025em}.empty-state-copy{max-width:390px;color:#94a3b8;font-size:.82rem!important;line-height:1.55}.empty-state-action{display:flex;align-items:center;gap:7px;margin-top:5px;color:#cbd5e1;font-size:.72rem;font-weight:750}.empty-state-action i{width:6px;height:6px;border-radius:50%;background:#4f8cff}.product-inbox-empty{min-height:230px;padding:24px;border:1px dashed rgba(148,163,184,.2);border-radius:12px}.product-inbox-empty svg{padding:9px;border:1px solid rgba(148,163,184,.16);border-radius:11px;font-size:36px!important;animation:empty-state-breathe 3.4s ease-in-out infinite}@keyframes empty-state-breathe{50%{transform:translateY(-2px);border-color:rgba(148,163,184,.3)}}@media(prefers-reduced-motion:reduce){.empty-state-mark,.product-inbox-empty svg{animation:none}}
.product-inbox-empty:after{content:'Continue monitoring live operations.';color:#94a3b8;font-size:.72rem}.asset-console-empty:after{content:'Suggested next: inspect the asset portfolio.';color:#cbd5e1;font-size:.72rem;font-weight:750}
/* RIG OS application navigation — navigation is a live system control, not a page list. */
.os-app{min-height:100vh;background:#090b0f;color:#f8fafc;--rail:246px;--nav-line:rgba(148,163,184,.12);display:flex}.os-sidebar{position:fixed;inset:0 auto 0 0;z-index:20;width:var(--rail);display:flex;flex-direction:column;padding:15px 12px 13px;background:#0d1015;border-right:1px solid var(--nav-line);overflow:hidden}.os-app.is-compact{--rail:72px}.os-stage{width:calc(100% - var(--rail));margin-left:var(--rail);min-width:0}.os-brand{height:42px;display:flex;align-items:center;gap:10px;padding:0 5px}.os-brand-mark{display:grid;place-items:center;flex:none;width:30px;height:30px;border-radius:9px;background:#edf3fb;color:#0d1015;font-weight:900}.os-brand p:first-child{font-size:.88rem;font-weight:850;letter-spacing:-.055em;line-height:1}.os-brand p:last-child,.os-overline{font-size:.6rem!important;font-weight:800!important;letter-spacing:.13em!important;color:#718096;text-transform:uppercase}.os-collapse{margin-left:auto;color:#94a3b8!important}.os-workspace{width:100%;min-height:51px;margin:20px 0 17px!important;padding:8px 9px!important;justify-content:space-between!important;align-items:center!important;border:1px solid rgba(148,163,184,.12)!important;border-radius:11px!important;background:rgba(255,255,255,.025)!important;color:#e2e8f0!important;text-align:left;text-transform:none!important}.os-workspace p:last-child{margin-top:2px;font-size:.78rem;font-weight:750;white-space:nowrap}.os-workspace:hover{background:rgba(255,255,255,.055)!important}.is-compact .os-workspace{justify-content:center!important;min-height:42px;margin-top:20px!important}.is-compact .os-workspace svg{transform:rotate(90deg)}.os-nav{display:grid;gap:18px}.os-nav-group{display:grid;gap:4px}.os-nav-group>.os-overline{padding:0 10px 5px}.os-nav a{position:relative;isolation:isolate;display:flex;align-items:center;gap:12px;height:39px;padding:0 10px;border-radius:9px;color:#91a0b5;font-size:.8rem;font-weight:700;text-decoration:none;white-space:nowrap;outline:none}.os-nav a>svg{position:relative;z-index:1;font-size:19px;flex:none}.os-nav a>span:last-child{position:relative;z-index:1}.os-nav a:hover{color:#edf3fb;background:rgba(255,255,255,.035)}.os-nav a:focus-visible{box-shadow:0 0 0 2px #74a5ff}.os-active-pill{position:absolute;z-index:0;inset:0;border:1px solid rgba(106,159,255,.27);border-radius:9px;background:rgba(79,140,255,.13);box-shadow:inset 2px 0 #65a0ff}.os-nav a.is-active{color:#f4f8ff}.is-compact .os-nav a{justify-content:center;padding:0}.os-sidebar-bottom{display:grid;gap:10px;margin-top:auto}.os-sidebar-bottom>.MuiButton-root{justify-content:flex-start!important;min-height:38px;padding:0 10px!important;color:#91a0b5!important;text-transform:none!important}.is-compact .os-sidebar-bottom>.MuiButton-root{justify-content:center!important}.os-connection{display:flex;align-items:center;gap:8px;padding:8px 10px;border-top:1px solid var(--nav-line);white-space:nowrap}.os-connection i{width:6px;height:6px;border-radius:50%;background:#34d399}.os-connection p{font-size:.66rem;color:#91a0b5}.is-compact .os-connection{justify-content:center;padding:8px 0}.os-topbar{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;height:66px;padding:0 34px;border-bottom:1px solid var(--nav-line);background:rgba(9,11,15,.9);backdrop-filter:blur(18px)}.os-command-trigger{width:310px;height:36px;justify-content:space-between!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:9px!important;background:rgba(255,255,255,.025)!important;color:#91a0b5!important;text-transform:none!important;font-weight:500!important}.os-command-trigger:hover{background:rgba(255,255,255,.055)!important;border-color:rgba(148,163,184,.24)!important}.os-command-trigger kbd{padding:2px 5px;border:1px solid rgba(148,163,184,.18);border-radius:4px;color:#91a0b5;font:500 .65rem "DM Mono",monospace}.os-top-context{display:grid;gap:1px;min-width:145px;padding-left:5px}.os-top-context p:first-child{font-size:.75rem;font-weight:750}.os-top-context p:last-child{font-size:.65rem;color:#718096}.os-sync,.os-ai-status{height:30px!important;padding:0 9px!important;border-radius:8px!important;color:#94a3b8!important;font-size:.68rem!important;text-transform:none!important}.os-sync.is-ready{color:#8ccfb7!important}.os-sync .MuiButton-startIcon{margin-right:4px}.os-ai-status{color:#b8c8e5!important;background:rgba(79,140,255,.07)!important}.os-ai-status i{width:5px;height:5px;margin-left:1px;border-radius:99px;background:#64a0ff}.os-profile{display:flex!important;align-items:center!important;gap:8px!important;margin-left:3px!important;padding:3px 4px!important;border-radius:9px!important;color:#e2e8f0!important;text-align:left;text-transform:none!important}.os-profile:hover{background:rgba(255,255,255,.05)!important}.os-profile .MuiAvatar-root{width:28px;height:28px;background:#5d7fc7;font-size:.67rem;font-weight:800}.os-profile p:first-child{font-size:.68rem;font-weight:750;line-height:1.1}.os-profile p:last-child{font-size:.62rem;color:#718096}.os-stage main{max-width:1520px;margin:auto;padding:28px 52px 64px}.os-crumb{display:flex;justify-content:space-between;margin-bottom:20px}.os-crumb p{font-size:.68rem;font-weight:800;letter-spacing:.1em;color:#718096;text-transform:uppercase}.os-menu{min-width:190px!important;margin-top:6px!important;border:1px solid rgba(148,163,184,.14)!important;border-radius:10px!important;background:#151a21!important;color:#e2e8f0!important}.os-menu .MuiMenuItem-root{gap:9px;font-size:.8rem}.os-menu .MuiMenuItem-root.Mui-selected{background:rgba(79,140,255,.12)!important}.os-command-dialog{margin-top:-18vh!important}.os-command-dialog .product-command-item{min-height:39px}.os-command-dialog .product-command-item:hover{background:rgba(255,255,255,.055)!important}
html[data-rigos-theme='light'] .os-app{background:#f6f7f9;color:#111827;--nav-line:rgba(15,23,42,.1)}html[data-rigos-theme='light'] .os-sidebar,html[data-rigos-theme='light'] .os-topbar{background:rgba(255,255,255,.92)}html[data-rigos-theme='light'] .os-workspace,html[data-rigos-theme='light'] .os-command-trigger{background:#f8fafc!important;color:#64748b!important}html[data-rigos-theme='light'] .os-nav a{color:#64748b}html[data-rigos-theme='light'] .os-nav a:hover{background:#f1f5f9;color:#111827}html[data-rigos-theme='light'] .os-menu{background:#fff!important;color:#111827!important}@media(max-width:900px){.os-app{--rail:72px}.os-sidebar{padding:15px 10px}.os-brand>div:not(.os-brand-mark),.os-workspace>div,.os-nav .os-overline,.os-nav a>span:last-child,.os-sidebar-bottom .MuiButton-root span,.os-connection p{display:none}.os-workspace{justify-content:center!important;min-height:42px;margin-top:20px!important}.os-workspace svg{transform:rotate(90deg)}.os-nav a{justify-content:center;padding:0}.os-sidebar-bottom>.MuiButton-root,.os-connection{justify-content:center!important;padding-left:0!important;padding-right:0!important}.os-topbar{padding:0 22px}.os-top-context,.os-sync{display:none}.os-stage main{padding:25px 24px}}@media(max-width:620px){.os-topbar{padding:0 14px}.os-command-trigger{width:42px!important;min-width:42px!important;font-size:0!important}.os-command-trigger .MuiButton-startIcon{margin:0!important}.os-command-trigger .MuiButton-endIcon,.os-ai-status{display:none}.os-profile>div:not(.MuiAvatar-root){display:none}.os-stage main{padding:20px 16px}.os-crumb p:last-child{display:none}}@media(prefers-reduced-motion:reduce){.os-sidebar,.os-stage,.os-nav a,.os-command-trigger{transition:none!important}}
/* Mission Control state layer. */
.mission-status-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:18px}.mission-stat{min-height:145px;padding:17px;border:1px solid rgba(148,163,184,.13);border-radius:14px;background:#11161e;overflow:hidden}.mission-stat-value{margin-top:12px!important;font-size:2rem!important;font-weight:800!important;letter-spacing:-.065em!important;font-variant-numeric:tabular-nums}.mission-stat-detail{margin-top:6px!important;color:#93a2b8;font-size:.72rem!important;line-height:1.4}.mission-status-dot{width:7px;height:7px;border-radius:50%;background:#5d9bff;box-shadow:0 0 0 4px rgba(93,155,255,.09)}.mission-stat.healthy .mission-status-dot{background:#38c998}.mission-stat.attention .mission-status-dot{background:#f4af42}.mission-expand{min-height:20px!important;margin-top:11px!important;padding:0!important;color:#aab8cd!important;font-size:.64rem!important;text-transform:none!important}.mission-insight{margin-top:7px;padding:8px;border-top:1px solid rgba(148,163,184,.11);color:#c1ccdc;font-size:.69rem;line-height:1.45}.mission-control-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:18px}.mission-facility,.mission-ai-summary,.mission-telemetry,.mission-workforce,.mission-portfolio{position:relative;overflow:hidden!important;background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;box-shadow:none!important;border-radius:15px!important}.mission-facility,.mission-ai-summary{min-height:320px;padding:23px!important}.mission-grid-pattern{position:absolute;inset:0;pointer-events:none;opacity:.38;background-image:linear-gradient(rgba(148,163,184,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(148,163,184,.08) 1px,transparent 1px);background-size:24px 24px;mask-image:linear-gradient(to bottom,black,transparent 76%)}.mission-facility>*:not(.mission-grid-pattern),.mission-ai-summary>*:not(.mission-grid-pattern){position:relative;z-index:1}.mission-facility-title{margin-top:7px!important;font-size:1.65rem!important;font-weight:800!important;letter-spacing:-.05em}.mission-facility-map{position:relative;height:166px;margin-top:18px;border:1px solid rgba(148,163,184,.1);border-radius:12px;background:radial-gradient(circle at 50% 50%,rgba(79,140,255,.13),transparent 34%),#0d1117;overflow:hidden}.facility-map-core{position:absolute;left:50%;top:50%;display:grid;place-items:center;width:79px;height:79px;border:1px solid rgba(100,160,255,.42);border-radius:50%;background:#131b27;transform:translate(-50%,-50%);box-shadow:0 0 0 9px rgba(79,140,255,.06)}.facility-map-core p:first-child{font-size:1.25rem;font-weight:850;letter-spacing:-.06em}.facility-map-core p:last-child{font-size:.48rem;font-weight:800;letter-spacing:.11em;color:#8798b2}.facility-map-node{position:absolute;display:grid;justify-items:center;gap:4px;font-size:.62rem;color:#b5c2d5}.facility-map-node i{width:8px;height:8px;border-radius:50%;background:#3dd09d;box-shadow:0 0 0 5px rgba(61,208,157,.08)}.facility-map-node.risk i{background:#f2a949}.facility-map-node:nth-of-type(3){left:19%;top:25%}.facility-map-node:nth-of-type(4){right:18%;top:22%}.facility-map-node:nth-of-type(5){left:22%;bottom:18%}.facility-map-node:nth-of-type(6){right:21%;bottom:17%}.mission-facility-footer{display:flex;justify-content:space-between;margin-top:15px}.mission-facility-footer p{font-size:.66rem;color:#91a0b5}.mission-facility-footer b{color:#e5edf8}.mission-decision{position:relative;margin:13px 0!important;font-size:2rem!important;font-weight:800!important;line-height:1.01!important;letter-spacing:-.065em!important}.mission-ai-summary:after{content:'';position:absolute;inset:auto -18% -28% auto;width:170px;height:170px;border:1px solid rgba(79,140,255,.16);border-radius:50%;box-shadow:0 0 0 26px rgba(79,140,255,.03),0 0 0 54px rgba(79,140,255,.02)}.mission-summary-signal{display:flex;align-items:center;gap:8px;margin:22px 0 16px}.mission-summary-signal i,.mission-telemetry-live i{width:6px;height:6px;border-radius:50%;background:#3dd09d}.mission-summary-signal i.risk{background:#f2a949}.mission-summary-signal p{font-size:.68rem;color:#b5c2d5}.mission-telemetry,.mission-workforce,.mission-portfolio{margin-top:18px;padding:22px!important}.mission-telemetry-live{display:flex;align-items:center;gap:7px;color:#79b3ff;font-size:.62rem;font-weight:800;letter-spacing:.11em}.mission-telemetry-chart{position:relative;margin-top:14px;overflow:hidden}.mission-telemetry-chart .mini-graph{margin-top:0}.telemetry-sweep{position:absolute;z-index:2;top:0;bottom:24px;width:18%;pointer-events:none;background:linear-gradient(90deg,transparent,rgba(103,176,255,.24),transparent);filter:blur(1px)}.mission-thresholds{gap:20px;margin-top:13px}.mission-thresholds p{display:flex;align-items:center;gap:6px;color:#91a0b5;font-size:.65rem}.mission-thresholds i{width:6px;height:6px;border-radius:50%}.mission-thresholds .nominal{background:#3dd09d}.mission-thresholds .watch{background:#f2a949}.mission-thresholds .critical{background:#ef7474}.mission-workforce-count{color:#8fb9ff;font-size:.7rem;font-weight:750}.mission-agent-marquee{display:grid;grid-template-columns:repeat(6,minmax(160px,1fr));gap:10px;overflow-x:auto;padding-top:15px}.mission-agent{display:grid;gap:9px;min-width:160px;padding:13px;border:1px solid rgba(148,163,184,.12);border-radius:11px;background:#0d1117}.mission-agent-avatar{display:grid;place-items:center;width:25px;height:25px;border-radius:8px;background:rgba(79,140,255,.15);color:#a7caff;font-size:.7rem;font-weight:850}.mission-agent>p:nth-of-type(1){min-height:30px;font-size:.66rem;line-height:1.35}.mission-agent-progress{height:4px;border-radius:99px;background:rgba(148,163,184,.12);overflow:hidden}.mission-agent-progress i{display:block;height:100%;border-radius:99px;background:#5f9dff}.mission-agent-meta{font:500 .56rem "DM Mono",monospace!important;color:#8493a8}.mission-portfolio .refinery-grid{margin-top:15px}.mission-portfolio-empty{position:relative;display:flex;align-items:center;gap:15px;min-height:130px;margin-top:15px;padding:18px;border:1px dashed rgba(148,163,184,.22);border-radius:12px;overflow:hidden;background:#0d1117}.mission-portfolio-empty p:last-child{margin-top:4px;max-width:480px;color:#93a2b8}.mission-portfolio-empty:before{content:'';flex:none;width:50px;height:50px;border:1px solid rgba(100,160,255,.4);border-radius:12px;background:linear-gradient(90deg,transparent 48%,rgba(100,160,255,.2) 49%,rgba(100,160,255,.2) 51%,transparent 52%),linear-gradient(transparent 48%,rgba(100,160,255,.2) 49%,rgba(100,160,255,.2) 51%,transparent 52%);background-size:12px 12px}@media(max-width:1050px){.mission-status-grid{grid-template-columns:repeat(2,1fr)}.mission-agent-marquee{grid-template-columns:repeat(3,minmax(160px,1fr))}}@media(max-width:760px){.mission-control-grid{grid-template-columns:1fr}.mission-agent-marquee{grid-template-columns:repeat(2,minmax(160px,1fr))}}@media(max-width:520px){.mission-status-grid{grid-template-columns:1fr}.mission-agent-marquee{grid-template-columns:1fr}.mission-facility-footer{gap:8px;flex-wrap:wrap}.mission-telemetry,.mission-workforce,.mission-portfolio,.mission-facility,.mission-ai-summary{padding:17px!important}}@media(prefers-reduced-motion:reduce){.telemetry-sweep{display:none}}
```

## frontend/src/redesign/ProductPage.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/ProductPage.jsx`

```javascript
/* Epic 6 — thin product page: facility scope + lazy workspace views */
import { Suspense, lazy, useEffect } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';
import { useOperations } from '../context/OperationsContext';
import { useObjectContext } from '../context/ObjectContext';
import { filterByFacility, assetLocation, incidentLocation, taskLocation } from '../context/objectNavigation';
import { inferProvenance, useOperatorAudit } from './accountability';
import { PageMotion } from './motion';

const MissionControlOS = lazy(() => import('./views/MissionControlOS').then((m) => ({ default: m.MissionControlOS })));
const AssetConsole = lazy(() => import('./views/AssetConsole').then((m) => ({ default: m.AssetConsole })));
const IncidentManagement = lazy(() => import('./views/IncidentManagement').then((m) => ({ default: m.IncidentManagement })));
const AIInvestigationOS = lazy(() => import('./views/AIInvestigationOS').then((m) => ({ default: m.AIInvestigationOS })));
const MaintenancePlanning = lazy(() => import('./views/MaintenancePlanning').then((m) => ({ default: m.MaintenancePlanning })));
const ForecastTerminal = lazy(() => import('./views/ForecastTerminal').then((m) => ({ default: m.ForecastTerminal })));
const ExecutiveBriefing = lazy(() => import('./views/ExecutiveBriefing').then((m) => ({ default: m.ExecutiveBriefing })));

const config = {
  '/': ['Command center', 'A concise view of facility condition, AI operations, and decisions requiring your attention.'],
  '/assets': ['Critical assets', 'The equipment currently creating the greatest operational and financial exposure.'],
  '/incident-simulator': ['Incident center', 'A traceable record of incidents, AI evidence, and operator decisions.'],
  '/agent-monitor': ['AI investigation', 'Supervise the active reasoning workflow before authorizing a response.'],
  '/maintenance': ['Maintenance', 'Work prioritized by operational risk, asset condition, and AI recommendations.'],
  '/health-prediction': ['Health forecasting', 'A forward-looking view of asset health and intervention timing.'],
  '/reports': ['Executive reports', 'Decision-ready incident outcomes and AI execution records.'],
};

function WorkspaceFallback() {
  return (
    <Box className="e6-workspace-fallback" role="status" aria-live="polite" sx={{ display: 'grid', placeItems: 'center', minHeight: 240, gap: 1.5 }}>
      <CircularProgress size={28} />
      <Typography color="text.secondary">Loading workspace…</Typography>
    </Box>
  );
}

export function ProductPage() {
  const { pathname } = useLocation();
  const { operations, connected } = useOperations();
  const objectApi = useObjectContext();
  const facility = objectApi.scope?.facility || 'Alpha Refinery';
  const auditEvents = useOperatorAudit(objectApi, operations);
  const dataProvenance = inferProvenance({ connected, syncAge: connected ? 4 : 40 });
  const [title, description] = config[pathname] || config['/'];
  useEffect(() => {
    if (pathname === '/assets' || ['/incident-simulator', '/agent-monitor', '/maintenance', '/health-prediction'].includes(pathname)) {
      document.querySelector('#main-content')?.focus?.({ preventScroll: true });
      return;
    }
    const heading = document.querySelector('.product-hero h1');
    heading?.focus?.({ preventScroll: true });
  }, [pathname]);

  const assetsAll = operations.assets || [];
  const assets = filterByFacility(assetsAll, facility, assetLocation);
  const incidents = filterByFacility(
    operations.critical_incidents || [],
    facility,
    (item) => incidentLocation(item, assetsAll),
  );
  const auditLogs = filterByFacility(
    operations.audit_logs || [],
    facility,
    (item) => incidentLocation(item, assetsAll),
  );
  const tasks = filterByFacility(
    operations.maintenance?.tasks || [],
    facility,
    (item) => taskLocation(item, assetsAll),
  );
  const predicted = filterByFacility(
    operations.predicted_failures?.length ? operations.predicted_failures : assetsAll,
    facility,
    assetLocation,
  );
  const activeInvestigationIncident = auditLogs.find(
    (item) => item.id === operations.investigation?.incident?.id || item.id === objectApi.selection.incidentId,
  ) || operations.investigation?.incident || incidents[0] || auditLogs[0];
  const stages = operations.investigation?.stages || [];
  const telemetry = operations.telemetry || { readings: [] };
  const maintenance = { ...(operations.maintenance || {}), tasks };
  const hideHero = ['/assets', '/incident-simulator', '/agent-monitor', '/maintenance', '/health-prediction'].includes(pathname);
  const opsClass = hideHero ? ' is-ops-os' : '';
  const assetsClass = pathname === '/assets' ? ' is-assets-os' : '';

  return (
    <PageMotion pageKey={pathname}>
      <Box className={`product-page${opsClass}${assetsClass}`}>
        {!hideHero && (
          <Box className="product-hero">
            <Typography className="product-kicker">{facility.toUpperCase()} - LIVE OPERATIONS</Typography>
            <Typography component="h1" tabIndex={-1}>{title}</Typography>
            <Typography>{description}</Typography>
          </Box>
        )}
        <Suspense fallback={<WorkspaceFallback />}>
          {pathname === '/' && (
            <MissionControlOS
              assets={assets}
              incidents={incidents}
              stages={stages}
              dashboard={operations.dashboard || {}}
              projection={operations.revenue_projection}
              refineries={operations.refineries || []}
              telemetry={telemetry}
              maintenance={maintenance}
              facility={facility}
              auditEvents={auditEvents}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/assets' && (
            <AssetConsole
              assets={assets}
              incidents={auditLogs}
              telemetry={telemetry}
              telemetryStreams={operations.critical_asset_telemetry || []}
              maintenance={maintenance}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/incident-simulator' && (
            <IncidentManagement incidents={auditLogs} telemetry={telemetry} provenance={dataProvenance} />
          )}
          {pathname === '/agent-monitor' && (
            <AIInvestigationOS
              stages={stages}
              investigation={operations.investigation || {}}
              incident={activeInvestigationIncident}
              telemetry={telemetry}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/maintenance' && <MaintenancePlanning maintenance={maintenance} />}
          {pathname === '/health-prediction' && (
            <ForecastTerminal
              assets={predicted}
              telemetry={telemetry}
              telemetryStreams={operations.critical_asset_telemetry || []}
              provenance={dataProvenance}
            />
          )}
          {pathname === '/reports' && <ExecutiveBriefing reports={operations.reports || []} />}
        </Suspense>
      </Box>
    </PageMotion>
  );
}
```

## frontend/src/redesign/ProductShell.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/ProductShell.jsx`

```javascript
import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Avatar, Badge, Box, Button, Dialog, Divider, IconButton, InputAdornment, Menu, MenuItem, Stack, TextField, Tooltip, Typography,
} from '@mui/material';
import {
  ArticleOutlined, BuildOutlined, ChevronLeftOutlined, ChevronRightOutlined, CloseOutlined, DashboardOutlined,
  DarkModeOutlined, DevicesOutlined, HistoryOutlined, LightModeOutlined, MemoryOutlined, MoreHorizOutlined,
  NotificationsOutlined, PushPinOutlined, ScienceOutlined, SearchOutlined, SettingsOutlined, SmartToyOutlined,
  SyncOutlined, ViewSidebarOutlined, WarningAmberOutlined,
} from '@mui/icons-material';
import { AnimatePresence, LayoutGroup, motion, useReducedMotion } from 'motion/react';
import { useColorMode } from '../context/ColorModeContext';
import { useOperations } from '../context/OperationsContext';
import { useObjectContext } from '../context/ObjectContext';
import { navigateTo, pathToWorkspace, WORKSPACE_LABELS } from '../context/objectNavigation';
import { resolveBreadcrumbs } from '../context/breadcrumbs';
import { markNotificationsRead } from '../api/client';
import { AssistantPanel } from './AssistantPanel';
import {
  AuditSpine, exportAuditLog, useOperatorAudit,
} from './accountability';

const nav = [
  ['Command Center', '/', DashboardOutlined, 'Overview', 'command'],
  ['Assets', '/assets', DevicesOutlined, 'Operations', 'assets'],
  ['Incidents', '/incident-simulator', WarningAmberOutlined, 'Operations', 'incidents'],
  ['Maintenance', '/maintenance', BuildOutlined, 'Operations', 'maintenance'],
  ['AI Investigation', '/agent-monitor', MemoryOutlined, 'Intelligence', 'investigation'],
  ['Forecasting', '/health-prediction', ScienceOutlined, 'Intelligence', 'forecasting'],
  ['Reports', '/reports', ArticleOutlined, 'Intelligence', 'reports'],
];
const facilities = ['Alpha Refinery', 'North Sea Portfolio', 'Enterprise view'];
const label = (value = '') => String(value).replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
const formatTime = (value) => (value ? new Date(value).toLocaleTimeString() : 'Live event');

/** Epic 4 — ProductShell wired to ObjectContext (scope, search, keyboard, breadcrumbs). */
export function ProductShell({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const { mode, toggle } = useColorMode();
  const { operations = {}, ambient = {}, connected = false, refresh = async () => {} } = useOperations();
  const objectApi = useObjectContext();

  const [collapsed, setCollapsed] = useState(() => localStorage.getItem('rigos-nav-collapsed') === 'true');
  const [facilityAnchor, setFacilityAnchor] = useState(null);
  const [profileAnchor, setProfileAnchor] = useState(null);
  const [commandOpen, setCommandOpen] = useState(false);
  const [commandIndex, setCommandIndex] = useState(0);
  const [inboxOpen, setInboxOpen] = useState(false);
  const [assistantOpen, setAssistantOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [clock, setClock] = useState(() => new Date());
  const [syncAge, setSyncAge] = useState(0);
  const auditSpineRef = useRef(null);
  const workspacePanelRef = useRef(null);
  const navRefs = useRef([]);

  const facility = objectApi.scope.facility || facilities[0];
  const workspaceKey = pathToWorkspace(location.pathname);
  const current = nav.find((item) => item[1] === location.pathname) || nav[0];
  const workspacePanel = objectApi.ui.workspacePanelOpen;
  const pinned = objectApi.ui.pinnedRoutes || [];

  const notifications = Array.isArray(operations.notifications) ? operations.notifications : [];
  const unread = notifications.filter((item) => item && !item.read);
  const agentsWorking = Array.isArray(operations.investigation?.stages)
    ? operations.investigation.stages.filter((stage) => stage?.state === 'running').length
    : 0;
  const activeIncidents = Number(operations.dashboard?.active_incidents || 0);
  const aiLabel = !connected
    ? 'Syncing'
    : agentsWorking
      ? `${agentsWorking} agents active`
      : activeIncidents
        ? 'AI review queued'
        : 'AI monitoring';

  const selectedAsset = (operations.assets || []).find((a) => a.id === objectApi.selection.assetId);
  const assetName = selectedAsset?.name;
  const unitLabel = (() => {
    const location = selectedAsset?.location || selectedAsset?.zone || objectApi.scope?.unit;
    if (!location) return null;
    const parts = String(location).split(/[›>\/|]/).map((part) => part.trim()).filter(Boolean);
    return parts[1] || parts[0] || null;
  })();
  const incident = (operations.audit_logs || []).find((i) => i.id === objectApi.selection.incidentId)
    || (operations.critical_incidents || []).find((i) => i.id === objectApi.selection.incidentId);
  const crumbs = useMemo(() => resolveBreadcrumbs({
    facility,
    workspace: workspaceKey,
    selection: objectApi.selection,
    labels: {
      assetName,
      unitLabel: workspaceKey === 'assets' ? unitLabel : null,
      incidentLabel: incident ? label(incident.incident_type || incident.id) : null,
      workOrderTitle: objectApi.draft?.workOrder?.title || objectApi.selection.workOrderId,
      reportTitle: (operations.reports || []).find((r) => r.id === objectApi.selection.reportId)?.title,
      stageLabel: objectApi.selection.agentStageId,
    },
  }), [facility, workspaceKey, objectApi.selection, objectApi.draft, assetName, unitLabel, incident, operations.reports]);

  const auditEvents = useOperatorAudit(objectApi, operations);

  const commands = useMemo(() => {
    const items = [
      ...nav.map(([name, , Icon, group, workspace]) => ({
        label: name,
        group,
        icon: <Icon />,
        run: () => navigateTo(objectApi, navigate, workspace),
      })),
      { label: 'Open notifications', group: 'System', icon: <NotificationsOutlined />, run: () => setInboxOpen(true) },
      { label: 'Ask RigOS AI', group: 'System', icon: <SmartToyOutlined />, run: () => setAssistantOpen(true) },
      {
        label: mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode',
        group: 'System',
        icon: mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />,
        run: toggle,
      },
      {
        label: 'Export audit log',
        group: 'System',
        icon: <HistoryOutlined />,
        description: 'Download immutable decision trail (CSV)',
        run: () => exportAuditLog({ events: auditEvents, facility }),
      },
      {
        label: 'Toggle asset inspector',
        group: 'System',
        icon: <ViewSidebarOutlined />,
        description: 'Keyboard ] on Assets',
        run: () => {
          navigateTo(objectApi, navigate, 'assets');
          objectApi.patchUi?.({ inspectorCollapsed: !objectApi.ui?.inspectorCollapsed });
        },
      },
    ];

    const assets = operations.assets || [];
    const byId = new Map(assets.map((asset) => [asset.id, asset]));

    (objectApi.favorites?.assetIds || []).forEach((id) => {
      const asset = byId.get(id);
      if (!asset) return;
      items.push({
        label: asset.name || asset.id,
        group: 'Favorites',
        description: [asset.tag, asset.location || asset.zone].filter(Boolean).join(' · ') || asset.id,
        icon: <PushPinOutlined />,
        run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
      });
    });

    (objectApi.recent?.assetIds || []).slice(0, 10).forEach((id) => {
      const asset = byId.get(id);
      if (!asset) return;
      items.push({
        label: asset.name || asset.id,
        group: 'Recent',
        description: [asset.tag, asset.location || asset.zone].filter(Boolean).join(' · ') || asset.id,
        icon: <HistoryOutlined />,
        run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
      });
    });

    assets.forEach((asset) => {
      const tag = asset.tag || asset.id;
      items.push({
        label: asset.name || asset.id,
        group: 'Assets',
        description: [tag, asset.location || asset.zone, asset.type].filter(Boolean).join(' · '),
        icon: <DevicesOutlined />,
        run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
      });
      if (asset.tag && String(asset.tag) !== String(asset.name)) {
        items.push({
          label: String(asset.tag),
          group: 'Tags',
          description: asset.name || asset.id,
          icon: <DevicesOutlined />,
          run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
        });
      }
    });

    [...(operations.audit_logs || []), ...(operations.critical_incidents || [])]
      .filter((item, index, list) => list.findIndex((row) => row.id === item.id) === index)
      .slice(0, 30)
      .forEach((item) => {
        items.push({
          label: label(item.incident_type || item.title || item.id),
          group: 'Incidents',
          description: item.asset_name || item.asset_id || item.id,
          icon: <WarningAmberOutlined />,
          run: () => navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null }),
        });
      });

    (operations.maintenance?.tasks || []).slice(0, 20).forEach((task, index) => {
      const id = task.id || `wo-${index}`;
      items.push({
        label: task.title || task.Task || task.name || `Work order ${index + 1}`,
        group: 'Work orders',
        description: task.asset_name || task.Owner || id,
        icon: <BuildOutlined />,
        run: () => navigateTo(objectApi, navigate, 'maintenance', { workOrderId: id }),
      });
    });

    (operations.reports || []).slice(0, 15).forEach((report) => {
      items.push({
        label: report.title || report.name || report.id,
        group: 'Reports',
        description: report.created_at ? formatTime(report.created_at) : 'Executive brief',
        icon: <ArticleOutlined />,
        run: () => navigateTo(objectApi, navigate, 'reports', { reportId: report.id }),
      });
    });

    return items;
  }, [mode, navigate, objectApi, operations, toggle, auditEvents, facility]);

  const matches = commands.filter((item) => (
    `${item.label} ${item.group} ${item.description || ''}`.toLowerCase().includes(query.toLowerCase())
  ));

  useEffect(() => {
    setCommandIndex(0);
  }, [query, commandOpen]);

  useEffect(() => {
    const onKey = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setCommandOpen(true);
      }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'j') {
        event.preventDefault();
        objectApi.toggleWorkspacePanel();
      }
      if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'a') {
        event.preventDefault();
        auditSpineRef.current?.focus?.();
      }
      if (event.key === 'Escape') {
        setCommandOpen(false);
        objectApi.setWorkspacePanelOpen(false);
        setAssistantOpen(false);
      }
      if (commandOpen && matches.length) {
        if (event.key === 'ArrowDown') {
          event.preventDefault();
          setCommandIndex((value) => Math.min(matches.length - 1, value + 1));
        }
        if (event.key === 'ArrowUp') {
          event.preventDefault();
          setCommandIndex((value) => Math.max(0, value - 1));
        }
        if (event.key === 'Enter') {
          event.preventDefault();
          const command = matches[commandIndex];
          if (command) {
            command.run();
            setCommandOpen(false);
            setQuery('');
          }
        }
      }
    };
    addEventListener('keydown', onKey);
    return () => removeEventListener('keydown', onKey);
  }, [objectApi, commandOpen, matches, commandIndex]);

  /* Part 8 — focus trap while WorkspacePanel is open */
  useEffect(() => {
    if (!workspacePanel) return undefined;
    const root = workspacePanelRef.current;
    if (!root) return undefined;
    const focusables = () => [...root.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')]
      .filter((el) => !el.hasAttribute('disabled') && el.offsetParent !== null);
    const first = focusables()[0];
    first?.focus?.();
    const onKey = (event) => {
      if (event.key !== 'Tab') return;
      const items = focusables();
      if (!items.length) return;
      const firstEl = items[0];
      const lastEl = items[items.length - 1];
      if (event.shiftKey && document.activeElement === firstEl) {
        event.preventDefault();
        lastEl.focus();
      } else if (!event.shiftKey && document.activeElement === lastEl) {
        event.preventDefault();
        firstEl.focus();
      }
    };
    root.addEventListener('keydown', onKey);
    return () => root.removeEventListener('keydown', onKey);
  }, [workspacePanel]);

  const onNavKeyDown = (event, index) => {
    if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp' && event.key !== 'Home' && event.key !== 'End') return;
    event.preventDefault();
    const links = navRefs.current.filter(Boolean);
    if (!links.length) return;
    let next = index;
    if (event.key === 'ArrowDown') next = Math.min(links.length - 1, index + 1);
    if (event.key === 'ArrowUp') next = Math.max(0, index - 1);
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = links.length - 1;
    links[next]?.focus?.();
  };

  useEffect(() => {
    setSyncAge(0);
    const timer = setInterval(() => {
      setClock(new Date());
      setSyncAge((value) => (connected ? Math.min(value + 1, 59) : value));
    }, 1000);
    return () => clearInterval(timer);
  }, [connected, operations.generated_at]);

  const updateCollapse = () => setCollapsed((value) => {
    localStorage.setItem('rigos-nav-collapsed', String(!value));
    return !value;
  });

  const selectFacility = (name) => {
    objectApi.setFacility(name);
    setFacilityAnchor(null);
  };

  const openInbox = async () => {
    setInboxOpen(true);
    if (unread.length) {
      try {
        await markNotificationsRead({ mark_all: true });
        await refresh();
      } catch { /* polling keeps shell current */ }
    }
  };

  const groups = ['Overview', 'Operations', 'Intelligence', 'Assets', 'Incidents', 'Work orders', 'Reports', 'System'];

  return (
    <Box className={`os-app ${collapsed ? 'is-compact' : ''}`}>
      <LayoutGroup id="rig-os-navigation">
        <motion.aside
          layout
          transition={{ layout: reduced ? { duration: 0 } : { duration: 0.12, ease: 'easeOut' } }}
          className="os-sidebar"
        >
          <Box className="os-brand">
            <Box className="os-brand-mark">R</Box>
            {!collapsed && (
              <motion.div initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0 }}>
                <Typography>RIG OS</Typography>
                <Typography>OPERATIONS</Typography>
              </motion.div>
            )}
            <Tooltip title={collapsed ? 'Expand navigation' : 'Collapse navigation'} placement="right">
              <IconButton className="os-collapse" onClick={updateCollapse}>
                {collapsed ? <ChevronRightOutlined /> : <ChevronLeftOutlined />}
              </IconButton>
            </Tooltip>
          </Box>
          <Button className="os-workspace" onClick={(event) => setFacilityAnchor(event.currentTarget)}>
            {!collapsed && (
              <Box>
                <Typography className="os-overline">FACILITY SCOPE</Typography>
                <Typography>{facility}</Typography>
              </Box>
            )}
            <MoreHorizOutlined />
          </Button>
          <nav className="os-nav" aria-label="Primary navigation">
            {['Overview', 'Operations', 'Intelligence'].map((group) => (
              <Box key={group} className="os-nav-group">
                {!collapsed && <Typography className="os-overline">{group}</Typography>}
                {nav.filter((item) => item[3] === group).map(([name, path, Icon, , workspace]) => {
                  const active = current[1] === path;
                  const flatIndex = nav.findIndex((item) => item[1] === path);
                  return (
                    <Tooltip key={path} title={collapsed ? name : ''} placement="right">
                      <Link
                        to={path}
                        className={active ? 'is-active' : ''}
                        ref={(node) => { navRefs.current[flatIndex] = node; }}
                        onKeyDown={(event) => onNavKeyDown(event, flatIndex)}
                        onClick={(event) => {
                          event.preventDefault();
                          navigateTo(objectApi, navigate, workspace);
                        }}
                      >
                        {active && (
                          <motion.span
                            className="os-active-pill"
                            layoutId="os-active-pill"
                            transition={{ duration: reduced ? 0 : 0.12, ease: 'easeOut' }}
                          />
                        )}
                        <Icon />
                        <AnimatePresence initial={false}>
                          {!collapsed && (
                            <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.12 }}>
                              {name}
                            </motion.span>
                          )}
                        </AnimatePresence>
                      </Link>
                    </Tooltip>
                  );
                })}
              </Box>
            ))}
          </nav>
          <Box className="os-sidebar-bottom">
            <Tooltip title={collapsed ? 'Settings' : ''} placement="right">
              <Button onClick={() => setProfileAnchor(document.querySelector('.os-profile'))} startIcon={<SettingsOutlined />}>
                {!collapsed && 'Settings'}
              </Button>
            </Tooltip>
            <Box className="os-connection">
              <motion.i
                animate={connected ? { opacity: [1, 0.5, 1] } : { opacity: [1, 0.35, 1] }}
                transition={{ repeat: Infinity, duration: connected ? 2.4 : 0.9 }}
              />
              {!collapsed && <Typography>{connected ? 'Live connection' : 'Reconnecting'}</Typography>}
            </Box>
          </Box>
        </motion.aside>
      </LayoutGroup>

      <Box className="os-stage">
        <a className="e6-skip-link" href="#main-content">Skip to main content</a>
        <header className="os-topbar" role="banner">
          <Stack direction="row" alignItems="center" spacing={1.25}>
            <Button className="os-command-trigger" onClick={() => setCommandOpen(true)} startIcon={<SearchOutlined />} endIcon={<kbd>⌘ K</kbd>} aria-label="Open command palette">
              Search assets, incidents, work orders…
            </Button>
            <Box className="os-top-context">
              <Typography>{WORKSPACE_LABELS[workspaceKey] || current[0]}</Typography>
              <Typography>{facility}</Typography>
            </Box>
          </Stack>
          <Stack direction="row" alignItems="center" spacing={0.5}>
            <Box className="os-ambient">
              <Typography>{clock.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</Typography>
              <Typography>
                {connected
                  ? `${ambient?.telemetry?.value ?? '—'}${ambient?.telemetry?.unit ? ` ${ambient.telemetry.unit}` : ''} · synced ${syncAge}s ago`
                  : 'reconnecting telemetry'}
              </Typography>
            </Box>
            <Tooltip title={connected ? 'Telemetry synchronized' : 'Synchronizing telemetry'}>
              <Button
                className={`os-sync ${connected ? 'is-ready' : ''}`}
                onClick={() => { setSyncAge(0); refresh(); }}
                startIcon={(
                  <motion.span animate={connected ? false : { rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}>
                    <SyncOutlined />
                  </motion.span>
                )}
              >
                {connected ? 'Synced' : 'Syncing'}
              </Button>
            </Tooltip>
            <Tooltip title={aiLabel}>
              <Button className="os-ai-status" onClick={() => setAssistantOpen(true)} startIcon={<SmartToyOutlined />}>
                <motion.i animate={agentsWorking ? { opacity: [1, 0.45, 1] } : false} transition={{ repeat: Infinity, duration: 1.6 }} />
                {aiLabel}
              </Button>
            </Tooltip>
            <Tooltip title="Notifications">
              <IconButton onClick={openInbox} aria-label="Open notifications">
                <Badge badgeContent={unread.length} color="error"><NotificationsOutlined /></Badge>
              </IconButton>
            </Tooltip>
            <Button className="os-profile" onClick={(event) => setProfileAnchor(event.currentTarget)}>
              <Avatar>CO</Avatar>
              <Box>
                <Typography>Control operator</Typography>
                <Typography>Shift A</Typography>
              </Box>
            </Button>
          </Stack>
        </header>
        <main id="main-content" tabIndex={-1}>
          <Box className="os-crumb" component="nav" aria-label="Breadcrumb">
            {crumbs.map((crumb, index) => (
              <Box key={`${crumb.label}-${index}`} component="span" sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.75 }}>
                {index > 0 && <Typography component="span" sx={{ opacity: 0.45 }} aria-hidden>›</Typography>}
                <Button
                  size="small"
                  onClick={() => crumb.workspace && navigateTo(objectApi, navigate, crumb.workspace, crumb.preserve || {})}
                  sx={{ minWidth: 0, textTransform: 'none', fontWeight: index === crumbs.length - 1 ? 800 : 600 }}
                  aria-current={index === crumbs.length - 1 ? 'page' : undefined}
                >
                  {crumb.label}
                </Button>
              </Box>
            ))}
          </Box>
          {children}
        </main>
        <Box
          ref={auditSpineRef}
          className="e5-audit-spine"
          tabIndex={-1}
          onKeyDown={(event) => {
            if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'e') {
              event.preventDefault();
              exportAuditLog({ events: auditEvents, facility });
            }
          }}
        >
          <AuditSpine events={auditEvents} />
          <Button size="small" onClick={() => exportAuditLog({ events: auditEvents, facility })} sx={{ flexShrink: 0, textTransform: 'none' }}>
            Export
          </Button>
        </Box>
      </Box>

      <Menu anchorEl={facilityAnchor} open={Boolean(facilityAnchor)} onClose={() => setFacilityAnchor(null)} PaperProps={{ className: 'os-menu' }}>
        {facilities.map((name) => (
          <MenuItem key={name} selected={name === facility} onClick={() => selectFacility(name)}>{name}</MenuItem>
        ))}
      </Menu>
      <Menu anchorEl={profileAnchor} open={Boolean(profileAnchor)} onClose={() => setProfileAnchor(null)} PaperProps={{ className: 'os-menu' }}>
        <MenuItem onClick={toggle}>{mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />} {mode === 'dark' ? 'Use light mode' : 'Use dark mode'}</MenuItem>
        <MenuItem onClick={() => { setProfileAnchor(null); setAssistantOpen(true); }}><SmartToyOutlined /> Ask RigOS AI</MenuItem>
      </Menu>

      <Dialog open={commandOpen} onClose={() => setCommandOpen(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'product-dialog os-command-dialog' }}>
        <Box className="product-command">
          <TextField
            autoFocus
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search assets, incidents, work orders, reports…"
            fullWidth
            InputProps={{
              startAdornment: <InputAdornment position="start"><SearchOutlined /></InputAdornment>,
              endAdornment: <InputAdornment position="end"><IconButton onClick={() => setCommandOpen(false)}><CloseOutlined /></IconButton></InputAdornment>,
            }}
          />
          {groups.map((group) => matches.some((item) => item.group === group) && (
            <Box key={group}>
              <Typography className="product-dialog-label">{group}</Typography>
              {matches.filter((item) => item.group === group).slice(0, 8).map((command) => {
                const flatIndex = matches.indexOf(command);
                const active = flatIndex === commandIndex;
                return (
                  <Button
                    key={`${command.group}-${command.label}`}
                    className={`product-command-item${active ? ' is-active' : ''}`}
                    startIcon={command.icon}
                    onMouseEnter={() => setCommandIndex(flatIndex)}
                    onClick={() => { command.run(); setCommandOpen(false); setQuery(''); }}
                  >
                    <Box textAlign="left">
                      <Typography fontWeight={700}>{command.label}</Typography>
                      {command.description && <Typography variant="caption" color="text.secondary">{command.description}</Typography>}
                    </Box>
                  </Button>
                );
              })}
            </Box>
          ))}
          {!matches.length && <Typography sx={{ p: 2, textAlign: 'center' }} color="text.secondary">No matches</Typography>}
        </Box>
      </Dialog>

      <Dialog open={inboxOpen} onClose={() => setInboxOpen(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'product-dialog product-notification-dialog' }}>
        <Box className="product-inbox">
          <Stack direction="row" justifyContent="space-between">
            <Box>
              <Typography className="product-dialog-label">OPERATOR INBOX</Typography>
              <Typography variant="h6">Live notifications</Typography>
            </Box>
            <IconButton onClick={() => setInboxOpen(false)}><CloseOutlined /></IconButton>
          </Stack>
          <Divider sx={{ my: 2 }} />
          {notifications.length ? notifications.map((item, index) => (
            <Box className="product-notification" key={item.id || index}>
              <Typography fontWeight={800}>{item.title}</Typography>
              <Typography variant="body2">{item.message}</Typography>
              <Typography variant="caption" color="text.secondary">{item.timestamp ? new Date(item.timestamp).toLocaleTimeString() : 'Live event'}</Typography>
            </Box>
          )) : (
            <Box className="product-inbox-empty">
              <NotificationsOutlined />
              <Typography fontWeight={700}>You’re all caught up</Typography>
            </Box>
          )}
        </Box>
      </Dialog>

      <Box className="workspace-dock" role="toolbar" aria-label="Workspace quick actions">
        <Tooltip title="Command palette (Ctrl K)"><IconButton onClick={() => setCommandOpen(true)}><SearchOutlined /></IconButton></Tooltip>
        <Tooltip title="AI copilot"><IconButton onClick={() => setAssistantOpen(true)}><SmartToyOutlined /></IconButton></Tooltip>
        <Tooltip title="Inspector and activity (Ctrl J)">
          <IconButton onClick={() => objectApi.toggleWorkspacePanel()}><ViewSidebarOutlined /></IconButton>
        </Tooltip>
        <Tooltip title="Pin current workspace">
          <IconButton
            onClick={() => {
              const entry = { label: current[0], path: current[1] };
              const next = pinned.some((item) => item.path === entry.path)
                ? pinned.filter((item) => item.path !== entry.path)
                : [...pinned, entry];
              objectApi.setPinnedRoutes(next);
            }}
          >
            <PushPinOutlined />
          </IconButton>
        </Tooltip>
      </Box>

      <AnimatePresence>
        {workspacePanel && (
          <motion.aside
            ref={workspacePanelRef}
            className="workspace-inspector is-open"
            data-focus-trap="true"
            role="dialog"
            aria-modal="true"
            aria-label="Workspace panel"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduced ? 0 : 0.12, ease: 'easeOut' }}
          >
            <Stack direction="row" justifyContent="space-between">
              <Box>
                <Typography className="product-dialog-label">WORKSPACE PANEL</Typography>
                <Typography fontWeight={800}>{current[0]} · audit & notifications</Typography>
              </Box>
              <IconButton onClick={() => objectApi.setWorkspacePanelOpen(false)} aria-label="Close workspace panel"><CloseOutlined /></IconButton>
            </Stack>
            <Box className="workspace-inspector-section">
              <Typography className="product-kicker">PINNED CONTEXT</Typography>
              {pinned.length
                ? pinned.map((item) => <Button key={item.path} onClick={() => navigate(item.path)}>{item.label}</Button>)
                : <Typography variant="body2" color="text.secondary">Pin an operational workspace to keep it one action away.</Typography>}
            </Box>
            <Box className="workspace-inspector-section">
              <Typography className="product-kicker">RECENT ACTIVITY</Typography>
              <Stack spacing={1}>
                {(operations.audit_logs || []).slice(0, 4).map((item, index) => (
                  <Box
                    className="workspace-activity"
                    key={item.id || index}
                    component="button"
                    type="button"
                    onClick={() => navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null })}
                    style={{ all: 'unset', cursor: 'pointer', display: 'flex', gap: 8 }}
                  >
                    <HistoryOutlined />
                    <Box>
                      <Typography>{label(item.incident_type || item.action_type || 'Operational update')}</Typography>
                      <Typography>{formatTime(item.timestamp || item.created_at)}</Typography>
                    </Box>
                  </Box>
                ))}
                {!(operations.audit_logs || []).length && (
                  <Typography variant="body2" color="text.secondary">No recent audit events. Telemetry monitoring remains active.</Typography>
                )}
              </Stack>
            </Box>
            <Box className="workspace-inspector-section">
              <Typography className="product-kicker">QUICK ACTIONS</Typography>
              <Button onClick={() => setAssistantOpen(true)}>Ask AI about this workspace</Button>
              <Button onClick={() => setCommandOpen(true)}>Navigate or run a command</Button>
            </Box>
          </motion.aside>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {assistantOpen && (
          <motion.aside
            className="copilot-dock"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduced ? 0 : 0.12, ease: 'easeOut' }}
          >
            <AssistantPanel onClose={() => setAssistantOpen(false)} />
          </motion.aside>
        )}
      </AnimatePresence>
    </Box>
  );
}
```

## frontend/src/redesign/reactbits.jsx

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/reactbits.jsx`

```javascript
import { Box } from '@mui/material';

// A minimal, repository-local ReactBits timeline shell for trace-oriented interfaces.
export function ReactBitsTimeline({ children }) {
  return <Box className="reactbits-timeline-shell" role="list" aria-label="AI investigation workflow">{children}</Box>;
}
```

## frontend/src/redesign/refinery-twin.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/refinery-twin.css`

```css
.refinery-twin{padding:14px;border:1px solid rgba(148,163,184,.13);border-radius:12px;background:#0c1016}.refinery-twin-value{color:#9bc3ff;font:600 .7rem "DM Mono",monospace}.refinery-twin svg{display:block;width:100%;margin-top:6px}.twin-pipeline{fill:none;stroke:rgba(138,166,201,.26);stroke-width:10;stroke-linecap:round}.twin-flow{fill:none;stroke:#5f9dff;stroke-width:2;stroke-linecap:round;stroke-dasharray:5 11;animation:twin-flow 1.8s linear infinite}.twin-tank{fill:#111a25;stroke:rgba(139,176,230,.48);stroke-width:2}.twin-pump circle,.twin-valve circle{fill:#111a25;stroke:#79aefd;stroke-width:2}.twin-pump path,.twin-valve path{stroke:#9fc6ff;stroke-width:2;fill:none}.twin-pump{transform-origin:215px 98px;animation:twin-pump 2.6s linear infinite}.twin-valve.closed circle,.refinery-twin.risk .twin-valve circle{stroke:#f2ab4c}.twin-output{fill:#42cc9b;animation:twin-output 1.7s ease-in-out infinite}.refinery-twin-legend{display:flex;gap:14px;flex-wrap:wrap}.refinery-twin-legend p{display:flex;align-items:center;gap:5px;color:#8fa0b8;font-size:.6rem}.refinery-twin-legend i{width:6px;height:6px;border-radius:50%}.refinery-twin-legend .tank{background:#5f9dff}.refinery-twin-legend .pump{background:#a989ff}.refinery-twin-legend .valve{background:#42cc9b}@keyframes twin-flow{to{stroke-dashoffset:-32}}@keyframes twin-pump{to{transform:rotate(360deg)}}@keyframes twin-output{50%{opacity:.38;transform:scale(.78)}}@media(prefers-reduced-motion:reduce){.twin-flow,.twin-pump,.twin-output{animation:none}}
```

## frontend/src/redesign/twin.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/twin.css`

```css
.twin-toolbar{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:20px}.twin-toolbar .product-toolbar-title{margin:4px 0 6px;font-size:1.6rem;font-weight:800;letter-spacing:-.045em}.twin-toolbar .MuiOutlinedInput-root{background:#11161e;border-radius:10px}.twin-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.twin-card{display:grid;gap:15px;padding:17px;border:1px solid rgba(148,163,184,.14);border-radius:15px;background:#10151c;cursor:pointer;overflow:hidden}.twin-card:hover{border-color:rgba(111,165,255,.34);background:#121923}.twin-card.risk{border-color:rgba(242,169,73,.32)}.twin-card-title{margin-top:6px!important;font-size:1.1rem!important;font-weight:800!important;letter-spacing:-.04em}.twin-card-instrument{display:flex;align-items:center;gap:14px;padding:10px 0;border-top:1px solid rgba(148,163,184,.1);border-bottom:1px solid rgba(148,163,184,.1)}.twin-gauge{width:112px;flex:none}.twin-gauge svg{display:block;width:100%;overflow:visible}.twin-gauge-track{fill:none;stroke:rgba(148,163,184,.16);stroke-width:8;stroke-linecap:round}.twin-gauge-value{fill:none;stroke:#42c99a;stroke-width:8;stroke-linecap:round}.twin-gauge.warn .twin-gauge-value{stroke:#f2a949}.twin-gauge-needle{stroke:#dbe7f6;stroke-width:2;stroke-linecap:round}.twin-gauge circle{fill:#dbe7f6}.twin-gauge>p{margin-top:-2px;color:#8090a7;font-size:.56rem!important;font-weight:800;letter-spacing:.1em;text-align:center}.twin-health-copy p:first-child{font-size:1.8rem;font-weight:850;letter-spacing:-.07em}.twin-health-copy p:nth-child(2){color:#8393aa;font-size:.66rem}.twin-health-copy i{display:block;width:84px;height:4px;margin-top:10px;border-radius:8px;background:#57a0ff;transform-origin:left}.twin-readings{display:grid;grid-template-columns:1fr 1fr;gap:8px}.twin-readings>div{padding:8px;border-radius:8px;background:#0c1016}.twin-readings p:first-child{color:#77879e;font-size:.57rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase}.twin-readings p:last-child{margin-top:4px;color:#dde7f4;font:600 .74rem "DM Mono",monospace}.twin-ai{display:flex;justify-content:space-between;gap:12px;padding:10px;border-left:2px solid #5e9fff;border-radius:0 8px 8px 0;background:rgba(79,140,255,.055)}.twin-ai>div:first-child p:last-child{margin-top:5px;color:#b8c5d7;font-size:.7rem;line-height:1.42}.twin-ai-score{text-align:right;white-space:nowrap}.twin-ai-score p:first-child{color:#94bfff;font-weight:850;font-size:.9rem}.twin-ai-score p:last-child{color:#8090a7;font-size:.58rem}.twin-card-footer{display:grid;grid-template-columns:1fr 1.3fr;gap:4px;color:#8393aa;font-size:.6rem}.twin-card-footer b{color:#cbd7e7;font-weight:750}.twin-inspect{grid-column:1/-1;margin-top:4px;color:#83b4ff;font-weight:750}.twin-empty{position:relative;display:grid;place-content:center;justify-items:center;min-height:360px;gap:9px;border:1px dashed rgba(148,163,184,.22);border-radius:16px;background:#0d1117;text-align:center;overflow:hidden}.twin-empty p:last-child{max-width:410px;color:#91a0b5}.twin-empty-orbit{width:72px;height:72px;border:1px solid rgba(99,159,255,.34);border-radius:50%;box-shadow:0 0 0 12px rgba(99,159,255,.035),0 0 0 28px rgba(99,159,255,.025);animation:twin-orbit 3s ease-in-out infinite}.twin-drawer{width:min(510px,100vw)!important;background:#10151c!important;border-left:1px solid rgba(148,163,184,.15)!important;color:#eef4fc!important}.twin-drawer-content{display:grid;gap:20px;padding:24px}.twin-drawer-title{margin-top:6px!important;font-size:1.7rem!important;font-weight:850!important;letter-spacing:-.06em}.twin-drawer-gauges{display:flex;align-items:center;justify-content:space-between;padding:15px;border-radius:12px;background:#0c1016}.twin-drawer-gauges .health{width:180px}.twin-drawer-telemetry{padding:13px;border:1px solid rgba(148,163,184,.1);border-radius:12px;background:#0c1016}.twin-drawer-telemetry .mini-graph{margin-top:10px}@keyframes twin-orbit{50%{transform:scale(.94);border-color:rgba(99,159,255,.62)}}@media(max-width:1160px){.twin-card-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:720px){.twin-toolbar{align-items:stretch;flex-direction:column}.twin-card-grid{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){.twin-empty-orbit{animation:none}}
```

## frontend/src/redesign/workspace-twin.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/workspace-twin.css`

```css
/* Digital twin workspace */
.twin-workspace{display:grid;gap:14px}.twin-workspace-head{display:flex;align-items:end;justify-content:space-between;gap:16px}.twin-workspace-title{margin-top:4px!important;font-size:1.35rem!important;font-weight:820!important;letter-spacing:-.045em}.twin-workspace-head .MuiOutlinedInput-root,.asset-explorer .MuiOutlinedInput-root{background:#0c1016;border-radius:9px}.twin-workspace-grid{display:grid;grid-template-columns:250px minmax(420px,1fr) 290px;gap:12px;min-height:570px}.asset-explorer,.twin-canvas,.twin-inspector,.twin-bottom{background:#10151c!important;border:1px solid rgba(148,163,184,.14)!important;box-shadow:none!important;border-radius:14px!important}.asset-explorer{display:flex;flex-direction:column;min-width:0;padding:14px!important;overflow:hidden}.asset-explorer-top,.twin-canvas-top,.twin-inspector-head{display:flex;align-items:start;justify-content:space-between;gap:8px}.asset-explorer .MuiTextField-root{margin-top:13px}.asset-explorer .MuiInputBase-input{font-size:.72rem}.asset-explorer-controls{display:flex;align-items:center;justify-content:space-between;margin:10px 0 8px}.asset-explorer-controls .MuiButton-root{min-width:0;padding:3px 0!important;color:#94bfff;font-size:.62rem!important;text-transform:none}.asset-explorer-controls>p{color:#718096;font:600 .6rem 'DM Mono',monospace}.asset-tree{display:grid;gap:13px;overflow:auto;padding-right:2px}.asset-tree-group{display:grid;gap:3px}.asset-tree-parent{display:flex;align-items:center;gap:6px;padding:3px 5px;color:#8293aa;font-size:.62rem!important;font-weight:800!important;letter-spacing:.04em;text-transform:uppercase}.asset-tree-parent span{font-size:.9rem}.asset-tree-parent b{margin-left:auto;color:#64748b;font-size:.58rem}.asset-tree-item{display:flex;align-items:center;gap:7px;width:100%;padding:7px 6px;border:0;border-radius:7px;background:transparent;color:#c9d5e6;cursor:pointer;text-align:left}.asset-tree-item:hover{background:rgba(255,255,255,.045)}.asset-tree-item.selected{background:rgba(79,140,255,.13);box-shadow:inset 2px 0 #67a3ff}.asset-tree-dot{width:6px;height:6px;border-radius:50%;background:#45c998;box-shadow:0 0 0 3px rgba(69,201,152,.1);flex:none}.asset-tree-dot.watch{background:#f0ac4f}.asset-tree-dot.critical{background:#ee7373;animation:asset-alert 1.6s ease infinite}.asset-tree-item span:nth-child(2){display:grid;gap:2px;min-width:0}.asset-tree-item b{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:.69rem}.asset-tree-item small{overflow:hidden;color:#7f90a8;font-size:.56rem;white-space:nowrap}.asset-tree-item em{margin-left:auto;color:#9bbef5;font:700 .62rem 'DM Mono',monospace;font-style:normal}
.twin-canvas{position:relative;display:grid;grid-template-rows:auto 1fr auto;min-width:0;overflow:hidden}.twin-canvas-top{padding:15px 16px;border-bottom:1px solid rgba(148,163,184,.1)}.twin-canvas-top>div>p:last-child{margin-top:4px;color:#b9c5d8;font-size:.74rem}.twin-canvas-top .MuiIconButton-root{color:#94a7c1}.twin-zoom{display:grid;place-items:center;min-width:34px;color:#8fa8ca;font:600 .6rem 'DM Mono',monospace}.twin-process-map{position:relative;min-height:420px;overflow:hidden;background:radial-gradient(circle at 52% 45%,rgba(77,141,255,.13),transparent 36%),#0c1016}.twin-process-map>svg{position:absolute;inset:5% 4%;width:92%;height:90%;transform:scale(var(--twin-zoom));transition:transform .25s ease}.twin-grid-lines{position:absolute;inset:0;opacity:.45;background-image:linear-gradient(rgba(112,145,191,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(112,145,191,.08) 1px,transparent 1px);background-size:24px 24px;mask-image:radial-gradient(circle at center,black,transparent 82%)}.map-pipe{fill:none;stroke:rgba(112,146,193,.26);stroke-width:15;stroke-linecap:round;stroke-linejoin:round}.map-flow{stroke:#5c9dff;stroke-width:3;stroke-dasharray:6 14;animation:map-flow 2s linear infinite}.map-tank,.map-unit{fill:#101924;stroke:rgba(117,171,255,.54);stroke-width:2}.map-level{fill:rgba(82,155,255,.32)}.map-pump{fill:#121c29;stroke:#71aaff;stroke-width:2}.map-pump-spoke,.map-stack{fill:none;stroke:#9fc4fa;stroke-width:2}.twin-map-node{position:absolute;z-index:2;display:flex;align-items:center;gap:5px;padding:6px 8px;border:1px solid rgba(95,156,255,.28);border-radius:8px;background:#141d2a;color:#dce9f9;cursor:pointer;box-shadow:0 5px 14px rgba(0,0,0,.17)}.twin-map-node:hover,.twin-map-node.selected{border-color:#76aeff;background:#18263a;box-shadow:0 0 0 3px rgba(92,157,255,.1)}.twin-map-node i{width:6px;height:6px;border-radius:50%;background:#45c998}.twin-map-node.critical i{background:#ec7373;animation:asset-alert 1.6s ease infinite}.twin-map-node span{max-width:105px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:.61rem;font-weight:760}.twin-map-node b{color:#8fc1ff;font:700 .59rem 'DM Mono',monospace}.node-0{left:7%;top:52%}.node-1{left:28%;top:20%}.node-2{left:47%;top:51%}.node-3{right:21%;top:20%}.node-4{right:5%;bottom:22%}.twin-map-legend{position:absolute;bottom:11px;left:15px;display:flex;gap:11px}.twin-map-legend p{display:flex;align-items:center;gap:4px;color:#8293a9;font-size:.57rem}.twin-map-legend i{width:5px;height:5px;border-radius:50%;background:#45c998}.twin-map-legend .warn{background:#f0ac4f}.twin-map-legend .risk{background:#ee7373}.twin-canvas-footer{display:flex;align-items:center;gap:15px;padding:10px 15px;border-top:1px solid rgba(148,163,184,.1);overflow:auto}.twin-canvas-footer p{display:flex;align-items:center;gap:5px;white-space:nowrap;color:#8496af;font-size:.6rem}.twin-canvas-footer svg{font-size:.8rem;color:#70a8ff}
.twin-inspector{display:grid;align-content:start;gap:15px;padding:15px!important;overflow:auto}.twin-inspector-title{margin:5px 0 2px!important;font-size:1.1rem!important;font-weight:830!important;letter-spacing:-.04em}.twin-inspector-head .MuiTypography-caption{color:#8192aa;font-size:.61rem}.inspector-status{display:grid;grid-template-columns:1fr 1fr;gap:8px}.inspector-status>div{min-width:0;padding:10px;border:1px solid rgba(148,163,184,.1);border-radius:10px;background:#0c1016}.inspector-status>div>p:first-child,.inspector-metrics p{color:#7f90a8;font-size:.58rem!important;font-weight:800!important;letter-spacing:.07em;text-transform:uppercase}.inspector-status b{display:block;margin:5px 0;color:#e3edf9;font-size:1.15rem;letter-spacing:-.05em}.inspector-status .health{gap:4px}.inspector-status .health>div{height:4px}.inspector-status .health p{font-size:.58rem!important}.risk-text{color:#f19a68!important}.inspector-status .MuiTypography-caption{color:#f0af63;font-size:.58rem}.inspector-metrics{display:grid;grid-template-columns:1fr 1fr;gap:7px}.inspector-metrics>div{padding:8px;border-bottom:1px solid rgba(148,163,184,.1)}.inspector-metrics b{display:block;margin-top:4px;color:#d9e5f4;font:650 .73rem 'DM Mono',monospace}.inspector-metrics small{margin-left:3px;color:#8292aa;font-size:.55rem}.inspector-prediction,.inspector-recommendation{padding:11px;border-radius:10px;background:#0c1016}.inspector-prediction>p:nth-child(2){margin-top:6px;color:#b9c8db;font-size:.68rem}.inspector-prediction b{color:#9dc5ff}.inspector-prediction>div{height:4px;margin:9px 0 5px;border-radius:99px;background:rgba(148,163,184,.14);overflow:hidden}.inspector-prediction span{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#f09c59,#5d9dff)}.inspector-prediction .MuiTypography-caption{color:#8292aa;font-size:.56rem}.inspector-recommendation{border-left:2px solid #609fff;background:rgba(79,140,255,.055)}.inspector-recommendation>p:last-child{margin-top:6px;color:#b9c8da;font-size:.66rem;line-height:1.45}
.twin-bottom{overflow:hidden}.twin-bottom-tabs{display:flex;gap:1px;overflow:auto;padding:4px 8px;border-bottom:1px solid rgba(148,163,184,.1)}.twin-bottom-tabs .MuiButton-root{min-width:max-content;padding:8px 9px!important;color:#8496ad!important;font-size:.63rem!important;text-transform:none!important}.twin-bottom-tabs .MuiButton-root.active{color:#cfe2ff!important;border-bottom:2px solid #67a5ff;border-radius:0}.twin-bottom-body{display:grid;grid-template-columns:1.65fr 1fr;gap:18px;padding:15px}.twin-bottom-title{margin:4px 0 9px!important;font-size:.83rem!important;font-weight:790!important}.twin-bottom .mini-graph{margin:0}.twin-bottom-events{display:grid;align-content:start;gap:10px}.twin-bottom-events>p:not(:first-child){display:flex;align-items:center;gap:6px;color:#95a6bc;font-size:.64rem}.twin-bottom-events b{margin-left:auto;color:#ced9e8;font-weight:700}.event-dot{width:6px;height:6px;border-radius:50%;background:#62a1ff}.event-dot.active{background:#4dd09e}.event-dot.risk{background:#ef9a62}.event-dot.doc{background:#a986ee}@keyframes map-flow{to{stroke-dashoffset:-40}}@keyframes asset-alert{50%{opacity:.35;box-shadow:0 0 0 5px rgba(238,115,115,.12)}}@media(max-width:1220px){.twin-workspace-grid{grid-template-columns:220px minmax(360px,1fr)}.twin-inspector{grid-column:1/-1;grid-template-columns:repeat(3,1fr)}.twin-inspector-head{grid-column:1/-1}.inspector-recommendation{grid-column:span 2}.twin-process-map{min-height:400px}}@media(max-width:850px){.twin-workspace-grid{grid-template-columns:1fr}.asset-explorer{max-height:320px}.twin-inspector{grid-column:auto}.twin-bottom-body{grid-template-columns:1fr}.twin-workspace-head{align-items:start;flex-direction:column}.twin-process-map{min-height:370px}}@media(max-width:520px){.twin-inspector{grid-template-columns:1fr}.inspector-recommendation{grid-column:auto}.twin-map-node span{max-width:56px}.twin-map-node{padding:5px}.twin-map-legend{display:none}.twin-canvas-footer{gap:9px}.twin-bottom-body{padding:12px}.node-1{left:25%}.node-3{right:13%}}@media(prefers-reduced-motion:reduce){.map-flow,.asset-tree-dot.critical,.twin-map-node.critical i{animation:none}}
```

## frontend/src/redesign/workspace.css

**Folder path:** `frontend/src/redesign`

**File path:** `frontend/src/redesign/workspace.css`

```css
.workspace-dock{position:fixed;z-index:1300;left:50%;bottom:18px;display:flex;gap:4px;padding:5px;border:1px solid rgba(148,163,184,.17);border-radius:13px;background:rgba(16,21,28,.9);box-shadow:0 14px 38px rgba(0,0,0,.25);backdrop-filter:blur(16px);transform:translateX(-50%)}.workspace-dock .MuiIconButton-root{color:#a9bad0}.workspace-dock .MuiIconButton-root:hover{color:#edf4ff;background:rgba(95,154,255,.12)}.workspace-inspector{position:fixed;z-index:1350;top:78px;right:18px;bottom:18px;width:min(350px,calc(100vw - 36px));padding:18px;border:1px solid rgba(148,163,184,.17);border-radius:15px;background:#10151c;box-shadow:-18px 20px 60px rgba(0,0,0,.34);overflow:auto}.workspace-inspector-section{display:grid;gap:8px;margin-top:19px;padding-top:15px;border-top:1px solid rgba(148,163,184,.11)}.workspace-inspector-section>.MuiButton-root{justify-content:flex-start;padding:7px 8px;color:#c3d0e1;text-transform:none}.workspace-activity{display:flex;gap:9px;align-items:start;padding:8px;border-radius:8px;background:#0c1016}.workspace-activity>svg{margin-top:2px;color:#7daeff;font-size:17px}.workspace-activity p:first-child{font-size:.7rem;font-weight:750}.workspace-activity p:last-child{margin-top:3px;color:#7e90a9;font-size:.58rem}@media(max-width:680px){.workspace-inspector{top:66px;right:0;bottom:0;width:100%;border-radius:0}.workspace-dock{bottom:10px}}
```

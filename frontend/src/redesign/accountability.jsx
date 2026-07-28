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
      outputs: stage.outputs || stage.output || stage.recommendation || (confidence != null ? `${confidence.toFixed(2)}% confidence finding` : null),
      modelId: stage.model_id || stage.modelId || investigation.model_id || 'gemini-flash · MAO',
      duration: stage.duration_seconds != null
        ? (Number(stage.duration_seconds) < 1
          ? `${Math.max(0.01, Number(stage.duration_seconds) * 1000).toFixed(2)} ms`
          : `${Number(stage.duration_seconds).toFixed(2)} s`)
        : stage.duration || null,
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
    facts.push({ id: 'conf', type: 'model', label: `${conf.toFixed(2)}% confidence`, detail: 'investigation aggregate' });
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
    what: action.note || action.title || action.action_type || action.status || 'Operator action',
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
  const seen = new Set();
  return [...fromSession, ...fromActions, ...fromLogs].filter((event) => {
    const key = event.id || `${event.when}-${event.what}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, 12);
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
    const seen = new Set();
    const pushAction = (action) => {
      const key = action.id || `${action.timestamp}-${action.action_type}`;
      if (seen.has(key)) return;
      seen.add(key);
      actions.push(action);
    };
    (operations.audit_logs || []).forEach((log) => {
      (log.operator_actions || []).forEach((action) => {
        pushAction({ ...action, incident_id: action.incident_id || log.id });
      });
    });
    if (Array.isArray(operations.operator_actions)) {
      operations.operator_actions.forEach(pushAction);
    }
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

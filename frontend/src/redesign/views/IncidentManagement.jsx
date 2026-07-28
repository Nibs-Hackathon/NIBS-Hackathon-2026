import { useCallback, useEffect, useRef, useState } from 'react';
import { Box, Button, MenuItem, Paper, Stack, TextField, Typography } from '@mui/material';
import {
  ArticleOutlined, DevicesOutlined, ExpandMoreOutlined,
  MemoryOutlined, SearchOutlined,
  ShieldOutlined, WarningAmberOutlined,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import toast from 'react-hot-toast';
import { useWorkspace } from '../../context/WorkspaceContext';
import { useObjectContext } from '../../context/ObjectContext';
import { useOperations } from '../../context/OperationsContext';
import { navigateTo } from '../../context/objectNavigation';
import { getIncidentAuditDetail, getTelemetry, triggerIncident } from '../../api/client';
import {
  timelineFromAudit,
  incidentTelemetryWindow,
  normalizeTelemetryReadings,
  decisionEntriesFromIncident,
} from '../../api/resourceAdapters';
import {
  OperatorDecisionBar, EvidenceLineage, buildEvidenceFacts, DecisionHistory, ProvenanceBadge,
} from '../accountability';
import { Status, MiniGraph, EvidenceItem, formatTime, label, round, safeReasoning } from './shared';

function riskScore(severity) {
  if (/critical/i.test(severity || '')) return 92;
  if (/high/i.test(severity || '')) return 76;
  if (/medium/i.test(severity || '')) return 54;
  return 28;
}

function confidencePercent(incident) {
  if (incident?.confidence == null) return null;
  const value = Number(incident.confidence);
  return (value <= 1 ? value * 100 : value).toFixed(2);
}

const SIMULATOR_FAULTS = [
  { type: 'pressure-spike', label: 'Pressure spike' },
  { type: 'gas-leak', label: 'Gas leak' },
  { type: 'high-vibration', label: 'High vibration' },
  { type: 'high-temperature', label: 'High temperature' },
  { type: 'flow-restriction', label: 'Flow restriction' },
];

export function IncidentManagement({ incidents, telemetry, provenance = 'live' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const { refresh } = useOperations();
  const timelineRef = useRef(null);
  const [query, setQuery] = useState('');
  const [severity, setSeverity] = useState('all');
  const { workspace, setWorkspaceValue } = useWorkspace();
  const selectedId = objectApi.selection.incidentId ?? workspace.incidentSelection ?? null;
  const setSelectedId = (id) => {
    objectApi.setSelection({ incidentId: id });
    setWorkspaceValue('incidentSelection', id);
  };
  const [reasoning, setReasoning] = useState(false);
  const [auditDetail, setAuditDetail] = useState(null);
  const [auditLoading, setAuditLoading] = useState(false);
  const [replayReadings, setReplayReadings] = useState([]);
  const [replayLoading, setReplayLoading] = useState(false);
  const [evidenceMode, setEvidenceMode] = useState('live');
  const [simulating, setSimulating] = useState(false);

  const visible = incidents.filter(
    (item) => `${item.incident_type || ''} ${item.asset_name || ''} ${item.severity || ''}`.toLowerCase().includes(query.toLowerCase())
      && (severity === 'all' || String(item.severity).toLowerCase() === severity),
  );
  const incident = visible.find((item) => item.id === selectedId) || visible[0];
  const activeIncident = auditDetail?.id === incident?.id ? { ...incident, ...auditDetail } : incident;

  useEffect(() => {
    if (!incident?.id) {
      setAuditDetail(null);
      return undefined;
    }
    let cancelled = false;
    setAuditLoading(true);
    getIncidentAuditDetail(incident.id)
      .then((response) => {
        if (!cancelled) setAuditDetail(response.data);
      })
      .catch(() => {
        if (!cancelled) setAuditDetail(null);
      })
      .finally(() => {
        if (!cancelled) setAuditLoading(false);
      });
    return () => { cancelled = true; };
  }, [incident?.id]);

  useEffect(() => {
    const assetId = activeIncident?.asset_id;
    const window = incidentTelemetryWindow(activeIncident);
    if (!assetId || !window) {
      setReplayReadings([]);
      return undefined;
    }
    let cancelled = false;
    setReplayLoading(true);
    getTelemetry(assetId, { limit: 120, since: window.since, until: window.until })
      .then((response) => {
        if (!cancelled) setReplayReadings(normalizeTelemetryReadings(response.data));
      })
      .catch(() => {
        if (!cancelled) setReplayReadings([]);
      })
      .finally(() => {
        if (!cancelled) setReplayLoading(false);
      });
    return () => { cancelled = true; };
  }, [activeIncident?.id, activeIncident?.asset_id, activeIncident?.timestamp, activeIncident?.created_at, activeIncident?.resolved_at]);

  useEffect(() => {
    if (!incident?.id) return undefined;
    const timer = requestAnimationFrame(() => timelineRef.current?.querySelector?.('.incident-event')?.scrollIntoView?.({ block: 'nearest', behavior: 'smooth' }));
    return () => cancelAnimationFrame(timer);
  }, [incident?.id]);

  const injectFault = useCallback(async (faultType) => {
    setSimulating(true);
    try {
      await triggerIncident(faultType);
      toast.success('Simulator fault injected — refreshing incident queue');
      await refresh();
    } catch (error) {
      const detail = error.response?.data?.detail || error.response?.data?.error;
      toast.error(typeof detail === 'string' ? detail : 'Could not inject simulator fault');
    } finally {
      setSimulating(false);
    }
  }, [refresh]);

  if (!incident) {
    return (
      <Box className="twin-empty">
        <WarningAmberOutlined fontSize="large" />
        <Typography fontWeight={800}>No incident records in this view</Typography>
        <Typography variant="body2">The live incident queue will populate when detection or operator escalation creates a case.</Typography>
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mt: 2 }}>
          {SIMULATOR_FAULTS.map((fault) => (
            <Button
              key={fault.type}
              size="small"
              variant="outlined"
              disabled={simulating}
              onClick={() => injectFault(fault.type)}
            >
              {simulating ? 'Injecting…' : `Simulate ${fault.label.toLowerCase()}`}
            </Button>
          ))}
        </Stack>
      </Box>
    );
  }

  const confidence = confidencePercent(activeIncident);
  const risk = riskScore(activeIncident.severity);
  const liveReadings = telemetry?.readings || [];
  const displayReadings = evidenceMode === 'replay' && replayReadings.length ? replayReadings : liveReadings;
  const auditTimeline = timelineFromAudit(activeIncident);
  const events = auditTimeline.length
    ? auditTimeline.map((step) => [step.title, step.time, step.detail, step.kind])
    : [
      ['Detection', activeIncident.timestamp || activeIncident.created_at, label(activeIncident.incident_type || 'Anomaly detected'), 'alert'],
      ['Evidence', null, activeIncident.evidence || 'Awaiting evidence from the audit record.', 'signal'],
    ];
  const pendingRec = Boolean(activeIncident.ai_recommendation || activeIncident.status !== 'closed');
  const operatorActions = Array.isArray(activeIncident.operator_actions) ? activeIncident.operator_actions : [];
  const sessionDecisions = objectApi.audit?.recentDecisions?.filter(
    (entry) => !incident?.id || entry.incidentId === incident.id,
  ) || [];
  const decisionEntries = decisionEntriesFromIncident(activeIncident, sessionDecisions);
  const persistedNotes = operatorActions.filter((action) => action.note);

  return (
    <Box className="incident-os">
      <Box className="incident-os-head">
        <Box>
          <Typography className="product-kicker">INCIDENT MANAGEMENT</Typography>
          <Typography className="incident-os-title">Active investigation workspace</Typography>
          {auditLoading && (
            <Typography variant="caption" color="text.secondary">Loading audit record…</Typography>
          )}
        </Box>
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          {SIMULATOR_FAULTS.map((fault) => (
            <Button
              key={fault.type}
              size="small"
              variant="outlined"
              disabled={simulating}
              onClick={() => injectFault(fault.type)}
            >
              {simulating ? 'Injecting…' : `Simulate ${fault.label.toLowerCase()}`}
            </Button>
          ))}
        </Stack>
      </Box>

      <Box className="incident-os-grid">
        <Paper className="incident-queue">
          <Box className="incident-queue-head">
            <Box>
              <Typography className="product-kicker">INCIDENT QUEUE</Typography>
              <Typography>{visible.length} active cases</Typography>
            </Box>
          </Box>
          <TextField size="small" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search cases" slotProps={{ input: { startAdornment: <SearchOutlined fontSize="small" /> } }} />
          <TextField select size="small" value={severity} onChange={(e) => setSeverity(e.target.value)}>
            <MenuItem value="all">All severities</MenuItem>
            <MenuItem value="critical">Critical</MenuItem>
            <MenuItem value="high">High</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
          </TextField>
          <Box className="incident-queue-list" tabIndex={0} onKeyDown={(event) => {
            if (!visible.length) return;
            const ids = visible.map((item) => item.id);
            const idx = Math.max(0, ids.indexOf(selectedId));
            if (event.key === 'ArrowDown') { event.preventDefault(); setSelectedId(ids[Math.min(ids.length - 1, idx + 1)]); }
            if (event.key === 'ArrowUp') { event.preventDefault(); setSelectedId(ids[Math.max(0, idx - 1)]); }
            if (event.key === 'Enter' && ids[idx]) setSelectedId(ids[idx]);
          }}
          >
            {visible.map((item, index) => (
              <button type="button" onClick={() => setSelectedId(item.id)} key={item.id || index} className={`incident-queue-item ${incident.id === item.id ? 'selected' : ''}`}>
                <Box>
                  <Status state={item.severity || item.status || 'open'} />
                  <Typography>{formatTime(item.timestamp || item.created_at)}</Typography>
                </Box>
                <b>{label(item.incident_type || 'Operational event')}</b>
                <Typography>{item.asset_name || item.asset_id || 'Asset identification pending'}</Typography>
                <Box>
                  <span>Severity risk {riskScore(item.severity)}</span>
                  <span>{confidencePercent(item) != null ? `${confidencePercent(item)}% confidence` : 'Confidence pending'}</span>
                </Box>
              </button>
            ))}
          </Box>
        </Paper>

        <Paper className="investigation-timeline p8-inspector-swap" key={incident.id} ref={timelineRef}>
          <Box className="investigation-head">
            <Box>
              <Typography className="product-kicker">INCIDENT TIMELINE</Typography>
              <Typography className="investigation-title">{label(activeIncident.incident_type || 'Operational event')}</Typography>
              <Typography variant="caption">
                Case {activeIncident.id || 'under review'} — affected asset:{' '}
                <Button size="small" onClick={() => activeIncident.asset_id && navigateTo(objectApi, navigate, 'assets', { assetId: activeIncident.asset_id })}>
                  {activeIncident.asset_name || activeIncident.asset_id || 'unresolved'}
                </Button>
              </Typography>
              <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                <Button size="small" variant="contained" onClick={() => navigateTo(objectApi, navigate, 'investigation', { incidentId: activeIncident.id, assetId: activeIncident.asset_id || null, focusDecisionBar: true })}>
                  View investigation
                </Button>
              </Stack>
            </Box>
            <Status state={activeIncident.status || activeIncident.severity || 'open'} />
          </Box>
          <Box className="incident-summary-strip">
            <Box><Typography>Severity</Typography><b>{label(activeIncident.severity || 'Medium')}</b><ProvenanceBadge value={provenance} /></Box>
            <Box><Typography>Severity risk</Typography><b className="risk-text">{risk}/100</b><Typography variant="caption" color="text.secondary">Derived from severity</Typography></Box>
            <Box><Typography>Impact</Typography><b>{activeIncident.impact || 'Production exposure'}</b></Box>
            <Box><Typography>Confidence</Typography><b>{confidence != null ? `${confidence}%` : '—'}</b></Box>
          </Box>
          <Box className="incident-timeline">
            {events.map(([title, time, detail, kind], index) => (
              <Box className={`incident-event ${kind}`} key={`${title}-${index}`}>
                <span>{index + 1}</span>
                <Box>
                  <Typography>{title}<small>{time ? formatTime(time) : 'live evidence stream'}</small></Typography>
                  <Typography>{detail}</Typography>
                  {title === 'Agent finding' && (
                    <Button size="small" onClick={() => setReasoning(!reasoning)} endIcon={<ExpandMoreOutlined />}>
                      {reasoning ? 'Collapse reasoning' : 'Expand reasoning'}
                    </Button>
                  )}
                  {title === 'Agent finding' && reasoning && (
                    <motion.div className="incident-reasoning" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} transition={{ duration: 0.12 }}>
                      {safeReasoning(activeIncident.reasoning || activeIncident.execution_report?.summary || 'No expanded reasoning recorded.')}
                    </motion.div>
                  )}
                </Box>
              </Box>
            ))}
          </Box>
        </Paper>

        <Paper className="incident-evidence">
          <Box className="incident-evidence-head">
            <Box>
              <Typography className="product-kicker">EVIDENCE</Typography>
              <Typography>Live case record</Typography>
            </Box>
          </Box>
          <Box className="evidence-snapshot">
            <Box>
              <Typography className="product-kicker">SENSOR SNAPSHOT</Typography>
              <Typography>
                {displayReadings.length
                  ? (evidenceMode === 'replay' ? 'Incident window replay' : 'Current historian window')
                  : 'No telemetry samples attached'}
              </Typography>
              {replayReadings.length > 0 && (
                <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                  <Button
                    size="small"
                    variant={evidenceMode === 'live' ? 'contained' : 'outlined'}
                    onClick={() => setEvidenceMode('live')}
                  >
                    Live
                  </Button>
                  <Button
                    size="small"
                    variant={evidenceMode === 'replay' ? 'contained' : 'outlined'}
                    onClick={() => setEvidenceMode('replay')}
                    disabled={replayLoading}
                  >
                    {replayLoading ? 'Loading replay…' : `Replay (${replayReadings.length})`}
                  </Button>
                </Stack>
              )}
            </Box>
            <MiniGraph
              values={displayReadings.map((reading) => reading.value)}
              area
              label={displayReadings.length
                ? `${displayReadings.length} captured samples`
                : 'No telemetry samples attached'}
            />
          </Box>
          <Box className="evidence-list">
            <EvidenceItem icon={<DevicesOutlined />} label="Sensor snapshots" detail={activeIncident.evidence ? 'Evidence packet attached' : 'Awaiting historian attachment'} />
            <EvidenceItem icon={<MemoryOutlined />} label="Agent findings" detail={confidence != null ? `${confidence}% corroborated confidence` : 'Confidence not recorded'} />
            <EvidenceItem icon={<ArticleOutlined />} label="Execution report" detail={activeIncident.execution_report?.summary ? 'Report attached' : 'No execution report yet'} />
            <EvidenceItem icon={<ShieldOutlined />} label="Audit trail" detail={`${operatorActions.length} operator actions recorded`} />
          </Box>
          <Box className="root-cause">
            <Typography className="product-kicker">ROOT CAUSE HYPOTHESIS</Typography>
            <Typography>{activeIncident.root_cause || activeIncident.reasoning || activeIncident.execution_report?.summary || 'Awaiting operator confirmation after diagnostic evidence is reviewed.'}</Typography>
          </Box>
        </Paper>
      </Box>

      <Paper className="incident-bottom">
        <Box className="incident-bottom-body">
          <Box>
            <Typography className="product-kicker">OPERATOR NOTES</Typography>
            {persistedNotes.length ? persistedNotes.map((action, index) => (
              <Typography key={action.id || index} className="operator-note" variant="body2">
                <b>{action.approved_by || action.operator || 'Operator'}</b>
                {action.timestamp ? ` · ${formatTime(action.timestamp)}` : ''}
                {' — '}
                {action.note}
              </Typography>
            )) : (
              <Typography className="operator-note" variant="body2" color="text.secondary">
                No free-form notes yet. Use the decision bar below to record an auditable action with rationale.
              </Typography>
            )}
          </Box>
          <Box className="decision-track">
            <Typography className="product-kicker">DECISION TIMELINE</Typography>
            {operatorActions.length ? operatorActions.map((action, index) => (
              <Typography key={action.id || index}>
                <i />{action.title || action.action_type || 'Operator action'} <b>{action.approved_by || action.status || 'recorded'}</b>
              </Typography>
            )) : (
              <Typography variant="body2" color="text.secondary">No operator actions recorded for this case yet.</Typography>
            )}
          </Box>
          <DecisionHistory entries={decisionEntries} />
        </Box>
      </Paper>

      <EvidenceLineage facts={buildEvidenceFacts({ incident: activeIncident, stages: auditTimeline })} />
      {pendingRec ? (
        <OperatorDecisionBar incident={activeIncident} objectApi={objectApi} recommendation={activeIncident.ai_recommendation} />
      ) : null}
    </Box>
  );
}

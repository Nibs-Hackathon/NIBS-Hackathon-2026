import { useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { exportReport, recordOperatorAction } from '../../api/client';
import { downloadReportExport } from '../../api/downloadHelpers';
import { DecisionRail } from '../../design-system/catalog/panels';
import { ExecutiveLayout } from '../../design-system/layouts';
import { ApprovalStamp, RATIONALE_MIN } from '../accountability';
import { Empty, formatTime, round, Metric } from './shared';

function timelineFromReport(report, approval, decisionAt) {
  if (Array.isArray(report.timeline) && report.timeline.length) {
    const rows = report.timeline.filter((row) => row?.event && row?.when);
    if (!approval.includes('Awaiting') && !rows.some((row) => row.event === 'Board decision') && decisionAt) {
      rows.push({ event: 'Board decision', detail: approval, when: decisionAt });
    }
    return rows;
  }
  const rows = [];
  const detected = report.created_at || report.started_at || report.timestamp;
  if (detected) rows.push({ event: 'Signal detected', detail: 'Case opened in the operating record', when: detected });
  if (report.completed_at) rows.push({ event: 'Investigation completed', detail: 'AI evidence package closed', when: report.completed_at });
  if (report.recommendation || report.ai_recommendation) {
    rows.push({
      event: 'Recommendation prepared',
      detail: String(report.recommendation || report.ai_recommendation).slice(0, 120),
      when: report.completed_at || report.updated_at || detected,
    });
  }
  if (!approval.includes('Awaiting') && report.id && decisionAt) {
    rows.push({ event: 'Board decision', detail: approval, when: decisionAt });
  }
  return rows;
}

function executiveSummary(report) {
  const raw = String(report?.executive_summary || report?.summary || '').trim();
  if (!raw) return 'No executive summary has been published for this brief yet.';
  const concise = raw.split(/\n\s*(?:Key Findings|Agent Analysis)\s*\n/i)[0].trim();
  return concise.length > 850 ? `${concise.slice(0, 847).trim()}…` : concise;
}

/** Part 8 - Executive approval with persisted board decisions + export package. */
const BOARD_OPERATOR = 'Operator';
const BOARD_LABELS = {
  approved: 'Approved for publication',
  deferred: 'Deferred pending revision',
  escalated: 'Escalated to operating committee',
};

function matchingBoardAction(report, operatorActions) {
  if (!report?.incident_id) return null;
  return operatorActions
    .filter((action) => (
      action?.incident_id === report.incident_id
      && ['board_approve', 'board_defer', 'board_escalate'].includes(action.action_type)
      && (!action.payload?.report_id || String(action.payload.report_id) === String(report.id))
    ))
    .sort((a, b) => Date.parse(b.timestamp || 0) - Date.parse(a.timestamp || 0))[0] || null;
}

function formatCurrency(value) {
  const amount = Number(value);
  return Number.isFinite(amount)
    ? amount.toLocaleString(undefined, { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
    : 'Not available';
}

function formatPercent(value) {
  const amount = Number(value);
  return Number.isFinite(amount)
    ? `${amount.toLocaleString(undefined, { maximumFractionDigits: 1 })}%`
    : 'Not available';
}

export function ExecutiveBriefing({ reports, operatorActions = [] }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const [exporting, setExporting] = useState(false);
  const [busy, setBusy] = useState(false);

  const safeReports = Array.isArray(reports) ? reports.filter(Boolean) : [];
  const orderedReports = [...safeReports].reverse();
  const [selectedId, setSelectedId] = useState(objectApi.selection.reportId);
  const [mode, setMode] = useState('brief');
  const [rationale, setRationale] = useState('');
  const [decisionOverrides, setDecisionOverrides] = useState({});
  const rationaleRef = useRef(null);

  const chooseReport = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ reportId: id });
  };

  const report = safeReports.find((item) => item.id === (selectedId || objectApi.selection.reportId)) || orderedReports[0] || null;
  const title = report?.title || report?.name || report?.incident_type || 'Operating brief';
  const confidenceRaw = report?.confidence;
  const confidence = confidenceRaw != null
    ? round(Number(confidenceRaw) <= 1 ? Number(confidenceRaw) * 100 : Number(confidenceRaw))
    : null;

  const persistedAction = matchingBoardAction(report, operatorActions);
  const linkedOperatorActions = report?.incident_id
    ? operatorActions.filter((action) => action?.incident_id === report.incident_id)
    : [];
  const decisionOverride = report?.id ? decisionOverrides[report.id] : null;
  const persistedDecision = report?.board_decision || persistedAction?.decision;
  const approval = decisionOverride?.status
    || report?.board_status
    || BOARD_LABELS[persistedDecision]
    || 'Awaiting board approval';
  const decisionAt = decisionOverride?.at
    || report?.board_decision_at
    || persistedAction?.timestamp
    || null;
  const decisionBy = decisionOverride?.operator
    || report?.board_decision_by
    || persistedAction?.operator
    || null;
  const timeline = report ? timelineFromReport(report, approval, decisionAt) : [];

  const boardDone = !approval.includes('Awaiting');
  const opsDone = Boolean(report?.completed_at || report?.summary || report?.executive_summary);
  const reliabilityDone = Boolean(report?.recommendation || report?.ai_recommendation || boardDone);
  const recordDecision = async (decision, statusLabel, actionType) => {
    if (!report?.id) {
      toast.error('Select a report before recording a board decision');
      return;
    }
    const note = String(rationale || '').trim();
    if (note.length < RATIONALE_MIN) {
      toast.error(`Rationale must be at least ${RATIONALE_MIN} characters`);
      rationaleRef.current?.focus?.();
      return;
    }
    setBusy(true);
    try {
      const response = await recordOperatorAction({
        incident_id: report.incident_id || null,
        asset_id: report.asset_id || null,
        report_id: report.id,
        action_type: actionType,
        decision,
        risk_level: report.severity || 'MEDIUM',
        note,
        operator: BOARD_OPERATOR,
      });
      const recordedAt = response?.data?.recorded_at || new Date().toISOString();
      setDecisionOverrides((current) => ({
        ...current,
        [report.id]: {
          status: statusLabel,
          decision,
          at: recordedAt,
          operator: BOARD_OPERATOR,
        },
      }));
      objectApi.pushAuditDecision({
        id: response?.data?.id || `brief-${report.id}-${decision}`,
        decision,
        what: `${decision.replace(/_/g, ' ')} - ${title.slice(0, 40)}`,
        who: BOARD_OPERATOR,
        operator: BOARD_OPERATOR,
        at: recordedAt,
        reportId: report.id,
        incidentId: report.incident_id,
        objectLabel: title,
        rationale: note,
      });
      setRationale('');
      toast.success(`Brief ${decision.replace(/_/g, ' ')}`);
    } catch (error) {
      const detail = error.response?.data?.detail;
      toast.error(detail?.message || detail || 'Board decision could not be persisted');
    } finally {
      setBusy(false);
    }
  };

  const handleExport = async () => {
    if (!report?.id) {
      toast.error('Select a report before exporting');
      return;
    }
    setExporting(true);
    try {
      const response = await exportReport(report.id, 'markdown');
      downloadReportExport(response.data);
      toast.success('Export package downloaded (markdown)');
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Export package unavailable');
    } finally {
      setExporting(false);
    }
  };

  if (!safeReports.length) {
    return (
      <Box className="executive-briefing">
        <Empty text="report" />
      </Box>
    );
  }

  return (
    <Box className={`executive-briefing ${mode === 'presentation' ? 'presentation' : ''}`}>
      <Box className="briefing-head">
        <Box>
          <Typography className="product-kicker">EXECUTIVE BRIEFING CENTER</Typography>
          <Typography className="briefing-title">{title}</Typography>
          <Typography>{report.created_at || report.completed_at ? formatTime(report.created_at || report.completed_at) : 'Timestamp not published'}</Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Button size="small" onClick={() => setMode(mode === 'brief' ? 'presentation' : 'brief')}>
            {mode === 'brief' ? 'Presentation mode' : 'Exit presentation'}
          </Button>
          <Button
            size="small"
            onClick={() => navigateTo(objectApi, navigate, 'investigation', {
              incidentId: report.incident_id || objectApi.selection.incidentId || null,
            })}
          >
            Evidence appendix
          </Button>
          <Button size="small" variant="contained" startIcon={<ArticleOutlined />} disabled={exporting || !report?.id} onClick={handleExport}>
            Export package
          </Button>
        </Stack>
      </Box>

      <ExecutiveLayout
        className="briefing-layout-shell"
        reportIndex={(
          <Paper className="briefing-index">
          <Typography className="product-kicker">BRIEFING PACK</Typography>
          <Typography className="briefing-index-title">Board view</Typography>
          <Typography variant="caption" color="text.secondary">
            {safeReports.length} generated report{safeReports.length === 1 ? '' : 's'} · available archive
          </Typography>
          {orderedReports.map((item, index) => (
            <button
              type="button"
              key={item.id || index}
              className={report.id === item.id ? 'selected' : ''}
              onClick={() => chooseReport(item.id)}
            >
              <span>{String(index + 1).padStart(2, '0')}</span>
              <Box>
                <b>{item.title || item.name || item.incident_type || `Executive brief ${index + 1}`}</b>
                <small>{item.status || 'Ready for review'} · {item.created_at || item.completed_at ? formatTime(item.created_at || item.completed_at) : 'Not dated'}</small>
              </Box>
            </button>
          ))}
          <Box className="briefing-index-audit">
            <Typography className="product-kicker">AUDIT TRAIL</Typography>
            {opsDone ? <Typography><i />Evidence package present</Typography> : <Typography><i />Evidence package pending</Typography>}
            {reliabilityDone ? <Typography><i />Recommendation published</Typography> : <Typography><i />Recommendation pending</Typography>}
            <Typography><i />{approval}</Typography>
          </Box>
          </Paper>
        )}

        briefDocument={(
          <Paper className="briefing-document">
          <Box className="briefing-document-top">
            <Typography className="product-kicker">OPERATING COMMITTEE · CONFIDENTIAL</Typography>
            <Typography>Publication status <b>{approval}</b></Typography>
          </Box>
          <Typography className="briefing-document-title">Executive summary</Typography>
          <Typography className="briefing-lede">
            {executiveSummary(report)}
          </Typography>
          <Box className="briefing-numbers">
            <Metric
              label="Modeled exposure"
              value={formatCurrency(report.financial_impact)}
              provenance={report.financial_impact != null ? 'estimated' : 'stale'}
            />
            <Metric label="Maintenance cost" value={formatCurrency(report.maintenance_cost)} provenance={report.maintenance_cost != null ? 'estimated' : 'stale'} />
            <Metric label="Production impact" value={formatPercent(report.production_impact)} provenance={report.production_impact != null ? 'estimated' : 'stale'} />
            <Metric label="AI confidence" value={confidence != null ? `${confidence}%` : 'Not available'} provenance={confidence != null ? 'live' : 'stale'} />
          </Box>
          <Box className="briefing-section">
            <Typography className="product-kicker">INCIDENT REVIEW & ROOT CAUSE</Typography>
            <Typography>
              {report.root_cause || report.reasoning || 'Root-cause narrative is not attached to this report yet.'}
            </Typography>
          </Box>
          <Box className="briefing-timeline">
            <Typography className="product-kicker">DECISION TIMELINE</Typography>
            {timeline.length ? timeline.map((row) => (
              <Box key={`${row.event}-${row.when}`}>
                <i />
                <Typography><b>{row.event}</b><small>{row.detail}</small></Typography>
                <span>{formatTime(row.when)}</span>
              </Box>
            )) : (
              <Typography variant="body2" color="text.secondary">No decision timeline recorded for this brief yet.</Typography>
            )}
          </Box>
          <Box className="briefing-section recommendation">
            <Typography className="product-kicker">RECOMMENDATION</Typography>
            <Typography>
              {report.recommendation || report.ai_recommendation || (Array.isArray(report.recommendations) ? report.recommendations[0] : null) || 'No board recommendation published yet.'}
            </Typography>
          </Box>
          </Paper>
        )}

        decisionRail={(
          <Paper className="briefing-rail">
          <Typography className="product-kicker">DECISION CONTROL</Typography>
          <ApprovalStamp
            signatory={boardDone ? (decisionBy || BOARD_OPERATOR) : 'Pending'}
            timestamp={decisionAt ? new Date(decisionAt).toLocaleString() : null}
            status={approval}
          />
          <Box className="briefing-confidence">
            <Typography>AI confidence</Typography>
            <b>{confidence != null ? `${confidence}%` : 'Not available'}</b>
          </Box>
          <Box className="briefing-evidence">
            <Typography className="product-kicker">EVIDENCE & ATTACHMENTS</Typography>
            <Typography><ArticleOutlined />Incident linkage<b>{report.incident_id ? 'linked' : 'none'}</b></Typography>
            <Typography><ArticleOutlined />Agent results<b>{report.agent_results ?? report.agents?.length ?? 'Not available'}</b></Typography>
            <Typography><ArticleOutlined />Operator actions<b>{Math.max(Number(report.operator_actions) || 0, linkedOperatorActions.length)}</b></Typography>
            <Typography><ArticleOutlined />Source<b>{report.source || 'operations'}</b></Typography>
          </Box>
          <Box className="briefing-approvals">
            <Typography className="product-kicker">APPROVAL WORKFLOW</Typography>
            <Typography><i className={opsDone ? 'done' : ''} />Operations review <b>{opsDone ? 'complete' : 'pending'}</b></Typography>
            <Typography><i className={reliabilityDone ? 'done' : ''} />Reliability review <b>{reliabilityDone ? 'complete' : 'pending'}</b></Typography>
            <Typography><i className={boardDone ? 'done' : ''} />Board approval <b>{boardDone ? 'recorded' : 'pending'}</b></Typography>
          </Box>
          <DecisionRail
            className="briefing-decision"
            recommendation={report.recommendation || report.ai_recommendation || 'No board recommendation published yet.'}
            rationale={rationale}
            onRationaleChange={setRationale}
            minRationale={RATIONALE_MIN}
            rationaleInputRef={rationaleRef}
            busy={busy}
            onAccept={() => recordDecision('approved', 'Approved for publication', 'board_approve')}
            onModify={() => recordDecision('deferred', 'Deferred pending revision', 'board_defer')}
            onReject={() => recordDecision('escalated', 'Escalated to operating committee', 'board_escalate')}
          />
          </Paper>
        )}
      />
    </Box>
  );
}

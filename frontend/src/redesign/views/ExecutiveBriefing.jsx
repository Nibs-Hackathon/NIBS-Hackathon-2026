import { useEffect, useMemo, useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { exportReport, getReports, recordOperatorAction } from '../../api/client';
import { downloadReportExport } from '../../api/downloadHelpers';
import { DecisionRail } from '../../design-system/catalog/panels';
import { ApprovalStamp, RATIONALE_MIN } from '../accountability';
import { formatTime, round, Metric } from './shared';

function timelineFromReport(report, approval) {
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
  if (!approval.includes('Awaiting') && report.id) {
    rows.push({ event: 'Board decision', detail: approval, when: new Date().toISOString() });
  }
  return rows;
}

/** Part 8 — Executive approval with persisted board decisions + export package. */
export function ExecutiveBriefing({ reports }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const sessionApprovals = objectApi.audit?.recentDecisions || [];
  const [reportList, setReportList] = useState(reports);
  const [exporting, setExporting] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => { setReportList(reports); }, [reports]);

  useEffect(() => {
    let cancelled = false;
    getReports()
      .then((response) => {
        if (cancelled) return;
        const rows = Array.isArray(response.data) ? response.data : [];
        if (rows.length) setReportList(rows);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, []);

  const safeReports = Array.isArray(reportList) ? reportList.filter(Boolean) : [];
  const [selectedId, setSelectedId] = useState(objectApi.selection.reportId);
  const [mode, setMode] = useState('brief');
  const [approval, setApproval] = useState('Awaiting board approval');
  const [rationale, setRationale] = useState('');
  const [decisionAt, setDecisionAt] = useState(null);
  const rationaleRef = useRef(null);

  const chooseReport = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ reportId: id });
    setApproval('Awaiting board approval');
    setDecisionAt(null);
  };

  const report = safeReports.find((item) => item.id === (selectedId || objectApi.selection.reportId)) || safeReports[0] || null;
  const title = report?.title || report?.name || report?.incident_type || 'Operating brief';
  const confidenceRaw = report?.confidence;
  const confidence = confidenceRaw != null
    ? round(Number(confidenceRaw) <= 1 ? Number(confidenceRaw) * 100 : Number(confidenceRaw))
    : null;

  const timeline = useMemo(
    () => (report ? timelineFromReport(report, approval) : []),
    [report, approval],
  );

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
        action_type: actionType,
        decision,
        risk_level: report.severity || 'MEDIUM',
        note,
        operator: 'Board chair',
      });
      setApproval(statusLabel);
      setDecisionAt(new Date().toISOString());
      objectApi.pushAuditDecision({
        id: response?.data?.id || `brief-${Date.now()}`,
        decision,
        what: `${decision.replace(/_/g, ' ')} — ${title.slice(0, 40)}`,
        who: 'Board chair',
        operator: 'Board chair',
        at: new Date().toISOString(),
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
        <Box className="briefing-head">
          <Box>
            <Typography className="product-kicker">EXECUTIVE BRIEFING CENTER</Typography>
            <Typography className="briefing-title">No board briefs published</Typography>
            <Typography>Executive packs appear after investigations produce execution reports.</Typography>
          </Box>
        </Box>
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

      <Stack spacing={1} sx={{ mt: 1.5, mb: 2, maxWidth: 360 }}>
        <ApprovalStamp
          signatory={boardDone ? 'Board chair' : '—'}
          timestamp={decisionAt ? new Date(decisionAt).toLocaleString() : null}
          status={approval}
        />
        {sessionApprovals.slice(0, 3).map((entry) => (
          <ApprovalStamp
            key={entry.id}
            signatory={entry.who || entry.operator}
            timestamp={entry.at ? new Date(entry.at).toLocaleString() : null}
            status={entry.decision || 'recorded'}
          />
        ))}
      </Stack>

      <Box className="briefing-layout">
        <Paper className="briefing-index">
          <Typography className="product-kicker">BRIEFING PACK</Typography>
          <Typography className="briefing-index-title">Board view</Typography>
          {safeReports.map((item, index) => (
            <button
              type="button"
              key={item.id || index}
              className={report.id === item.id ? 'selected' : ''}
              onClick={() => chooseReport(item.id)}
            >
              <span>{String(index + 1).padStart(2, '0')}</span>
              <Box>
                <b>{item.title || item.name || item.incident_type || `Executive brief ${index + 1}`}</b>
                <small>{item.status || 'Ready for review'} · {item.created_at || item.completed_at ? formatTime(item.created_at || item.completed_at) : '—'}</small>
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

        <Paper className="briefing-document">
          <Box className="briefing-document-top">
            <Typography className="product-kicker">OPERATING COMMITTEE · CONFIDENTIAL</Typography>
            <Typography>Publication status <b>{approval}</b></Typography>
          </Box>
          <Typography className="briefing-document-title">Executive summary</Typography>
          <Typography className="briefing-lede">
            {report.summary || report.executive_summary || 'No executive summary has been published for this brief yet.'}
          </Typography>
          <Box className="briefing-numbers">
            <Metric label="Financial impact" value={report.financial_impact || '—'} provenance="live" />
            <Metric label="Maintenance cost" value={report.maintenance_cost || '—'} provenance="live" />
            <Metric label="Production impact" value={report.production_impact || '—'} provenance="live" />
            <Metric label="AI confidence" value={confidence != null ? `${confidence}%` : '—'} provenance="live" />
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

        <Paper className="briefing-rail">
          <Typography className="product-kicker">DECISION CONTROL</Typography>
          <Box className="briefing-confidence">
            <Typography>AI confidence</Typography>
            <b>{confidence != null ? `${confidence}%` : '—'}</b>
            {confidence != null ? <i><span style={{ width: `${confidence}%` }} /></i> : null}
          </Box>
          <Box className="briefing-evidence">
            <Typography className="product-kicker">EVIDENCE & ATTACHMENTS</Typography>
            <Typography><ArticleOutlined />Incident linkage<b>{report.incident_id ? 'linked' : 'none'}</b></Typography>
            <Typography><ArticleOutlined />Agent results<b>{report.agent_results ?? report.agents?.length ?? '—'}</b></Typography>
            <Typography><ArticleOutlined />Operator actions<b>{report.operator_actions ?? 0}</b></Typography>
            <Typography><ArticleOutlined />Source<b>{report.source || 'operations'}</b></Typography>
          </Box>
          <Box className="briefing-approvals">
            <Typography className="product-kicker">APPROVAL WORKFLOW</Typography>
            <Typography><i className={opsDone ? 'done' : ''} />Operations review <b>{opsDone ? 'complete' : 'pending'}</b></Typography>
            <Typography><i className={reliabilityDone ? 'done' : ''} />Reliability review <b>{reliabilityDone ? 'complete' : 'pending'}</b></Typography>
            <Typography><i className={boardDone ? 'done' : ''} />Board approval <b>{boardDone ? 'recorded' : 'pending'}</b></Typography>
          </Box>
          <DecisionRail
            className="e5-decision-bar"
            recommendation={report.recommendation || report.ai_recommendation || 'Approve publication of this operating brief.'}
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
      </Box>
    </Box>
  );
}

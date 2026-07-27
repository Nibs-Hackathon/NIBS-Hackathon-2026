import { useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { DecisionRail } from '../../design-system/catalog/panels';
import { ApprovalStamp, RATIONALE_MIN } from '../accountability';
import { formatTime, round, Metric } from './shared';

/** Part 8 — Executive approval in-place with rationale + AuditSpine append. */
export function ExecutiveBriefing({ reports }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const sessionApprovals = objectApi.audit?.recentDecisions || [];
  const safeReports = Array.isArray(reports) ? reports.filter(Boolean) : [];
  const [selectedId, setSelectedId] = useState(objectApi.selection.reportId);
  const [mode, setMode] = useState('brief');
  const [approval, setApproval] = useState('Awaiting board approval');
  const [rationale, setRationale] = useState('');
  const rationaleRef = useRef(null);

  const chooseReport = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ reportId: id });
  };

  const report = safeReports.find((item) => item.id === (selectedId || objectApi.selection.reportId)) || safeReports[0] || {};
  const title = report.title || report.name || report.incident_type || 'Alpha refinery operating brief';
  const confidence = round(Number(report.confidence ?? 0.86) <= 1 ? Number(report.confidence ?? 0.86) * 100 : Number(report.confidence ?? 0.86));

  const recordDecision = (decision, statusLabel) => {
    const note = String(rationale || '').trim();
    if (note.length < RATIONALE_MIN) {
      toast.error(`Rationale must be at least ${RATIONALE_MIN} characters`);
      rationaleRef.current?.focus?.();
      return;
    }
    setApproval(statusLabel);
    objectApi.pushAuditDecision({
      id: `brief-${Date.now()}`,
      decision,
      what: `${decision.replace(/_/g, ' ')} — ${title.slice(0, 40)}`,
      who: 'Board chair',
      operator: 'Board chair',
      at: new Date().toISOString(),
      reportId: report.id,
      objectLabel: title,
      rationale: note,
    });
    setRationale('');
    toast.success(`Brief ${decision.replace(/_/g, ' ')}`);
  };

  return (
    <Box className={`executive-briefing ${mode === 'presentation' ? 'presentation' : ''}`}>
      <Box className="briefing-head">
        <Box>
          <Typography className="product-kicker">EXECUTIVE BRIEFING CENTER</Typography>
          <Typography className="briefing-title">{title}</Typography>
          <Typography>{report.created_at ? formatTime(report.created_at) : 'Prepared for the operating committee · live data reconciled'}</Typography>
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
          <Button size="small" variant="contained" startIcon={<ArticleOutlined />} onClick={() => toast.success('Board-ready PDF export prepared')}>
            Export PDF
          </Button>
        </Stack>
      </Box>

      <Stack spacing={1} sx={{ mt: 1.5, mb: 2, maxWidth: 360 }}>
        <ApprovalStamp
          signatory={approval.includes('Awaiting') ? 'Control operator' : 'Board chair'}
          timestamp={new Date().toLocaleString()}
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
          {(safeReports.length ? safeReports : [{ id: 'current', title }]).map((item, index) => (
            <button
              type="button"
              key={item.id || index}
              className={(report.id || 'current') === (item.id || 'current') ? 'selected' : ''}
              onClick={() => chooseReport(item.id)}
            >
              <span>{String(index + 1).padStart(2, '0')}</span>
              <Box>
                <b>{item.title || item.name || item.incident_type || `Executive brief ${index + 1}`}</b>
                <small>{item.status || 'Ready for review'} · {item.created_at ? formatTime(item.created_at) : 'current'}</small>
              </Box>
            </button>
          ))}
          <Box className="briefing-index-audit">
            <Typography className="product-kicker">AUDIT TRAIL</Typography>
            <Typography><i />Evidence assembled</Typography>
            <Typography><i />AI synthesis complete</Typography>
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
            {report.summary || report.executive_summary || 'The facility remains operational while a focused reliability intervention is recommended to contain emerging asset risk and preserve the upcoming production window.'}
          </Typography>
          <Box className="briefing-numbers">
            <Metric label="Financial impact" value={report.financial_impact || '$184k projected exposure'} />
            <Metric label="Maintenance cost" value={report.maintenance_cost || '$28k intervention estimate'} />
            <Metric label="Production impact" value={report.production_impact || '1.8% at-risk throughput'} />
            <Metric label="AI confidence" value={`${confidence}%`} />
          </Box>
          <Box className="briefing-section">
            <Typography className="product-kicker">INCIDENT REVIEW & ROOT CAUSE</Typography>
            <Typography>
              {report.root_cause || report.reasoning || 'Evidence indicates a condition-driven risk pattern. Diagnostic and maintenance evidence support an intervention during the next controlled low-load window.'}
            </Typography>
          </Box>
          <Box className="briefing-timeline">
            <Typography className="product-kicker">DECISION TIMELINE</Typography>
            {[
              ['Signal detected', 'Telemetry deviation corroborated'],
              ['Investigation completed', 'AI evidence and maintenance history reconciled'],
              ['Recommendation prepared', 'Target intervention window proposed'],
              ['Board approval', approval],
            ].map(([event, detail], index) => (
              <Box key={event}>
                <i />
                <Typography><b>{event}</b><small>{detail}</small></Typography>
                <span>{index === 3 ? 'Now' : `${index + 1}h ago`}</span>
              </Box>
            ))}
          </Box>
          <Box className="briefing-section recommendation">
            <Typography className="product-kicker">RECOMMENDATION</Typography>
            <Typography>
              {report.recommendation || report.ai_recommendation || 'Approve the condition-based intervention plan and maintain elevated monitoring until the work order is complete.'}
            </Typography>
          </Box>
        </Paper>

        <Paper className="briefing-rail">
          <Typography className="product-kicker">DECISION CONTROL</Typography>
          <Box className="briefing-confidence">
            <Typography>AI confidence</Typography>
            <b>{confidence}%</b>
            <i><span style={{ width: `${confidence}%` }} /></i>
          </Box>
          <Box className="briefing-evidence">
            <Typography className="product-kicker">EVIDENCE & ATTACHMENTS</Typography>
            {['Telemetry deviation packet', 'Maintenance history extract', 'Operating procedure reference', 'Incident evidence log'].map((item, index) => (
              <Typography key={item}><ArticleOutlined />{item}<b>{index < 2 ? 'verified' : 'linked'}</b></Typography>
            ))}
          </Box>
          <Box className="briefing-approvals">
            <Typography className="product-kicker">APPROVAL WORKFLOW</Typography>
            <Typography><i className="done" />Operations review <b>complete</b></Typography>
            <Typography><i className="done" />Reliability review <b>complete</b></Typography>
            <Typography><i />Board approval <b>pending</b></Typography>
          </Box>
          <DecisionRail
            className="e5-decision-bar"
            recommendation={report.recommendation || report.ai_recommendation || 'Approve publication of this operating brief.'}
            rationale={rationale}
            onRationaleChange={setRationale}
            minRationale={RATIONALE_MIN}
            rationaleInputRef={rationaleRef}
            onAccept={() => recordDecision('approved', 'Approved for publication')}
            onModify={() => recordDecision('deferred', 'Deferred pending revision')}
            onReject={() => recordDecision('escalated', 'Escalated to operating committee')}
          />
        </Paper>
      </Box>
    </Box>
  );
}

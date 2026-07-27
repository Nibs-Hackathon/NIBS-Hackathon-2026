import { useState, useEffect } from 'react';
import { Box, Button, Chip, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined, PlayArrowOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { getIncidentAuditDetail } from '../../api/client';
import {
  OperatorDecisionBar,
  EvidenceLineage,
  buildEvidenceFacts,
  normalizeTraceStages,
  TracePanel,
  DecisionHistory,
  ProvenanceBadge,
} from '../accountability';
import { MiniGraph, Empty, Metric, round } from './shared';

function stageConfidence(stage) {
  if (stage?.confidence == null) return null;
  const value = Number(stage.confidence);
  return round(value <= 1 ? value * 100 : value);
}

export function AIInvestigationOS({ stages, investigation, incident, telemetry, provenance = 'live' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const [auditIncident, setAuditIncident] = useState(null);

  useEffect(() => {
    if (!incident?.id) {
      setAuditIncident(null);
      return undefined;
    }
    let cancelled = false;
    getIncidentAuditDetail(incident.id)
      .then((response) => {
        if (!cancelled) setAuditIncident(response.data);
      })
      .catch(() => {
        if (!cancelled) setAuditIncident(null);
      });
    return () => { cancelled = true; };
  }, [incident?.id]);

  const activeIncident = auditIncident?.id === incident?.id ? { ...incident, ...auditIncident } : incident;
  const pipeline = Array.isArray(stages) ? stages.filter(Boolean) : [];
  const [expanded, setExpanded] = useState(pipeline.length ? 0 : null);

  const selectStage = (index) => {
    setExpanded(expanded === index ? null : index);
    objectApi.setSelection({
      agentStageId: pipeline[index]?.id || pipeline[index]?.agent || `stage-${index}`,
      incidentId: incident?.id || objectApi.selection.incidentId,
    });
  };

  const traceStages = normalizeTraceStages(pipeline, investigation);
  const evidenceFacts = buildEvidenceFacts({ incident: activeIncident, stages: pipeline, investigation });
  const readings = Array.isArray(telemetry?.readings) ? telemetry.readings : [];

  const investigationConfidence = investigation?.confidence != null
    ? round(Number(investigation.confidence) <= 1
      ? Number(investigation.confidence) * 100
      : Number(investigation.confidence))
    : null;

  const liveAgents = pipeline.filter((stage) => /running|streaming/i.test(String(stage.state || ''))).length;
  const retrievedDocs = pipeline.flatMap((stage) => {
    if (Array.isArray(stage.documents)) return stage.documents;
    if (Array.isArray(stage.evidence)) {
      return stage.evidence.filter((item) => typeof item === 'string' && /procedure|manual|document/i.test(item));
    }
    return [];
  });

  const confidenceHistory = pipeline
    .map((stage) => stageConfidence(stage))
    .filter((value) => value != null);

  return (
    <Box className="ai-flagship">
      <Box className="ai-flagship-head">
        <Box>
          <Typography className="product-kicker">RIGOS AI INVESTIGATION</Typography>
          <Typography className="ai-flagship-title">Watching the operational model reason</Typography>
          <Typography>
            Live investigation of {activeIncident?.asset_name || activeIncident?.asset_id || 'the active process signal'}
            {' '}
            — every conclusion is traceable to evidence.
          </Typography>
          <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
            {activeIncident?.id ? (
              <Chip
                clickable
                label={`Linked case ${String(activeIncident.id).slice(0, 8)}`}
                onClick={() => navigateTo(objectApi, navigate, 'incidents', {
                  incidentId: activeIncident.id,
                  assetId: activeIncident.asset_id || null,
                })}
              />
            ) : null}
            {activeIncident?.asset_id ? (
              <Chip
                clickable
                label={activeIncident.asset_name || activeIncident.asset_id}
                onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: activeIncident.asset_id })}
              />
            ) : null}
          </Stack>
        </Box>
        <Box className="ai-flagship-live">
          <i />
          {pipeline.length ? 'STREAMING EXECUTION' : 'AWAITING WORKFLOW'}
          <small>
            {investigationConfidence != null ? `${investigationConfidence}% model confidence` : 'No active investigation confidence'}
          </small>
          <ProvenanceBadge value={provenance} />
        </Box>
      </Box>

      <Box className="ai-flagship-grid">
        <Paper className="ai-pipeline">
          <Box className="ai-panel-head">
            <Box>
              <Typography className="product-kicker">AGENT PIPELINE</Typography>
              <Typography>Execution graph</Typography>
            </Box>
            <Chip label={`${liveAgents} agents live`} />
          </Box>
          {pipeline.length ? (
            <Box className="ai-pipeline-list">
              {pipeline.map((stage, index) => {
                const state = String(stage.state || 'queued').toLowerCase();
                const confidence = stageConfidence(stage);
                const evidenceCount = Array.isArray(stage.evidence) ? stage.evidence.length : 0;
                const artifactCount = Array.isArray(stage.documents) ? stage.documents.length : 0;
                return (
                  <motion.button
                    layout={false}
                    type="button"
                    key={`${stage.id || stage.agent}-${index}`}
                    className={`ai-stage ${state} ${expanded === index ? 'expanded' : ''}`}
                    onClick={() => selectStage(index)}
                  >
                    <span className="ai-stage-index">{index + 1}</span>
                    <Box>
                      <Typography>{traceLabel(stage.agent, index)}</Typography>
                      <Typography>
                        {state === 'queued'
                          ? 'Awaiting upstream evidence'
                          : state === 'running' || state === 'streaming'
                            ? 'Evidence streaming'
                            : 'Execution recorded'}
                      </Typography>
                      <i>
                        <span style={{
                          width: `${state === 'queued' ? 16 : state === 'running' || state === 'streaming' ? 68 : 100}%`,
                        }}
                        />
                      </i>
                    </Box>
                    <Box className="ai-stage-state">
                      <b>{confidence != null ? `${confidence}%` : '—'}</b>
                      <small>{label(state)}</small>
                    </Box>
                    {index < pipeline.length - 1 && <em />}
                    {expanded === index && (
                      <motion.div
                        className="ai-stage-expanded"
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        transition={{ duration: 0.12 }}
                      >
                        <Typography>
                          {safeReasoning(stage.reasoning || stage.output || stage.task || 'No reasoning recorded for this stage.')}
                        </Typography>
                        <Box>
                          <span>Evidence {evidenceCount}</span>
                          <span>Artifacts {artifactCount}</span>
                          <span>
                            Duration {stage.duration_seconds
                              ? `${Number(stage.duration_seconds).toFixed(1)}s`
                              : '—'}
                          </span>
                        </Box>
                      </motion.div>
                    )}
                  </motion.button>
                );
              })}
            </Box>
          ) : (
            <Box sx={{ p: 2 }}>
              <Empty text="agent activity" />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {investigation?.status === 'investigating'
                  ? 'Investigation is active but no agent stages have been published yet.'
                  : 'No investigation workflow is running. Stages appear when MAO processes an incident.'}
              </Typography>
            </Box>
          )}
        </Paper>

        <Paper className="ai-reasoning">
          <Box className="ai-panel-head">
            <Box>
              <Typography className="product-kicker">REASONING TREE</Typography>
              <Typography>Hypotheses and evidence</Typography>
            </Box>
          </Box>
          <Box className="reasoning-tree">
            <Box className="reasoning-root">
              <b>Observed deviation</b>
              <Typography>
                {activeIncident?.incident_type
                  ? label(activeIncident.incident_type)
                  : investigation?.current_reasoning || 'No active deviation under investigation'}
              </Typography>
            </Box>
            {pipeline.length ? (
              <Box className="reasoning-branches">
                {pipeline.slice(0, 5).map((stage, index) => {
                  const confidence = stageConfidence(stage);
                  return (
                    <Box key={`${stage.id || stage.agent}-${index}`}>
                      <span>{String(index + 1).padStart(2, '0')}</span>
                      <Typography>
                        <b>{traceLabel(stage.agent, index)}</b>
                        {safeReasoning(stage.reasoning || stage.output || stage.task || 'Stage recorded without narrative.')}
                        <small>
                          {label(stage.state || 'recorded')}
                          {confidence != null ? ` · confidence ${confidence}%` : ''}
                        </small>
                      </Typography>
                    </Box>
                  );
                })}
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                Reasoning branches appear when agent stages publish findings.
              </Typography>
            )}
          </Box>
        </Paper>

        <Paper className="ai-evidence">
          <Box className="ai-panel-head">
            <Box>
              <Typography className="product-kicker">LIVE EVIDENCE</Typography>
              <Typography>Data and artifacts</Typography>
            </Box>
            <Button size="small" startIcon={<PlayArrowOutlined />} disabled>
              Replay
            </Button>
          </Box>
          <Box className="ai-telemetry">
            <Typography className="product-kicker">TELEMETRY WINDOW</Typography>
            <MiniGraph
              values={readings.map((reading) => reading.value)}
              area
              label={readings.length
                ? `${readings.length} samples · live historian feed`
                : 'No telemetry samples for this incident window'}
            />
          </Box>
          <Box className="ai-documents">
            <Typography className="product-kicker">RETRIEVED DOCUMENTS & KNOWLEDGE LINKS</Typography>
            {retrievedDocs.length ? retrievedDocs.map((doc, index) => (
              <Typography key={`${doc}-${index}`}>
                <ArticleOutlined />
                <span>{typeof doc === 'string' ? doc : doc.title || 'Document'}</span>
              </Typography>
            )) : (
              <Typography variant="body2" color="text.secondary">
                No retrieved documents for this investigation yet.
              </Typography>
            )}
          </Box>
          <Box className="ai-artifacts">
            <Typography className="product-kicker">GENERATED ACTIONS</Typography>
            {pipeline.some((stage) => Array.isArray(stage.recommendations) && stage.recommendations.length) ? (
              pipeline.flatMap((stage) => (Array.isArray(stage.recommendations) ? stage.recommendations : []))
                .slice(0, 5)
                .map((item, index) => (
                  <Typography key={index}><i />{typeof item === 'string' ? item : item.title || 'Recommendation'}</Typography>
                ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                Recommendations appear when agent stages complete.
              </Typography>
            )}
          </Box>
        </Paper>
      </Box>

      <Paper className="ai-bottom">
        <Box className="ai-confidence">
          <Typography className="product-kicker">CONFIDENCE EVOLUTION</Typography>
          {confidenceHistory.length ? (
            <>
              <Box>
                {confidenceHistory.map((value, index) => (
                  <span key={index} style={{ height: `${value}%` }}><small>{value}%</small></span>
                ))}
              </Box>
              <Typography>Recorded stage confidence values</Typography>
            </>
          ) : (
            <Typography variant="body2" color="text.secondary">
              Confidence history is unavailable until agent stages report scores.
            </Typography>
          )}
        </Box>
        <Box className="ai-execution">
          <Typography className="product-kicker">EXECUTION TIMELINE & LOGS</Typography>
          {pipeline.length ? pipeline.slice(0, 6).map((stage, index) => (
            <Typography key={`${stage.id || stage.agent}-${index}`}>
              <i />
              {traceLabel(stage.agent, index)}
              {' '}
              <b>
                {label(stage.state || 'recorded')}
                {stage.timestamp ? ` · ${new Date(stage.timestamp).toLocaleTimeString()}` : ''}
              </b>
            </Typography>
          )          ) : (
            <Typography variant="body2" color="text.secondary">
              No execution log entries yet.
            </Typography>
          )}
        </Box>
        <Box className="ai-decisions">
          <Typography className="product-kicker">OPERATOR DECISION</Typography>
          <Typography>Generated actions are advisory. Approval preserves the auditable execution record.</Typography>
        </Box>
      </Paper>

      <Box className="e5-trace-wrap">
        <EvidenceLineage facts={evidenceFacts} />
        <TracePanel
          stages={traceStages}
          selectedId={expanded != null ? traceStages[expanded]?.id : objectApi.selection.agentStageId}
          onSelect={(stage) => {
            const idx = traceStages.findIndex((row) => row.id === stage.id);
            if (idx >= 0) selectStage(idx);
          }}
        />
        <DecisionHistory
          entries={objectApi.audit?.recentDecisions?.filter(
            (entry) => !incident?.id || entry.incidentId === incident.id,
          ) || []}
        />
        <OperatorDecisionBar
          incident={activeIncident}
          objectApi={objectApi}
          recommendation={investigation?.current_recommendation || activeIncident?.ai_recommendation}
        />
      </Box>
    </Box>
  );
}

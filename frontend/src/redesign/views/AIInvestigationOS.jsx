import { useState, useEffect } from 'react';
import { Box, Chip, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { getIncidentAuditDetail, getTelemetry, searchKnowledge, getAgents, getAgentMetrics } from '../../api/client';
import {
  incidentTelemetryWindow,
  normalizeTelemetryReadings,
  decisionEntriesFromIncident,
  normalizeAgentActivityRow,
  normalizeAgentRegistryRow,
  normalizeAgentMetricRow,
} from '../../api/resourceAdapters';
import {
  OperatorDecisionBar,
  EvidenceLineage,
  buildEvidenceFacts,
  normalizeTraceStages,
  TracePanel,
  DecisionHistory,
  ProvenanceBadge,
} from '../accountability';
import {
  MiniGraph,
  Empty,
  Metric,
  label,
  round,
  safeReasoning,
  traceLabel,
} from './shared';

function stageConfidence(stage) {
  if (stage?.confidence == null) return null;
  const value = Number(stage.confidence);
  return Number((value <= 1 ? value * 100 : value).toFixed(2));
}

export function AIInvestigationOS({ stages, investigation, incident, telemetry, aiActivity = [], provenance = 'live' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const [auditIncident, setAuditIncident] = useState(null);
  const [replayReadings, setReplayReadings] = useState([]);
  const [replayLoading, setReplayLoading] = useState(false);
  const [evidenceMode, setEvidenceMode] = useState('live');
  const [knowledgeResults, setKnowledgeResults] = useState([]);
  const [knowledgeLoading, setKnowledgeLoading] = useState(false);
  const [agentRegistry, setAgentRegistry] = useState([]);
  const [agentMetrics, setAgentMetrics] = useState([]);

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
    if (!activeIncident) {
      setKnowledgeResults([]);
      return undefined;
    }
    const query = [
      activeIncident.incident_type,
      activeIncident.asset_name,
      activeIncident.reasoning,
      activeIncident.root_cause,
    ].filter(Boolean).join(' ').trim();
    if (!query) {
      setKnowledgeResults([]);
      return undefined;
    }
    let cancelled = false;
    setKnowledgeLoading(true);
    searchKnowledge(query)
      .then((response) => {
        if (!cancelled) setKnowledgeResults(Array.isArray(response.data?.results) ? response.data.results : []);
      })
      .catch(() => {
        if (!cancelled) setKnowledgeResults([]);
      })
      .finally(() => {
        if (!cancelled) setKnowledgeLoading(false);
      });
    return () => { cancelled = true; };
  }, [activeIncident?.id, activeIncident?.incident_type, activeIncident?.asset_name, activeIncident?.reasoning, activeIncident?.root_cause]);

  const pipeline = Array.isArray(stages) ? stages.filter(Boolean) : [];

  useEffect(() => {
    if (pipeline.length) return undefined;
    let cancelled = false;
    Promise.all([getAgents(), getAgentMetrics()])
      .then(([agentsResponse, metricsResponse]) => {
        if (cancelled) return;
        setAgentRegistry(
          (Array.isArray(agentsResponse.data) ? agentsResponse.data : [])
            .map(normalizeAgentRegistryRow)
            .filter(Boolean),
        );
        setAgentMetrics(
          (Array.isArray(metricsResponse.data) ? metricsResponse.data : [])
            .map(normalizeAgentMetricRow)
            .filter(Boolean),
        );
      })
      .catch(() => {
        if (!cancelled) {
          setAgentRegistry([]);
          setAgentMetrics([]);
        }
      });
    return () => { cancelled = true; };
  }, [pipeline.length]);

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
  const liveReadings = Array.isArray(telemetry?.readings) ? telemetry.readings : [];
  const displayReadings = evidenceMode === 'replay' && replayReadings.length ? replayReadings : liveReadings;

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
  const knowledgeDocs = knowledgeResults.map((doc) => ({
    title: doc.filename || doc.source || doc.title || 'Knowledge document',
    content: doc.content || doc.snippet,
    score: doc.score,
  }));
  const displayedDocs = knowledgeDocs.length
    ? knowledgeDocs
    : retrievedDocs.map((doc) => (typeof doc === 'string' ? { title: doc } : doc));
  const sessionDecisions = objectApi.audit?.recentDecisions?.filter(
    (entry) => !incident?.id || entry.incidentId === incident.id,
  ) || [];
  const decisionEntries = decisionEntriesFromIncident(activeIncident, sessionDecisions);
  const activityLog = (Array.isArray(aiActivity) ? aiActivity : [])
    .map(normalizeAgentActivityRow)
    .filter(Boolean);

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
            {investigationConfidence != null ? `${Number(investigationConfidence).toFixed(2)}% model confidence` : 'No active investigation confidence'}
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
                      <b>{confidence != null ? `${confidence.toFixed(2)}%` : '—'}</b>
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
                          <span>Evidence {evidenceCount.toFixed(2)}</span>
                          <span>Artifacts {artifactCount.toFixed(2)}</span>
                          <span>
                            Duration {stage.duration_seconds
                              ? `${Number(stage.duration_seconds).toFixed(2)}s`
                              : '—'}
                          </span>
                        </Box>
                      </motion.div>
                    )}
                  </motion.button>
                );
              })}
            </Box>
          ) : agentRegistry.length ? (
            <Box className="ai-pipeline-list">
              {agentRegistry.map((agent, index) => (
                <Box key={`${agent.name}-${index}`} className="ai-stage completed">
                  <span className="ai-stage-index">{index + 1}</span>
                  <Box>
                    <Typography>{agent.name}</Typography>
                    <Typography>{agent.task}</Typography>
                  </Box>
                  <Box className="ai-stage-state">
                    <b>{agent.confidence || '—'}</b>
                    <small>{label(agent.state || 'ready')}</small>
                  </Box>
                </Box>
              ))}
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
                          {confidence != null ? ` · confidence ${confidence.toFixed(2)}%` : ''}
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
          </Box>
          <Box className="ai-telemetry">
            <Typography className="product-kicker">TELEMETRY WINDOW</Typography>
            {replayReadings.length > 0 && (
              <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
                <Chip
                  clickable
                  size="small"
                  label="Live feed"
                  color={evidenceMode === 'live' ? 'primary' : 'default'}
                  onClick={() => setEvidenceMode('live')}
                />
                <Chip
                  clickable
                  size="small"
                  label={replayLoading ? 'Loading replay…' : `Incident replay (${replayReadings.length})`}
                  color={evidenceMode === 'replay' ? 'primary' : 'default'}
                  onClick={() => setEvidenceMode('replay')}
                  disabled={replayLoading}
                />
              </Stack>
            )}
            <MiniGraph
              values={displayReadings.map((reading) => reading.value)}
              area
              label={displayReadings.length
                ? `${displayReadings.length} samples · ${evidenceMode === 'replay' ? 'incident window replay' : 'live historian feed'}`
                : 'No telemetry samples for this incident window'}
            />
          </Box>
          <Box className="ai-documents">
            <Typography className="product-kicker">RETRIEVED DOCUMENTS & KNOWLEDGE LINKS</Typography>
            {knowledgeLoading && (
              <Typography variant="caption" color="text.secondary">Searching knowledge base…</Typography>
            )}
            {displayedDocs.length ? displayedDocs.map((doc, index) => (
              <Typography key={`${doc.title}-${index}`}>
                <ArticleOutlined />
                <span title={doc.content || ''}>
                  {doc.title || 'Document'}
                  {doc.score != null ? ` · ${(doc.score * 100).toFixed(0)}% match` : ''}
                </span>
              </Typography>
            )) : (
              <Typography variant="body2" color="text.secondary">
                {knowledgeLoading
                  ? 'Retrieving documents…'
                  : 'No retrieved documents for this investigation yet.'}
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
                  <span key={index} style={{ height: `${value}%` }}><small>{value.toFixed(2)}%</small></span>
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
          )) : activityLog.length ? activityLog.slice(0, 6).map((entry, index) => (
            <Typography key={`${entry.agent}-${index}`}>
              <i />
              {entry.agent}
              {' '}
              <b>
                {label(entry.state || 'recorded')}
                {entry.time ? ` · ${new Date(entry.time).toLocaleTimeString()}` : ''}
              </b>
              {' — '}
              {entry.action}
            </Typography>
          )) : (
            <Typography variant="body2" color="text.secondary">
              No execution log entries yet.
            </Typography>
          )}
        </Box>
        <Box className="ai-decisions">
          <Typography className="product-kicker">OPERATOR DECISION</Typography>
          <Typography>Generated actions are advisory. Approval preserves the auditable execution record.</Typography>
          {agentMetrics.length ? (
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mt: 1 }}>
              {agentMetrics.map((metric) => (
                <Chip key={metric.label} size="small" label={`${metric.label}: ${metric.value}`} title={metric.detail} />
              ))}
            </Stack>
          ) : null}
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
        <DecisionHistory entries={decisionEntries} />
        <OperatorDecisionBar
          incident={activeIncident}
          objectApi={objectApi}
          recommendation={investigation?.current_recommendation || activeIncident?.ai_recommendation}
        />
      </Box>
    </Box>
  );
}

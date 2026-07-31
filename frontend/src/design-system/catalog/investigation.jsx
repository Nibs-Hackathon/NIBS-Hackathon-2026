import { Box, Chip, Stack, Typography } from '@mui/material';
import { ConfidenceMeter, StatusBadge, normalizeStatus } from './status';

function evidenceItems(inputs) {
  if (!inputs) return [];
  if (Array.isArray(inputs)) return inputs.filter(Boolean).map(String);
  return [String(inputs)];
}

function numericText(value) {
  return String(value).replace(/-?\d+(?:\.\d+)?/g, (match) => Number(match).toFixed(2));
}

function findingText(value) {
  return String(value).replace(/-?\d+(?:\.\d+)?/g, (match) => Number(match).toFixed(0));
}

/** AgentStageCard */
export function AgentStageCard({
  name, state = 'queued', duration, confidence, active = false, onClick, className = '', sx,
}) {
  const status = normalizeStatus(state);
  return (
    <Box
      component="button"
      type="button"
      className={`rig-agent-stage ${active ? 'is-active' : ''} ${status === 'ai-active' || state === 'running' ? 'is-running' : ''} ${className}`}
      onClick={onClick}
      aria-pressed={active}
      sx={sx}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
        <Typography fontWeight={700}>{name}</Typography>
        <StatusBadge status={status} label={state} live={state === 'running'} />
      </Stack>
      <Stack direction="row" spacing={1.5} sx={{ mt: 1 }}>
        {duration != null && <Typography variant="caption" color="text.secondary">{Number(duration).toFixed(2)}s</Typography>}
        {confidence != null && <Typography className="rig-data">{Number(confidence).toFixed(2)}%</Typography>}
      </Stack>
    </Box>
  );
}

/** AgentPipeline — horizontal stage graph */
export function AgentPipeline({ stages = [], selectedId, onSelect, className = '', sx }) {
  return (
    <Box className={`rig-agent-pipeline ${className}`} sx={sx} role="list" aria-label="Agent pipeline">
      {stages.map((stage, index) => (
        <AgentStageCard
          key={stage.id || stage.name || index}
          name={stage.name || stage.agent || `Stage ${index + 1}`}
          state={stage.state}
          duration={stage.duration_seconds ?? stage.duration}
          confidence={stage.confidence}
          active={selectedId === (stage.id || stage.name || index)}
          onClick={() => onSelect?.(stage)}
        />
      ))}
      {!stages.length && <Typography color="text.secondary">No agents running</Typography>}
    </Box>
  );
}

/** TracePanel — expandable agent reasoning lineage */
export function TracePanel({ stages = [], selectedId, onSelect, className = '', sx }) {
  return (
    <Box className={`rig-trace-panel ${className}`} sx={sx}>
      <Box className="rig-trace-heading">
        <Box>
          <Typography className="rig-label">Agent decisions</Typography>
          <Typography variant="body2" color="text.secondary">
            Select a step to see its conclusion and supporting evidence.
          </Typography>
        </Box>
        <Chip size="small" label={`${stages.length} steps`} />
      </Box>
      <Stack spacing={1.25}>
        {stages.map((stage, index) => {
          const id = stage.id || stage.name || index;
          const open = selectedId === id;
          const evidence = evidenceItems(stage.inputs);
          return (
            <Box
              key={id}
              component="button"
              type="button"
              onClick={() => onSelect?.(stage)}
              className={`rig-trace-card ${open ? 'is-open' : ''}`}
              aria-expanded={open}
            >
              <Box className="rig-trace-summary">
                <span className="rig-trace-step">{String(index + 1).padStart(2, '0')}</span>
                <Box>
                  <Typography fontWeight={750}>{stage.name || stage.agent}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {open ? 'Showing decision details' : findingText(stage.reasoning || 'Decision recorded')}
                  </Typography>
                </Box>
                <Box className="rig-trace-meta">
                  {stage.confidence != null && <b>{Number(stage.confidence).toFixed(2)}%</b>}
                  <StatusBadge status={stage.state} label={stage.state} />
                </Box>
              </Box>
              {open && (
                <Box className="rig-trace-details">
                  {stage.reasoning && (
                    <Box className="rig-trace-finding">
                      <Typography className="rig-label">Finding</Typography>
                      <Typography>{findingText(stage.reasoning)}</Typography>
                    </Box>
                  )}
                  {stage.outputs && (
                    <Box className="rig-trace-action">
                      <Typography className="rig-label">Recommended next step</Typography>
                      <Typography>{numericText(stage.outputs)}</Typography>
                    </Box>
                  )}
                  {evidence.length > 0 && (
                    <Box className="rig-trace-evidence">
                      <Typography className="rig-label">Evidence used</Typography>
                      <Stack direction="row" gap={0.75} useFlexGap sx={{ flexWrap: 'wrap' }}>
                        {evidence.map((item, evidenceIndex) => (
                          <Chip
                            key={`${id}-evidence-${evidenceIndex}`}
                            size="small"
                            label={numericText(item)}
                            title={item}
                          />
                        ))}
                      </Stack>
                    </Box>
                  )}
                  <Box className="rig-trace-footer">
                    {stage.confidence != null && (
                      <ConfidenceMeter value={stage.confidence} label="Decision confidence" />
                    )}
                    {stage.duration && <Typography variant="caption">Completed in {numericText(stage.duration)}</Typography>}
                  </Box>
                </Box>
              )}
            </Box>
          );
        })}
        {!stages.length && <Typography color="text.secondary">No agent decisions recorded yet.</Typography>}
      </Stack>
    </Box>
  );
}

/** EvidencePanel */
export function EvidencePanel({ items = [], onSelect, className = '', sx }) {
  return (
    <Box className={`rig-evidence-panel ${className}`} sx={sx}>
      <Typography className="rig-label">Evidence</Typography>
      <Stack spacing={0.75} sx={{ mt: 1 }}>
        {items.map((item, index) => (
          <Box
            key={item.id || index}
            onClick={() => onSelect?.(item)}
            sx={{ p: 1, borderRadius: 1, border: '1px solid', borderColor: 'divider', cursor: onSelect ? 'pointer' : 'default' }}
          >
            <Typography fontWeight={700}>{item.title || item.type || 'Evidence'}</Typography>
            {item.source && <Typography variant="caption" color="text.secondary">{item.source}</Typography>}
            {item.detail && <Typography variant="body2" color="text.secondary">{item.detail}</Typography>}
          </Box>
        ))}
        {!items.length && <Typography color="text.secondary">No evidence attached</Typography>}
      </Stack>
    </Box>
  );
}

/** EvidenceGraph — node-link style chips */
export function EvidenceGraph({ nodes = [], className = '', sx }) {
  return (
    <Box className={`rig-evidence-graph ${className}`} sx={sx} role="list" aria-label="Evidence graph">
      {nodes.map((node, index) => (
        <Box key={node.id || index} className="rig-evidence-node" role="listitem">
          <Typography className="rig-label" sx={{ fontSize: 9 }}>{node.type || 'node'}</Typography>
          <Typography fontWeight={700}>{node.label}</Typography>
        </Box>
      ))}
      {!nodes.length && <Typography color="text.secondary">No graph nodes</Typography>}
    </Box>
  );
}

/** RecommendationPanel */
export function RecommendationPanel({
  title = 'Recommended action', recommendation, confidence, dissent, action, className = '', sx,
}) {
  return (
    <Box className={`rig-recommendation-panel ${className}`} sx={{ borderLeft: `3px solid ${resolveTone('info').main}`, ...sx }}>
      <Typography className="rig-label">{title}</Typography>
      <Typography fontWeight={700} sx={{ mt: 0.5 }}>{recommendation}</Typography>
      {confidence != null && <ConfidenceMeter value={confidence} sx={{ mt: 1 }} />}
      {dissent && <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>Dissent: {dissent}</Typography>}
      {action && <Box sx={{ mt: 1.5 }}>{action}</Box>}
    </Box>
  );
}

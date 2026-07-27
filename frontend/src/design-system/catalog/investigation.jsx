import { Box, Stack, Typography } from '@mui/material';
import { ConfidenceMeter, StatusBadge, normalizeStatus } from './status';
import { resolveTone } from '../tokens';

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
        {duration != null && <Typography variant="caption" color="text.secondary">{duration}s</Typography>}
        {confidence != null && <Typography className="rig-data">{Math.round(confidence)}%</Typography>}
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
      <Typography className="rig-label">Agent trace</Typography>
      <Stack spacing={1} sx={{ mt: 1 }}>
        {stages.map((stage, index) => {
          const id = stage.id || stage.name || index;
          const open = selectedId == null || selectedId === id;
          return (
            <Box
              key={id}
              onClick={() => onSelect?.(stage)}
              sx={{
                p: 1.25, borderRadius: 1, cursor: 'pointer',
                border: '1px solid', borderColor: selectedId === id ? resolveTone('ai-active').main : 'divider',
                bgcolor: selectedId === id ? 'rgba(94,77,178,.08)' : 'transparent',
              }}
            >
              <Stack direction="row" justifyContent="space-between">
                <Typography fontWeight={700}>{stage.name || stage.agent}</Typography>
                <StatusBadge status={stage.state} label={stage.state} />
              </Stack>
              {open && (
                <Box sx={{ mt: 1 }}>
                  {stage.reasoning && <Typography variant="body2" color="text.secondary">{stage.reasoning}</Typography>}
                  {stage.inputs && <Typography className="rig-mono" sx={{ mt: 0.5 }}>in: {String(stage.inputs)}</Typography>}
                  {stage.outputs && <Typography className="rig-mono">out: {String(stage.outputs)}</Typography>}
                  {stage.modelId && <Typography className="rig-mono" color="text.secondary">model: {stage.modelId}</Typography>}
                  {stage.duration && <Typography className="rig-mono" color="text.secondary">duration: {stage.duration}</Typography>}
                </Box>
              )}
            </Box>
          );
        })}
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

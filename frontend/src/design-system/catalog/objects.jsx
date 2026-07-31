import { Box, Stack, Typography } from '@mui/material';
import { StatusBadge, RiskBadge } from './status';
import { resolveTone } from '../tokens';

/** ObjectRow — compact list item (ListRow base) */
export function ObjectRow({
  name, status, secondaryId, detail, selected = false, disabled = false, onClick, leading, trailing, className = '', sx,
}) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-object-row ${selected ? 'is-selected' : ''} ${className}`}
      onClick={onClick}
      disabled={disabled}
      aria-pressed={selected}
      sx={sx}
    >
      <Stack direction="row" spacing={1.25} alignItems="center" minWidth={0} flex={1}>
        {leading}
        <Box minWidth={0}>
          <Typography fontWeight={700} noWrap>{name}</Typography>
          <Stack direction="row" spacing={1} alignItems="center">
            {secondaryId && <Typography className="rig-mono" color="text.secondary" noWrap>{secondaryId}</Typography>}
            {detail && <Typography variant="caption" color="text.secondary" noWrap>{detail}</Typography>}
          </Stack>
        </Box>
      </Stack>
      <Stack direction="row" spacing={1} alignItems="center" flexShrink={0}>
        {status && <StatusBadge status={status} label={status} />}
        {trailing}
      </Stack>
    </Box>
  );
}

/** IncidentQueueItem */
export function IncidentQueueItem({
  id, title, severity, age, assetName, selected = false, onClick, className = '', sx,
}) {
  const status = severity || 'attention';
  const t = resolveTone(status);
  return (
    <Box
      component="button"
      type="button"
      className={`rig-list-row ${selected ? 'is-selected' : ''} ${className}`}
      onClick={onClick}
      aria-pressed={selected}
      sx={sx}
    >
      <Box className="rig-severity-stripe" style={{ backgroundColor: t.main }} aria-hidden />
      <Box flex={1} minWidth={0} textAlign="left">
        <Typography fontWeight={700} noWrap>{title || 'Incident'}</Typography>
        <Typography variant="caption" color="text.secondary" noWrap>
          {[assetName, age, id].filter(Boolean).join(' · ')}
        </Typography>
      </Box>
      <StatusBadge status={status} label={severity || status} />
    </Box>
  );
}

/** WorkOrderCard — kanban card */
export function WorkOrderCard({
  title, priority, asset, cost, window, selected = false, onClick, className = '', sx,
}) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-work-order-card ${selected ? 'is-selected' : ''} ${className}`}
      onClick={onClick}
      aria-pressed={selected}
      sx={sx}
    >
      <Stack direction="row" justifyContent="space-between" spacing={1}>
        <Typography fontWeight={700}>{title}</Typography>
        {priority && <StatusBadge status={priority === 'P1' ? 'critical' : 'advisory'} label={priority} />}
      </Stack>
      {asset && <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5 }}>{asset}</Typography>}
      <Stack direction="row" spacing={1.5} sx={{ mt: 1 }}>
        {cost != null && <Typography className="rig-data">{typeof cost === 'number' ? `$${cost.toLocaleString()}` : cost}</Typography>}
        {window && <Typography variant="caption" color="text.secondary">{window}</Typography>}
      </Stack>
    </Box>
  );
}

/** AssetTreeNode */
export function AssetTreeNode({
  name, health, depth = 0, selected = false, onClick, expanded, onToggle, children, className = '', sx,
}) {
  const status = health < 50 ? 'critical' : health < 80 ? 'attention' : 'nominal';
  return (
    <Box className={className} sx={sx}>
      <ObjectRow
        name={name}
        status={status}
        detail={health != null ? `${Math.round(health)}%` : undefined}
        selected={selected}
        onClick={onClick}
        leading={
          onToggle ? (
            <Box
              component="button"
              type="button"
              onClick={(e) => { e.stopPropagation(); onToggle(); }}
              sx={{ border: 0, background: 'transparent', color: 'text.secondary', cursor: 'pointer', width: 20 }}
              aria-expanded={expanded}
            >
              {expanded ? '−' : '+'}
            </Box>
          ) : (
            <Box sx={{ width: depth * 12 }} />
          )
        }
        trailing={health != null ? <RiskBadge value={100 - health} /> : null}
        sx={{ pl: 1 + depth * 1.5 }}
      />
      {expanded && children}
    </Box>
  );
}

/** TwinNode — schematic anchor */
export function TwinNode({
  label, x = 0, y = 0, risk = false, selected = false, onClick, className = '', sx,
}) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-twin-node ${selected ? 'is-selected' : ''} ${risk ? 'is-risk' : ''} ${className}`}
      style={{ left: x, top: y }}
      onClick={onClick}
      aria-pressed={selected}
      sx={sx}
    >
      <Typography className="rig-label" sx={{ fontSize: 9 }}>{label}</Typography>
    </Box>
  );
}

/** ReportIndexItem */
export function ReportIndexItem({
  title, date, approvalState, selected = false, onClick, className = '', sx,
}) {
  return (
    <ObjectRow
      name={title}
      detail={date}
      status={approvalState}
      selected={selected}
      onClick={onClick}
      className={className}
      sx={sx}
    />
  );
}

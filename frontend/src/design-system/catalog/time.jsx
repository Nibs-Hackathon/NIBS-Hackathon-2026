import { Box, Stack, Typography } from '@mui/material';
import { StatusBadge, normalizeStatus } from './status';
import { resolveTone } from '../tokens';

/** EventMarker */
export function EventMarker({ title, time, detail, status = 'info', className = '', sx }) {
  const t = resolveTone(normalizeStatus(status));
  return (
    <Box className={`rig-timeline-item ${className}`} sx={sx}>
      <Box className="rig-timeline-rail">
        <Box className="rig-timeline-dot" style={{ backgroundColor: t.main }} />
        <Box className="rig-timeline-line" />
      </Box>
      <Box className="rig-timeline-body">
        <Stack direction="row" justifyContent="space-between" spacing={1}>
          <Typography fontWeight={700}>{title}</Typography>
          {time && <Typography className="rig-mono" color="text.secondary">{time}</Typography>}
        </Stack>
        {detail && <Typography variant="body2" color="text.secondary" sx={{ mt: 0.35 }}>{detail}</Typography>}
      </Box>
    </Box>
  );
}

/** Timeline — variant="incident" adds decision markers styling */
export function Timeline({ items = [], variant = 'default', onSelect, className = '', sx }) {
  return (
    <Box className={`rig-timeline ${className}`} sx={sx} role="list" aria-label={variant === 'incident' ? 'Incident timeline' : 'Timeline'}>
      {items.map((item, index) => (
        <Box
          key={item.id || index}
          role="listitem"
          onClick={() => onSelect?.(item)}
          sx={{ cursor: onSelect ? 'pointer' : 'default' }}
        >
          <EventMarker
            title={item.title}
            time={item.time}
            detail={item.description || item.detail}
            status={item.status || item.tone || (item.decision ? 'ai-active' : 'info')}
          />
          {variant === 'incident' && item.decision && (
            <Typography className="rig-label" sx={{ ml: 3.5, mb: 1.5, color: resolveTone('ai-active').main }}>
              Decision · {item.decision}
            </Typography>
          )}
        </Box>
      ))}
      {!items.length && <Typography color="text.secondary" sx={{ p: 1 }}>No events</Typography>}
    </Box>
  );
}

/** IncidentTimeline — alias */
export function IncidentTimeline(props) {
  return <Timeline {...props} variant="incident" />;
}

/** AuditEvent — immutable log row */
export function AuditEvent({ who, what, when, objectLabel, className = '', sx }) {
  return (
    <Box className={`rig-audit-event ${className}`} sx={sx}>
      <StatusBadge status="info" label="Audit" />
      <Typography component="span" className="rig-data">{who || 'Operator'}</Typography>
      <Typography component="span">{what}</Typography>
      {objectLabel && <Typography component="span" className="rig-mono">{objectLabel}</Typography>}
      {when && <Typography component="span" className="rig-mono">{when}</Typography>}
    </Box>
  );
}

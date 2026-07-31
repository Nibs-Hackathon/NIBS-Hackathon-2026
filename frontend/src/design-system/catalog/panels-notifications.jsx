import { Box, Stack, Typography } from '@mui/material';
import { StatusBadge } from './status';
import { resolveTone } from '../tokens';

/** NotificationInbox — lives inside WorkspacePanel */
export function NotificationInbox({ items = [], onSelect, className = '', sx }) {
  if (!items.length) {
    return <Typography color="text.secondary" className={className} sx={sx}>No notifications</Typography>;
  }
  return (
    <Stack spacing={0.5} className={className} sx={sx} role="list" aria-label="Notifications">
      {items.map((item, index) => {
        const t = resolveTone(item.tone || item.severity || 'info');
        return (
          <Box
            key={item.id || index}
            role="listitem"
            onClick={() => onSelect?.(item)}
            sx={{
              p: 1.25, borderRadius: 1, cursor: onSelect ? 'pointer' : 'default',
              borderLeft: `3px solid ${t.main}`, bgcolor: item.unread ? 'rgba(38,132,255,.06)' : 'transparent',
              '&:hover': onSelect ? { bgcolor: 'action.hover' } : undefined,
            }}
          >
            <Stack direction="row" justifyContent="space-between" spacing={1}>
              <Typography fontWeight={700}>{item.title}</Typography>
              {item.time && <Typography className="rig-mono" color="text.secondary">{item.time}</Typography>}
            </Stack>
            {item.message && <Typography variant="body2" color="text.secondary">{item.message}</Typography>}
            {item.severity && <StatusBadge status={item.severity} label={item.severity} sx={{ mt: 0.5 }} />}
          </Box>
        );
      })}
    </Stack>
  );
}

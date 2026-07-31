import { Box, Button, Stack, Typography } from '@mui/material';
import { StatusBadge } from './status';
import { SectionHeader } from './panels';

/** BriefDocument — structured executive summary */
export function BriefDocument({
  title, summary, sections = [], metrics = [], className = '', sx,
}) {
  return (
    <Box className={`rig-brief-document ${className}`} sx={sx}>
      <SectionHeader eyebrow="Executive brief" title={title || 'Operating brief'} />
      {summary && <Typography sx={{ mt: 1, maxWidth: '68ch' }}>{summary}</Typography>}
      {metrics.length > 0 && (
        <Stack direction="row" spacing={2} sx={{ mt: 2, flexWrap: 'wrap' }}>
          {metrics.map((metric, index) => (
            <Box key={metric.label || index}>
              <Typography className="rig-label">{metric.label}</Typography>
              <Typography className="rig-kpi" sx={{ fontSize: '1.25rem' }}>{metric.value}</Typography>
            </Box>
          ))}
        </Stack>
      )}
      {sections.map((section, index) => (
        <Box key={section.title || index} sx={{ mt: 2 }}>
          <Typography className="rig-label">{section.title}</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{section.body}</Typography>
        </Box>
      ))}
    </Box>
  );
}

/** ApprovalStamp — signatory + timestamp + status */
export function ApprovalStamp({
  signatory, timestamp, status = 'Awaiting approval', className = '', sx,
}) {
  return (
    <Box className={`rig-approval-stamp ${className}`} sx={sx}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography className="rig-label">Approval</Typography>
        <StatusBadge status={status} label={status} />
      </Stack>
      <Typography fontWeight={700} sx={{ mt: 1 }}>{signatory || '—'}</Typography>
      {timestamp && <Typography className="rig-mono" color="text.secondary">{timestamp}</Typography>}
    </Box>
  );
}

/** EvidenceAppendixLink — jump to investigation trace */
export function EvidenceAppendixLink({ label = 'Open evidence appendix', onClick, disabled = false, className = '', sx }) {
  return (
    <Button
      className={className}
      onClick={onClick}
      disabled={disabled}
      sx={{ textTransform: 'none', justifyContent: 'flex-start', ...sx }}
    >
      {label}
    </Button>
  );
}

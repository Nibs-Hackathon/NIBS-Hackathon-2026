import { Box, Button, Slider, Stack, TextField, Typography } from '@mui/material';
import { Close } from '@mui/icons-material';

/** PrimaryCTA — one per panel maximum */
export function PrimaryCTA({ children, loading, disabled, ...props }) {
  return (
    <Button variant="contained" disabled={disabled || loading} sx={{ textTransform: 'none', fontWeight: 700 }} {...props}>
      {loading ? 'Working…' : children}
    </Button>
  );
}

/** DecisionButtonGroup — Accept / Modify / Reject */
export function DecisionButtonGroup({
  onAccept, onModify, onReject, disabled = false, acceptLabel = 'Accept', modifyLabel = 'Modify', rejectLabel = 'Reject',
}) {
  return (
    <Stack direction="row" spacing={1} flexWrap="wrap">
      <Button variant="contained" color="success" disabled={disabled} onClick={onAccept} sx={{ textTransform: 'none' }}>{acceptLabel}</Button>
      <Button variant="outlined" disabled={disabled} onClick={onModify} sx={{ textTransform: 'none' }}>{modifyLabel}</Button>
      <Button variant="outlined" color="error" disabled={disabled} onClick={onReject} sx={{ textTransform: 'none' }}>{rejectLabel}</Button>
    </Stack>
  );
}

/** RationaleField — required for decisions (Epic 5 enforces ≥20 chars). Part 8: Ctrl/⌘ Enter submits. */
export function RationaleField({
  value, onChange, minLength = 20, required = true, disabled = false, label = 'Rationale',
  onSubmitShortcut, inputRef, className = '', sx,
}) {
  const len = String(value || '').trim().length;
  const invalid = required && len > 0 && len < minLength;
  const canSubmit = !disabled && (!required || len >= minLength);
  return (
    <Box className={className} sx={{ flex: 1, minWidth: 200, ...sx }}>
      <TextField
        fullWidth size="small" multiline minRows={2}
        label={label}
        value={value || ''}
        onChange={(e) => onChange?.(e.target.value)}
        disabled={disabled}
        error={invalid}
        inputRef={inputRef}
        helperText={required ? `${len}/${minLength} characters minimum · Ctrl/⌘ Enter to accept` : undefined}
        onKeyDown={(event) => {
          if ((event.metaKey || event.ctrlKey) && event.key === 'Enter' && canSubmit) {
            event.preventDefault();
            onSubmitShortcut?.();
          }
        }}
      />
    </Box>
  );
}

/** ScenarioSlider — what-if control */
export function ScenarioSlider({
  value = 0, onChange, min = 0, max = 10, step = 1, label = 'Scenario stress', className = '', sx,
}) {
  return (
    <Box className={className} sx={sx}>
      <Stack direction="row" justifyContent="space-between">
        <Typography className="rig-label">{label}</Typography>
        <Typography className="rig-data">{value}</Typography>
      </Stack>
      <Slider value={value} min={min} max={max} step={step} onChange={(_, v) => onChange?.(v)} aria-label={label} />
    </Box>
  );
}

/** FilterChipBar */
export function FilterChipBar({ chips = [], onClear, className = '', sx }) {
  return (
    <Box className={`rig-filter-chips ${className}`} sx={sx} role="list" aria-label="Active filters">
      {chips.map((chip) => (
        <Box
          component="button"
          type="button"
          key={chip.id || chip.label}
          className={`rig-filter-chip ${chip.active !== false ? 'is-active' : ''}`}
          onClick={() => chip.onRemove?.(chip)}
          role="listitem"
        >
          {chip.label}
          {chip.onRemove && <Close sx={{ fontSize: 14 }} />}
        </Box>
      ))}
      {chips.length > 0 && onClear && (
        <Button size="small" onClick={onClear} sx={{ textTransform: 'none' }}>Clear all</Button>
      )}
    </Box>
  );
}

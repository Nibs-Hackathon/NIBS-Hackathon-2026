import { useState } from 'react';
import { Box, Drawer, IconButton, Stack, Tab, Tabs, Typography } from '@mui/material';
import { Close } from '@mui/icons-material';
import { EmptyState } from './data';
import { DecisionButtonGroup, RationaleField, PrimaryCTA } from './actions';
import { NotificationInbox } from './panels-notifications';
import { EvidencePanel, RecommendationPanel } from './investigation';

/** SectionHeader */
export function SectionHeader({ eyebrow, title, description, action, className = '', sx }) {
  return (
    <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ sm: 'flex-end' }} spacing={1} className={className} sx={sx}>
      <Box>
        {eyebrow && <Typography className="rig-label">{eyebrow}</Typography>}
        <Typography sx={{ fontSize: '1.125rem', fontWeight: 600, letterSpacing: '-0.01em', mt: 0.35 }}>{title}</Typography>
        {description && <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{description}</Typography>}
      </Box>
      {action}
    </Stack>
  );
}

/** SplitPaneHandle */
export function SplitPaneHandle({ onMouseDown, className = '', sx, orientation = 'vertical' }) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-split-handle ${className}`}
      aria-label="Resize panels"
      onMouseDown={onMouseDown}
      sx={{
        ...(orientation === 'horizontal' ? { height: 6, width: '100%', cursor: 'row-resize' } : {}),
        ...sx,
      }}
    />
  );
}

/** ObjectInspector — fixed right pane for selected object */
export function ObjectInspector({
  title, subtitle, empty = false, emptyTitle = 'Select an object', emptyDescription = 'Choose an asset, incident, or work order to inspect.',
  children, sections, footer, width, className = '', sx,
}) {
  return (
    <Box className={`rig-object-inspector ${className}`} sx={{ maxWidth: width || 360, ...sx }} role="complementary" aria-label="Object inspector">
      {(title || subtitle) && (
        <Box sx={{ p: 2, borderBottom: '1px solid rgba(164,196,228,.12)' }}>
          {subtitle && <Typography className="rig-label">{subtitle}</Typography>}
          {title && <Typography fontWeight={700}>{title}</Typography>}
        </Box>
      )}
      <Box className="rig-object-inspector-body">
        {empty ? (
          <Box className="rig-object-inspector-empty">
            <EmptyState title={emptyTitle} description={emptyDescription} />
          </Box>
        ) : (
          <>
            {sections?.map((section, index) => (
              <Box key={section.id || section.title || index} className="rig-object-inspector-section">
                {section.title && <Typography className="rig-label">{section.title}</Typography>}
                {section.content}
              </Box>
            ))}
            {children}
          </>
        )}
      </Box>
      {footer && <Box sx={{ p: 1.5, borderTop: '1px solid rgba(164,196,228,.12)' }}>{footer}</Box>}
    </Box>
  );
}

/** WorkspacePanel — global ⌘J slide-over */
export function WorkspacePanel({
  open, onClose, auditContent, notifications = [], onNotificationClick, width = 400, className = '', sx,
}) {
  const [tab, setTab] = useState(0);
  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{ className: `rig-workspace-panel ${className}`, sx: { width: { xs: '100%', sm: width }, ...sx } }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ px: 2, pt: 2 }}>
        <Typography className="rig-label">Workspace panel</Typography>
        <IconButton onClick={onClose} aria-label="Close workspace panel"><Close /></IconButton>
      </Stack>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} className="rig-workspace-panel-tabs" sx={{ px: 1 }}>
        <Tab label="Audit" />
        <Tab label="Notifications" />
      </Tabs>
      <Box className="rig-workspace-panel-body">
        {tab === 0 && (auditContent || <Typography color="text.secondary">No audit activity</Typography>)}
        {tab === 1 && <NotificationInbox items={notifications} onSelect={onNotificationClick} />}
      </Box>
    </Drawer>
  );
}

/**
 * DecisionSurface — shared core for DecisionBar + DecisionRail
 * variant: operational | executive
 */
export function DecisionSurface({
  variant = 'operational',
  recommendation,
  rationale, onRationaleChange,
  onAccept, onModify, onReject,
  disabled = false, busy = false,
  minRationale = 0,
  rationaleInputRef,
  acceptLabel, modifyLabel, rejectLabel,
  children, className = '', sx,
}) {
  const rationaleOk = minRationale <= 0 || String(rationale || '').trim().length >= minRationale;
  const actionsDisabled = disabled || busy || !rationaleOk;
  const shellClass = variant === 'executive' ? 'rig-decision-rail' : 'rig-decision-bar';
  const labels = variant === 'executive'
    ? { acceptLabel: acceptLabel || 'Approve', modifyLabel: modifyLabel || 'Defer', rejectLabel: rejectLabel || 'Escalate' }
    : { acceptLabel, modifyLabel, rejectLabel };
  return (
    <Box className={`${shellClass} ${className}`} sx={sx} role="region" aria-label={variant === 'executive' ? 'Decision rail' : 'Decision bar'} data-decision-surface={variant}>
      {recommendation && (
        <Box sx={{ flex: variant === 'executive' ? undefined : 1, minWidth: 160 }}>
          <Typography className="rig-label">Recommendation</Typography>
          <Typography fontWeight={700}>{recommendation}</Typography>
        </Box>
      )}
      <RationaleField
        value={rationale}
        onChange={onRationaleChange}
        minLength={minRationale > 0 ? minRationale : 20}
        required={minRationale > 0}
        disabled={disabled || busy}
        inputRef={rationaleInputRef}
        onSubmitShortcut={() => { if (!actionsDisabled) onAccept?.(); }}
      />
      <DecisionButtonGroup
        disabled={actionsDisabled}
        onAccept={onAccept}
        onModify={onModify}
        onReject={onReject}
        {...labels}
      />
      {children}
    </Box>
  );
}

/** DecisionBar — sticky operational (Epic 5: rationale required by default) */
export function DecisionBar({ minRationale = 20, ...props }) {
  return <DecisionSurface variant="operational" minRationale={minRationale} {...props} />;
}

/** DecisionRail — executive */
export function DecisionRail(props) {
  return <DecisionSurface variant="executive" {...props} />;
}

/** CaseDossier — EvidencePanel + RecommendationPanel composition */
export function CaseDossier({
  title = 'Case dossier', evidence = [], recommendation, confidence, children, className = '', sx,
}) {
  return (
    <Box className={`rig-case-dossier ${className}`} sx={sx}>
      <SectionHeader eyebrow="Dossier" title={title} />
      <EvidencePanel items={evidence} />
      {recommendation && <RecommendationPanel recommendation={recommendation} confidence={confidence} />}
      {children}
    </Box>
  );
}

export { PrimaryCTA };

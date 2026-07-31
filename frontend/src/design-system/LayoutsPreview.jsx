/**
 * Isolated layouts preview — Epic 2 exit criterion.
 * Route: /__layouts — placeholders only, no live data.
 */
import { useState } from 'react';
import { Box, Button, CssBaseline, Stack, ThemeProvider, Typography } from '@mui/material';
import { useColorMode } from '../context/ColorModeContext';
import { createRigOSV2Theme } from './RigOSV2Theme';
import { AuditSpine, PrimaryCTA } from './catalog';
import {
  ApplicationShell,
  ExplorerLayout,
  ExecutiveLayout,
  IncidentLayout,
  InvestigationLayout,
  KanbanLayout,
  LayoutPlaceholder,
  MissionControlLayout,
} from './layouts';
import './layouts/layouts.css';
import './catalog.css';
import './motion.css';

const LAYOUTS = [
  { id: 'mission', label: 'Mission Control' },
  { id: 'explorer', label: 'Explorer (twin)' },
  { id: 'forecast', label: 'Explorer (forecast)' },
  { id: 'incident', label: 'Incident' },
  { id: 'investigation', label: 'Investigation' },
  { id: 'kanban', label: 'Kanban' },
  { id: 'executive', label: 'Executive' },
];

function LayoutDemo({ id }) {
  switch (id) {
    case 'mission':
      return <MissionControlLayout />;
    case 'explorer':
      return <ExplorerLayout canvasVariant="twin" signalStrip={<LayoutPlaceholder label="signalStrip" />} />;
    case 'forecast':
      return <ExplorerLayout canvasVariant="forecast" />;
    case 'incident':
      return <IncidentLayout />;
    case 'investigation':
      return <InvestigationLayout />;
    case 'kanban':
      return <KanbanLayout />;
    case 'executive':
      return <ExecutiveLayout />;
    default:
      return <LayoutPlaceholder label="Unknown layout" />;
  }
}

function LayoutsBody() {
  const { mode, toggle } = useColorMode();
  const [layoutId, setLayoutId] = useState('mission');
  const isExecutive = layoutId === 'executive';

  return (
    <ThemeProvider theme={createRigOSV2Theme(mode)}>
      <CssBaseline />
      <ApplicationShell
        title={LAYOUTS.find((item) => item.id === layoutId)?.label || 'Layouts'}
        breadcrumbs={[
          { label: 'Design system' },
          { label: 'Layouts preview' },
        ]}
        scope="Alpha Refinery"
        facilities={['Alpha Refinery', 'Enterprise view']}
        connected
        syncAge={1}
        activeNavId={layoutId === 'forecast' ? 'forecasting' : layoutId === 'mission' ? 'command' : layoutId}
        onNavigate={(item) => {
          const map = {
            command: 'mission',
            assets: 'explorer',
            forecasting: 'forecast',
            incidents: 'incident',
            investigation: 'investigation',
            maintenance: 'kanban',
            reports: 'executive',
          };
          if (map[item.id]) setLayoutId(map[item.id]);
        }}
        showAuditSpine={!isExecutive}
        auditSpine={(
          <AuditSpine
            events={[
              { who: 'Preview', what: 'Layout slot demo', when: 'now', objectLabel: layoutId },
            ]}
          />
        )}
        headerActions={<PrimaryCTA onClick={toggle}>{mode === 'dark' ? 'Light' : 'Dark'}</PrimaryCTA>}
        workspacePanelAudit={<Typography variant="body2" color="text.secondary">WorkspacePanel slot — no API.</Typography>}
        notifications={[{ id: 1, title: 'Preview notice', message: 'Epic 2 placeholder', unread: true }]}
      >
        <Stack spacing={1.5} sx={{ height: '100%', minHeight: 0 }}>
          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
            {LAYOUTS.map((item) => (
              <Button
                key={item.id}
                size="small"
                variant={layoutId === item.id ? 'contained' : 'outlined'}
                onClick={() => setLayoutId(item.id)}
                sx={{ textTransform: 'none' }}
              >
                {item.label}
              </Button>
            ))}
          </Stack>
          <Typography variant="caption" color="text.secondary">
            Epic 2 preview · slot placeholders only · resize below 1024px for tab mode
          </Typography>
          <Box sx={{ flex: 1, minHeight: 420 }}>
            <LayoutDemo id={layoutId} />
          </Box>
        </Stack>
      </ApplicationShell>
    </ThemeProvider>
  );
}

export function LayoutsPreview() {
  return <LayoutsBody />;
}

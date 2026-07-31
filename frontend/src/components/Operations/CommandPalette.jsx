import { useEffect, useState } from 'react';
import { Box, Dialog, DialogContent, InputAdornment, Stack, TextField, Typography } from '@mui/material';
import { Search } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const commands = [
  ['Go to Mission Control', '/', 'Operations overview'],
  ['Open Asset Explorer', '/assets', 'Equipment health and AI summaries'],
  ['Review Incident Audit', '/incident-simulator', 'Incident history and evidence'],
  ['Open Live Investigation', '/agent-monitor', 'Active agents, reasoning and approvals'],
  ['Inspect AI Activity', '/ai-activity', 'Autonomous agent event stream'],
  ['Open Maintenance Command', '/maintenance', 'Priority work queue'],
  ['Open Health Forecast', '/health-prediction', 'Failure risk and intervention'],
  ['Open Digital Twin', '/digital-twin', 'Live facility map'],
  ['Open Reports', '/reports', 'Executive and operational reports'],
];

export function CommandPalette({ open, onClose }) {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();
  useEffect(() => { if (!open) setQuery(''); }, [open]);
  const visible = commands.filter(([label, , detail]) => `${label} ${detail}`.toLowerCase().includes(query.toLowerCase()));
  const select = (path) => { navigate(path); onClose(); };
  return <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" PaperProps={{ sx: { overflow: 'hidden', borderRadius: 3, bgcolor: 'background.paper', backdropFilter: 'blur(28px)' } }}><DialogContent sx={{ p: 1.25 }}><TextField autoFocus fullWidth placeholder="Search RigOS or run a command…" value={query} onChange={(event) => setQuery(event.target.value)} InputProps={{ startAdornment: <InputAdornment position="start"><Search /></InputAdornment> }} sx={{ '& .MuiOutlinedInput-notchedOutline': { border: 0 } }} /> <Box sx={{ px: 1, py: 1.25 }}><Typography variant="caption" color="text.secondary" sx={{ letterSpacing: '.12em', fontWeight: 700 }}>COMMANDS</Typography></Box><Stack spacing={.4}>{visible.map(([label, path, detail]) => <Box key={path} role="button" tabIndex={0} onClick={() => select(path)} onKeyDown={(event) => event.key === 'Enter' && select(path)} sx={{ p: 1.3, borderRadius: 2, cursor: 'pointer', '&:hover': { bgcolor: 'action.hover', transform: 'translateX(2px)' }, transition: 'all .18s ease' }}><Typography fontWeight={700}>{label}</Typography><Typography variant="caption" color="text.secondary">{detail}</Typography></Box>)}</Stack></DialogContent></Dialog>;
}

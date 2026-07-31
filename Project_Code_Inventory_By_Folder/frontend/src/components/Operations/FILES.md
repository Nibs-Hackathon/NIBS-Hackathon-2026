# Folder: frontend/src/components/Operations Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/components/Operations`

Contains 4 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/components/Operations/Assistant.jsx

**Folder path:** `frontend/src/components/Operations`

**File path:** `frontend/src/components/Operations/Assistant.jsx`

```javascript
import { useState } from 'react';
import { Box, Button, CircularProgress, Drawer, IconButton, Stack, TextField, Typography } from '@mui/material';
import { Close, Memory, Send } from '@mui/icons-material';
import { askAssistant } from '../../api/client';

const prompts = ['What requires attention right now?', 'Explain the active investigation', 'Summarize maintenance risk'];

export function Assistant() {
  const [open, setOpen] = useState(false); const [question, setQuestion] = useState(''); const [busy, setBusy] = useState(false);
  const [messages, setMessages] = useState([]);
  const submit = async (value = question) => { const text = value.trim(); if (!text || busy) return; setMessages((items) => [...items, { role: 'operator', text }]); setQuestion(''); setBusy(true); try { const response = await askAssistant(text); setMessages((items) => [...items, { role: 'assistant', text: response.data.answer }]); } catch { setMessages((items) => [...items, { role: 'assistant', text: 'I could not reach the operational knowledge service. Please try again.' }]); } finally { setBusy(false); } };
  return <><IconButton onClick={() => setOpen(true)} aria-label="Open RigOS Assistant" sx={{ position: 'fixed', zIndex: 1200, right: { xs: 18, md: 32 }, bottom: { xs: 18, md: 30 }, width: 58, height: 58, color: '#fff', background: 'linear-gradient(135deg,#1677FF,#6D5DFB)', boxShadow: '0 14px 36px rgba(22,119,255,.36)', '&:hover': { background: 'linear-gradient(135deg,#2685FF,#7C6CFF)', transform: 'translateY(-2px)' }, transition: 'all .2s ease' }}><Memory /></IconButton><Drawer anchor="right" open={open} onClose={() => setOpen(false)} PaperProps={{ sx: { width: { xs: '100%', sm: 460 }, p: 2.25, bgcolor: 'background.paper', backdropFilter: 'blur(26px)' } }}><Stack direction="row" justifyContent="space-between" alignItems="start"><Box><Typography variant="overline" color="primary" fontWeight={850} letterSpacing=".14em">RIGOS AI</Typography><Typography variant="h5">Operations copilot</Typography><Typography variant="body2" color="text.secondary" sx={{ mt: .4 }}>Ask about equipment, incidents, evidence, or recommended next actions.</Typography></Box><IconButton onClick={() => setOpen(false)}><Close /></IconButton></Stack><Stack direction="row" flexWrap="wrap" gap={.75} sx={{ mt: 2 }}>{prompts.map((prompt) => <Button key={prompt} size="small" variant="outlined" onClick={() => submit(prompt)}>{prompt}</Button>)}</Stack><Box sx={{ flex: 1, overflowY: 'auto', my: 2.25, pr: .5 }}>{messages.length ? <Stack spacing={1.3}>{messages.map((message, index) => <Box key={index} sx={{ alignSelf: message.role === 'operator' ? 'flex-end' : 'flex-start', maxWidth: '90%', p: 1.3, borderRadius: 2.2, bgcolor: message.role === 'operator' ? 'primary.main' : 'action.hover', color: message.role === 'operator' ? '#fff' : 'text.primary', whiteSpace: 'pre-wrap' }}>{message.text}</Box>)}{busy && <CircularProgress size={20} />}</Stack> : <Box sx={{ pt: 8, textAlign: 'center' }}><Memory sx={{ color: 'primary.main', fontSize: 44 }} /><Typography fontWeight={750} sx={{ mt: 1 }}>How can I help?</Typography><Typography variant="body2" color="text.secondary" sx={{ mt: .5 }}>I use RigOS operational knowledge and live context.</Typography></Box>}</Box><Stack direction="row" spacing={1}><TextField fullWidth placeholder="Ask RigOS…" value={question} onChange={(event) => setQuestion(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); submit(); } }} /><Button variant="contained" onClick={() => submit()} disabled={!question.trim() || busy}><Send /></Button></Stack></Drawer></>;
}
```

## frontend/src/components/Operations/CommandPalette.jsx

**Folder path:** `frontend/src/components/Operations`

**File path:** `frontend/src/components/Operations/CommandPalette.jsx`

```javascript
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
```

## frontend/src/components/Operations/Primitives.jsx

**Folder path:** `frontend/src/components/Operations`

**File path:** `frontend/src/components/Operations/Primitives.jsx`

```javascript
import { Box, Paper, Stack, Typography } from '@mui/material';

export function PageHero({ eyebrow = 'RigOS Operations Center', title, description, action }) {
  return <Stack direction={{ xs: 'column', lg: 'row' }} justifyContent="space-between" spacing={3} sx={{ mb: { xs: 4, md: 6 }, pt: 1 }}><Box><Typography variant="overline" sx={{ color: '#55D6FF', letterSpacing: '.16em', fontWeight: 800 }}>{eyebrow}</Typography><Typography component="h1" sx={{ mt: .55, fontSize: 'clamp(2.8rem, 6vw, 5.8rem)', fontWeight: 800, lineHeight: .92, letterSpacing: '-.07em' }}>{title}</Typography><Typography sx={{ color: 'text.secondary', mt: 1.5, maxWidth: 680, fontSize: '1rem', lineHeight: 1.65 }}>{description}</Typography></Box>{action}</Stack>;
}

export function Metric({ label, value, detail, color = '#55D6FF' }) {
  return <Box sx={{ py: 1.25, px: { xs: 0, md: 1.5 }, borderLeft: { md: '1px solid rgba(164,196,228,.12)' } }}><Typography variant="caption" sx={{ color: 'text.secondary', textTransform: 'uppercase', letterSpacing: '.12em', fontWeight: 800 }}>{label}</Typography><Typography sx={{ color, fontSize: 'clamp(1.8rem,3vw,2.8rem)', fontWeight: 800, lineHeight: 1, letterSpacing: '-.06em', mt: .45 }}>{value}</Typography><Typography variant="caption" sx={{ color: 'text.secondary' }}>{detail}</Typography></Box>;
}

export function Panel({ title, children, action, sx }) {
  return <Paper elevation={0} sx={{ p: { xs: 0, md: 1 }, bgcolor: 'transparent', border: 0, boxShadow: 'none', ...sx }}><Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2.5 }}><Typography variant="overline" sx={{ color: '#77DFFF', letterSpacing: '.15em', fontWeight: 800 }}>{title}</Typography>{action}</Stack>{children}</Paper>;
}
```

## frontend/src/components/Operations/System.jsx

**Folder path:** `frontend/src/components/Operations`

**File path:** `frontend/src/components/Operations/System.jsx`

```javascript
import { Box, Chip, Paper, Stack, Typography } from '@mui/material';

export function GlassCard({ title, subtitle, children, sx }) { return <Paper sx={{ p: 2.25, borderRadius: 3, overflow: 'hidden', ...sx }}><Stack direction="row" justifyContent="space-between" sx={{ mb: 1.75 }}><Box><Typography fontWeight={780}>{title}</Typography>{subtitle && <Typography variant="caption" color="text.secondary">{subtitle}</Typography>}</Box></Stack>{children}</Paper>; }
export function StatusBadge({ label, tone = 'success' }) { const colors = { success: '#12B981', warning: '#F59E0B', danger: '#EF4444', info: '#55D6FF' }; const color = colors[tone]; return <Chip size="small" label={label} sx={{ color, bgcolor: `${color}14`, fontWeight: 800, letterSpacing: '.07em' }} />; }
export function HealthRing({ value }) { const color = value < 50 ? '#EF4444' : value < 80 ? '#F59E0B' : '#12B981'; return <Box sx={{ width: 104, height: 104, borderRadius: '50%', display: 'grid', placeItems: 'center', background: `conic-gradient(${color} ${Math.max(0, Math.min(100, value)) * 3.6}deg, rgba(127,148,178,.16) 0)` }}><Box sx={{ width: 84, height: 84, borderRadius: '50%', display: 'grid', placeItems: 'center', bgcolor: 'background.paper' }}><Typography variant="h5" fontWeight={800} sx={{ color }}>{Math.round(value)}%</Typography></Box></Box>; }
```

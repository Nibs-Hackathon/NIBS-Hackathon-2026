# Folder: frontend/src/ui Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/ui`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/ui/index.jsx

**Folder path:** `frontend/src/ui`

**File path:** `frontend/src/ui/index.jsx`

```javascript
import { Box, Button, Chip, CircularProgress, LinearProgress, Paper, Stack, TextField, Typography } from '@mui/material';
import { Search } from '@mui/icons-material';

const tones = { neutral: '#94A3B8', info: '#4F8CFF', success: '#22C55E', warning: '#F59E0B', danger: '#EF4444' };

export function PageLayout({ eyebrow, title, description, action, children }) {
  return <Box className="premium-page"><Stack className="premium-page-hero" direction={{ xs: 'column', lg: 'row' }} justifyContent="space-between" alignItems={{ lg: 'end' }} spacing={3}><Box><Typography className="premium-eyebrow">{eyebrow}</Typography><Typography component="h1" className="premium-title">{title}</Typography>{description && <Typography className="premium-description">{description}</Typography>}</Box>{action}</Stack>{children}</Box>;
}

export function SectionHeader({ label, title, description, action }) {
  return <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ sm: 'end' }} spacing={2} className="premium-section-header"><Box>{label && <Typography className="premium-eyebrow">{label}</Typography>}<Typography className="premium-section-title">{title}</Typography>{description && <Typography className="premium-section-description">{description}</Typography>}</Box>{action}</Stack>;
}

export function Surface({ children, className = '', sx, interactive = false }) { return <Paper elevation={0} className={`premium-surface ${interactive ? 'is-interactive' : ''} ${className}`} sx={sx}>{children}</Paper>; }

export function StatusBadge({ children, tone = 'neutral', pulse = false }) { const color = tones[tone] || tones.neutral; return <Chip className="premium-status" label={<><i className={pulse ? 'is-pulsing' : ''} style={{ backgroundColor: color }} />{children}</>} size="small" sx={{ color, backgroundColor: `${color}14` }} />; }

export function MetricCard({ label, value, detail, tone = 'info', loading = false }) { return <Box className="premium-metric"><Typography className="premium-metric-label">{label}</Typography><Typography className="premium-metric-value" sx={{ color: tones[tone] || 'text.primary' }}>{loading ? <CircularProgress size={22} /> : value}</Typography>{detail && <Typography className="premium-metric-detail">{detail}</Typography>}</Box>; }

export function StatGrid({ children }) { return <Box className="premium-stat-grid">{children}</Box>; }

export function SearchBar({ value, onChange, placeholder = 'Search assets, incidents, knowledge…' }) { return <TextField value={value} onChange={(event) => onChange?.(event.target.value)} placeholder={placeholder} fullWidth size="small" InputProps={{ startAdornment: <Search fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} /> }} className="premium-search" />; }

export function Progress({ label, value, tone = 'info' }) { const color = tones[tone] || tones.info; return <Box className="premium-progress"><Stack direction="row" justifyContent="space-between"><Typography variant="caption" color="text.secondary">{label}</Typography><Typography variant="caption" sx={{ color }}>{Math.round(value || 0)}%</Typography></Stack><LinearProgress variant="determinate" value={Math.max(0, Math.min(100, value || 0))} sx={{ '& .MuiLinearProgress-bar': { backgroundColor: color } }} /></Box>; }

export function EmptyState({ title, description }) { return <Box className="premium-empty"><Box className="premium-empty-mark" /><Typography fontWeight={750}>{title}</Typography><Typography variant="body2" color="text.secondary">{description}</Typography></Box>; }

export function PrimaryButton({ children, ...props }) { return <Button variant="contained" className="premium-primary-button" {...props}>{children}</Button>; }
```

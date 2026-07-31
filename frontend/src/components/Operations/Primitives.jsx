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

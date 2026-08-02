/* Shared product view helpers — Epic 6 */
import { Box, Chip, Typography } from '@mui/material';
import {
  AccountTreeOutlined, ArticleOutlined, BuildOutlined, DevicesOutlined, MemoryOutlined,
  MoreHorizOutlined, ScienceOutlined, ShieldOutlined,
} from '@mui/icons-material';
import { motion, useReducedMotion } from 'motion/react';
import { MetricWithProvenance } from '../accountability';


export function InspectorMetric({ label: metricLabel, value, unit }) {
  const displayValue = value === null || value === undefined || value === '' ? '--' : value;
  return <Box><Typography>{metricLabel}</Typography><b>{displayValue}{displayValue !== '--' && unit ? <small>{unit}</small> : null}</b></Box>;
}

export function EvidenceItem({ icon, label: evidenceLabel, detail }) { return <Box><span>{icon}</span><Typography><b>{evidenceLabel}</b><small>{detail}</small></Typography><MoreHorizOutlined fontSize="small" /></Box>; }

export function MaintenanceSchedule({ work, lane, onSelect }) { return <Box className="maintenance-schedule-grid"><Box className="maintenance-days">{['Mon 14','Tue 15','Wed 16','Thu 17','Fri 18','Sat 19','Sun 20'].map((day) => <Typography key={day}>{day}</Typography>)}</Box>{work.map((item, index) => <button type="button" onClick={() => onSelect(item.id)} key={item.id} className="schedule-work" style={{ '--start': index % 5 + 1, '--span': index % 2 + 2 }}><b>{item.title}</b><span>{item.owner}  -  {item.downtime}</span></button>)}</Box>; }

export function MiniGraph({ values = [], label, area = false }) { const numbers = values.map(Number).filter(Number.isFinite); if (!numbers.length) return <Box className="mini-graph empty"><Typography>{label}</Typography></Box>; const max = Math.max(...numbers), min = Math.min(...numbers), span = Math.max(max - min, 1); const points = numbers.map((n, i) => `${i * (440 / Math.max(numbers.length - 1, 1))},${116 - ((n - min) / span) * 82}`).join(' '); return <Box className="mini-graph"><svg viewBox="0 0 440 130" preserveAspectRatio="none"><defs><linearGradient id="rigosFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#4f8cff" stopOpacity=".34" /><stop offset="1" stopColor="#4f8cff" stopOpacity="0" /></linearGradient></defs>{[28, 58, 88].map((y) => <line key={y} x1="0" x2="440" y1={y} y2={y} stroke="rgba(148,163,184,.15)" />)}{area && <polyline points={`0,130 ${points} 440,130`} fill="url(#rigosFill)" />}<polyline points={points} fill="none" stroke="#4f8cff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" /></svg><Typography>{label}</Typography></Box>; }

export function Health({ value, large = false }) { const health = round(value); const tone = health < 50 ? 'critical' : health < 80 ? 'watch' : 'nominal'; return <Box className={`health ${tone} ${large ? 'large' : ''}`}><Box><i style={{ width: `${Math.max(0, Math.min(health, 100))}%` }} /></Box><Typography>{health}%</Typography></Box>; }

export function Confidence({ value }) { const percent = round(Number(value) <= 1 ? Number(value) * 100 : value); return <Box className="confidence"><Box><i style={{ width: `${percent}%` }} /></Box><Typography variant="caption">{percent}% confidence</Typography></Box>; }

export function Status({ state }) { return <Chip size="small" className="state" label={label(state || 'Available')} />; }

export function Metric({ label: metricLabel, value, provenance = 'estimated' }) { return <MetricWithProvenance label={metricLabel} value={value} provenance={provenance} />; }

export function Empty({ text = '' }) {
  const lower = text.toLowerCase();
  const reduceMotion = useReducedMotion();
  const state = lower.includes('register') || lower.includes('facility') ? { Icon: DevicesOutlined, title: 'No facility assets in scope.', copy: 'Switch facility scope or wait for the asset register to populate.', action: 'Check the active facility scope.' } : lower.includes('incident') ? { Icon: ShieldOutlined, title: 'Facility operating normally.', copy: 'No incident records require operator review.', action: 'Continue monitoring live telemetry.' } : lower.includes('maintenance') ? { Icon: BuildOutlined, title: 'No scheduled maintenance.', copy: 'New work orders will appear after planning agent review.', action: 'Review asset condition trends.' } : lower.includes('report') ? { Icon: ArticleOutlined, title: 'Reports will appear after investigations.', copy: 'Completed evidence workflows generate decision-ready briefs here.', action: 'Review active investigations.' } : lower.includes('forecast') || lower.includes('health') ? { Icon: ScienceOutlined, title: 'Forecasting is standing by.', copy: 'Condition projections appear when enough asset telemetry is available.', action: 'Check connected asset telemetry.' } : lower.includes('workforce') || lower.includes('activity') ? { Icon: MemoryOutlined, title: 'AI workforce is ready.', copy: 'The reasoning trace starts automatically when an incident is received.', action: 'Review the live incident ledger.' } : lower.includes('asset') || lower.includes('refinery') ? { Icon: DevicesOutlined, title: 'Fleet condition is within threshold.', copy: 'Assets move here when health or incident signals need attention.', action: 'Inspect the asset portfolio.' } : { Icon: AccountTreeOutlined, title: 'Nothing needs attention here.', copy: 'RigOS will populate this workspace as operating data becomes available.', action: 'Return to Command Center.' };
  return <motion.div className="product-empty-state" initial={reduceMotion ? false : { opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduceMotion ? 0 : .2 }}><Box className="empty-state-mark"><state.Icon /></Box><Typography className="empty-state-title">{state.title}</Typography><Typography className="empty-state-copy">{state.copy}</Typography><Box className="empty-state-action">{state.action}</Box></motion.div>;
}

export function safeReasoning(value = '') { return /connection to server|operationalerror|permission denied/i.test(String(value)) ? 'Knowledge retrieval was unavailable for this workflow; the remaining agent evidence is retained.' : String(value); }

export function label(value = '') { return String(value).replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase()); }

export function formatTime(value) { if (!value) return 'Live record'; const date = new Date(value); return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }); }

export function formatDuration(seconds) { if (!Number.isFinite(Number(seconds))) return null; const total = Math.round(Number(seconds)); return total < 60 ? `${total}s` : `${Math.floor(total / 60)}m ${total % 60}s`; }

export function averageHealth(assets) { return assets.length ? round(assets.reduce((total, asset) => total + Number(asset.health || 0), 0) / assets.length) : 0; }

export function round(value) { return Math.round(Number(value) || 0); }

export function assetRisk(asset, incident) { const healthRisk = 100 - round(asset?.health); const incidentRisk = /critical/i.test(incident?.severity || '') ? 35 : /high/i.test(incident?.severity || '') ? 20 : 0; return Math.max(0, Math.min(100, healthRisk + incidentRisk)); }

// Legacy condition cards remain as implementation reference during the twin migration.
// eslint-disable-next-line no-unused-vars

export function traceLabel(agent, index) { const fallback = ['Telemetry', 'Atlas', 'Phoenix', 'Knowledge retrieval', 'Maintenance planner', 'Executive report']; const name = String(agent || '').toLowerCase(); if (!agent) return fallback[index] || 'Workflow stage'; if (name.includes('sensor') || name.includes('telemetry')) return 'Telemetry'; if (name.includes('knowledge')) return 'Knowledge retrieval'; if (name.includes('maintenance') || name.includes('planning')) return 'Maintenance planner'; if (name.includes('report')) return 'Executive report'; return label(agent); }

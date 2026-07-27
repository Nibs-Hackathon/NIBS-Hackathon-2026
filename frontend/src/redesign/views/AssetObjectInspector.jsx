import { useState } from 'react';
import { Box, Button, Chip, Paper, Stack, TextField, Typography } from '@mui/material';
import { ExpandMoreOutlined } from '@mui/icons-material';
import { ProvenanceBadge } from '../accountability';
import { StatusBadge, RiskBadge } from '../../design-system/catalog/status';
import { HealthRing, SignalCard, Sparkline } from '../../design-system/catalog/data';
import { Health, label, round } from './shared';

function AccordionSection({ id, title, open, onToggle, children, count }) {
  return (
    <Box className={`assets-accordion ${open ? 'is-open' : ''}`}>
      <button type="button" className="assets-accordion-head" onClick={() => onToggle(id)} aria-expanded={open}>
        <ExpandMoreOutlined className="assets-accordion-chevron" fontSize="small" />
        <Typography className="product-kicker">{title}</Typography>
        {count != null && <em>{count}</em>}
      </button>
      {open && <Box className="assets-accordion-body">{children}</Box>}
    </Box>
  );
}

/**
 * Part E — Object Inspector: Identity/Health/Signals open; sections 4–10 accordion; sticky CTA.
 */
export function AssetObjectInspector({
  asset,
  selected,
  risk,
  statusLabel,
  signalValues = [],
  provenance = 'live',
  primaryLabel,
  primaryAction,
  actionRef,
  clean,
  workOrders = [],
  note = '',
  onNoteChange,
  onOpenIncident,
  onOpenForecast,
  onCreateWorkOrder,
  onOpenInvestigation,
}) {
  const [openSections, setOpenSections] = useState(() => new Set());

  const toggle = (id) => {
    setOpenSections((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (!asset) {
    return (
      <Paper className="twin-inspector assets-pane assets-inspector">
        <Typography variant="body2" color="text.secondary" sx={{ p: 2 }}>
          Select a critical asset or click a unit.
        </Typography>
      </Paper>
    );
  }

  const health = round(asset.health ?? 0);
  const rull = Number(asset.remaining_life_days ?? asset.remaining_life ?? Math.max(8, Math.round(health * 0.9)));
  const failure = Math.min(94, Math.max(6, 100 - health));
  const assetWOs = workOrders.filter(
    (wo) => wo.assetId === asset.id || wo.asset_id === asset.id || wo.asset === asset.name,
  );
  const docs = Number(asset.documents_count) || 0;
  const aiText = selected?.incident?.reasoning
    || asset.ai_recommendation
    || (risk > 70
      ? 'Condition trend supports containment planning — verify linked evidence before authorizing work.'
      : 'No elevated agent recommendation for this object.');
  const confidence = selected?.incident?.confidence != null
    ? Math.round(Number(selected.incident.confidence) <= 1
      ? Number(selected.incident.confidence) * 100
      : Number(selected.incident.confidence))
    : risk > 70 ? 78 : 54;

  return (
    <Paper className="twin-inspector p8-inspector-swap assets-pane assets-inspector" key={asset.id}>
      <Box className="twin-inspector-head assets-inspector-sticky">
        <Stack direction="row" spacing={1} alignItems="center">
          <Typography className="product-kicker">OBJECT</Typography>
          <ProvenanceBadge value={provenance} />
        </Stack>
      </Box>

      <Box className="assets-inspector-scroll">
        <Box className="p8-inspector-section assets-inspector-identity">
          <Typography className="product-kicker">IDENTITY</Typography>
          <Typography className="twin-inspector-title">{asset.name}</Typography>
          <Typography variant="caption">
            Tag {clean(asset.tag || asset.id)} · {clean(asset.location || asset.zone, 'Facility')} · {clean(label(asset.type || 'Process asset'), 'Asset')}
          </Typography>
        </Box>

        <Box className="p8-inspector-section p8-inspector-state">
          <Typography className="product-kicker">CURRENT HEALTH</Typography>
          <StatusBadge label={statusLabel} status={statusLabel} live={risk > 40} />
          <RiskBadge value={risk} />
          <HealthRing value={asset.health} size={72} />
          <Box>
            <Typography>Health</Typography>
            <b>{health}%</b>
            <Health value={asset.health} />
            <Typography variant="caption" display="block" sx={{ mt: 0.5 }}>
              Last inspection {clean(asset.last_inspection, 'Pending')}
            </Typography>
          </Box>
        </Box>

        <Box className="p8-inspector-section">
          <Typography className="product-kicker">SIGNALS</Typography>
          <Sparkline values={signalValues.length ? signalValues : [Number(asset.health) || 0]} label="Condition trend" height={36} />
          <Box className="p8-inspector-signals" sx={{ mt: 1 }}>
            <SignalCard name="Temperature" value={clean(asset.temperature)} unit="°C" threshold={120} provenance={provenance} />
            <SignalCard name="Pressure" value={clean(asset.pressure)} unit="psi" threshold={200} provenance={provenance} />
            <SignalCard name="Vibration" value={clean(asset.vibration)} unit="mm/s" threshold={12} provenance={provenance} />
          </Box>
        </Box>

        <AccordionSection id="linked" title="LINKED INCIDENTS" open={openSections.has('linked')} onToggle={toggle} count={selected?.incident ? 1 : 0}>
          {selected?.incident ? (
            <Chip
              clickable
              color="warning"
              size="small"
              label={`${label(selected.incident.incident_type || selected.incident.id)}`}
              onClick={onOpenIncident}
            />
          ) : (
            <Typography variant="body2" color="text.secondary">No open cases for this asset.</Typography>
          )}
        </AccordionSection>

        <AccordionSection id="forecast" title="FORECAST" open={openSections.has('forecast')} onToggle={toggle}>
          <Typography variant="body2">Failure probability <b>{failure}%</b></Typography>
          <Typography variant="body2">Remaining useful life <b>{rull} days</b></Typography>
          <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onOpenForecast}>Open forecast terminal</Button>
        </AccordionSection>

        <AccordionSection id="maintenance" title="MAINTENANCE" open={openSections.has('maintenance')} onToggle={toggle} count={assetWOs.length}>
          {assetWOs.length
            ? assetWOs.map((wo, index) => (
              <Typography key={wo.id || index} variant="body2">
                {wo.title || wo.name || `WO ${index + 1}`} · {wo.status || 'Backlog'}
              </Typography>
            ))
            : <Typography variant="body2" color="text.secondary">No open work orders.</Typography>}
          <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onCreateWorkOrder}>Create work order</Button>
        </AccordionSection>

        <AccordionSection id="knowledge" title="KNOWLEDGE" open={openSections.has('knowledge')} onToggle={toggle}>
          <Typography variant="body2" color="text.secondary">
            Similar past events and procedures load when retrieval is available for this tag class.
          </Typography>
        </AccordionSection>

        <AccordionSection id="documents" title="DOCUMENTS" open={openSections.has('documents')} onToggle={toggle} count={docs}>
          <Typography variant="body2">
            {docs > 0 ? `${docs} controlled records linked.` : 'No controlled documents linked yet.'}
          </Typography>
        </AccordionSection>

        <AccordionSection id="notes" title="OPERATOR NOTES" open={openSections.has('notes')} onToggle={toggle}>
          <TextField
            multiline
            minRows={3}
            fullWidth
            size="small"
            placeholder="Shift notes for this asset (session persisted)"
            value={note}
            onChange={(event) => onNoteChange?.(event.target.value)}
          />
        </AccordionSection>

        <AccordionSection id="ai" title="AI RECOMMENDATIONS" open={openSections.has('ai')} onToggle={toggle}>
          <Typography variant="body2">{aiText}</Typography>
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.75 }}>
            Confidence {confidence}% · lineage via investigation trace
          </Typography>
          {selected?.incident && (
            <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onOpenInvestigation}>
              Open investigation
            </Button>
          )}
        </AccordionSection>
      </Box>

      <Box className="assets-inspector-cta">
        <Button
          ref={actionRef}
          size="small"
          variant="contained"
          fullWidth
          onClick={primaryAction}
          sx={{ textTransform: 'none', fontWeight: 700 }}
        >
          {primaryLabel}
        </Button>
      </Box>
    </Paper>
  );
}

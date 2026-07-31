import { useEffect, useState } from 'react';
import { Box, Button, Chip, Paper, Stack, TextField, Typography } from '@mui/material';
import { ExpandMoreOutlined } from '@mui/icons-material';
import { ProvenanceBadge } from '../accountability';
import { StatusBadge, RiskBadge } from '../../design-system/catalog/status';
import { HealthRing, SignalCard, Sparkline } from '../../design-system/catalog/data';
import { getKnowledgeDocuments, searchKnowledge } from '../../api/client';
import { formatTime, label, round } from './shared';

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
  knowledgeQuery = '',
  onOpenIncident,
  onOpenForecast,
  onCreateWorkOrder,
  onOpenInvestigation,
}) {
  const [openSections, setOpenSections] = useState(() => new Set());
  const [knowledge, setKnowledge] = useState([]);
  const [knowledgeStatus, setKnowledgeStatus] = useState('idle');
  const [referenceDocuments, setReferenceDocuments] = useState([]);
  const [documentsStatus, setDocumentsStatus] = useState('idle');

  const toggle = (id) => {
    const willOpen = !openSections.has(id);
    if (willOpen && id === 'knowledge' && knowledgeQuery) setKnowledgeStatus('loading');
    if (willOpen && id === 'documents' && documentsStatus === 'idle') setDocumentsStatus('loading');
    setOpenSections((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  useEffect(() => {
    if (!openSections.has('knowledge') || !knowledgeQuery) return undefined;
    let cancelled = false;
    searchKnowledge(knowledgeQuery)
      .then((response) => {
        if (cancelled) return;
        setKnowledge(Array.isArray(response.data?.results) ? response.data.results : []);
        setKnowledgeStatus('ready');
      })
      .catch(() => {
        if (cancelled) return;
        setKnowledge([]);
        setKnowledgeStatus('unavailable');
      });
    return () => { cancelled = true; };
  }, [openSections, knowledgeQuery, asset?.id]);

  useEffect(() => {
    if (!openSections.has('documents') || documentsStatus !== 'loading') return undefined;
    let cancelled = false;
    getKnowledgeDocuments()
      .then((response) => {
        if (cancelled) return;
        setReferenceDocuments(Array.isArray(response.data?.documents) ? response.data.documents : []);
        setDocumentsStatus('ready');
      })
      .catch(() => {
        if (cancelled) return;
        setDocumentsStatus('unavailable');
      });
    return () => { cancelled = true; };
  }, [openSections, documentsStatus]);

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
  const hasForecast = asset.remaining_life_days != null
    || asset.remaining_life != null
    || asset.failure_probability != null
    || asset.risk_score != null
    || asset.forecast_available;
  const rull = asset.remaining_life_days ?? asset.remaining_life ?? null;
  const failure = asset.failure_probability ?? asset.risk_score ?? null;
  const assetWOs = workOrders.filter(
    (wo) => wo.assetId === asset.id || wo.asset_id === asset.id || wo.asset === asset.name || wo.Asset === asset.name,
  );
  const controlledDocs = Number(asset.documents_count) || 0;
  const aiText = selected?.incident?.reasoning
    || asset.ai_recommendation
    || asset.recommendation
    || (risk > 70
      ? 'Condition trend supports containment planning — verify linked evidence before authorizing work.'
      : 'No elevated agent recommendation for this object.');
  const confidence = selected?.incident?.confidence != null
    ? Math.round(Number(selected.incident.confidence) <= 1
      ? Number(selected.incident.confidence) * 100
      : Number(selected.incident.confidence))
    : null;

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
          <Box className="assets-identity-meta">
            <Typography variant="caption"><span>Tag</span>{clean(asset.tag || asset.id)}</Typography>
            <Typography variant="caption"><span>Location</span>{clean(asset.location || asset.zone, 'Facility')}</Typography>
            <Typography variant="caption"><span>Class</span>{clean(label(asset.type || 'Process asset'), 'Asset')}</Typography>
          </Box>
        </Box>

        <Box className="p8-inspector-section p8-inspector-state">
          <Box className="assets-health-heading">
            <Typography className="product-kicker">CURRENT CONDITION</Typography>
            <Box className="assets-health-badges">
              <StatusBadge label={statusLabel} status={statusLabel} live={risk > 40} />
              <Typography component="span" className="assets-risk-label">Risk</Typography>
              <RiskBadge value={risk} />
            </Box>
          </Box>
          <Box className="assets-health-summary">
            <HealthRing value={asset.health} size={84} />
            <Box>
              <Typography className="assets-health-label">Asset health</Typography>
              <Typography className="assets-health-value">{health}<span>/100</span></Typography>
              <Typography variant="caption" className="assets-last-reading">
                Updated {asset.last_reading_at || asset.last_inspection
                  ? formatTime(asset.last_reading_at || asset.last_inspection)
                  : 'pending live reading'}
              </Typography>
            </Box>
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
          {hasForecast ? (
            <>
              <Typography variant="body2">
                Failure probability <b>{failure != null ? `${round(failure)}%` : '—'}</b>
              </Typography>
              <Typography variant="body2">
                Remaining useful life <b>{rull != null ? `${round(rull)} days` : '—'}</b>
              </Typography>
            </>
          ) : (
            <Typography variant="body2" color="text.secondary">
              No forecast published for this asset. Open the forecast terminal when predictions are available.
            </Typography>
          )}
          <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onOpenForecast}>Open forecast terminal</Button>
        </AccordionSection>

        <AccordionSection id="maintenance" title="MAINTENANCE" open={openSections.has('maintenance')} onToggle={toggle} count={assetWOs.length}>
          {assetWOs.length
            ? assetWOs.map((wo, index) => (
              <Typography key={wo.id || index} variant="body2">
                {wo.title || wo['Work order'] || wo.name || `WO ${index + 1}`} · {wo.status || wo.State || 'Backlog'}
              </Typography>
            ))
            : <Typography variant="body2" color="text.secondary">No open work orders.</Typography>}
          <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onCreateWorkOrder}>Create work order</Button>
        </AccordionSection>

        <AccordionSection id="knowledge" title="KNOWLEDGE" open={openSections.has('knowledge')} onToggle={toggle} count={knowledge.length || undefined}>
          {knowledgeStatus === 'loading' && (
            <Typography variant="body2" color="text.secondary">Searching knowledge base…</Typography>
          )}
          {knowledgeStatus === 'unavailable' && (
            <Typography variant="body2" color="text.secondary">Knowledge search is unavailable right now.</Typography>
          )}
          {knowledgeStatus === 'ready' && !knowledge.length && (
            <Typography variant="body2" color="text.secondary">No retrieved documents for this asset class yet.</Typography>
          )}
          {knowledge.map((doc, index) => (
            <Typography key={`${doc.filename || doc.source}-${index}`} variant="body2" sx={{ mb: 1 }}>
              <b>{doc.filename || doc.source || `Document ${index + 1}`}</b>
              <br />
              {(doc.content || '').slice(0, 180)}{(doc.content || '').length > 180 ? '…' : ''}
            </Typography>
          ))}
        </AccordionSection>

        <AccordionSection
          id="documents"
          title="DOCUMENTS"
          open={openSections.has('documents')}
          onToggle={toggle}
          count={controlledDocs + referenceDocuments.length || undefined}
        >
          {controlledDocs > 0 && (
            <Typography variant="body2" sx={{ mb: 1 }}>
              {controlledDocs} controlled {controlledDocs === 1 ? 'record' : 'records'} linked to this asset.
            </Typography>
          )}
          {documentsStatus === 'loading' && (
            <Typography variant="body2" color="text.secondary">Loading refinery reference corpus...</Typography>
          )}
          {documentsStatus === 'unavailable' && (
            <Typography variant="body2" color="text.secondary">
              Reference catalog is available when the backend reconnects.
            </Typography>
          )}
          {documentsStatus === 'ready' && (
            <>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                {referenceDocuments.length} local refinery references are searchable for every asset.
                Site-controlled manuals and procedures remain authoritative.
              </Typography>
              <Stack spacing={0.75}>
                {referenceDocuments.slice(0, 6).map((document) => (
                  <Box
                    key={document.id}
                    sx={{
                      px: 1,
                      py: 0.75,
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                    }}
                  >
                    <Typography variant="caption" fontWeight={750}>{document.title}</Typography>
                    <Typography variant="caption" color="text.secondary" display="block">
                      {document.section_count} sections
                    </Typography>
                  </Box>
                ))}
              </Stack>
              {referenceDocuments.length > 6 && (
                <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
                  +{referenceDocuments.length - 6} additional references available through Knowledge search
                </Typography>
              )}
            </>
          )}
        </AccordionSection>

        <AccordionSection id="notes" title="OPERATOR NOTES" open={openSections.has('notes')} onToggle={toggle}>
          <TextField
            multiline
            minRows={3}
            fullWidth
            size="small"
            placeholder="Shift notes for this asset (persisted)"
            value={note}
            onChange={(event) => onNoteChange?.(event.target.value)}
          />
        </AccordionSection>

        <AccordionSection id="ai" title="AI RECOMMENDATIONS" open={openSections.has('ai')} onToggle={toggle}>
          <Typography variant="body2">{aiText}</Typography>
          {confidence != null && (
            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.75 }}>
              Confidence {confidence}% · lineage via investigation trace
            </Typography>
          )}
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

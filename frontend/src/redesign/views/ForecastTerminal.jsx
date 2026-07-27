import { useEffect, useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { ProvenanceBadge } from '../accountability';
import { createWorkOrder, getPredictions } from '../../api/client';
import { normalizePredictionResponse } from '../../api/resourceAdapters';
import { MiniGraph, Empty, Metric, round } from './shared';

function formatMetric(value, suffix = '') {
  if (value == null || Number.isNaN(Number(value))) return '—';
  return `${round(Number(value))}${suffix}`;
}

/** Part 8 — Forecast in-place select + draft WO navigate. Phase 3: stress scenarios. */
export function ForecastTerminal({ assets, telemetry, telemetryStreams, provenance = 'estimated' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const scenarioRef = useRef(null);
  const safeAssets = Array.isArray(assets) ? assets.filter(Boolean) : [];
  const [selectedId, setSelectedId] = useState(objectApi.selection.assetId);
  const [prediction, setPrediction] = useState(null);
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [stress, setStress] = useState(0);
  const [creatingWo, setCreatingWo] = useState(false);

  const chooseAsset = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ assetId: id });
  };

  const baseFocus = safeAssets.find((asset) => asset.id === (selectedId || objectApi.selection.assetId)) || safeAssets[0];
  const focus = prediction && baseFocus && prediction.id === baseFocus.id
    ? { ...baseFocus, ...prediction }
    : baseFocus;
  const stream = (Array.isArray(telemetryStreams) ? telemetryStreams : []).find((item) => item?.asset_id === focus?.id) || telemetry;
  const raw = Array.isArray(stream?.readings)
    ? stream.readings.map((item) => Number(item.value)).filter(Number.isFinite)
    : [];
  const health = focus?.health != null ? round(focus.health) : null;

  const hasForecastPayload = focus && (
    focus.remaining_life_days != null
    || focus.remaining_life != null
    || focus.failure_probability != null
    || focus.risk_score != null
    || focus.forecast_available
    || (Array.isArray(focus.projected_health) && focus.projected_health.length > 0)
  );

  const rull = focus?.remaining_life_days ?? focus?.remaining_life ?? null;
  const failure = focus?.failure_probability ?? focus?.risk_score ?? null;
  const projected = Array.isArray(focus?.projected_health) && focus.projected_health.length > 1
    ? focus.projected_health.map(Number).filter(Number.isFinite)
    : raw.length > 3
      ? raw
      : [];
  const scenario = focus?.scenario;

  useEffect(() => {
    if (!baseFocus?.id) {
      setPrediction(null);
      return undefined;
    }
    let cancelled = false;
    setPredictionLoading(true);
    getPredictions(baseFocus.id, 14, stress)
      .then((response) => {
        if (!cancelled) {
          setPrediction(normalizePredictionResponse(response.data, baseFocus));
        }
      })
      .catch(() => {
        if (!cancelled) setPrediction(null);
      })
      .finally(() => {
        if (!cancelled) setPredictionLoading(false);
      });
    return () => { cancelled = true; };
  }, [baseFocus?.id, stress]);

  useEffect(() => {
    if (!focus?.id) return undefined;
    const timer = requestAnimationFrame(() => scenarioRef.current?.focus?.({ preventScroll: true }));
    return () => cancelAnimationFrame(timer);
  }, [focus?.id]);

  const createWorkOrderAction = async () => {
    if (!focus) return;
    setCreatingWo(true);
    try {
      const response = await createWorkOrder({
        asset_id: focus.id,
        title: `Intervene on ${focus.name || focus.id}`,
        priority: 'P1',
        owner: 'Control operator',
        downtime: scenario?.estimated_downtime_hours != null
          ? `${scenario.estimated_downtime_hours}h`
          : undefined,
        estimated_cost: scenario?.estimated_intervention_cost_usd ?? undefined,
        note: stress > 0
          ? `Created from forecast terminal with stress=${stress.toFixed(2)}.`
          : 'Created from forecast terminal.',
      });
      const created = response.data || {};
      navigateTo(objectApi, navigate, 'maintenance', {
        assetId: focus.id,
        workOrderId: created.id,
        draftWorkOrder: {
          id: created.id,
          title: created.title || `Intervene on ${focus.name || focus.id}`,
          asset: focus.name,
          assetName: focus.name,
          assetId: focus.id,
          status: 'Ready',
          priority: 'P1',
          cost: created.estimated_cost,
          downtime: created.downtime,
        },
      });
      toast.success('Work order submitted for approval');
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Work order could not be created');
    } finally {
      setCreatingWo(false);
    }
  };

  const watchlist = safeAssets.slice().sort((a, b) => Number(a.health ?? 100) - Number(b.health ?? 100));

  return (
    <Box className="forecast-terminal">
      <Box className="forecast-terminal-head">
        <Box>
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography className="product-kicker">FORECASTING TERMINAL</Typography>
            <ProvenanceBadge value={provenance} />
          </Stack>
          <Typography className="forecast-terminal-title">Asset risk curve · forward operating model</Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Button size="small" variant="outlined" disabled={!focus || creatingWo} onClick={createWorkOrderAction}>
            Create work order
          </Button>
        </Stack>
      </Box>

      <Box className="forecast-terminal-grid">
        <Paper className="terminal-watchlist">
          <Typography className="product-kicker">ASSET WATCHLIST</Typography>
          <Typography className="terminal-watchlist-sub">Sort: highest forward risk</Typography>
          <Box
            tabIndex={0}
            onKeyDown={(event) => {
              if (!watchlist.length) return;
              const ids = watchlist.map((asset) => asset.id);
              const idx = Math.max(0, ids.indexOf(focus?.id));
              if (event.key === 'ArrowDown') {
                event.preventDefault();
                chooseAsset(ids[Math.min(ids.length - 1, idx + 1)]);
              }
              if (event.key === 'ArrowUp') {
                event.preventDefault();
                chooseAsset(ids[Math.max(0, idx - 1)]);
              }
            }}
          >
            {watchlist.length
              ? watchlist.map((asset, index) => (
                <button
                  type="button"
                  key={asset.id || index}
                  onClick={() => chooseAsset(asset.id)}
                  className={focus?.id === asset.id ? 'selected' : ''}
                >
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <Box>
                    <b>{asset.name || `Asset ${index + 1}`}</b>
                    <small>{asset.location || asset.zone || 'Process train'} · {round(asset.health)}% health</small>
                  </Box>
                  <em>
                    {asset.risk_score != null
                      ? `${round(asset.risk_score)}%`
                      : asset.failure_probability != null
                        ? `${round(asset.failure_probability)}%`
                        : '—'}
                  </em>
                </button>
              ))
              : <Empty text="health forecasts" />}
          </Box>
        </Paper>

        <Paper className="terminal-chart p8-inspector-swap" key={focus?.id || 'chart'}>
          <Box className="terminal-chart-head">
            <Box>
              <Typography className="product-kicker">HEALTH FORECAST · {focus?.name || 'Awaiting asset'}</Typography>
              <Typography>Observed + predicted trajectory with uncertainty</Typography>
              {predictionLoading && (
                <Typography variant="caption" color="text.secondary">Loading prediction model…</Typography>
              )}
            </Box>
            {projected.length > 1 && (
              <Box className="terminal-chart-legend">
                <span><i className="observed" />Observed</span>
                <span><i className="model" />Forecast</span>
                <span><i className="band" />80% confidence band</span>
              </Box>
            )}
          </Box>
          {projected.length > 1 ? (
            <>
              <Box className="terminal-graph">
                <svg viewBox="0 0 760 285" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="uncertainty" x1="0" x2="0" y1="0" y2="1">
                      <stop stopColor="#5f9eff" stopOpacity=".25" />
                      <stop offset="1" stopColor="#5f9eff" stopOpacity=".02" />
                    </linearGradient>
                  </defs>
                  {[55, 115, 175, 235].map((y) => <line key={y} x1="0" x2="760" y1={y} y2={y} />)}
                  <rect x="0" y="195" width="760" height="40" className="terminal-watch-zone" />
                  <rect x="0" y="235" width="760" height="50" className="terminal-critical-zone" />
                  <polyline
                    points={projected.map((value, index) => `${index * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9}`).join(' ')}
                    className="terminal-line"
                  />
                </svg>
                <Box className="terminal-axis"><span>Now</span><span>7d</span><span>14d</span><span>21d</span><span>30d</span></Box>
              </Box>
              <Box className="terminal-stats">
                <Metric label="Failure probability" value={formatMetric(failure, '%')} />
                <Metric label="Remaining useful life" value={rull != null ? `${round(rull)} days` : '—'} />
                <Metric label="Current health" value={health != null ? `${health}%` : '—'} />
                <Metric label="Model confidence" value={focus?.prediction_confidence != null ? `${round(focus.prediction_confidence)}%` : '—'} />
              </Box>
            </>
          ) : (
            <Box sx={{ p: 3 }}>
              <Empty text="health forecasts" />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {focus
                  ? 'No forecast series is available for this asset yet. Predictions appear when the backend publishes projected health or enough telemetry history exists.'
                  : 'Select an asset from the watchlist to view forecasts.'}
              </Typography>
            </Box>
          )}
        </Paper>

        <Paper className="terminal-scenario">
          <Typography className="product-kicker">WHAT IF SIMULATION</Typography>
          <Typography className="terminal-scenario-title">Operating stress</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Stress scales degradation in the prediction API (0 = baseline, 1 = high load).
          </Typography>
          <Box sx={{ mt: 2 }}>
            <input
              ref={scenarioRef}
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={stress}
              disabled={!focus}
              onChange={(event) => setStress(Number(event.target.value))}
              style={{ width: '100%' }}
              aria-label="Operating stress"
            />
            <Typography variant="caption" color="text.secondary">
              Stress {stress.toFixed(2)} · multiplier {focus?.stress_multiplier != null ? `${focus.stress_multiplier}×` : '—'}
            </Typography>
          </Box>
          {scenario ? (
            <Box className="terminal-stats" sx={{ mt: 2 }}>
              <Metric label="Intervention cost" value={`$${Number(scenario.estimated_intervention_cost_usd || 0).toLocaleString()}`} />
              <Metric label="Downtime" value={`${scenario.estimated_downtime_hours ?? '—'}h`} />
              <Metric label="Prod. impact" value={`${scenario.estimated_production_impact_pct ?? '—'}%`} />
            </Box>
          ) : (
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              Scenario estimates appear once a forecast is available.
            </Typography>
          )}
          <Box className="terminal-recommendation" sx={{ mt: 2 }}>
            <Typography className="product-kicker">MODEL RECOMMENDATION</Typography>
            <Typography variant="body2" color="text.secondary">
              {hasForecastPayload
                ? 'Review the published forecast and open maintenance planning when intervention is warranted.'
                : 'Awaiting a verified forecast before recommending intervention timing.'}
            </Typography>
            <Button size="small" sx={{ mt: 1 }} variant="contained" disabled={!focus || creatingWo} onClick={createWorkOrderAction}>
              Create work order
            </Button>
          </Box>
        </Paper>
      </Box>

      <Paper className="terminal-bottom">
        <Box>
          <Typography className="product-kicker">HISTORICAL COMPARISON</Typography>
          {projected.length > 1 ? (
            <>
              <Typography>
                Showing {projected.length} points from {focus?.forecast_method ? 'published forecast' : 'telemetry history'}.
              </Typography>
              <MiniGraph values={projected} label="Forecast / telemetry series" />
            </>
          ) : (
            <Typography variant="body2" color="text.secondary">
              Historical comparison requires a forecast or telemetry series from the backend.
            </Typography>
          )}
        </Box>
        <Box>
          <Typography className="product-kicker">RISK & IMPACT SENSITIVITY</Typography>
          {scenario ? (
            <Typography variant="body2">
              Method: {scenario.method || focus?.forecast_method || 'stress-scaled forecast'}.
              Higher stress increases failure probability and estimated intervention cost.
            </Typography>
          ) : (
            <Typography variant="body2" color="text.secondary">
              Sensitivity drivers will appear when the prediction service publishes scenario data.
            </Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
}

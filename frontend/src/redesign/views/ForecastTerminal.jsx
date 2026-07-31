import { useEffect, useMemo, useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import {
  AccessTimeOutlined,
  AutoAwesomeOutlined,
  BuildOutlined,
  FavoriteBorderOutlined,
  TrendingDownOutlined,
  TuneOutlined,
  VerifiedOutlined,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { ProvenanceBadge } from '../accountability';
import { createWorkOrder, getPredictions } from '../../api/client';
import { normalizePredictionResponse } from '../../api/resourceAdapters';
import {
  ChartTooltip,
  Grid,
  Line,
  LineChart,
  LineChartLoading,
  LineSeriesTerminalMarker,
  projectedHealthToChartRows,
  XAxis,
} from '@/components/charts';
import { Empty, round } from './shared';

function formatMetric(value, suffix = '') {
  if (value == null || Number.isNaN(Number(value))) return '—';
  return `${round(Number(value))}${suffix}`;
}

function ForecastMetric({ icon: Icon, label, value, detail, tone = 'blue' }) {
  return (
    <Box className={`forecast-os-metric tone-${tone}`}>
      <Box className="forecast-os-metric-icon"><Icon /></Box>
      <Box>
        <Typography>{label}</Typography>
        <b>{value}</b>
        <small>{detail}</small>
      </Box>
    </Box>
  );
}

export function ForecastTerminal({ assets, provenance = 'estimated' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const safeAssets = useMemo(
    () => (Array.isArray(assets) ? assets.filter(Boolean) : []),
    [assets],
  );
  const [selectedId, setSelectedId] = useState(objectApi.selection.assetId);
  const [prediction, setPrediction] = useState(null);
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [stress, setStress] = useState(0);
  const [creatingWo, setCreatingWo] = useState(false);

  const chooseAsset = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ assetId: id });
  };

  const baseFocus = safeAssets.find(
    (asset) => asset.id === (selectedId || objectApi.selection.assetId),
  ) || safeAssets[0];
  const baseFocusRef = useRef(baseFocus);
  const baseFocusId = baseFocus?.id;
  const focus = prediction && baseFocus && prediction.id === baseFocus.id
    ? { ...baseFocus, ...prediction }
    : baseFocus;
  const health = focus?.health != null ? round(focus.health) : null;
  const rull = focus?.remaining_life_days ?? focus?.remaining_life ?? null;
  const failure = focus?.failure_probability ?? null;
  const projected = Array.isArray(focus?.projected_health) && focus.projected_health.length > 1
    ? focus.projected_health.map(Number).filter(Number.isFinite)
    : [];
  const { chartData, projectionStartIndex } = useMemo(
    () => projectedHealthToChartRows(focus?.historical_health, focus?.predicted_health),
    [focus?.historical_health, focus?.predicted_health],
  );
  const scenario = focus?.scenario;
  const hasForecastPayload = Boolean(
    focus
    && (
      focus.forecast_available
      || projected.length > 1
      || rull != null
      || (failure != null && focus.forecast_method)
    ),
  );

  useEffect(() => {
    baseFocusRef.current = baseFocus;
  }, [baseFocus]);

  useEffect(() => {
    if (!baseFocusId) return undefined;
    let cancelled = false;
    const timer = window.setTimeout(() => {
      if (!cancelled) setPredictionLoading(true);
      getPredictions(baseFocusId, 14, stress)
        .then((response) => {
          const requestedFocus = baseFocusRef.current;
          if (!cancelled && requestedFocus?.id === baseFocusId) {
            setPrediction(normalizePredictionResponse(response.data, requestedFocus));
          }
        })
        .catch(() => {
          if (!cancelled) setPrediction(null);
        })
        .finally(() => {
          if (!cancelled) setPredictionLoading(false);
        });
    }, 140);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [baseFocusId, stress]);

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

  const watchlist = useMemo(
    () => safeAssets.slice().sort(
      (a, b) => Number(a.health ?? 100) - Number(b.health ?? 100),
    ),
    [safeAssets],
  );

  return (
    <Box className="forecast-os">
      <Box className="forecast-os-head">
        <Box>
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography className="product-kicker">FORECASTING</Typography>
            <ProvenanceBadge value={provenance} />
          </Stack>
          <Typography className="forecast-os-title">Forward reliability model</Typography>
          <Typography className="forecast-os-subtitle">
            Compare asset degradation, test operating stress, and stage intervention work.
          </Typography>
        </Box>
        <Button
          size="small"
          variant="contained"
          startIcon={<BuildOutlined />}
          disabled={!focus || creatingWo}
          onClick={createWorkOrderAction}
        >
          Create work order
        </Button>
      </Box>

      <Box className="forecast-os-layout">
        <Paper className="forecast-os-watchlist">
          <Box className="forecast-os-watchlist-head">
            <Box>
              <Typography className="product-kicker">ASSET RISK QUEUE</Typography>
              <Typography>Lowest health first</Typography>
            </Box>
            <b>{watchlist.length}</b>
          </Box>
          <Box
            className="forecast-os-watchlist-body"
            tabIndex={0}
            onKeyDown={(event) => {
              if (!watchlist.length) return;
              const ids = watchlist.map((asset) => asset.id);
              const index = Math.max(0, ids.indexOf(focus?.id));
              if (event.key === 'ArrowDown') {
                event.preventDefault();
                chooseAsset(ids[Math.min(ids.length - 1, index + 1)]);
              }
              if (event.key === 'ArrowUp') {
                event.preventDefault();
                chooseAsset(ids[Math.max(0, index - 1)]);
              }
            }}
          >
            {watchlist.length ? watchlist.map((asset, index) => {
              const assetHealth = round(asset.health);
              const risk = asset.risk_score != null
                ? round(asset.risk_score)
                : asset.failure_probability != null
                  ? round(asset.failure_probability)
                  : Math.max(0, 100 - assetHealth);
              return (
                <button
                  type="button"
                  key={asset.id || index}
                  onClick={() => chooseAsset(asset.id)}
                  className={`forecast-os-asset ${focus?.id === asset.id ? 'selected' : ''}`}
                >
                  <span className="forecast-os-rank">{String(index + 1).padStart(2, '0')}</span>
                  <span className="forecast-os-asset-copy">
                    <b>{asset.name || `Asset ${index + 1}`}</b>
                    <small>{asset.location || asset.zone || 'Process train'}</small>
                    <i><span style={{ width: `${Math.max(2, Math.min(100, risk))}%` }} /></i>
                  </span>
                  <span className="forecast-os-risk">
                    <b>{risk}%</b>
                    <small>risk</small>
                  </span>
                </button>
              );
            }) : <Empty text="health forecasts" />}
          </Box>
        </Paper>

        <Box className="forecast-os-main">
          <Paper className="forecast-os-model" key={focus?.id || 'forecast-model'}>
            <Box className="forecast-os-model-head">
              <Box>
                <Typography className="product-kicker">HEALTH FORECAST</Typography>
                <Typography className="forecast-os-model-title">
                  {focus?.name || 'Select an asset'}
                </Typography>
                <Typography>
                  {focus?.location || focus?.zone || 'Observed and projected operating condition'}
                </Typography>
              </Box>
              <Box className="forecast-os-legend">
                <span><i className="observed" />Observed</span>
                <span><i />Projected</span>
              </Box>
            </Box>

            <Box className="forecast-os-metrics">
              <ForecastMetric icon={TrendingDownOutlined} label="Failure probability" value={formatMetric(failure, '%')} detail="Model horizon" tone="amber" />
              <ForecastMetric icon={AccessTimeOutlined} label="Useful life" value={rull != null ? `${round(rull)} days` : '—'} detail="Remaining estimate" tone="violet" />
              <ForecastMetric icon={FavoriteBorderOutlined} label="Current health" value={health != null ? `${health}%` : '—'} detail="Latest condition" tone="green" />
              <ForecastMetric icon={VerifiedOutlined} label="Confidence" value={focus?.prediction_confidence != null ? `${round(focus.prediction_confidence)}%` : '—'} detail={focus?.forecast_method || 'Model pending'} />
            </Box>

            <Box className="forecast-os-chart">
              {predictionLoading && !chartData.length ? (
                <LineChartLoading loadingStyle="sweep" />
              ) : chartData.length > 1 ? (
                <LineChart
                  data={chartData}
                  aspectRatio={null}
                  margin={{ top: 18, right: 24, bottom: 34, left: 24 }}
                  style={{ height: '100%' }}
                >
                  <Grid horizontal numTicksRows={5} strokeOpacity={0.26} hideHorizontalEdgeLines />
                  <Line
                    dataKey="value"
                    strokeWidth={2.2}
                    stroke="var(--chart-line-primary, #55d6ff)"
                    dashFromIndex={projectionStartIndex}
                    animate
                  />
                  <LineSeriesTerminalMarker dataKey="value" />
                  <XAxis />
                  <ChartTooltip />
                </LineChart>
              ) : (
                <Box className="forecast-os-chart-empty">
                  <Empty text="health forecasts" />
                  <Typography>
                    {focus
                      ? 'A verified projected-health series has not been published for this asset.'
                      : 'Select an asset from the risk queue.'}
                  </Typography>
                </Box>
              )}
              {predictionLoading && chartData.length ? (
                <Box className="forecast-os-chart-updating">Recalculating stress scenario…</Box>
              ) : null}
            </Box>
          </Paper>

          <Paper className="forecast-os-scenario">
            <Box className="forecast-os-stress">
              <Box className="forecast-os-scenario-title">
                <TuneOutlined />
                <Box>
                  <Typography className="product-kicker">WHAT-IF MODEL</Typography>
                  <Typography>Operating stress</Typography>
                </Box>
                <b>{Math.round(stress * 100)}%</b>
              </Box>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={stress}
                disabled={!focus}
                onChange={(event) => setStress(Number(event.target.value))}
                aria-label="Operating stress"
              />
              <Box className="forecast-os-stress-scale">
                <span>Baseline</span>
                <span>High load</span>
              </Box>
            </Box>

            <Box className="forecast-os-outcomes">
              <Box><span>Intervention cost</span><b>{scenario ? `$${Number(scenario.estimated_intervention_cost_usd || 0).toLocaleString()}` : '—'}</b></Box>
              <Box><span>Downtime</span><b>{scenario ? `${scenario.estimated_downtime_hours ?? '—'}h` : '—'}</b></Box>
              <Box><span>Production impact</span><b>{scenario ? `${scenario.estimated_production_impact_pct ?? '—'}%` : '—'}</b></Box>
            </Box>

            <Box className="forecast-os-recommendation">
              <AutoAwesomeOutlined />
              <Box>
                <Typography className="product-kicker">MODEL RECOMMENDATION</Typography>
                <Typography>
                  {hasForecastPayload
                    ? 'Review the forecast horizon and stage maintenance before the modeled risk window.'
                    : 'Awaiting a verified forecast before recommending intervention timing.'}
                </Typography>
              </Box>
              <Button size="small" disabled={!focus || creatingWo} onClick={createWorkOrderAction}>
                Stage work
              </Button>
            </Box>
          </Paper>

          <Paper className="forecast-os-context">
            <Box>
              <Typography className="product-kicker">MODEL EVIDENCE</Typography>
              <Typography>
                {chartData.length > 1
                  ? `${focus?.predicted_health?.length || projected.length} projected points${focus?.forecast_method ? ` · ${focus.forecast_method}` : ''}. The dashed tail is the stress-adjusted model horizon.`
                  : 'Historical comparison begins when the backend publishes a projected-health series.'}
              </Typography>
            </Box>
            <Box>
              <Typography className="product-kicker">SENSITIVITY</Typography>
              <Typography>
                {scenario
                  ? `Stress multiplier ${focus?.stress_multiplier ?? '—'}×. Higher stress steepens projected health decline and increases modeled exposure.`
                  : 'Scenario impacts appear after the prediction service publishes a stress response.'}
              </Typography>
            </Box>
          </Paper>
        </Box>
      </Box>
    </Box>
  );
}

import { useEffect, useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { FilterListOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { ProvenanceBadge } from '../accountability';
import { MiniGraph, Empty, Metric, round } from './shared';

/** Part 8 — Forecast in-place select + draft WO navigate + scenario focus. */
export function ForecastTerminal({ assets, telemetry, telemetryStreams, provenance = 'estimated' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const scenarioRef = useRef(null);
  const safeAssets = Array.isArray(assets) ? assets.filter(Boolean) : [];
  const [selectedId, setSelectedId] = useState(objectApi.selection.assetId);
  const [scenario, setScenario] = useState(0);

  const chooseAsset = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ assetId: id });
  };

  const focus = safeAssets.find((asset) => asset.id === (selectedId || objectApi.selection.assetId)) || safeAssets[0];
  const stream = (Array.isArray(telemetryStreams) ? telemetryStreams : []).find((item) => item?.asset_id === focus?.id) || telemetry;
  const raw = Array.isArray(stream?.readings) ? stream.readings.map((item) => Number(item.value)).filter(Number.isFinite) : [];
  const health = round(focus?.health ?? raw.at?.(-1) ?? 78);
  const rull = Number(focus?.remaining_life_days ?? focus?.remaining_life ?? Math.max(8, Math.round(health * 0.9)));
  const failure = Math.min(94, Math.max(6, 100 - health + scenario * 5));
  const projected = raw.length > 3
    ? raw
    : Array.from({ length: 18 }, (_, index) => Math.max(16, health - index * (1.2 + scenario * 0.24) + Math.sin(index) * 2));

  useEffect(() => {
    if (!focus?.id) return undefined;
    const timer = requestAnimationFrame(() => scenarioRef.current?.focus?.({ preventScroll: true }));
    return () => cancelAnimationFrame(timer);
  }, [focus?.id]);

  const createWorkOrder = () => {
    if (!focus) return;
    navigateTo(objectApi, navigate, 'maintenance', {
      assetId: focus.id,
      draftWorkOrder: {
        id: `draft-${focus.id}`,
        title: `Intervene on ${focus.name || focus.id}`,
        asset: focus.name,
        assetName: focus.name,
        assetId: focus.id,
        cost: 24500,
        downtime: '12h',
        status: 'Backlog',
        priority: 'P1',
      },
    });
  };

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
          <Button size="small" startIcon={<FilterListOutlined />}>Asset universe</Button>
          <Button size="small" variant="outlined" disabled={!focus} onClick={createWorkOrder}>Create work order</Button>
          <Button size="small" variant="contained">Export scenario</Button>
        </Stack>
      </Box>

      <Box className="forecast-terminal-grid">
        <Paper className="terminal-watchlist">
          <Typography className="product-kicker">ASSET WATCHLIST</Typography>
          <Typography className="terminal-watchlist-sub">Sort: highest forward risk</Typography>
          <Box
            tabIndex={0}
            onKeyDown={(event) => {
              const list = safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health));
              if (!list.length) return;
              const ids = list.map((asset) => asset.id);
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
            {safeAssets.length
              ? safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health)).map((asset, index) => (
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
                  <em>{Math.max(8, 100 - round(asset.health))}%</em>
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
            </Box>
            <Box className="terminal-chart-legend">
              <span><i className="observed" />Observed</span>
              <span><i className="model" />Forecast</span>
              <span><i className="band" />80% confidence band</span>
            </Box>
          </Box>
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
              <polygon
                points={`${projected.map((value, index) => `${index * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9 - (8 + index * 0.7)}`).join(' ')} ${projected.slice().reverse().map((value, index) => `${(projected.length - 1 - index) * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9 + (8 + (projected.length - 1 - index) * 0.7)}`).join(' ')}`}
                fill="url(#uncertainty)"
              />
              <polyline
                points={projected.map((value, index) => `${index * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9}`).join(' ')}
                className="terminal-line"
              />
              <line x1="420" x2="420" y1="20" y2="272" className="terminal-marker" />
              <text x="426" y="32">Maintenance window</text>
            </svg>
            <Box className="terminal-axis"><span>Now</span><span>7d</span><span>14d</span><span>21d</span><span>30d</span></Box>
            <Box className="terminal-brush"><span style={{ left: '15%', width: '55%' }} /></Box>
          </Box>
          <Box className="terminal-stats">
            <Metric label="Failure probability" value={`${failure}%`} />
            <Metric label="Remaining useful life" value={`${rull} days`} />
            <Metric label="Maintenance window" value={`Day ${Math.max(4, Math.round(rull * 0.55))}–${Math.max(7, Math.round(rull * 0.72))}`} />
            <Metric label="Model confidence" value={`${Math.max(61, 93 - scenario * 4)}%`} />
          </Box>
        </Paper>

        <Paper className="terminal-scenario">
          <Typography className="product-kicker">WHAT IF SIMULATION</Typography>
          <Typography className="terminal-scenario-title">Operating sensitivity</Typography>
          <Typography>Stress the model to compare risk, downtime, and production impact.</Typography>
          <Box className="scenario-control">
            <Typography>Load increase</Typography>
            <Stack direction="row" spacing={1}>
              <Button size="small" onClick={() => setScenario(Math.max(0, scenario - 1))}>−</Button>
              <b>{scenario * 5}%</b>
              <Button ref={scenarioRef} size="small" onClick={() => setScenario(Math.min(4, scenario + 1))}>+</Button>
            </Stack>
          </Box>
          <Box className="scenario-outcomes">
            <Metric label="Projected cost" value={`$${(18400 + scenario * 7200).toLocaleString()}`} />
            <Metric label="Downtime estimate" value={`${4 + scenario * 2.5}h`} />
            <Metric label="Production impact" value={`${1.2 + scenario * 0.8}%`} />
          </Box>
          <Box className="terminal-recommendation">
            <Typography className="product-kicker">MODEL RECOMMENDATION</Typography>
            <Typography>
              {scenario > 2
                ? 'Advance intervention and protect the next scheduled production window.'
                : 'Plan condition-based maintenance in the identified low-load window.'}
            </Typography>
            <Button size="small" sx={{ mt: 1 }} variant="contained" disabled={!focus} onClick={createWorkOrder}>
              Create work order
            </Button>
          </Box>
        </Paper>
      </Box>

      <Paper className="terminal-bottom">
        <Box>
          <Typography className="product-kicker">HISTORICAL COMPARISON</Typography>
          <Typography>Current trajectory is <b>{failure > 45 ? 'above' : 'within'}</b> the prior 90-day risk envelope.</Typography>
          <MiniGraph values={projected.map((value, index) => value + ((index % 3) - 1) * 4)} label="90-day baseline overlay" />
        </Box>
        <Box>
          <Typography className="product-kicker">RISK & IMPACT SENSITIVITY</Typography>
          <Box className="sensitivity-bars">
            {['Process load', 'Ambient heat', 'Vibration trend', 'Maintenance delay'].map((labelText, index) => (
              <Typography key={labelText}>
                <span>{labelText}</span>
                <i><b style={{ width: `${38 + index * 14 + scenario * 4}%` }} /></i>
                <em>{['Low', 'Medium', 'High', 'Critical'][Math.min(3, Math.floor((index + scenario) / 2))]}</em>
              </Typography>
            ))}
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}

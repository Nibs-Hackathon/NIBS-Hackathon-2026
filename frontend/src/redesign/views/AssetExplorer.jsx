import { useEffect, useMemo, useRef, useState } from 'react';
import { Box, Button, MenuItem, Paper, TextField, Typography } from '@mui/material';
import { SearchOutlined, UnfoldMoreOutlined } from '@mui/icons-material';
import { assetRisk, label, round } from './shared';

const BUILTIN_VIEWS = [
  { id: 'shift-critical', label: 'Shift Critical', riskBand: 'critical', favoritesOnly: false, alarmsOnly: false, sort: 'risk' },
  { id: 'my-pins', label: 'My Pins', riskBand: 'all', favoritesOnly: true, alarmsOnly: false, sort: 'name' },
  { id: 'open-alarms', label: 'Open Alarms', riskBand: 'all', favoritesOnly: false, alarmsOnly: true, sort: 'risk' },
  { id: 'all-facility', label: 'Show all', riskBand: 'all', favoritesOnly: false, alarmsOnly: false, showAll: true, sort: 'name' },
];

const ROW_H = 36;
const OVERSCAN = 10;

export function parseAssetPath(asset, clean) {
  const cleaner = clean || ((value, fallback = '—') => String(value ?? '').trim() || fallback);
  const location = cleaner(asset.location || asset.zone, 'Facility network');
  const parts = String(location).split(/[›>\/|]/).map((part) => part.trim()).filter(Boolean);
  const area = parts[0] || location;
  const unit = parts[1] || parts[0] || 'Unit';
  const system = cleaner(label(asset.type || 'Process system'), 'Process system');
  return { facility: 'Facility', area, unit, system };
}

function useVirtualWindow(count, rowHeight = ROW_H) {
  const ref = useRef(null);
  const [range, setRange] = useState({ start: 0, end: Math.min(count, 40) });

  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const update = () => {
      const start = Math.max(0, Math.floor(el.scrollTop / rowHeight) - OVERSCAN);
      const visible = Math.ceil(el.clientHeight / rowHeight) + OVERSCAN * 2;
      setRange({ start, end: Math.min(count, start + visible) });
    };
    update();
    el.addEventListener('scroll', update, { passive: true });
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(update) : null;
    ro?.observe(el);
    return () => {
      el.removeEventListener('scroll', update);
      ro?.disconnect();
    };
  }, [count, rowHeight]);

  return {
    ref,
    start: range.start,
    end: range.end,
    totalHeight: count * rowHeight,
    offsetY: range.start * rowHeight,
  };
}

/**
 * Part G + QA§3 — Queues first; lazy unit tree; windowed hierarchy rows.
 */
export function AssetExplorer({
  rows = [],
  allRows = rows,
  selectedId,
  onSelect,
  query,
  onQueryChange,
  favorites = [],
  recentIds = [],
  activeViewId,
  onActivateView,
  showFullTree,
  onToggleFullTree,
  clean,
}) {
  const [expanded, setExpanded] = useState({});

  const criticalRows = useMemo(
    () => allRows.filter(({ asset, incident }) => assetRisk(asset, incident) > 70 || Boolean(incident)).slice(0, 10),
    [allRows],
  );
  const incidentRows = useMemo(
    () => allRows.filter(({ incident }) => Boolean(incident)).slice(0, 10),
    [allRows],
  );
  const favoriteRows = useMemo(
    () => allRows.filter(({ asset }) => favorites.includes(asset.id)),
    [allRows, favorites],
  );
  const recentRows = useMemo(() => {
    const byId = new Map(allRows.map((row) => [row.asset.id, row]));
    return recentIds.map((id) => byId.get(id)).filter(Boolean).slice(0, 10);
  }, [allRows, recentIds]);

  const hierarchy = useMemo(() => {
    const root = {};
    rows.forEach((row) => {
      const path = parseAssetPath(row.asset, clean);
      const areaNode = (root[path.area] ||= {});
      const unitNode = (areaNode[path.unit] ||= {});
      const systemNode = (unitNode[path.system] ||= []);
      systemNode.push(row);
    });
    return root;
  }, [rows, clean]);

  const selectedPath = useMemo(() => {
    const row = allRows.find((item) => item.asset.id === selectedId);
    return row ? parseAssetPath(row.asset, clean) : null;
  }, [allRows, selectedId, clean]);

  useEffect(() => {
    if (!selectedPath) return;
    const areaKey = `area:${selectedPath.area}`;
    const unitKey = `${areaKey}/unit:${selectedPath.unit}`;
    const systemKey = `${unitKey}/sys:${selectedPath.system}`;
    setExpanded((current) => ({
      ...current,
      [areaKey]: true,
      [unitKey]: true,
      [systemKey]: true,
    }));
  }, [selectedPath]);

  const isExpanded = (key) => {
    if (showFullTree && expanded[key] === undefined) return true;
    return Boolean(expanded[key]);
  };

  const toggleExpand = (key) => {
    setExpanded((current) => ({ ...current, [key]: !isExpanded(key) }));
  };

  const selectFromExplorer = (id) => onSelect?.(id, 'explorer');

  const flatRows = useMemo(() => {
    const list = [];
    Object.entries(hierarchy).forEach(([area, units]) => {
      const areaKey = `area:${area}`;
      const areaCount = Object.values(units).reduce(
        (sum, systems) => sum + Object.values(systems).reduce((n, members) => n + members.length, 0),
        0,
      );
      list.push({
        kind: 'area',
        key: areaKey,
        label: area,
        count: areaCount,
        onPath: selectedPath?.area === area,
      });
      if (!isExpanded(areaKey)) return;
      Object.entries(units).forEach(([unit, systems]) => {
        const unitKey = `${areaKey}/unit:${unit}`;
        const unitCount = Object.values(systems).reduce((n, members) => n + members.length, 0);
        list.push({
          kind: 'unit',
          key: unitKey,
          label: unit,
          count: unitCount,
          onPath: selectedPath?.area === area && selectedPath?.unit === unit,
        });
        if (!isExpanded(unitKey)) return;
        Object.entries(systems).forEach(([system, members]) => {
          const systemKey = `${unitKey}/sys:${system}`;
          list.push({
            kind: 'system',
            key: systemKey,
            label: system,
            count: members.length,
            onPath: selectedPath?.area === area && selectedPath?.unit === unit && selectedPath?.system === system,
          });
          if (!isExpanded(systemKey)) return;
          members.forEach((row) => {
            list.push({
              kind: 'asset',
              key: `asset:${row.asset.id}`,
              row,
              onPath: selectedId === row.asset.id,
            });
          });
        });
      });
    });
    return list;
  // expanded + showFullTree intentionally included
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hierarchy, expanded, showFullTree, selectedPath, selectedId]);

  const virt = useVirtualWindow(flatRows.length, ROW_H);
  const windowed = flatRows.slice(virt.start, virt.end);

  const onSearchKey = (event) => {
    if (event.key !== 'Enter' || !rows.length) return;
    selectFromExplorer(rows[0].asset.id);
  };

  const renderQueue = (title, items) => {
    if (!items.length) return null;
    return (
      <Box className="assets-critical-queue">
        <Typography className="product-kicker">{title}</Typography>
        {items.map((row) => {
          const rowRisk = assetRisk(row.asset, row.incident);
          return (
            <button
              type="button"
              key={`${title}-${row.asset.id}`}
              className={`asset-tree-item ${selectedId === row.asset.id ? 'selected' : ''}`}
              onClick={() => selectFromExplorer(row.asset.id)}
            >
              <span className={`asset-tree-dot ${rowRisk > 70 ? 'critical' : rowRisk > 40 ? 'watch' : ''}`} />
              <span>
                <b>{row.asset.name}</b>
                <small>
                  {row.incident
                    ? label(row.incident.incident_type || 'Open incident')
                    : `${round(row.asset.health)}% · risk ${rowRisk}`}
                </small>
              </span>
              {row.incident ? <em className="assets-incident-pip">!</em> : <em>{rowRisk}</em>}
            </button>
          );
        })}
      </Box>
    );
  };

  const assetIds = useMemo(
    () => flatRows.filter((item) => item.kind === 'asset').map((item) => item.row.asset.id),
    [flatRows],
  );

  return (
    <Paper className="asset-explorer assets-pane">
      <Box className="asset-explorer-top">
        <Typography className="product-kicker">EXPLORER</Typography>
        <Typography variant="caption">{rows.length} in view · windowed</Typography>
      </Box>

      <TextField
        value={query}
        onChange={(event) => onQueryChange?.(event.target.value)}
        onKeyDown={onSearchKey}
        size="small"
        placeholder="Search tag, name, area"
        slotProps={{ input: { startAdornment: <SearchOutlined fontSize="small" /> } }}
      />

      <Box className="assets-saved-views">
        <TextField
          select
          size="small"
          fullWidth
          label="Saved view"
          value={activeViewId || 'shift-critical'}
          onChange={(event) => onActivateView?.(event.target.value)}
        >
          {BUILTIN_VIEWS.map((view) => (
            <MenuItem key={view.id} value={view.id}>{view.label}</MenuItem>
          ))}
        </TextField>
      </Box>

      {renderQueue('CRITICAL NOW', criticalRows)}
      {renderQueue('OPEN INCIDENTS', incidentRows)}
      {renderQueue('FAVORITES', favoriteRows)}
      {renderQueue('RECENT', recentRows)}

      <Box className="assets-tree-head">
        <Typography className="product-kicker">FACILITY HIERARCHY</Typography>
        <Button size="small" startIcon={<UnfoldMoreOutlined />} onClick={onToggleFullTree}>
          {showFullTree ? 'Queues focus' : 'Show all'}
        </Button>
      </Box>

      {!showFullTree && (
        <Typography variant="caption" className="assets-lazy-hint" color="text.secondary">
          Expand Area → Unit to load equipment (lazy). Show all mounts the full filtered tree windowed.
        </Typography>
      )}

      <Box
        className={`asset-tree assets-tree-virtual ${selectedId ? 'has-selection' : ''}`}
        ref={virt.ref}
        tabIndex={0}
        onKeyDown={(event) => {
          if (!assetIds.length) return;
          const idx = Math.max(0, assetIds.indexOf(selectedId));
          if (event.key === 'ArrowDown') {
            event.preventDefault();
            selectFromExplorer(assetIds[Math.min(assetIds.length - 1, idx + 1)]);
          }
          if (event.key === 'ArrowUp') {
            event.preventDefault();
            selectFromExplorer(assetIds[Math.max(0, idx - 1)]);
          }
          if (event.key === 'Enter' && assetIds[idx]) selectFromExplorer(assetIds[idx]);
        }}
      >
        {!flatRows.length && (
          <Typography variant="body2" color="text.secondary" sx={{ p: 1.5 }}>
            No assets match this view. Switch saved view or clear search.
          </Typography>
        )}

        <div className="assets-tree-spacer" style={{ height: virt.totalHeight }}>
          <div className="assets-tree-window" style={{ transform: `translateY(${virt.offsetY}px)` }}>
            {windowed.map((item) => {
              if (item.kind !== 'asset') {
                return (
                  <button
                    type="button"
                    key={item.key}
                    className={`asset-tree-parent assets-tree-toggle assets-virt-row is-${item.kind} ${selectedId && !item.onPath ? 'is-dimmed' : ''}`}
                    style={{ height: ROW_H }}
                    onClick={() => toggleExpand(item.key)}
                  >
                    <span>{isExpanded(item.key) ? '▾' : '▸'}</span>
                    {item.label}
                    <b>{item.count}</b>
                  </button>
                );
              }
              const row = item.row;
              const rowRisk = assetRisk(row.asset, row.incident);
              const isSelected = selectedId === row.asset.id;
              return (
                <button
                  type="button"
                  key={item.key}
                  className={`asset-tree-item assets-virt-row ${isSelected ? 'selected' : ''} ${selectedId && !isSelected ? 'is-dimmed' : ''}`}
                  style={{ height: ROW_H }}
                  onClick={() => selectFromExplorer(row.asset.id)}
                >
                  <span className={`asset-tree-dot ${rowRisk > 70 ? 'critical' : rowRisk > 40 ? 'watch' : ''}`} />
                  <span>
                    <b>{row.asset.name}</b>
                    <small>{round(row.asset.health)}% health</small>
                  </span>
                  <em>{rowRisk}</em>
                </button>
              );
            })}
          </div>
        </div>
      </Box>
    </Paper>
  );
}

export { BUILTIN_VIEWS };

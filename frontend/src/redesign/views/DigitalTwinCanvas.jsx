import { useEffect, useRef, useState } from 'react';
import { Box, Button, Menu, MenuItem, Typography } from '@mui/material';
import {
  CenterFocusStrongOutlined, FitScreenOutlined, ZoomInOutlined, ZoomOutOutlined,
} from '@mui/icons-material';
import { assetRisk, label, round } from './shared';

const NODE_SLOTS = [
  { x: 12, y: 48 }, { x: 28, y: 28 }, { x: 46, y: 52 }, { x: 64, y: 28 },
  { x: 82, y: 50 }, { x: 18, y: 72 }, { x: 38, y: 74 }, { x: 58, y: 70 },
  { x: 76, y: 74 }, { x: 14, y: 18 }, { x: 50, y: 16 }, { x: 88, y: 18 },
];

/**
 * Part D + H + I — Digital Twin: selection coupling, no marketing chrome, context menu only on RMB.
 */
export function DigitalTwinCanvas({
  rows = [],
  selectedId,
  onSelect,
  layers,
  camera,
  onCameraChange,
  onFitSelection,
  onFitUnit,
  onOpenIncident,
  onViewForecast,
  onCreateWorkOrder,
  onToggleFavorite,
  onCopyTag,
  onTagClick,
  onAlarmClick,
  isFavorite,
  clean,
}) {
  const viewportRef = useRef(null);
  const [menu, setMenu] = useState(null);
  const [spaceDown, setSpaceDown] = useState(false);
  const dragRef = useRef(null);

  const zoom = Number(camera?.zoom) || 1;
  const panX = Number(camera?.panX) || 0;
  const panY = Number(camera?.panY) || 0;
  const twinNodes = rows.slice(0, NODE_SLOTS.length);
  const selected = twinNodes.find((row) => row.asset.id === selectedId) || twinNodes[0];
  const heatmapMode = layers?.deviation ? 'deviation' : layers?.health ? 'health' : layers?.risk ? 'risk' : null;

  useEffect(() => {
    const onKey = (event) => {
      if (event.code === 'Space') setSpaceDown(event.type === 'keydown');
    };
    window.addEventListener('keydown', onKey);
    window.addEventListener('keyup', onKey);
    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('keyup', onKey);
    };
  }, []);

  useEffect(() => {
    if (!selectedId || !onCameraChange) return;
    const index = twinNodes.findIndex((row) => row.asset.id === selectedId);
    if (index < 0) return;
    const slot = NODE_SLOTS[index];
    onCameraChange({
      fitMode: 'selection',
      panX: (50 - slot.x) * 0.35,
      panY: (50 - slot.y) * 0.35,
    });
  // Intentionally only when selection changes
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedId]);

  const setZoom = (next) => onCameraChange?.({ zoom: Math.min(2.2, Math.max(0.55, next)), fitMode: 'free' });
  const selectTwin = (id) => onSelect?.(id, 'twin');

  const onWheel = (event) => {
    if (!event.ctrlKey && !event.metaKey) return;
    event.preventDefault();
    setZoom(zoom + (event.deltaY < 0 ? 0.08 : -0.08));
  };

  const onPointerDown = (event) => {
    if (!spaceDown && event.button !== 1) return;
    dragRef.current = { x: event.clientX, y: event.clientY, panX, panY };
    event.currentTarget.setPointerCapture?.(event.pointerId);
  };

  const onPointerMove = (event) => {
    if (!dragRef.current) return;
    const dx = (event.clientX - dragRef.current.x) / 4;
    const dy = (event.clientY - dragRef.current.y) / 4;
    onCameraChange?.({
      panX: dragRef.current.panX + dx,
      panY: dragRef.current.panY + dy,
      fitMode: 'free',
    });
  };

  const onPointerUp = () => { dragRef.current = null; };

  const openContext = (event, row) => {
    event.preventDefault();
    selectTwin(row.asset.id);
    setMenu({ mouseX: event.clientX, mouseY: event.clientY, row });
  };

  const nodeFill = (row) => {
    const risk = assetRisk(row.asset, row.incident);
    const health = Number(row.asset.health) || 0;
    if (heatmapMode === 'health') return health < 50 ? 'heat-critical' : health < 80 ? 'heat-watch' : 'heat-ok';
    if (heatmapMode === 'deviation') return risk > 55 ? 'heat-critical' : 'heat-watch';
    if (heatmapMode === 'risk') return risk > 70 ? 'heat-critical' : risk > 40 ? 'heat-watch' : 'heat-ok';
    return '';
  };

  const flowSpeed = selected ? Math.max(0.4, Math.min(2.2, (Number(selected.asset.health) || 50) / 50)) : 1;

  return (
    <Box className="twin-canvas assets-twin" ref={viewportRef}>
      <Box className="twin-canvas-top assets-twin-chrome">
        <Typography className="assets-twin-sync" variant="caption">
          {twinNodes.length} nodes · {Math.round(zoom * 100)}%
        </Typography>
        <Box className="assets-twin-tools">
          <Button size="small" onClick={() => setZoom(zoom - 0.1)} aria-label="Zoom out"><ZoomOutOutlined fontSize="small" /></Button>
          <Button size="small" onClick={() => setZoom(zoom + 0.1)} aria-label="Zoom in"><ZoomInOutlined fontSize="small" /></Button>
          <Button size="small" startIcon={<FitScreenOutlined />} onClick={onFitUnit}>Fit unit</Button>
          <Button size="small" startIcon={<CenterFocusStrongOutlined />} onClick={onFitSelection} disabled={!selectedId}>Fit selection</Button>
        </Box>
      </Box>

      {selected && (
        <Box className="assets-causal-strip" role="status">
          <span>{selected.incident ? 'Why: linked case evidence' : 'Why: within baseline envelope'}</span>
          <b>
            {selected.incident
              ? label(selected.incident.incident_type || selected.incident.reasoning || 'Deviation vs baseline')
              : `Health ${round(selected.asset.health)}% · risk ${assetRisk(selected.asset, selected.incident)}`}
          </b>
        </Box>
      )}

      <Box
        className={`twin-process-map assets-twin-viewport ${spaceDown ? 'is-panning' : ''}`}
        onWheel={onWheel}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        tabIndex={0}
        onKeyDown={(event) => {
          if (!twinNodes.length) return;
          const ids = twinNodes.map((row) => row.asset.id);
          const idx = Math.max(0, ids.indexOf(selectedId));
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            event.preventDefault();
            selectTwin(ids[Math.min(ids.length - 1, idx + 1)]);
          }
          if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            event.preventDefault();
            selectTwin(ids[Math.max(0, idx - 1)]);
          }
        }}
      >
        <div
          className="assets-twin-world"
          style={{
            transform: `translate(${panX}%, ${panY}%) scale(${zoom})`,
            '--flow-speed': `${1.8 / flowSpeed}s`,
          }}
        >
          <div className="twin-grid-lines" />
          {layers?.process !== false && (
            <svg viewBox="0 0 740 380" className="assets-topology" role="img" aria-label="Unit process topology">
              <path className={`map-pipe ${layers?.maintenance ? 'is-maintenance' : ''}`} d="M80 200H205V115H355V200H495V115H655" />
              <path className="map-pipe map-flow assets-flow" d="M80 200H205V115H355V200H495V115H655" />
              <rect className="map-tank" x="35" y="130" width="82" height="140" rx="12" />
              <path className="map-level" d="M42 232h68v31H42z" />
              <circle className="map-pump" cx="280" cy="115" r="39" />
              <path className="map-pump-spoke" d="M280 76v78M241 115h78M252 87l56 56M308 87l-56 56" />
              <rect className="map-unit" x="420" y="155" width="95" height="90" rx="12" />
              <path className="map-stack" d="M570 115v145M610 115v145" />
            </svg>
          )}

          {twinNodes.map((row, index) => {
            const rowRisk = assetRisk(row.asset, row.incident);
            const slot = NODE_SLOTS[index];
            const heat = nodeFill(row);
            const alarm = Boolean(row.incident) && layers?.alarms !== false;
            const isSelected = row.asset.id === selectedId;
            return (
              <button
                type="button"
                key={row.asset.id}
                onClick={() => selectTwin(row.asset.id)}
                onContextMenu={(event) => openContext(event, row)}
                style={{ left: `${slot.x}%`, top: `${slot.y}%` }}
                className={[
                  'twin-map-node',
                  isSelected ? 'selected' : '',
                  selectedId && !isSelected ? 'is-neighbor' : '',
                  rowRisk > 70 ? 'critical' : '',
                  heat,
                  alarm ? 'has-alarm' : '',
                ].filter(Boolean).join(' ')}
              >
                <i />
                <span>{row.asset.name}</span>
                <b>{round(row.asset.health)}%</b>
                {alarm && (
                  <em
                    className="assets-alarm-pip"
                    title="Open incident"
                    onClick={(event) => {
                      event.stopPropagation();
                      onAlarmClick?.(row, event);
                    }}
                  />
                )}
                {layers?.sensors !== false && (
                  <small
                    className="assets-tag-overlay"
                    onClick={(event) => {
                      event.stopPropagation();
                      onTagClick?.(row);
                    }}
                  >
                    {String(row.asset.tag || row.asset.id).slice(0, 10)}
                  </small>
                )}
              </button>
            );
          })}
        </div>

        <Box className="assets-minimap" aria-label="Minimap">
          <button
            type="button"
            className="assets-minimap-frame"
            onClick={() => onCameraChange?.({ panX: 0, panY: 0, zoom: 1, fitMode: 'unit' })}
          >
            {twinNodes.map((row, index) => (
              <i
                key={row.asset.id}
                className={row.asset.id === selectedId ? 'is-selected' : ''}
                style={{ left: `${NODE_SLOTS[index].x}%`, top: `${NODE_SLOTS[index].y}%` }}
              />
            ))}
          </button>
        </Box>
      </Box>

      <Menu
        open={Boolean(menu)}
        onClose={() => setMenu(null)}
        anchorReference="anchorPosition"
        anchorPosition={menu ? { top: menu.mouseY, left: menu.mouseX } : undefined}
      >
        {menu?.row?.incident && (
          <MenuItem onClick={() => { onOpenIncident?.(menu.row); setMenu(null); }}>Open incident</MenuItem>
        )}
        <MenuItem onClick={() => { onViewForecast?.(menu.row); setMenu(null); }}>View forecast</MenuItem>
        <MenuItem onClick={() => { onCreateWorkOrder?.(menu.row); setMenu(null); }}>Create work order</MenuItem>
        <MenuItem onClick={() => { onToggleFavorite?.(menu.row.asset.id); setMenu(null); }}>
          {isFavorite?.(menu?.row?.asset?.id) ? 'Unpin favorite' : 'Pin favorite'}
        </MenuItem>
        <MenuItem onClick={() => { onCopyTag?.(menu.row); setMenu(null); }}>Copy tag</MenuItem>
        <MenuItem onClick={() => { selectTwin(menu.row.asset.id); setMenu(null); }}>Show in explorer</MenuItem>
      </Menu>
    </Box>
  );
}

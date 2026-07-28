import { useEffect, useRef, useState } from 'react';
import { Box, Button, Menu, MenuItem, Typography } from '@mui/material';
import {
  CenterFocusStrongOutlined, FitScreenOutlined, ZoomInOutlined, ZoomOutOutlined,
} from '@mui/icons-material';
import { assetRisk, label, round } from './shared';

const NODE_LAYOUT = [
  { x: 13, y: 10, equipmentY: 24 },
  { x: 38, y: 10, equipmentY: 24 },
  { x: 63, y: 10, equipmentY: 24 },
  { x: 87, y: 10, equipmentY: 24 },
  { x: 87, y: 42, equipmentY: 56 },
  { x: 63, y: 42, equipmentY: 56 },
  { x: 38, y: 42, equipmentY: 56 },
  { x: 13, y: 42, equipmentY: 56 },
  { x: 13, y: 74, equipmentY: 88 },
  { x: 38, y: 74, equipmentY: 88 },
  { x: 63, y: 74, equipmentY: 88 },
  { x: 87, y: 74, equipmentY: 88 },
];

function EquipmentGlyph({ row, slot, selected }) {
  const type = String(row.asset.type || row.asset.asset_type || row.asset.name || '').toLowerCase();
  const className = `assets-equipment ${selected ? 'is-selected' : ''} ${row.incident ? 'is-critical' : ''}`;
  const common = { className, transform: `translate(${slot.x} ${slot.equipmentY})` };

  if (type.includes('pump')) {
    return (
      <g {...common}>
        <circle r="4.8" />
        <path d="M0-4.8V4.8M-4.8 0H4.8M-3.4-3.4L3.4 3.4M3.4-3.4L-3.4 3.4" />
      </g>
    );
  }
  if (type.includes('compressor')) {
    return (
      <g {...common}>
        <circle r="5.2" />
        <path d="M-3.6-2.8L1 0l-4.6 2.8zM3.6-2.8L-1 0l4.6 2.8z" />
      </g>
    );
  }
  if (type.includes('boiler') || type.includes('heater')) {
    return (
      <g {...common}>
        <rect x="-5.2" y="-5.6" width="10.4" height="11.2" rx="2" />
        <path d="M-2.8-2.6c1.8 1.2-1.8 2.2 0 3.4s-1.8 2.2 0 3.4M1-2.6c1.8 1.2-1.8 2.2 0 3.4s-1.8 2.2 0 3.4" />
      </g>
    );
  }
  if (type.includes('valve')) {
    return (
      <g {...common}>
        <path d="M-5-4L0 0l-5 4zM5-4L0 0l5 4zM0-5.5v11" />
      </g>
    );
  }
  if (type.includes('pipeline') || type.includes('pipe')) {
    return (
      <g {...common}>
        <path d="M-6 0H6M-3-3v6M3-3v6" />
      </g>
    );
  }
  return (
    <g {...common}>
      <rect x="-5.2" y="-4.8" width="10.4" height="9.6" rx="2" />
      <path d="M-2.8 0h5.6" />
    </g>
  );
}

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
  const twinNodes = rows.slice(0, NODE_LAYOUT.length);
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
  const processPath = NODE_LAYOUT
    .slice(0, twinNodes.length)
    .map((slot, index) => `${index ? 'L' : 'M'}${slot.x} ${slot.equipmentY}`)
    .join(' ');

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
            <svg viewBox="0 0 100 100" className="assets-topology" role="img" aria-label="Unit process topology">
              {processPath && (
                <>
                  <path className={`map-pipe assets-process-path ${layers?.maintenance ? 'is-maintenance' : ''}`} d={processPath} />
                  <path className="map-pipe map-flow assets-flow assets-process-path" d={processPath} />
                </>
              )}
              {twinNodes.map((row, index) => (
                <EquipmentGlyph
                  key={`equipment-${row.asset.id}`}
                  row={row}
                  slot={NODE_LAYOUT[index]}
                  selected={row.asset.id === selectedId}
                />
              ))}
            </svg>
          )}

          {twinNodes.map((row, index) => {
            const rowRisk = assetRisk(row.asset, row.incident);
            const slot = NODE_LAYOUT[index];
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
                style={{ left: `${NODE_LAYOUT[index].x}%`, top: `${NODE_LAYOUT[index].equipmentY}%` }}
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

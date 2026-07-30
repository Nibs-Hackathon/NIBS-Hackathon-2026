import { memo, useEffect, useRef } from 'react';
import { geoContains } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
import world from 'world-atlas/countries-110m.json';
import {
  EARTH_COLS,
  EARTH_ROWS,
  SITE_RADIUS_DEG,
  angularDistanceDeg,
  cellCenter,
} from '../../data/earthLandMask';
import './DotMatrixGlobe.css';

const TWO_PI = Math.PI * 2;
const DEG = Math.PI / 180;
const CAMERA_LAT = 14 * DEG;
const SIN_CAMERA_LAT = Math.sin(CAMERA_LAT);
const COS_CAMERA_LAT = Math.cos(CAMERA_LAT);
const DEPTH_BUCKETS = 5;
const NORMAL_RENDER_FPS = 24;
const DEGRADED_RENDER_FPS = 16;
const LAND = feature(world, world.objects.land);
const COUNTRY_LINES = mesh(world, world.objects.countries).coordinates;
function buildDots() {
  const dots = [];
  for (let row = 0; row < EARTH_ROWS; row += 1) {
    for (let col = 0; col < EARTH_COLS; col += 1) {
      const { lat, lng } = cellCenter(col, row);
      dots.push({
        lat,
        lng,
        land: geoContains(LAND, [lng, lat]),
        sinPhi: Math.sin(lat * DEG),
        cosPhi: Math.cos(lat * DEG),
        sinLng: Math.sin(lng * DEG),
        cosLng: Math.cos(lng * DEG),
      });
    }
  }
  return dots;
}

const BASE_DOTS = buildDots();
const PREPARED_COUNTRY_LINES = COUNTRY_LINES.map((line) => (
  line
    .filter((_, index) => index % 2 === 0 || index === line.length - 1)
    .map(([lng, lat]) => ({
      lng,
      sinPhi: Math.sin(lat * DEG),
      cosPhi: Math.cos(lat * DEG),
      sinLng: Math.sin(lng * DEG),
      cosLng: Math.cos(lng * DEG),
    }))
));

function prepareDots(sites, focusName, enterprise) {
  return BASE_DOTS.map((dot) => {
    let weight = 0;
    let isFocus = false;
    for (const site of sites) {
      const dist = angularDistanceDeg(dot.lat, dot.lng, site.lat, site.lng);
      if (dist > SITE_RADIUS_DEG) continue;
      const localWeight = (1 - dist / SITE_RADIUS_DEG) ** 2;
      if (site.name === focusName) {
        isFocus = true;
        weight = Math.max(weight, localWeight);
      } else if (enterprise) {
        weight = Math.max(weight, localWeight * 0.45);
      }
    }
    return { ...dot, siteWeight: weight, isFocus };
  });
}

const DotMatrixGlobe = memo(function DotMatrixGlobe({
  sites = [],
  focusName = null,
  enterprise = false,
  fleetHealth = 0,
  caption = '',
  reducedMotion = false,
}) {
  const wrapRef = useRef(null);
  const canvasRef = useRef(null);
  const dotsRef = useRef([]);
  const rafRef = useRef(null);
  const sitesRef = useRef(sites);
  const rotationRef = useRef(-18);
  const rotationFocusRef = useRef(null);
  sitesRef.current = sites;
  const siteGeometryKey = sites
    .map((site) => `${site.name}:${site.lat}:${site.lng}`)
    .sort()
    .join('|');

  useEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    if (!wrap || !canvas) return undefined;

    const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
    const lowPowerDevice = (navigator.hardwareConcurrency || 8) <= 4
      || (navigator.deviceMemory || 8) <= 4;
    const saveData = Boolean(navigator.connection?.saveData);
    // The globe turns at only ~0.48°/second. Redrawing its 10k-point projection
    // at 60–120 Hz burns CPU without producing a perceptible motion benefit.
    // Keep animation time-based, but cap expensive canvas reconstruction.
    let targetFps = lowPowerDevice || saveData
      ? DEGRADED_RENDER_FPS
      : NORMAL_RENDER_FPS;
    let frameInterval = 1000 / targetFps;
    // Dot radii are around one CSS pixel, so high-DPI backing stores add fill
    // cost far faster than useful detail.
    const dpr = Math.min(window.devicePixelRatio || 1, lowPowerDevice ? 1 : 1.1);
    const currentSites = sitesRef.current;
    const focusSite = currentSites.find((site) => site.name === focusName);
    const renderDots = prepareDots(currentSites, focusName, enterprise);
    if (rotationFocusRef.current !== focusName) {
      rotationRef.current = Number.isFinite(Number(focusSite?.lng))
        ? Number(focusSite.lng)
        : rotationRef.current;
      rotationFocusRef.current = focusName;
    }
    let rotation = rotationRef.current;
    let lastTime = performance.now();
    let lastDraw = 0;
    let inViewport = true;
    let windowFocused = document.hasFocus();
    let disposed = false;
    let halo = null;
    let haloTheme = null;
    let averageDrawMs = 0;
    let recoveryFrames = 0;

    const resize = () => {
      const rect = wrap.getBoundingClientRect();
      const size = Math.round(Math.min(rect.width, rect.height));
      if (!size) return;
      canvas.width = Math.round(size * dpr);
      canvas.height = Math.round(size * dpr);
      canvas.style.width = `${size}px`;
      canvas.style.height = `${size}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      dotsRef.current = renderDots;
      halo = null;
    };

    const schedule = () => {
      if (
        disposed
        || reducedMotion
        || !inViewport
        || !windowFocused
        || document.visibilityState !== 'visible'
        || rafRef.current != null
      ) return;
      rafRef.current = requestAnimationFrame(tick);
    };

    const tick = (now) => {
      rafRef.current = null;
      if (
        disposed
        || !inViewport
        || !windowFocused
        || document.visibilityState !== 'visible'
      ) return;
      if (frameInterval && now - lastDraw < frameInterval - 1) {
        schedule();
        return;
      }

      const elapsed = Math.min(34, now - lastTime);
      lastTime = now;
      lastDraw = now;
      // Time-based motion remains the same speed on 60/90/120 Hz displays and
      // completes a true 360-degree revolution without a visual reset.
      if (!reducedMotion) {
        rotation = (rotation + elapsed * 0.008) % 360;
        rotationRef.current = rotation;
      }

      const size = canvas.width / dpr;
      const radius = size * 0.465;
      const cx = size / 2;
      const cy = size / 2;
      const lightTheme = document.documentElement.dataset.rigosTheme === 'light';
      const landColor = lightTheme ? '20, 27, 38' : '239, 244, 248';
      const oceanColor = lightTheme ? '80, 91, 108' : '125, 139, 156';
      const rotationRad = rotation * DEG;
      const sinRotation = Math.sin(rotationRad);
      const cosRotation = Math.cos(rotationRad);
      const renderStarted = performance.now();

      ctx.clearRect(0, 0, size, size);
      if (!halo || haloTheme !== lightTheme) {
        halo = ctx.createRadialGradient(cx, cy, radius * 0.72, cx, cy, radius * 1.12);
        halo.addColorStop(0, 'rgba(100, 116, 139, 0)');
        halo.addColorStop(0.88, lightTheme ? 'rgba(15, 23, 42, 0.025)' : 'rgba(255, 255, 255, 0.018)');
        halo.addColorStop(1, lightTheme ? 'rgba(15, 23, 42, 0.08)' : 'rgba(255, 255, 255, 0.07)');
        haloTheme = lightTheme;
      }
      ctx.fillStyle = halo;
      ctx.beginPath();
      ctx.arc(cx, cy, radius * 1.1, 0, TWO_PI);
      ctx.fill();

      const landPaths = Array.from({ length: DEPTH_BUCKETS }, () => new Path2D());
      const oceanPaths = Array.from({ length: DEPTH_BUCKETS }, () => new Path2D());
      const siteDots = [];
      for (const dot of dotsRef.current) {
        const sinLambda = dot.sinLng * cosRotation - dot.cosLng * sinRotation;
        const cosLambda = dot.cosLng * cosRotation + dot.sinLng * sinRotation;
        const z = SIN_CAMERA_LAT * dot.sinPhi + COS_CAMERA_LAT * dot.cosPhi * cosLambda;
        if (z <= 0) continue;

        const x = dot.cosPhi * sinLambda;
        const y = COS_CAMERA_LAT * dot.sinPhi - SIN_CAMERA_LAT * dot.cosPhi * cosLambda;
        const drawX = cx + x * radius;
        const drawY = cy - y * radius;
        const weight = dot.siteWeight;
        const isFocus = dot.isFocus;
        if (weight > 0) {
          siteDots.push({
            x: drawX,
            y: drawY,
            alpha: Math.min(1, (dot.land ? 0.9 : 0.1) * Math.max(0.16, Math.sqrt(z)) + weight * 0.55),
            color: isFocus ? '#66d9ff' : '#4f8cff',
            radius: isFocus ? 0.82 + weight * 0.45 : 0.7 + weight * 0.25,
            isFocus,
          });
          continue;
        }

        const bucket = Math.min(DEPTH_BUCKETS - 1, Math.floor(z * DEPTH_BUCKETS));
        const bucketDepth = (bucket + 0.5) / DEPTH_BUCKETS;
        const dotRadius = (dot.land ? 0.74 : 0.31) * (0.72 + bucketDepth * 0.32);
        const dotPath = dot.land ? landPaths[bucket] : oceanPaths[bucket];
        // `arc()` continues the current subpath. Start a fresh one for every
        // dot or Canvas joins neighboring circles with giant filled wedges.
        dotPath.moveTo(drawX + dotRadius, drawY);
        dotPath.arc(drawX, drawY, dotRadius, 0, TWO_PI);
      }

      // Batch thousands of same-style dots into a handful of fills. Canvas
      // shadowBlur rasterized every dot into an expensive temporary surface;
      // a translucent batched stroke provides the same luminous edge at a
      // fraction of the cost.
      for (let bucket = 0; bucket < DEPTH_BUCKETS; bucket += 1) {
        const bucketDepth = (bucket + 0.5) / DEPTH_BUCKETS;
        const edgeFade = Math.max(0.16, Math.sqrt(bucketDepth));
        ctx.globalAlpha = 0.1 * edgeFade;
        ctx.fillStyle = `rgba(${oceanColor}, 1)`;
        ctx.fill(oceanPaths[bucket]);
        ctx.globalAlpha = (lightTheme ? 0.12 : 0.2) * edgeFade;
        ctx.strokeStyle = `rgba(${landColor}, 1)`;
        ctx.lineWidth = lightTheme ? 0.75 : 1.05;
        ctx.stroke(landPaths[bucket]);
        ctx.globalAlpha = 0.9 * edgeFade;
        ctx.fillStyle = `rgba(${landColor}, 1)`;
        ctx.fill(landPaths[bucket]);
      }

      for (const dot of siteDots) {
        ctx.globalAlpha = dot.alpha;
        ctx.fillStyle = dot.color;
        ctx.shadowColor = dot.color;
        ctx.shadowBlur = dot.isFocus ? 5 : 3;
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.radius, 0, TWO_PI);
        ctx.fill();
      }
      ctx.shadowBlur = 0;

      // Natural Earth country boundaries make national and continental structure readable.
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, TWO_PI);
      ctx.clip();
      ctx.beginPath();
      for (const line of PREPARED_COUNTRY_LINES) {
        let penDown = false;
        let previousX = 0;
        let previousY = 0;
        for (const coordinate of line) {
          const sinLambda = coordinate.sinLng * cosRotation - coordinate.cosLng * sinRotation;
          const cosLambda = coordinate.cosLng * cosRotation + coordinate.sinLng * sinRotation;
          const z = SIN_CAMERA_LAT * coordinate.sinPhi
            + COS_CAMERA_LAT * coordinate.cosPhi * cosLambda;
          if (z <= 0.012) {
            penDown = false;
            continue;
          }

          const x = cx + coordinate.cosPhi * sinLambda * radius;
          const y = cy - (
            COS_CAMERA_LAT * coordinate.sinPhi
            - SIN_CAMERA_LAT * coordinate.cosPhi * cosLambda
          ) * radius;
          const jumped = penDown && Math.hypot(x - previousX, y - previousY) > radius * 0.22;
          if (!penDown || jumped) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
          penDown = true;
          previousX = x;
          previousY = y;
        }
      }
      // A quiet under-stroke cuts through the dot field, then a crisp theme-
      // aware line makes individual nations distinguishable.
      ctx.strokeStyle = lightTheme ? 'rgba(255, 255, 255, 0.72)' : 'rgba(2, 6, 12, 0.78)';
      ctx.lineWidth = 1.65;
      ctx.stroke();
      ctx.strokeStyle = lightTheme ? 'rgba(15, 23, 42, 0.48)' : 'rgba(255, 255, 255, 0.46)';
      ctx.lineWidth = lightTheme ? 0.76 : 0.7;
      ctx.stroke();
      ctx.restore();

      ctx.globalAlpha = 1;
      ctx.strokeStyle = lightTheme ? 'rgba(15, 23, 42, 0.14)' : 'rgba(226, 232, 240, 0.13)';
      ctx.lineWidth = 0.85;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, TWO_PI);
      ctx.stroke();

      // Directional rim accents give the sphere depth without adding another
      // center glow. The opposing arcs stay neutral in both themes.
      ctx.lineCap = 'round';
      ctx.lineWidth = 1.15;
      ctx.strokeStyle = lightTheme
        ? 'rgba(15, 23, 42, 0.22)'
        : 'rgba(255, 255, 255, 0.3)';
      ctx.beginPath();
      ctx.arc(cx, cy, radius - 1.2, Math.PI * 1.08, Math.PI * 1.72);
      ctx.stroke();

      ctx.lineWidth = 0.8;
      ctx.strokeStyle = lightTheme
        ? 'rgba(255, 255, 255, 0.72)'
        : 'rgba(2, 6, 12, 0.72)';
      ctx.beginPath();
      ctx.arc(cx, cy, radius - 1.2, Math.PI * 0.08, Math.PI * 0.72);
      ctx.stroke();
      ctx.lineCap = 'butt';

      const drawMs = performance.now() - renderStarted;
      averageDrawMs = averageDrawMs ? averageDrawMs * 0.92 + drawMs * 0.08 : drawMs;
      if (!lowPowerDevice && !saveData) {
        if (averageDrawMs > 14) {
          targetFps = DEGRADED_RENDER_FPS;
          frameInterval = 1000 / targetFps;
          recoveryFrames = 0;
        } else if (targetFps !== NORMAL_RENDER_FPS && averageDrawMs < 8) {
          recoveryFrames += 1;
          if (recoveryFrames >= 48) {
            targetFps = NORMAL_RENDER_FPS;
            frameInterval = 1000 / targetFps;
            recoveryFrames = 0;
          }
        } else {
          recoveryFrames = 0;
        }
      }
      canvas.dataset.renderFps = String(targetFps);
      canvas.dataset.drawMs = averageDrawMs.toFixed(1);
      schedule();
    };

    resize();
    if (reducedMotion) tick(performance.now());
    else schedule();

    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(resize) : null;
    const io = typeof IntersectionObserver !== 'undefined'
      ? new IntersectionObserver(([entry]) => {
        inViewport = entry.isIntersecting;
        if (!inViewport && rafRef.current != null) {
          cancelAnimationFrame(rafRef.current);
          rafRef.current = null;
        } else {
          lastTime = performance.now();
          schedule();
        }
      }, { threshold: 0.05 })
      : null;
    const onVisibilityChange = () => {
      if (document.visibilityState !== 'visible' && rafRef.current != null) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      } else {
        lastTime = performance.now();
        schedule();
      }
    };
    const onWindowBlur = () => {
      windowFocused = false;
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    };
    const onWindowFocus = () => {
      windowFocused = true;
      lastTime = performance.now();
      schedule();
    };
    ro?.observe(wrap);
    io?.observe(wrap);
    document.addEventListener('visibilitychange', onVisibilityChange);
    window.addEventListener('blur', onWindowBlur);
    window.addEventListener('focus', onWindowFocus);

    return () => {
      disposed = true;
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
      ro?.disconnect();
      io?.disconnect();
      document.removeEventListener('visibilitychange', onVisibilityChange);
      window.removeEventListener('blur', onWindowBlur);
      window.removeEventListener('focus', onWindowFocus);
    };
  }, [siteGeometryKey, focusName, enterprise, reducedMotion]);

  return (
    <div className="dot-matrix-globe">
      <div ref={wrapRef} className="dot-matrix-globe__canvas-wrap">
        <canvas ref={canvasRef} className="dot-matrix-globe__canvas" aria-hidden />
      </div>
      <div className="dot-matrix-globe__health">
        <b>{fleetHealth == null ? '—' : `${Math.round(Number(fleetHealth) || 0)}%`}</b>
        <span>FLEET HEALTH</span>
      </div>
      {caption ? <p className="dot-matrix-globe__caption">{caption}</p> : null}
    </div>
  );
});

DotMatrixGlobe.displayName = 'DotMatrixGlobe';

export default DotMatrixGlobe;

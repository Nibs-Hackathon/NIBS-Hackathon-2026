/** Lightweight, dependency-free land silhouette for the dashboard globe. */

// 2.5-degree sampling keeps coastlines readable while remaining cheap enough
// for the adaptive 60/30 FPS canvas renderer.
export const EARTH_COLS = 144;
export const EARTH_ROWS = 72;
export const SITE_RADIUS_DEG = 12;

const LAND_POLYGONS = [
  [[-168, 71], [-142, 70], [-126, 58], [-124, 49], [-114, 32], [-99, 18],
    [-82, 24], [-81, 31], [-65, 44], [-53, 49], [-60, 60], [-79, 73], [-110, 76], [-140, 72]],
  [[-105, 24], [-97, 15], [-87, 9], [-77, 7], [-79, 18], [-90, 22]],
  [[-81, 12], [-70, 12], [-52, 5], [-35, -7], [-42, -24], [-54, -35],
    [-63, -56], [-72, -50], [-76, -31], [-81, -5]],
  [[-55, 82], [-21, 80], [-17, 67], [-42, 59], [-61, 66], [-68, 77]],
  [[-11, 36], [-10, 44], [-6, 58], [8, 71], [30, 70], [42, 58],
    [31, 45], [22, 36], [8, 36]],
  [[-18, 36], [4, 37], [24, 32], [40, 12], [51, 10], [43, -12],
    [31, -35], [16, -35], [5, -18], [-9, 4], [-17, 20]],
  [[28, 41], [40, 58], [62, 72], [104, 77], [145, 69], [180, 65],
    [180, 48], [143, 43], [128, 30], [118, 20], [104, 2], [94, 8],
    [80, 7], [68, 24], [52, 28], [42, 40]],
  [[35, 31], [57, 27], [64, 14], [51, 12], [43, 17]],
  [[67, 25], [78, 31], [90, 24], [81, 7], [74, 9]],
  [[96, 23], [108, 20], [105, 4], [115, -8], [103, -7], [98, 7]],
  [[130, 34], [143, 46], [146, 42], [137, 31]],
  [[112, -11], [132, -10], [154, -23], [151, -39], [132, -44], [114, -31]],
  [[46, -13], [51, -16], [49, -27], [44, -25]],
  [[-8, 50], [-3, 59], [2, 57], [1, 51]],
];

function pointInPolygon(lng, lat, polygon) {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i, i += 1) {
    const [xi, yi] = polygon[i];
    const [xj, yj] = polygon[j];
    const intersects = ((yi > lat) !== (yj > lat))
      && (lng < ((xj - xi) * (lat - yi)) / (yj - yi) + xi);
    if (intersects) inside = !inside;
  }
  return inside;
}

export function cellCenter(col, row) {
  return {
    lat: 90 - (row + 0.5) * (180 / EARTH_ROWS),
    lng: -180 + (col + 0.5) * (360 / EARTH_COLS),
  };
}

export function isLand(lat, lng) {
  return LAND_POLYGONS.some((polygon) => pointInPolygon(lng, lat, polygon));
}

export function angularDistanceDeg(lat1, lng1, lat2, lng2) {
  const dlat = lat1 - lat2;
  let dlng = lng1 - lng2;
  while (dlng > 180) dlng -= 360;
  while (dlng < -180) dlng += 360;
  return Math.hypot(dlat, dlng);
}

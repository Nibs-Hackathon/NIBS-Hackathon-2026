/** Trigger a browser download from an API export package. */

export function downloadTextFile(filename, content, mime = 'text/plain;charset=utf-8') {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename || 'rigos-export.txt';
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

export function downloadReportExport(payload) {
  if (!payload) return;
  if (payload.format === 'json' || typeof payload.content === 'object') {
    downloadTextFile(
      payload.filename || 'rigos-report.json',
      JSON.stringify(payload.content ?? payload.report ?? payload, null, 2),
      'application/json;charset=utf-8',
    );
    return;
  }
  downloadTextFile(
    payload.filename || 'rigos-report.md',
    payload.content || payload.markdown || '',
    'text/markdown;charset=utf-8',
  );
}

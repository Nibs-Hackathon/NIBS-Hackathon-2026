const DAY_MS = 86_400_000;

/** Map observed and backend-projected health to one line with a dashed tail. */
export function projectedHealthToChartRows(historical = [], predicted = []) {
  const observedValues = (Array.isArray(historical) ? historical : [])
    .map(Number)
    .filter(Number.isFinite);
  const predictedValues = (Array.isArray(predicted) ? predicted : [])
    .map(Number)
    .filter(Number.isFinite);
  const values = predictedValues.length
    ? [...observedValues, ...predictedValues]
    : observedValues;

  if (values.length < 2) {
    return { chartData: [], projectionStartIndex: null };
  }

  const start = Date.now() - (values.length - 1) * DAY_MS;
  const chartData = values.map((value, index) => ({
    date: new Date(start + index * DAY_MS),
    value,
  }));

  return {
    chartData,
    projectionStartIndex: predictedValues.length
      ? Math.max(0, observedValues.length - 1)
      : null,
  };
}

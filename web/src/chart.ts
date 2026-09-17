import type { ScenarioRow } from './data';
import type { Language } from './i18n';
import { ui } from './i18n';

const NS = 'http://www.w3.org/2000/svg';
const W = 920;
const H = 480;
const M = { left: 72, right: 24, top: 30, bottom: 54 };

interface ChartOptions {
  rows: ScenarioRow[];
  horizon: number;
  showUncertainty: boolean;
  unit: string;
  language: Language;
  label: string;
}

function svgEl<K extends keyof SVGElementTagNameMap>(name: K, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] {
  const element = document.createElementNS(NS, name);
  Object.entries(attrs).forEach(([key, value]) => element.setAttribute(key, String(value)));
  return element;
}

function values(rows: ScenarioRow[], showUncertainty: boolean): number[] {
  const list: number[] = [];
  for (const row of rows) {
    for (const value of [row.observed, row.original_bau, row.original_bau2, row.hybrid_2026]) if (value !== null) list.push(value);
    if (showUncertainty) for (const value of [row.p10, row.p90]) if (value !== null) list.push(value);
  }
  return list;
}

function linePath(rows: ScenarioRow[], accessor: (row: ScenarioRow) => number | null, x: (year: number) => number, y: (value: number) => number): string {
  let path = '';
  let open = false;
  for (const row of rows) {
    const value = accessor(row);
    if (value === null) { open = false; continue; }
    path += `${open ? 'L' : 'M'}${x(row.year).toFixed(2)},${y(value).toFixed(2)} `;
    open = true;
  }
  return path.trim();
}

function formatValue(value: number | null, language: Language): string {
  if (value === null) return '—';
  const abs = Math.abs(value);
  const digits = abs >= 100 ? 1 : abs >= 10 ? 2 : 3;
  return value.toLocaleString(language === 'ro' ? 'ro-RO' : 'en-US', { maximumFractionDigits: digits });
}

export function renderChart(container: HTMLElement, options: ChartOptions): void {
  const t = ui[options.language];
  const rows = options.rows.filter((row) => row.year <= options.horizon);
  container.innerHTML = '';
  if (!rows.length) return;

  const minYear = rows[0]!.year;
  const maxYear = rows[rows.length - 1]!.year;
  const numeric = values(rows, options.showUncertainty);
  const minRaw = Math.min(...numeric);
  const maxRaw = Math.max(...numeric);
  const padding = Math.max((maxRaw - minRaw) * 0.08, Math.abs(maxRaw) * 0.02, 0.01);
  const minValue = minRaw - padding;
  const maxValue = maxRaw + padding;
  const x = (year: number) => M.left + ((year - minYear) / Math.max(1, maxYear - minYear)) * (W - M.left - M.right);
  const y = (value: number) => H - M.bottom - ((value - minValue) / Math.max(1e-12, maxValue - minValue)) * (H - M.top - M.bottom);

  const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', tabindex: '0', 'aria-label': `${options.label}, ${options.unit}. ${t.keyboardHint}` });
  svg.classList.add('trajectory-chart');

  const grid = svgEl('g', { class: 'chart-grid' });
  const yTicks = 5;
  for (let index = 0; index <= yTicks; index++) {
    const value = minValue + (index / yTicks) * (maxValue - minValue);
    const yy = y(value);
    grid.append(svgEl('line', { x1: M.left, x2: W - M.right, y1: yy, y2: yy }));
    const label = svgEl('text', { x: M.left - 10, y: yy + 4, 'text-anchor': 'end' });
    label.textContent = formatValue(value, options.language);
    grid.append(label);
  }
  const xStep = maxYear - minYear > 100 ? 25 : maxYear - minYear > 60 ? 20 : 10;
  for (let year = Math.ceil(minYear / xStep) * xStep; year <= maxYear; year += xStep) {
    const xx = x(year);
    const label = svgEl('text', { x: xx, y: H - 20, 'text-anchor': 'middle' });
    label.textContent = String(year);
    grid.append(label);
  }
  svg.append(grid);

  if (options.showUncertainty) {
    const bandRows = rows.filter((row) => row.p10 !== null && row.p90 !== null);
    if (bandRows.length > 1) {
      const upper = bandRows.map((row) => `${x(row.year).toFixed(2)},${y(row.p90!).toFixed(2)}`);
      const lower = [...bandRows].reverse().map((row) => `${x(row.year).toFixed(2)},${y(row.p10!).toFixed(2)}`);
      svg.append(svgEl('polygon', { points: [...upper, ...lower].join(' '), class: 'uncertainty-band' }));
    }
  }

  const series: Array<[(row: ScenarioRow) => number | null, string]> = [
    [(row) => row.original_bau, 'series-bau'],
    [(row) => row.original_bau2, 'series-bau2'],
    [(row) => row.hybrid_2026, 'series-hybrid'],
  ];
  for (const [accessor, className] of series) {
    svg.append(svgEl('path', { d: linePath(rows, accessor, x, y), class: `series-line ${className}` }));
  }

  const observations = svgEl('g', { class: 'observations' });
  for (const row of rows) {
    if (row.observed === null) continue;
    observations.append(svgEl('circle', { cx: x(row.year), cy: y(row.observed), r: 3.2 }));
  }
  svg.append(observations);

  if (minYear <= 2025 && maxYear >= 2025) {
    const xx = x(2025);
    svg.append(svgEl('line', { x1: xx, x2: xx, y1: M.top, y2: H - M.bottom, class: 'cutoff-line' }));
    const cutoff = svgEl('text', { x: xx + 7, y: M.top + 13, class: 'cutoff-label' });
    cutoff.textContent = t.observedCutoff;
    svg.append(cutoff);
  }

  const guide = svgEl('line', { y1: M.top, y2: H - M.bottom, class: 'hover-guide' });
  guide.style.display = 'none';
  svg.append(guide);

  const tooltip = document.createElement('div');
  tooltip.className = 'chart-tooltip';
  tooltip.hidden = true;
  container.append(svg, tooltip);

  const inspect = (clientX: number) => {
    const rect = svg.getBoundingClientRect();
    const relative = ((clientX - rect.left) / rect.width) * W;
    const year = minYear + ((relative - M.left) / (W - M.left - M.right)) * (maxYear - minYear);
    const row = rows.reduce((best, current) => Math.abs(current.year - year) < Math.abs(best.year - year) ? current : best, rows[0]!);
    const xx = x(row.year);
    guide.setAttribute('x1', String(xx)); guide.setAttribute('x2', String(xx)); guide.style.display = '';
    const screenX = (xx / W) * rect.width;
    tooltip.style.left = `${Math.min(Math.max(screenX, 92), rect.width - 92)}px`;
    tooltip.style.top = '42px';
    tooltip.innerHTML = `<strong>${row.year}</strong><span>${t.observed}: ${formatValue(row.observed, options.language)}</span><span>${t.bau}: ${formatValue(row.original_bau, options.language)}</span><span>${t.bau2}: ${formatValue(row.original_bau2, options.language)}</span><span>${t.hybrid}: ${formatValue(row.hybrid_2026, options.language)}</span>${options.showUncertainty && row.p10 !== null && row.p90 !== null ? `<span>P10–P90: ${formatValue(row.p10, options.language)}–${formatValue(row.p90, options.language)}</span>` : ''}`;
    tooltip.hidden = false;
  };

  svg.addEventListener('pointermove', (event) => inspect(event.clientX));
  svg.addEventListener('pointerleave', () => { guide.style.display = 'none'; tooltip.hidden = true; });
  svg.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    const current = Number(svg.dataset.inspectYear ?? rows.find((row) => row.observed !== null)?.year ?? rows[0]!.year);
    const index = Math.max(0, rows.findIndex((row) => row.year >= current));
    const next = Math.min(rows.length - 1, Math.max(0, index + (event.key === 'ArrowRight' ? 1 : -1)));
    const row = rows[next]!;
    svg.dataset.inspectYear = String(row.year);
    const rect = svg.getBoundingClientRect();
    inspect(rect.left + (x(row.year) / W) * rect.width);
  });
}

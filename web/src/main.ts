import './style.css';
import { dashboardOrder, indicatorOrder, indicators, type IndicatorKey } from './catalog';
import { findDiagnostic, latestObserved, loadAppData, rowAt, type AppData, type DiagnosticRow } from './data';
import { renderChart } from './chart';
import { ui, type Language } from './i18n';

interface State {
  language: Language;
  indicator: IndicatorKey;
  horizon: number;
  uncertainty: boolean;
}

const app = document.querySelector<HTMLDivElement>('#app')!;
let data: AppData | null = null;
let state: State = readState();

function readState(): State {
  const query = new URLSearchParams(location.search);
  const indicator = query.get('indicator') as IndicatorKey | null;
  const horizon = Number(query.get('horizon'));
  return {
    language: query.get('lang') === 'ro' ? 'ro' : 'en',
    indicator: indicator && indicatorOrder.includes(indicator) ? indicator : 'population',
    horizon: [2035, 2050, 2100].includes(horizon) ? horizon : 2050,
    uncertainty: query.get('uncertainty') !== '0',
  };
}

function syncUrl(): void {
  const query = new URLSearchParams();
  if (state.language === 'ro') query.set('lang', 'ro');
  if (state.indicator !== 'population') query.set('indicator', state.indicator);
  if (state.horizon !== 2050) query.set('horizon', String(state.horizon));
  if (!state.uncertainty) query.set('uncertainty', '0');
  history.replaceState(null, '', `${location.pathname}${query.size ? `?${query}` : ''}${location.hash}`);
}

function fmt(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—';
  return value.toLocaleString(state.language === 'ro' ? 'ro-RO' : 'en-US', { maximumFractionDigits: digits });
}

function pct(value: string | undefined): string {
  const number = Number(value);
  return Number.isFinite(number) ? `${number.toLocaleString(state.language === 'ro' ? 'ro-RO' : 'en-US', { maximumFractionDigits: 2 })}%` : '—';
}

function roleLabel(role: string): string {
  const labels: Record<string, [string, string]> = { observed: ['observed', 'observat'], derived_observed_diagnostic: ['derived diagnostic', 'diagnostic derivat'], latent: ['latent', 'latent'] };
  const pair = labels[role];
  return pair ? pair[state.language === 'ro' ? 1 : 0] : role.replaceAll('_', ' ');
}

function diagnosticMetric(row: DiagnosticRow | undefined, key: string): string {
  return row ? pct(row[key]) : '—';
}

function renderShell(): void {
  const t = ui[state.language];
  document.documentElement.lang = state.language;
  app.innerHTML = `
    <header class="suite-header">
      <div class="brand">
        <img src="./world3.svg" alt="" class="brand-icon" />
        <div><h1>World3 Empirical</h1><p>${t.subtitle}</p></div>
      </div>
      <div class="header-meta" id="header-meta"></div>
      <div class="language-switch" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-pressed="${state.language === 'en'}">EN</button>
        <button type="button" data-lang="ro" aria-pressed="${state.language === 'ro'}">RO</button>
      </div>
    </header>
    <main id="workspace" class="workspace" tabindex="-1">
      <section class="panel model-panel" aria-labelledby="model-heading">
        <div class="panel-heading"><div><p class="eyebrow">01</p><h2 id="model-heading">${t.modelPanel}</h2></div><span class="status-chip">BAU · BAU2 · Hybrid 2026</span></div>
        <div class="controls">
          <label><span>${t.indicator}</span><select id="indicator-select"></select></label>
          <label><span>${t.horizon}</span><select id="horizon-select"><option>2035</option><option>2050</option><option>2100</option></select></label>
          <label class="check-control"><input id="uncertainty-toggle" type="checkbox" ${state.uncertainty ? 'checked' : ''}/><span>${t.uncertainty}</span></label>
        </div>
        <div class="legend" aria-label="Chart legend"><span class="legend-dot observed"></span>${t.observed}<span class="legend-line bau"></span>${t.bau}<span class="legend-line bau2"></span>${t.bau2}<span class="legend-line hybrid"></span>${t.hybrid}</div>
        <div id="chart-wrap" class="chart-wrap"></div>
        <p class="unit-line" id="unit-line"></p>
      </section>
      <section class="panel theory-panel" aria-labelledby="theory-heading">
        <div class="panel-heading"><div><p class="eyebrow">02</p><h2 id="theory-heading">${t.theoryPanel}</h2></div></div>
        <div id="theory-content"></div>
      </section>
      <section class="panel dashboard-panel" aria-labelledby="dashboard-heading">
        <div class="panel-heading"><div><p class="eyebrow">03</p><h2 id="dashboard-heading">${t.dashboardPanel}</h2></div></div>
        <p class="panel-intro">${t.dashboardHelp}</p>
        <div id="dashboard-grid" class="dashboard-grid"></div>
      </section>
      <section class="panel evidence-panel" aria-labelledby="evidence-heading">
        <div class="panel-heading"><div><p class="eyebrow">04</p><h2 id="evidence-heading">${t.evidencePanel}</h2></div></div>
        <div id="evidence-content"></div>
      </section>
    </main>
    <footer><span>InfoClar Model Suite Design Standard v1.1</span><span id="data-integrity"></span></footer>`;

  const select = document.querySelector<HTMLSelectElement>('#indicator-select')!;
  for (const key of indicatorOrder) {
    const option = document.createElement('option'); option.value = key; option.textContent = indicators[key].label[state.language]; option.selected = key === state.indicator; select.append(option);
  }
  document.querySelector<HTMLSelectElement>('#horizon-select')!.value = String(state.horizon);

  document.querySelectorAll<HTMLButtonElement>('[data-lang]').forEach((button) => button.addEventListener('click', () => {
    state.language = button.dataset.lang as Language; syncUrl(); render();
  }));
  select.addEventListener('change', () => { state.indicator = select.value as IndicatorKey; syncUrl(); renderDynamic(); });
  document.querySelector<HTMLSelectElement>('#horizon-select')!.addEventListener('change', (event) => { state.horizon = Number((event.target as HTMLSelectElement).value); syncUrl(); renderDynamic(); });
  document.querySelector<HTMLInputElement>('#uncertainty-toggle')!.addEventListener('change', (event) => { state.uncertainty = (event.target as HTMLInputElement).checked; syncUrl(); renderDynamic(); });
}

function renderDynamic(): void {
  if (!data) return;
  const t = ui[state.language];
  const meta = indicators[state.indicator];
  const rows = data.scenarios[state.indicator];
  const chartWrap = document.querySelector<HTMLElement>('#chart-wrap')!;
  renderChart(chartWrap, { rows, horizon: state.horizon, showUncertainty: state.uncertainty, unit: meta.unit[state.language], language: state.language, label: meta.label[state.language] });
  document.querySelector<HTMLElement>('#unit-line')!.textContent = `${meta.label[state.language]} · ${meta.unit[state.language]}`;

  document.querySelector<HTMLElement>('#header-meta')!.innerHTML = `<span>${t.appVersion} 1.0.0</span><span>${t.modelVersion} ${data.schema.model_version}</span><span>${t.dataSnapshot} ${data.schema.data_snapshot}</span>`;
  document.querySelector<HTMLElement>('#data-integrity')!.textContent = `${Object.keys(data.hashes).length} ${t.copiedData}`;

  const structure = data.structure;
  const candidates = structure.candidate_interfaces.map((candidate) => `<li><strong>${candidate.id.replaceAll('_', ' ')}</strong><span>${candidate.active_by_default ? t.central : t.inactive} · ${candidate.central ? t.central : t.nonCentral}</span></li>`).join('');
  document.querySelector<HTMLElement>('#theory-content')!.innerHTML = `
    <h3>${meta.label[state.language]}</h3><p>${meta.theory[state.language]}</p>
    <div class="learn-block"><h4>${t.stockFlowRole}</h4><p>${meta.role[state.language]}</p></div>
    <div class="learn-block boundary"><h4>${t.boundary}</h4><p>${meta.interpretationBoundary[state.language]}</p></div>
    <details><summary>${t.structure}</summary>
      <dl class="compact-dl"><div><dt>${t.referenceCore}</dt><dd>${structure.architecture.reference_model.name} · ${structure.modules.length} modules · ${t.immutableEquations}</dd></div><div><dt>${t.gates}</dt><dd>${structure.promotion_gates.map((gate) => gate.id).join('–')}</dd></div></dl>
      <h4>${t.candidates}</h4><ul class="candidate-list">${candidates}</ul>
    </details>`;

  const dashboard = dashboardOrder.map((key) => {
    const cardMeta = indicators[key]; const cardRows = data!.scenarios[key]; const year2035 = rowAt(cardRows, 2035); const latest = latestObserved(cardRows);
    const range = year2035?.p10 !== null && year2035?.p90 !== null ? `${fmt(year2035?.p10)}–${fmt(year2035?.p90)}` : '—';
    return `<article class="kpi-card"><h3>${cardMeta.shortLabel[state.language]}</h3><div class="kpi-primary">${fmt(year2035?.hybrid_2026)}</div><p>${t.value2035} · ${cardMeta.unit[state.language]}</p><dl><div><dt>${t.latestObserved}</dt><dd>${latest ? `${fmt(latest.observed)} <small>${latest.year}</small>` : t.noObservation}</dd></div><div><dt>${t.sensitivity2035}</dt><dd>${range}</dd></div></dl></article>`;
  }).join('');
  document.querySelector<HTMLElement>('#dashboard-grid')!.innerHTML = dashboard;

  const backtest = findDiagnostic(data.backtest, state.indicator);
  const multi = findDiagnostic(data.multiOrigin, state.indicator);
  const fit = findDiagnostic(data.fit, state.indicator);
  const role = data.schema.indicator_files[`${state.indicator}.csv`] ?? '—';
  document.querySelector<HTMLElement>('#evidence-content')!.innerHTML = `
    <div class="evidence-source"><span class="role-chip">${roleLabel(role)}</span><h3>${t.provenance}</h3><p>${meta.status[state.language]}</p><a href="${meta.sourceUrl}" target="_blank" rel="noreferrer">${meta.source[state.language]} ↗</a></div>
    <div class="validation-grid">
      <article><h4>${t.frozenBacktest}</h4><dl><div><dt>${t.hybridMape}</dt><dd>${diagnosticMetric(backtest, 'bau2_e2026_mape_pct')}</dd></div><div><dt>${t.referenceMape}</dt><dd>${diagnosticMetric(backtest, 'bau2_level_anchored_mape_pct')}</dd></div><div><dt>${t.improvement}</dt><dd>${diagnosticMetric(backtest, 'improvement_pct')}</dd></div></dl></article>
      <article><h4>${t.multiOrigin}</h4><dl><div><dt>${t.origins}</dt><dd>${multi?.origins ?? '—'}</dd></div><div><dt>${t.hybridMape}</dt><dd>${diagnosticMetric(multi, 'bau2_e2026_mape_pct')}</dd></div><div><dt>${t.improvement}</dt><dd>${diagnosticMetric(multi, 'improvement_pct')}</dd></div></dl></article>
      <article><h4>${t.descriptiveFit}</h4><dl><div><dt>${t.historicalMape}</dt><dd>${diagnosticMetric(fit, 'historical_mape_pct')}</dd></div><div><dt>${t.bias}</dt><dd>${diagnosticMetric(fit, 'historical_bias_pct')}</dd></div><div><dt>n</dt><dd>${fit?.n ?? '—'}</dd></div></dl></article>
    </div>
    <div class="limits"><h3>${t.limitations}</h3><p>${t.centralCurvesNote}</p><p>${t.structuralSensitivityNote}</p><p>${t.latentNote}</p><p>${t.inactiveNote}</p></div>`;

  const select = document.querySelector<HTMLSelectElement>('#indicator-select');
  if (select) select.value = state.indicator;
}

function render(): void {
  renderShell();
  if (data) renderDynamic(); else document.querySelector<HTMLElement>('#chart-wrap')!.innerHTML = `<div class="loading">${ui[state.language].loading}</div>`;
}

render();
loadAppData(indicatorOrder).then((loaded) => { data = loaded; render(); }).catch((error: unknown) => {
  console.error(error);
  document.querySelector<HTMLElement>('#chart-wrap')!.innerHTML = `<div class="error"><strong>${ui[state.language].error}</strong><span>${error instanceof Error ? error.message : String(error)}</span></div>`;
});

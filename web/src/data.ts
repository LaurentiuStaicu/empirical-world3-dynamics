import type { IndicatorKey } from './catalog';

export interface ScenarioRow {
  year: number;
  observed: number | null;
  original_bau: number | null;
  original_bau2: number | null;
  hybrid_2026: number | null;
  p10: number | null;
  p90: number | null;
  benchmark: number | null;
}

export interface DiagnosticRow { [key: string]: string; }

export interface ScenarioSchema {
  app_release: string;
  model_version: string;
  data_snapshot: string;
  indicator_files: Record<string, string>;
  semantic_contract: Record<string, string>;
}

export interface StructuralContract {
  contract_version: string;
  architecture: {
    reference_core_mutable: boolean;
    reference_model: { name: string; source: string; equation_policy: string };
    comparison_baselines: Array<{ id: string; status: string }>;
  };
  modules: Array<{ id: string; role: string; variables: Array<{ id: string; kind: string; unit: string; evidence_role: string }> }>;
  candidate_interfaces: Array<{ id: string; active_by_default: boolean; central: boolean; evidence_role: string; maturity: string }>;
  promotion_gates: Array<{ id: string; name: string; class: string }>;
}

export interface AppData {
  scenarios: Record<IndicatorKey, ScenarioRow[]>;
  schema: ScenarioSchema;
  structure: StructuralContract;
  backtest: DiagnosticRow[];
  multiOrigin: DiagnosticRow[];
  fit: DiagnosticRow[];
  hashes: Record<string, string>;
}

const requiredColumns = ['year', 'observed', 'original_bau', 'original_bau2', 'hybrid_2026', 'p10', 'p90', 'benchmark'];

function parseCsv(text: string): DiagnosticRow[] {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (!lines.length) return [];
  const headers = lines[0]!.split(',');
  return lines.slice(1).map((line) => {
    const cells = line.split(',');
    return Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? '']));
  });
}

function numberOrNull(value: string | undefined): number | null {
  if (value === undefined || value === '') return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function parseScenario(text: string): ScenarioRow[] {
  const rows = parseCsv(text);
  if (!rows.length) throw new Error('Indicator file is empty');
  for (const column of requiredColumns) {
    if (!(column in rows[0]!)) throw new Error(`Missing required indicator column: ${column}`);
  }
  return rows.map((row) => ({
    year: Number(row.year),
    observed: numberOrNull(row.observed),
    original_bau: numberOrNull(row.original_bau),
    original_bau2: numberOrNull(row.original_bau2),
    hybrid_2026: numberOrNull(row.hybrid_2026),
    p10: numberOrNull(row.p10),
    p90: numberOrNull(row.p90),
    benchmark: numberOrNull(row.benchmark),
  })).filter((row) => Number.isFinite(row.year));
}

async function fetchText(path: string): Promise<string> {
  const response = await fetch(path, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.text();
}

async function fetchJson<T>(path: string): Promise<T> {
  return JSON.parse(await fetchText(path)) as T;
}

export async function loadAppData(keys: IndicatorKey[]): Promise<AppData> {
  const base = './data';
  const scenarioEntries = await Promise.all(keys.map(async (key) => [key, parseScenario(await fetchText(`${base}/${key}.csv`))] as const));
  const [schema, structure, backtestText, multiText, fitText, hashes] = await Promise.all([
    fetchJson<ScenarioSchema>(`${base}/scenario_schema.json`),
    fetchJson<StructuralContract>(`${base}/real_model_structure.json`),
    fetchText(`${base}/backtest_2019_latest.csv`),
    fetchText(`${base}/backtest_multi_origin.csv`),
    fetchText(`${base}/fit_diagnostics.csv`),
    fetchJson<Record<string, string>>(`${base}/source-hashes.json`),
  ]);
  return {
    scenarios: Object.fromEntries(scenarioEntries) as Record<IndicatorKey, ScenarioRow[]>,
    schema,
    structure,
    backtest: parseCsv(backtestText),
    multiOrigin: parseCsv(multiText),
    fit: parseCsv(fitText),
    hashes,
  };
}

export function findDiagnostic(rows: DiagnosticRow[], key: IndicatorKey): DiagnosticRow | undefined {
  return rows.find((row) => row.key === key);
}

export function latestObserved(rows: ScenarioRow[]): ScenarioRow | undefined {
  return [...rows].reverse().find((row) => row.observed !== null);
}

export function rowAt(rows: ScenarioRow[], year: number): ScenarioRow | undefined {
  return rows.find((row) => row.year === year);
}

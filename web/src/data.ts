export type IndicatorKey = 'population'|'industry_per_capita'|'food_per_capita'|'pollution_pressure'|'human_welfare'|'industry_total'|'persistent_pollution_stock'|'resources_remaining_pct';
export type ScenarioKey = 'original_bau'|'original_bau2'|'hybrid_2026';

export interface ScenarioRow {
  year:number;
  observed:number|null;
  original_bau:number|null;
  original_bau2:number|null;
  hybrid_2026:number|null;
  p10:number|null;
  p90:number|null;
  benchmark:number|null;
}
export interface DiagnosticRow { [key:string]:string; }
export interface ScenarioSchema { app_release:string; model_version:string; data_snapshot:string; indicator_files:Record<string,string>; semantic_contract:Record<string,string>; }
export interface StructuralContract { contract_version:string; architecture:{reference_core_mutable:boolean; reference_model:{name:string;source:string;equation_policy:string};comparison_baselines:Array<{id:string;status:string}>}; modules:Array<{id:string;role:string;variables:Array<{id:string;kind:string;unit:string;evidence_role:string}>}>; candidate_interfaces:Array<{id:string;active_by_default:boolean;central:boolean;evidence_role:string;maturity:string;forbidden_couplings?:string[]}>; promotion_gates:Array<{id:string;name:string;class:string}>; }
export interface HybridParameterBound { model_name:string; baseline:number; lower:number; upper:number; }
export interface HybridManifest {
  model:string;
  version:string;
  scientific_status:string;
  generated_on:string;
  structural_model:string;
  method:string;
  candidate_count:number;
  selection_cutoff:number;
  production_fit_cutoff:number;
  central_candidate_id:number;
  ensemble_candidate_ids:number[];
  central_selection_rule:string;
  central_parameters:Record<string,number>;
  parameter_bounds:Record<string,HybridParameterBound>;
  weakly_identified_parameters:string[];
  observation_scales:Record<string,number>;
  observation_bridges:Record<string,unknown>;
  uncertainty:string;
  band_definition:string;
  plausibility_guardrails:Record<string,string>;
  validation:string;
  diagnostics:string;
  important_limit:string;
}
export interface AppData {
  scenarios:Record<IndicatorKey,ScenarioRow[]>;
  schema:ScenarioSchema;
  structure:StructuralContract;
  hybridManifest:HybridManifest;
  backtest:DiagnosticRow[];
  multiOrigin:DiagnosticRow[];
  fit:DiagnosticRow[];
  hashes:Record<string,string>;
}

const requiredColumns=['year','observed','original_bau','original_bau2','hybrid_2026','p10','p90','benchmark'];
function parseCsv(text:string):DiagnosticRow[]{
  const lines=text.trim().split(/\r?\n/).filter(Boolean);
  if(!lines.length)return[];
  const headers=lines[0]!.split(',');
  return lines.slice(1).map(line=>{
    const cells=line.split(',');
    return Object.fromEntries(headers.map((h,i)=>[h,cells[i]??'']));
  });
}
function numberOrNull(value:string|undefined):number|null{
  if(value===undefined||value==='')return null;
  const n=Number(value);
  return Number.isFinite(n)?n:null;
}
function parseScenario(text:string):ScenarioRow[]{
  const rows=parseCsv(text);
  if(!rows.length)throw new Error('Indicator file is empty');
  for(const col of requiredColumns)if(!(col in rows[0]!))throw new Error(`Missing required indicator column: ${col}`);
  return rows.map(row=>({
    year:Number(row.year),
    observed:numberOrNull(row.observed),
    original_bau:numberOrNull(row.original_bau),
    original_bau2:numberOrNull(row.original_bau2),
    hybrid_2026:numberOrNull(row.hybrid_2026),
    p10:numberOrNull(row.p10),
    p90:numberOrNull(row.p90),
    benchmark:numberOrNull(row.benchmark),
  })).filter(row=>Number.isFinite(row.year));
}
async function fetchText(path:string){
  const response=await fetch(path,{cache:'no-cache'});
  if(!response.ok)throw new Error(`${path}: HTTP ${response.status}`);
  return response.text();
}
async function fetchJson<T>(path:string):Promise<T>{return JSON.parse(await fetchText(path)) as T;}

export async function loadAppData(keys:IndicatorKey[]):Promise<AppData>{
  const base='./data';
  const entries=await Promise.all(keys.map(async key=>[key,parseScenario(await fetchText(`${base}/${key}.csv`))] as const));
  const [schema,structure,hybridManifest,backtestText,multiText,fitText,hashes]=await Promise.all([
    fetchJson<ScenarioSchema>(`${base}/scenario_schema.json`),
    fetchJson<StructuralContract>(`${base}/real_model_structure.json`),
    fetchJson<HybridManifest>(`${base}/bau_hybrid_2026_manifest.json`),
    fetchText(`${base}/backtest_2019_latest.csv`),
    fetchText(`${base}/backtest_multi_origin.csv`),
    fetchText(`${base}/fit_diagnostics.csv`),
    fetchJson<Record<string,string>>(`${base}/source-hashes.json`),
  ]);
  return {
    scenarios:Object.fromEntries(entries) as Record<IndicatorKey,ScenarioRow[]>,
    schema,structure,hybridManifest,
    backtest:parseCsv(backtestText),
    multiOrigin:parseCsv(multiText),
    fit:parseCsv(fitText),
    hashes,
  };
}
export function latestObserved(rows:ScenarioRow[]):ScenarioRow|undefined{return [...rows].reverse().find(row=>row.observed!==null);}
export function findDiagnostic(rows:DiagnosticRow[],key:IndicatorKey):DiagnosticRow|undefined{return rows.find(row=>row.key===key);}

import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here=dirname(fileURLToPath(import.meta.url));
const root=resolve(here,'..','..');
const copied=resolve(root,'web','public','data');
const hashes=JSON.parse(await readFile(resolve(copied,'source-hashes.json'),'utf8'));
const scenarios=resolve(root,'data','scenarios');
for(const[file,expected]of Object.entries(hashes)){
  const source=file==='real_model_structure.json'?resolve(root,'science','configs',file):resolve(scenarios,file);
  const target=resolve(copied,file);
  const[sourceBytes,targetBytes]=await Promise.all([readFile(source),readFile(target)]);
  const sourceHash=createHash('sha256').update(sourceBytes).digest('hex');
  const targetHash=createHash('sha256').update(targetBytes).digest('hex');
  if(sourceHash!==expected||targetHash!==expected)throw new Error(`Web scientific artifact diverged from source: ${file}`);
}

const schema=JSON.parse(await readFile(resolve(scenarios,'scenario_schema.json'),'utf8'));
for(const key of ['year','observed','original_bau','original_bau2','hybrid_2026','p10','p90','benchmark'])if(!schema.indicator_required_columns.includes(key))throw new Error(`Scenario schema missing required web column: ${key}`);
if(schema.semantic_contract.p10?.includes('confidence')||schema.semantic_contract.p90?.includes('confidence'))throw new Error('P10/P90 must remain sensitivity, not confidence intervals.');

const structure=JSON.parse(await readFile(resolve(root,'science','configs','real_model_structure.json'),'utf8'));
if(structure.architecture.reference_core_mutable!==false)throw new Error('World3 reference core must remain immutable.');
const baselines=structure.architecture.comparison_baselines.map(item=>item.id);
for(const baseline of ['bau','bau2','bau_hybrid_2026'])if(!baselines.includes(baseline))throw new Error(`Missing comparison baseline: ${baseline}`);
for(const candidate of structure.candidate_interfaces)if(candidate.active_by_default!==false||candidate.central!==false)throw new Error(`Candidate must remain inactive and non-central: ${candidate.id}`);
const gateIds=structure.promotion_gates.map(g=>g.id).join(',');
if(gateIds!=='S1,S2,S3,S4,S5,S6,S7,S8,S9,S10')throw new Error(`Promotion gates must remain S1-S10, got ${gateIds}`);
const netEnergy=structure.candidate_interfaces.find(c=>c.id==='net_energy');
if(!netEnergy?.forbidden_couplings?.includes('world3_resource_fraction_to_fossil_eroi'))throw new Error('Rejected resource-fraction → fossil-EROI coupling must remain forbidden.');

const manifest=JSON.parse(await readFile(resolve(scenarios,'bau_hybrid_2026_manifest.json'),'utf8'));
if(manifest.structural_model!=='official World3-03 scenario 2 (BAU2)')throw new Error('Hybrid structural basis changed unexpectedly.');
if(manifest.candidate_count!==128||manifest.ensemble_candidate_ids?.length!==12)throw new Error('Hybrid candidate/ensemble provenance changed unexpectedly.');
if(!String(manifest.uncertainty).includes('not a calibrated probability interval'))throw new Error('Hybrid uncertainty semantics weakened.');
if(!String(manifest.band_definition).includes('pointwise'))throw new Error('Hybrid P10/P90 band must remain pointwise.');

const product=JSON.parse(await readFile(resolve(root,'web','public','product-recovery-contract.json'),'utf8'));
if(product.scientific_non_regression.energy_direct_emissions_verdict!=='RETAIN AS DIAGNOSTIC')throw new Error('Direct-emissions diagnostic verdict changed.');
if(product.metrics.scenario_alignment.interpretation!=='descriptive empirical alignment only')throw new Error('Scenario alignment semantics drifted.');
if(product.metrics.event_timing_sensitivity.pointwise_p10_p90_event_timing!=='not permitted')throw new Error('Pointwise P10/P90 must not become event-time uncertainty.');
if(product.intervention_gate.numeric_intervention_results_currently_enabled!==false)throw new Error('Unvalidated intervention runner must remain disabled.');
if(product.metrics.systemic_deterioration_window.primary_quorum!==3||product.metrics.systemic_deterioration_window.primary_clustering_window_years!==15)throw new Error('Preregistered systemic-deterioration definition changed.');
if(product.metrics.systemic_collapse_window.primary_quorum!==3||product.metrics.systemic_collapse_window.primary_clustering_window_years!==20)throw new Error('Preregistered systemic-collapse definition changed.');
if(product.p10_p90_audit.candidate_count!==128||product.p10_p90_audit.production_ensemble_size!==12||product.p10_p90_audit.sampling_seed!==20260829)throw new Error('P10/P90 audit provenance incomplete.');
if(product.p10_p90_audit.varied_parameters.length!==7)throw new Error('P10/P90 varied-parameter audit must list seven parameters.');
if(!product.p10_p90_audit.public_label_en.startsWith('Show model sensitivity range'))throw new Error('User-facing sensitivity label regressed.');

const manual=JSON.parse(await readFile(resolve(root,'web','public','theory-manual.json'),'utf8'));
const required=['club-of-rome','forrester-system-dynamics','authors-1972','world3-structure','stocks-flows-feedbacks','five-domains','overshoot-collapse','bau-bau2','comprehensive-technology','stabilized-world','editions-1972-1992-2004','turner','herrington','empirical-comparisons','nebel-recalibration','bau-hybrid-2026','observations-calibration-backtesting','scenario-forecast-probability','uncertainty-sensitivity','interventions-resilience','limits'];
for(const id of required)if(!manual.chapters.some(c=>c.id===id))throw new Error(`Theory manual missing chapter: ${id}`);
for(const chapter of manual.chapters){
  if(!chapter.title?.en||!chapter.title?.ro||!chapter.summary?.en||!chapter.summary?.ro||!chapter.paragraphs?.en?.length||!chapter.paragraphs?.ro?.length)throw new Error(`Theory chapter incomplete EN/RO: ${chapter.id}`);
  if(!chapter.sources?.length)throw new Error(`Theory chapter has no source: ${chapter.id}`);
}
const manualText=JSON.stringify(manual);
for(const requiredTerm of ['Nebel','corrigendum','BAU Hybrid 2026','Latin Hypercube','scenario'])if(!manualText.includes(requiredTerm))throw new Error(`Theory manual missing audited concept: ${requiredTerm}`);

console.log('World3 final product-recovery scientific, sensitivity and semantic contract verified.');

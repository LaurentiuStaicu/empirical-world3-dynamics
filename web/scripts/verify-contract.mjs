import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..', '..');
const copied = resolve(root, 'web', 'public', 'data');
const hashes = JSON.parse(await readFile(resolve(copied, 'source-hashes.json'), 'utf8'));
const scenarios = resolve(root, 'data', 'scenarios');

for (const [file, expected] of Object.entries(hashes)) {
  const source = file === 'real_model_structure.json' ? resolve(root, 'science', 'configs', file) : resolve(scenarios, file);
  const target = resolve(copied, file);
  const [sourceBytes, targetBytes] = await Promise.all([readFile(source), readFile(target)]);
  const sourceHash = createHash('sha256').update(sourceBytes).digest('hex');
  const targetHash = createHash('sha256').update(targetBytes).digest('hex');
  if (sourceHash !== expected || targetHash !== expected) throw new Error(`Web scientific artifact diverged from source: ${file}`);
}

const schema = JSON.parse(await readFile(resolve(scenarios, 'scenario_schema.json'), 'utf8'));
for (const key of ['year', 'observed', 'original_bau', 'original_bau2', 'hybrid_2026', 'p10', 'p90', 'benchmark']) {
  if (!schema.indicator_required_columns.includes(key)) throw new Error(`Scenario schema missing required web column: ${key}`);
}
if (schema.semantic_contract.p10?.includes('confidence') || schema.semantic_contract.p90?.includes('confidence')) throw new Error('P10/P90 must remain structural sensitivity, not confidence intervals.');

const structure = JSON.parse(await readFile(resolve(root, 'science', 'configs', 'real_model_structure.json'), 'utf8'));
if (structure.architecture.reference_core_mutable !== false) throw new Error('World3 reference core must remain immutable.');
const baselines = structure.architecture.comparison_baselines.map((item) => item.id);
for (const baseline of ['bau', 'bau2', 'bau_hybrid_2026']) if (!baselines.includes(baseline)) throw new Error(`Missing comparison baseline: ${baseline}`);
for (const candidate of structure.candidate_interfaces) {
  if (candidate.active_by_default !== false || candidate.central !== false) throw new Error(`Candidate must remain inactive and non-central: ${candidate.id}`);
}
const gateIds = structure.promotion_gates.map((gate) => gate.id).join(',');
if (gateIds !== 'S1,S2,S3,S4,S5,S6,S7,S8,S9,S10') throw new Error(`Promotion gates must remain S1-S10, got ${gateIds}`);
const netEnergy = structure.candidate_interfaces.find((candidate) => candidate.id === 'net_energy');
if (!netEnergy?.forbidden_couplings?.includes('world3_resource_fraction_to_fossil_eroi')) throw new Error('Rejected resource-fraction → fossil-EROI coupling must remain forbidden.');
console.log('Web v1 scientific non-regression contract verified.');

import { createHash } from 'node:crypto';
import { copyFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..', '..');
const destination = resolve(root, 'web', 'public', 'data');
const scenarioRoot = resolve(root, 'data', 'scenarios');
const files = [
  'population.csv', 'industry_per_capita.csv', 'food_per_capita.csv', 'pollution_pressure.csv',
  'human_welfare.csv', 'industry_total.csv', 'persistent_pollution_stock.csv', 'resources_remaining_pct.csv',
  'scenario_schema.json', 'backtest_2019_latest.csv', 'backtest_multi_origin.csv', 'fit_diagnostics.csv',
  'bau_hybrid_2026_manifest.json', 'bridge_validation.csv', 'lookup_extrapolation_audit.csv',
];

await rm(destination, { recursive: true, force: true });
await mkdir(destination, { recursive: true });
const hashes = {};
for (const file of files) {
  const source = resolve(scenarioRoot, file);
  const target = resolve(destination, file);
  const content = await readFile(source);
  hashes[file] = createHash('sha256').update(content).digest('hex');
  await copyFile(source, target);
}
const structureSource = resolve(root, 'science', 'configs', 'real_model_structure.json');
const structureContent = await readFile(structureSource);
hashes['real_model_structure.json'] = createHash('sha256').update(structureContent).digest('hex');
await copyFile(structureSource, resolve(destination, 'real_model_structure.json'));
await writeFile(resolve(destination, 'source-hashes.json'), `${JSON.stringify(hashes, null, 2)}\n`);
await mkdir(resolve(root, 'web', 'public'), { recursive: true });
await copyFile(resolve(root, 'data', 'icons', 'io.github.laurentiustaicu.World3Empirical.svg'), resolve(root, 'web', 'public', 'world3.svg'));
console.log(`Synced ${Object.keys(hashes).length} validated scientific artifacts into web/public.`);

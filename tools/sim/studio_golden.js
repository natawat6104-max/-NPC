// Run Star Studio's simulate() under node with the default world, to get golden logs for the Godot port.
const fs = require('fs');
const h = fs.readFileSync(process.argv[2], 'utf8').split(String.fromCharCode(13)).join('');
const seg = (start, end) => { const a = h.indexOf(start); const b = h.indexOf(end, a); if (a < 0 || b < 0) throw new Error('missing ' + start); return h.slice(a, b); };
const line = (start) => { const a = h.indexOf(start); if (a < 0) throw new Error('missing ' + start); return h.slice(a, h.indexOf('\n', a)); };
const fnBlock = (name) => { const a = h.indexOf('function ' + name + '('); const b = h.indexOf('\n}\n', a); return h.slice(a, b + 3); };
let code = '';
code += seg('const DEFAULT = {', '\nconst clone =') + '\n';
code += 'const clone = (o) => JSON.parse(JSON.stringify(o));\nlet S = clone(DEFAULT);\n';
for (const k of ['const ADVENTURER_ROLES', 'const RISK_BONUS', 'const clamp', 'const byId']) code += line(k) + '\n';
for (const k of ['function partyPower(', 'function monsterPower(', 'function priceIndex(', 'function fillTemplate(', 'function mulberry32(']) {
  const s = line(k); code += (s.trim().endsWith('}') ? s : fnBlock(k.slice(9, -1))) + '\n';
}
code += fnBlock('decide') + fnBlock('simulate');
code += `
const runs = [[1234, 30, 'warn', true], [1234, 30, 'warn', false], [7, 60, 'death', true], [42, 45, 'death', false], [99, 120, 'warn', true]];
const out = runs.map(([seed, days, death, omen]) => ({ seed, days, death, omen, result: simulate({ seed, days, death, omen }) }));
module.exports = { out, balance: S.balance };
`;
const tmp = process.argv[3] + '/studio_sim.js';
fs.writeFileSync(tmp, code);
const { out, balance } = require(tmp);
fs.writeFileSync(process.argv[4], JSON.stringify({ _about: 'Star Studio simulate() output for these options (tests/run_tests.gd checks the Godot port against it)', studio_balance: balance, runs: out }, null, 1) + '\n');
for (const r of out) console.log(r.seed, r.days, r.death, r.omen, 'log', r.result.log.length, JSON.stringify(r.result.stats));

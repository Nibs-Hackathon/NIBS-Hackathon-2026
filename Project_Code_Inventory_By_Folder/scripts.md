# Folder: scripts Code Inventory

Generated: 2026-07-24T03:28:50 UTC

Contains 12 project files.

## scripts/benchmark.py

**File path:** `scripts/benchmark.py`

```python

```

## scripts/build_knowledge.py

**File path:** `scripts/build_knowledge.py`

```python
"""Build the Neon/pgvector knowledge index used by the Streamlit UI."""

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(
        str(ROOT_DIR)
    )


from rag.ingestion import KnowledgeIngestion


def parse_args():
    parser = argparse.ArgumentParser(
        description="Index PDF knowledge documents into the configured Neon database."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=ROOT_DIR / "docs",
        help="Directory containing PDF source documents (default: ./docs).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing knowledge chunks before indexing. Use for a clean rebuild.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        raise SystemExit(f"Documents directory does not exist: {docs_dir}")

    engine = KnowledgeIngestion()
    if args.replace:
        deleted = engine.vector_store.clear()
        print(f"Removed {deleted} existing knowledge chunk(s).")

    count = engine.ingest_folder(docs_dir)
    total = engine.vector_store.count()
    print(f"Indexed {count} chunk(s). Neon now contains {total} searchable chunk(s).")


if __name__ == "__main__":
    main()
```

## scripts/build_project_code_inventory.js

**File path:** `scripts/build_project_code_inventory.js`

````javascript
/* Builds a portable Markdown and DOCX inventory of the repository's text source. */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const root = path.resolve(__dirname, '..');
const outputMd = path.join(root, 'Project_Code_Inventory_Updated.md');
const outputDocx = path.join(root, 'Project_Code_Inventory_Updated.docx');
const outputByFolder = path.join(root, 'Project_Code_Inventory_By_Folder');
const allowed = new Set(['.py', '.md', '.txt', '.ini', '.mako', '.yml', '.yaml', '.json', '.toml']);
const skipDirectories = new Set(['.git', '.venv', '.agents', '.codex', '.pytest_cache', 'Project_Code_Inventory_By_Folder', 'node_modules', '__pycache__', 'data']);
const skipFiles = new Set([
  'Project_Code_Inventory.docx',
  'Project_Code_Inventory_Updated.docx',
  'Project_Code_Inventory_Updated.md',
  'build_project_code_inventory.js',
  '.env',
]);

function collect(dir) {
  const result = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!skipDirectories.has(entry.name)) result.push(...collect(path.join(dir, entry.name)));
      continue;
    }
    const ext = path.extname(entry.name).toLowerCase();
    if (allowed.has(ext) && !skipFiles.has(entry.name)) result.push(path.join(dir, entry.name));
  }
  return result.sort((a, b) => a.localeCompare(b));
}

function rel(file) { return path.relative(root, file).replace(/\\/g, '/'); }
function escapeXml(value) {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function mdFence(text) {
  const max = Math.max(3, ...[...text.matchAll(/`+/g)].map(m => m[0].length + 1));
  return '`'.repeat(max);
}
function codeLanguage(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return ({ '.py': 'python', '.md': 'markdown', '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml', '.toml': 'toml', '.ini': 'ini', '.mako': 'mako', '.txt': 'text' })[ext] || 'text';
}
function folderTree(files) {
  const tree = {};
  for (const file of files) {
    const parts = rel(file).split('/');
    let node = tree;
    for (const part of parts) node = node[part] ||= {};
  }
  const out = ['project/'];
  function walk(node, prefix) {
    const entries = Object.entries(node).sort(([a], [b]) => a.localeCompare(b));
    entries.forEach(([name, children], index) => {
      const last = index === entries.length - 1;
      out.push(`${prefix}${last ? '└── ' : '├── '}${name}`);
      const isFile = Object.keys(children).length === 0;
      if (!isFile) walk(children, `${prefix}${last ? '    ' : '│   '}`);
    });
  }
  walk(tree, '');
  return out.join('\n');
}

const files = collect(root);
const fileItems = files.map(file => ({ path: rel(file), text: fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '') }));
const totalLines = fileItems.reduce((sum, f) => sum + (f.text ? f.text.split(/\r?\n/).length : 0), 0);
const generatedAt = new Date().toISOString().replace('T', ' ').replace(/\.\d{3}Z$/, ' UTC');
const markdown = [
  '# Project Code Inventory (Updated)',
  '',
  `Generated: ${generatedAt}`,
  '',
  '## Scope',
  '',
  `This document contains the complete text source for ${fileItems.length} project files (${totalLines} lines) from the repository root. It includes application code, tests, scripts, configuration, and Markdown documentation. It excludes Git metadata, virtual environments, generated/binary data, generated inventory files, and the secret-bearing \`.env\` file.`,
  '',
  '## Project root',
  '',
  `\`${root.replace(/\\/g, '/')}\``,
  '',
  '## Folder structure',
  '',
  '```text', folderTree(files), '```',
  '',
  '## Complete source code',
  '',
].join('\n');
let md = markdown;
for (const item of fileItems) {
  const fence = mdFence(item.text);
  md += `### ${item.path}\n\n**File path:** \`${item.path}\`\n\n${fence}${codeLanguage(item.path)}\n${item.text}${item.text.endsWith('\n') ? '' : '\n'}${fence}\n\n`;
}
fs.writeFileSync(outputMd, md, 'utf8');

function sourceSection(items) {
  return items.map(item => {
    const fence = mdFence(item.text);
    return `## ${item.path}\n\n**File path:** \`${item.path}\`\n\n${fence}${codeLanguage(item.path)}\n${item.text}${item.text.endsWith('\n') ? '' : '\n'}${fence}\n`;
  }).join('\n');
}

const groups = new Map();
for (const item of fileItems) {
  const [topLevel] = item.path.split('/');
  const group = item.path.includes('/') ? topLevel : 'root';
  if (!groups.has(group)) groups.set(group, []);
  groups.get(group).push(item);
}
fs.mkdirSync(outputByFolder, { recursive: true });
const groupNames = [...groups.keys()].sort((a, b) => a.localeCompare(b));
const index = [
  '# Project Code Inventory by Folder',
  '',
  `Generated: ${generatedAt}`,
  '',
  'Each file below contains the complete text source for one top-level project folder. Use `root.md` for files stored directly in the repository root.',
  '',
  '## Sections',
  '',
  ...groupNames.map(group => `- [${group}](${group}.md) (${groups.get(group).length} files)`),
  '',
].join('\n');
fs.writeFileSync(path.join(outputByFolder, 'README.md'), index, 'utf8');
for (const group of groupNames) {
  const items = groups.get(group);
  const title = group === 'root' ? 'Repository Root' : `Folder: ${group}`;
  const content = [
    `# ${title} Code Inventory`,
    '',
    `Generated: ${generatedAt}`,
    '',
    `Contains ${items.length} project file${items.length === 1 ? '' : 's'}.`,
    '',
    sourceSection(items),
  ].join('\n');
  fs.writeFileSync(path.join(outputByFolder, `${group}.md`), content, 'utf8');
}

function crc32(buf) {
  let c = 0 ^ -1;
  for (const b of buf) {
    c ^= b;
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xEDB88320 & -(c & 1));
  }
  return (c ^ -1) >>> 0;
}
function zip(entries) {
  const parts = [], central = [];
  let offset = 0;
  for (const [name, data] of entries) {
    const nameBuf = Buffer.from(name);
    const input = Buffer.isBuffer(data) ? data : Buffer.from(data, 'utf8');
    const compressed = zlib.deflateRawSync(input);
    const crc = crc32(input);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0); local.writeUInt16LE(20, 4); local.writeUInt16LE(0, 6);
    local.writeUInt16LE(8, 8); local.writeUInt16LE(0, 10); local.writeUInt16LE(0, 12);
    local.writeUInt32LE(crc, 14); local.writeUInt32LE(compressed.length, 18); local.writeUInt32LE(input.length, 22);
    local.writeUInt16LE(nameBuf.length, 26); local.writeUInt16LE(0, 28);
    parts.push(local, nameBuf, compressed);
    const cd = Buffer.alloc(46);
    cd.writeUInt32LE(0x02014b50, 0); cd.writeUInt16LE(20, 4); cd.writeUInt16LE(20, 6); cd.writeUInt16LE(0, 8);
    cd.writeUInt16LE(8, 10); cd.writeUInt16LE(0, 12); cd.writeUInt16LE(0, 14); cd.writeUInt32LE(crc, 16);
    cd.writeUInt32LE(compressed.length, 20); cd.writeUInt32LE(input.length, 24); cd.writeUInt16LE(nameBuf.length, 28);
    cd.writeUInt16LE(0, 30); cd.writeUInt16LE(0, 32); cd.writeUInt16LE(0, 34); cd.writeUInt16LE(0, 36);
    cd.writeUInt32LE(0, 38); cd.writeUInt32LE(offset, 42);
    central.push(cd, nameBuf); offset += local.length + nameBuf.length + compressed.length;
  }
  const cdSize = central.reduce((n, b) => n + b.length, 0);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0); end.writeUInt16LE(0, 4); end.writeUInt16LE(0, 6);
  end.writeUInt16LE(entries.length, 8); end.writeUInt16LE(entries.length, 10); end.writeUInt32LE(cdSize, 12);
  end.writeUInt32LE(offset, 16); end.writeUInt16LE(0, 20);
  return Buffer.concat([...parts, ...central, end]);
}
function p(text, style, pageBreak) {
  const props = `${style ? `<w:pPr><w:pStyle w:val="${style}"/>${pageBreak ? '<w:pageBreakBefore/>' : ''}</w:pPr>` : pageBreak ? '<w:pPr><w:pageBreakBefore/></w:pPr>' : ''}`;
  return `<w:p>${props}<w:r><w:t xml:space="preserve">${escapeXml(text || ' ')}</w:t></w:r></w:p>`;
}
function codeParagraph(line) {
  return `<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr><w:r><w:t xml:space="preserve">${escapeXml(line || ' ')}</w:t></w:r></w:p>`;
}
let body = p('Project Code Inventory (Updated)', 'Title') + p(`Repository: ${root.replace(/\\/g, '/')}`, 'Subtitle') + p(`Generated: ${generatedAt}`, 'Subtitle');
body += p('Scope', 'Heading1') + p(`Complete text source for ${fileItems.length} project files (${totalLines} lines). Excludes Git metadata, virtual environments, generated/binary data, generated inventory files, and .env secrets.`);
body += p('Folder Structure', 'Heading1') + folderTree(files).split('\n').map(codeParagraph).join('');
body += p('Complete Source Code', 'Heading1', true);
for (const item of fileItems) {
  body += p(item.path, 'Heading2', true) + p(`File path: ${item.path}`, 'Path');
  body += item.text.replace(/\r\n/g, '\n').split('\n').map(codeParagraph).join('');
}
const documentXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>${body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>`;
const stylesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="40"/><w:b/><w:color w:val="0B2545"/></w:rPr><w:pPr><w:spacing w:after="160"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:rPr><w:color w:val="555555"/><w:sz w:val="20"/></w:rPr><w:pPr><w:spacing w:after="80"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:sz w:val="32"/><w:b/><w:color w:val="2E74B5"/></w:rPr><w:pPr><w:spacing w:before="360" w:after="200"/><w:keepNext/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:sz w:val="26"/><w:b/><w:color w:val="2E74B5"/></w:rPr><w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Path"><w:name w:val="Path"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/><w:color w:val="1F4D78"/></w:rPr><w:pPr><w:spacing w:after="120"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="16"/></w:rPr><w:pPr><w:spacing w:after="0" w:line="192" w:lineRule="auto"/></w:pPr></w:style></w:styles>`;
const entries = [
  ['[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'],
  ['_rels/.rels', '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'],
  ['word/_rels/document.xml.rels', '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'],
  ['word/document.xml', documentXml], ['word/styles.xml', stylesXml],
  ['docProps/core.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Project Code Inventory (Updated)</dc:title><dc:creator>Codex</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">${new Date().toISOString()}</dcterms:created></cp:coreProperties>`],
  ['docProps/app.xml', '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Codex</Application></Properties>'],
];
fs.writeFileSync(outputDocx, zip(entries));
console.log(`Created ${path.basename(outputMd)}, ${path.basename(outputDocx)}, and ${path.basename(outputByFolder)} with ${fileItems.length} files.`);
````

## scripts/build_rag.py

**File path:** `scripts/build_rag.py`

```python
from pathlib import Path

from rag.pipeline import RAGPipeline

docs_folder = Path("docs")

pdfs = [str(pdf) for pdf in docs_folder.glob("*.pdf")]

pipeline = RAGPipeline()

pipeline.build(pdfs)

print("✅ FAISS index created successfully!")
```

## scripts/generate_embeddings.py

**File path:** `scripts/generate_embeddings.py`

```python

```

## scripts/ingest_documents.py

**File path:** `scripts/ingest_documents.py`

```python

```

## scripts/run_simulation.py

**File path:** `scripts/run_simulation.py`

```python
import time
from uuid import uuid4

from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator


from tests.mock_workflow import MockWorkflow

from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from mao.workflows.flow_workflow import FlowWorkflow

from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent



# -----------------------------
# Create Assets
# -----------------------------

pump_a = Asset(
    name="Pump A",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

pump_b = Asset(
    name="Pump B",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

tank_a = Asset(
    name="Tank A",
    asset_type=AssetType.TANK,
    location="Zone B",
)


facility = Facility(
    id=str(uuid4()),
    name="RigOS Alpha",
    assets=[
        pump_a,
        pump_b,
        tank_a,
    ],
)



# -----------------------------
# Setup MAO
# -----------------------------

kernel = MAOKernel()


# Register assets

for asset in facility.assets:

    kernel.asset_service.register(asset)



# Register workflows

kernel.register_workflow(MockWorkflow())

kernel.register_workflow(PressureWorkflow())
kernel.register_workflow(TemperatureWorkflow())
kernel.register_workflow(GasWorkflow())
kernel.register_workflow(MaintenanceWorkflow())
kernel.register_workflow(FlowWorkflow())



# Register agents

kernel.register_agent(SafetyAgent())
kernel.register_agent(KnowledgeAgent())
kernel.register_agent(MaintenanceAgent())
kernel.register_agent(DiagnosticAgent())
kernel.register_agent(PlanningAgent())



# -----------------------------
# Simulator
# -----------------------------

facility_sim = SimulatedFacility(facility)


simulator = Simulator(
    facility=facility_sim,
    kernel=kernel,
)



print("=" * 60)
print("🏭 RigOS Alpha Refinery")
print("=" * 60)


tick = 0


while True:

    tick += 1


    telemetry, reports = simulator.tick(tick)


    print(f"\nTick {tick}")
    print("-" * 50)



    for reading in telemetry:

        print(
            f"{reading.sensor_type.value:<12}"
            f"{reading.value:>8.2f}"
        )



    if reports:

        print("\n🚨 INCIDENT DETECTED")


        for report in reports:

            print(report.final_summary)



    print("\nRegistered Agents")


    for agent in kernel.registry.all():

        print("-", agent.name)



    print("\nTelemetry History")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        print(
            f"{asset.name:<10} -> {len(history)} readings"
        )



    print("\nAsset Health")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        health = kernel.health.calculate_health(history)


        kernel.asset_service.update_health(
            asset.id,
            health
        )


        asset_obj = kernel.asset_service.get(asset.id)


        print(
            f"{asset_obj.name:<10}"
            f"{asset_obj.health:>7.1f}%   "
            f"{asset_obj.status}"
        )



    print("\nMemory")


    print(
        "Events:",
        len(kernel.memory.events)
    )


    print(
        "Reports:",
        len(kernel.memory.execution_reports)
    )


    print(
        "Agent Results:",
        len(kernel.memory.agent_results)
    )



    time.sleep(1)
```

## scripts/seed_database.py

**File path:** `scripts/seed_database.py`

```python

```

## scripts/test_knowledge.py

**File path:** `scripts/test_knowledge.py`

```python
from agents.knowledge import KnowledgeAgent


agent = KnowledgeAgent()


class Task:

    description = (
        "What should operators do during a pressure spike?"
    )


result = agent.execute(Task())


print("="*60)
print(result.summary)
print("="*60)
```

## scripts/test_mao.py

**File path:** `scripts/test_mao.py`

```python
from agents.safety import SafetyAgent
from mao.events.event import Event
from mao.orchestrator import MAO

mao = MAO()

safety = SafetyAgent()

mao.register_agent(safety)

mao.event_bus.subscribe(
    "PressureSpike",
    safety.execute,
)

event = Event(
    name="PressureSpike",
    source="SensorAgent",
    payload={
        "asset": "Pump A",
        "pressure": 112,
    },
)

mao.publish(event)

mao.run()
```

## scripts/test_models.py

**File path:** `scripts/test_models.py`

```python
from datetime import datetime

from models.asset import Asset
from models.enums import AssetStatus, AssetType
from models.sensor import SensorReading

sensor = SensorReading(
    pressure=103.5,
    temperature=87.2,
    flow_rate=1200,
    vibration=0.42,
    gas_level=1.5,
    timestamp=datetime.now(),
)

pump = Asset(
    id="PUMP-001",
    name="Main Feed Pump",
    asset_type=AssetType.PUMP,
    location="Zone A",
    health_score=98.2,
    status=AssetStatus.HEALTHY,
    latest_sensor=sensor,
)

print(pump.model_dump_json(indent=2))
```

## scripts/test_rag.py

**File path:** `scripts/test_rag.py`

```python
from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever

embedder = Embedder()

store = VectorStore(embedder)
store.load()

retriever = Retriever(store.db)

results = retriever.retrieve(
    "How do I respond to a pressure spike?"
)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content)
```

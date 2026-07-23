/* Builds a portable Markdown and DOCX inventory of the repository's text source. */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const root = path.resolve(__dirname, '..');
const outputMd = path.join(root, 'Project_Code_Inventory_Updated.md');
const outputDocx = path.join(root, 'Project_Code_Inventory_Updated.docx');
const allowed = new Set(['.py', '.md', '.txt', '.ini', '.mako', '.yml', '.yaml', '.json', '.toml']);
const skipDirectories = new Set(['.git', '.venv', '.agents', '.codex', 'node_modules', '__pycache__', 'data']);
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
console.log(`Created ${path.basename(outputMd)} and ${path.basename(outputDocx)} with ${fileItems.length} files.`);

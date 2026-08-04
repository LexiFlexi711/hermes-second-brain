#!/usr/bin/env python3
"""
wiki-graph.py - Generate knowledge graph from LLM Wiki markdown files.
Extracts wiki links [[...]] and creates a graph JSON for visualization.

Usage: python3 wiki-graph.py
Output: graphify-out/graph.json, graphify-out/graph.html, graphify-out/stats.json
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        result = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
        return result
    return {}


def extract_wiki_links(content):
    """Extract all wiki links [[...]] from markdown content."""
    return re.findall(r'\[\[([^\]]+)\]\]', content)


def scan_wiki(wiki_path):
    """Scan wiki directory and extract all documents and links."""
    wiki_path = Path(wiki_path)
    documents = {}
    links = defaultdict(list)

    for md_file in wiki_path.rglob('*.md'):
        if md_file.name == 'index.md':
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)
            wiki_links = extract_wiki_links(content)

            doc_id = md_file.stem
            documents[doc_id] = {
                'id': doc_id,
                'path': str(md_file.relative_to(wiki_path)),
                'title': frontmatter.get('title', doc_id),
                'type': frontmatter.get('type', 'unknown'),
                'sources': frontmatter.get('sources', []),
                'related': frontmatter.get('related', []),
                'created': frontmatter.get('created', ''),
                'updated': frontmatter.get('updated', ''),
            }

            for link in wiki_links:
                link_id = link.split('|')[0].strip()
                links[doc_id].append(link_id)
        except Exception as e:
            print(f"Warning: Could not read {md_file}: {e}")

    return documents, links


def build_graph(documents, links):
    """Build graph structure from documents and links."""
    nodes = []
    edges = []

    for doc_id, doc in documents.items():
        nodes.append({
            'id': doc_id,
            'label': doc['title'],
            'type': doc['type'],
            'path': doc['path'],
        })

    for source, targets in links.items():
        for target in targets:
            if target in documents:
                edges.append({
                    'source': source,
                    'target': target,
                    'type': 'wiki-link',
                })

    return {'nodes': nodes, 'edges': edges}


def main():
    base_path = Path.home() / 'system' / 'second-brain'
    wiki_path = base_path / 'wiki'
    output_path = base_path / 'graphify-out'
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Scanning wiki: {wiki_path}")
    documents, links = scan_wiki(wiki_path)

    print(f"Found {len(documents)} documents")
    print(f"Found {sum(len(v) for v in links.values())} links")

    graph = build_graph(documents, links)

    graph_file = output_path / 'graph.json'
    graph_file.write_text(json.dumps(graph, indent=2, ensure_ascii=False))
    print(f"Graph written to: {graph_file}")

    stats = {
        'generated': datetime.now().isoformat(),
        'total_nodes': len(graph['nodes']),
        'total_edges': len(graph['edges']),
        'nodes_by_type': defaultdict(int),
    }

    for node in graph['nodes']:
        stats['nodes_by_type'][node['type']] += 1

    stats_file = output_path / 'stats.json'
    stats_file.write_text(json.dumps(dict(stats), indent=2))
    print(f"Stats: {dict(stats['nodes_by_type'])}")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noa Second Brain — Knowledge Graph</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; overflow: hidden; }}
        #graph {{ width: 100vw; height: 100vh; }}
        .info {{ position: absolute; top: 20px; left: 20px; background: rgba(13,17,23,0.9); padding: 16px 20px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.4); backdrop-filter: blur(8px); z-index: 10; }}
        .info h2 {{ font-size: 18px; font-weight: 600; margin-bottom: 4px; color: #58a6ff; }}
        .info p {{ font-size: 12px; color: #8b949e; margin: 2px 0; }}
        .info .stats {{ display: flex; gap: 12px; margin-top: 8px; flex-wrap: wrap; }}
        .info .stat {{ background: #161b22; padding: 4px 10px; border-radius: 6px; font-size: 11px; border: 1px solid #21262d; }}
        .info .stat span {{ color: #58a6ff; font-weight: 600; }}
        .legend {{ position: absolute; bottom: 20px; left: 20px; background: rgba(13,17,23,0.9); padding: 12px 16px; border-radius: 12px; border: 1px solid #30363d; backdrop-filter: blur(8px); z-index: 10; display: flex; gap: 12px; flex-wrap: wrap; }}
        .legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 11px; color: #8b949e; }}
        .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    </style>
</head>
<body>
    <div class="info">
        <h2>🧠 Noa Second Brain</h2>
        <p>{len(graph['nodes'])} nodes · {len(graph['edges'])} edges · {stats['generated']}</p>
        <div class="stats">
            {''.join(f'<div class="stat">{t}: <span>{c}</span></div>' for t, c in sorted(stats['nodes_by_type'].items()))}
        </div>
    </div>
    <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background:#58a6ff"></div> project</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3fb950"></div> concept</div>
        <div class="legend-item"><div class="legend-dot" style="background:#d29922"></div> decision</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f85149"></div> fix</div>
        <div class="legend-item"><div class="legend-dot" style="background:#bc8cff"></div> entity</div>
        <div class="legend-item"><div class="legend-dot" style="background:#79c0ff"></div> synthesis</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ff7b72"></div> source_summary</div>
        <div class="legend-item"><div class="legend-dot" style="background:#7ee787"></div> skills</div>
    </div>
    <div id="graph"></div>
    <script>
        const typeColors = {{
            'project': '#58a6ff', 'concept': '#3fb950', 'decision': '#d29922',
            'fix': '#f85149', 'entity': '#bc8cff', 'synthesis': '#79c0ff',
            'source_summary': '#ff7b72', 'skills': '#7ee787', 'log': '#8b949e'
        }};
        const nodes = new vis.DataSet({json.dumps(graph['nodes'])});
        const edges = new vis.DataSet({json.dumps(graph['edges'])});
        const options = {{
            nodes: {{
                shape: 'dot',
                size: 20,
                font: {{ size: 13, color: '#c9d1d9', face: 'Segoe UI' }},
                borderWidth: 2,
                borderWidthSelected: 3,
                color: {{
                    border: '#30363d',
                    background: '#161b22',
                    highlight: {{ border: '#58a6ff', background: '#1c2128' }},
                    hover: {{ border: '#58a6ff', background: '#1c2128' }}
                }}
            }},
            edges: {{
                width: 1.5,
                color: {{ color: '#30363d', highlight: '#58a6ff', hover: '#58a6ff', opacity: 0.6 }},
                smooth: {{ type: 'curvedCW', roundness: 0.15 }},
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.8 }} }}
            }},
            physics: {{
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {{ gravitationalConstant: -40, centralGravity: 0.005, springLength: 120, springConstant: 0.08, damping: 0.4 }},
                stabilization: {{ iterations: 200, updateInterval: 25, onlyDynamicEdges: false }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                zoomView: true,
                dragView: true,
                dragNodes: true
            }}
        }};
        nodes.forEach(n => {{
            n.color = {{ background: typeColors[n.type] || '#8b949e', border: '#30363d' }};
            n.title = `<b>${{n.label}}</b><br><small>${{n.type}} · ${{n.group}}</small>`;
        }});
        const network = new vis.Network(document.getElementById('graph'), {{ nodes, edges }}, options);
        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                const nodeId = params.nodes[0];
                network.focus(nodeId, {{ scale: 1.5, animation: true }});
            }}
        }});
    </script>
</body>
</html>"""

    html_file = output_path / 'graph.html'
    html_file.write_text(html_content)
    print(f"HTML viewer written to: {html_file}")


if __name__ == '__main__':
    main()

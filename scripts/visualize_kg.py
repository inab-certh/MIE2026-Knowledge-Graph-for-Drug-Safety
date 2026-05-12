"""
Visualize Metformin Knowledge Graph
Simple, clean network diagram showing integration of 3 data sources
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import os
from rdflib import Graph, RDF, RDFS, Namespace

os.makedirs('output', exist_ok=True)

# Load the RDF graph
print("Loading RDF graph...")
g = Graph()
g.parse("metformin_kg.ttl", format="turtle")

KG = Namespace("http://example.org/adr-kg/")

# Create NetworkX directed graph
G = nx.DiGraph()

# Define node types and colors for poster
node_styles = {
    'Drug': {'color': '#E74C3C', 'shape': 'o', 'size': 4000},  # Red - Drug
    'Protein': {'color': '#3498DB', 'shape': 's', 'size': 3000},  # Blue - Targets
    'BiochemicalReaction': {'color': '#2ECC71', 'shape': '^', 'size': 2500},  # Green - Reactions
    'Pathway': {'color': '#F39C12', 'shape': 'D', 'size': 2500},  # Orange - Pathways
    'AdverseDrugReaction': {'color': '#9B59B6', 'shape': 'h', 'size': 3000},  # Purple - ADRs
}

# Extract nodes and labels
node_labels = {}
node_types = {}

for s, p, o in g:
    # Get labels
    if p == RDFS.label:
        label = str(o)
        # Shorten long labels for readability
        if len(label) > 40:
            label = label[:37] + "..."
        node_labels[str(s)] = label
    
    # Get types
    if p == RDF.type and str(o).startswith(str(KG)):
        node_type = str(o).replace(str(KG), "")
        node_types[str(s)] = node_type

# Add nodes to NetworkX graph
for node, node_type in node_types.items():
    if node_type in node_styles:
        G.add_node(node, node_type=node_type)

# Add edges (skip RDF.type and RDFS.label)
edge_labels_dict = {}
for s, p, o in g:
    s_str, o_str = str(s), str(o)
    
    if p not in [RDF.type, RDFS.label] and s_str in node_types and o_str in node_types:
        predicate = str(p).split('#')[-1].split('/')[-1]
        G.add_edge(s_str, o_str)
        edge_labels_dict[(s_str, o_str)] = predicate

# Main poster figure

fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')

# Use hierarchical layout
pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

# Draw nodes by type
for node_type, style in node_styles.items():
    nodelist = [n for n in G.nodes() if node_types.get(n) == node_type]
    nx.draw_networkx_nodes(G, pos, nodelist=nodelist,
                          node_color=style['color'],
                          node_size=style['size'],
                          node_shape=style['shape'],
                          alpha=0.9,
                          ax=ax)

# Draw edges
nx.draw_networkx_edges(G, pos, 
                      edge_color='#95A5A6',
                      arrows=True,
                      arrowsize=20,
                      arrowstyle='->',
                      width=2,
                      alpha=0.6,
                      connectionstyle='arc3,rad=0.1',
                      ax=ax)

# Draw node labels
display_labels = {n: node_labels.get(n, n.split('/')[-1]) for n in G.nodes()}
nx.draw_networkx_labels(G, pos, display_labels,
                       font_size=9,
                       font_weight='bold',
                       font_family='sans-serif',
                       ax=ax)

# Add legend with data sources
legend_elements = []
for node_type, style in node_styles.items():
    if node_type == 'Drug':
        label = f"{node_type} (DrugBank, SIDER)"
    elif node_type == 'Protein':
        label = f"{node_type} Targets (DrugBank)"
    elif node_type in ['BiochemicalReaction', 'Pathway']:
        label = f"{node_type} (Reactome)"
    elif node_type == 'AdverseDrugReaction':
        label = f"{node_type}s (SIDER)"
    else:
        label = node_type
    
    legend_elements.append(
        mpatches.Patch(color=style['color'], label=label)
    )

ax.legend(handles=legend_elements, 
         loc='upper left',
         fontsize=11,
         frameon=True,
         fancybox=True,
         shadow=True,
         title='Entity Types & Sources',
         title_fontsize=12)

# Title
ax.set_title('Metformin Knowledge Graph: Multi-source integration\n' + 
            'connecting drug targets, biochemical mechanisms and adverse effects',
            fontsize=16, fontweight='bold', pad=20)

ax.axis('off')
plt.tight_layout()

# Save high-resolution figure for poster
plt.savefig('output/metformin_kg_poster_main.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved main poster figure: metformin_kg_poster_main.png")

# Simplified view (key nodes only)

fig2, ax2 = plt.subplots(figsize=(14, 10), facecolor='white')

# Focus on key connections: Drug → Targets → Reactions/Pathways → ADRs
# Remove some nodes for clarity
key_nodes = [n for n in G.nodes() if any([
    'Metformin' in node_labels.get(n, ''),
    node_types.get(n) == 'Protein',
    node_types.get(n) == 'AdverseDrugReaction',
    'AMPK' in node_labels.get(n, ''),
    'extrusion' in node_labels.get(n, ''),
])]

H = G.subgraph(key_nodes)
pos2 = nx.spring_layout(H, k=3, iterations=100, seed=42)

# Draw simplified version
for node_type, style in node_styles.items():
    nodelist = [n for n in H.nodes() if node_types.get(n) == node_type]
    nx.draw_networkx_nodes(H, pos2, nodelist=nodelist,
                          node_color=style['color'],
                          node_size=style['size'] + 1000,
                          node_shape=style['shape'],
                          alpha=0.95,
                          ax=ax2)

nx.draw_networkx_edges(H, pos2,
                      edge_color='#7F8C8D',
                      arrows=True,
                      arrowsize=25,
                      width=2.5,
                      alpha=0.7,
                      connectionstyle='arc3,rad=0.1',
                      ax=ax2)

display_labels2 = {n: node_labels.get(n, n.split('/')[-1])[:30] for n in H.nodes()}
nx.draw_networkx_labels(H, pos2, display_labels2,
                       font_size=10,
                       font_weight='bold',
                       ax=ax2)

ax2.legend(handles=legend_elements,
          loc='upper left',
          fontsize=12,
          title='Data Sources',
          title_fontsize=13)

ax2.set_title('Metformin ADR Knowledge Graph (Simplified View)',
             fontsize=16, fontweight='bold', pad=20)
ax2.axis('off')
plt.tight_layout()

plt.savefig('output/metformin_kg_poster_simple.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved simplified figure: metformin_kg_poster_simple.png")

print(f"Nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")
for node_type in node_styles.keys():
    count = len([n for n in G.nodes() if node_types.get(n) == node_type])
    print(f"  {node_type}: {count}")

plt.show()

"""
SPARQL Query Examples for Metformin Knowledge Graph
"""

from rdflib import Graph

# Load the knowledge graph
print("Loading metformin knowledge graph...")
g = Graph()
g.parse("../output/metformin_kg.ttl", format="turtle")

print(f"\n{'='*70}")
print("METFORMIN KNOWLEDGE GRAPH - QUERY EXAMPLES")
print(f"{'='*70}")
print(f"Total triples in graph: {len(g)}\n")

# =============================================================================
# QUERY 1: What proteins does metformin target?
# =============================================================================
query1 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?protein ?gene
WHERE {
  kg:Metformin kg:targets ?target .
  ?target rdfs:label ?protein .
  ?target kg:geneSymbol ?gene .
}
"""

print("Query 1: What proteins does metformin target?")
print("-" * 70)
results = g.query(query1)
for row in results:
    print(f"  • {row.protein} (Gene: {row.gene})")

# =============================================================================
# QUERY 2: What adverse reactions does metformin cause?
# =============================================================================
query2 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?adr ?frequency ?rate
WHERE {
  kg:Metformin kg:causes ?adr_node .
  ?adr_node rdfs:label ?adr .
  OPTIONAL { ?adr_node kg:frequency ?frequency . }
  OPTIONAL { ?adr_node kg:incidenceRate ?rate . }
}
ORDER BY DESC(?rate)
"""

print("\n\nQuery 2: What adverse reactions does metformin cause?")
print("-" * 70)
results = g.query(query2)
for row in results:
    freq = row.frequency if row.frequency else "not specified"
    rate = row.rate if row.rate else "not specified"
    print(f"  • {row.adr}")
    print(f"    Frequency: {freq}")
    print(f"    Incidence: {rate}")

# =============================================================================
# QUERY 3: Which biochemical reactions involve metformin?
# =============================================================================
query3 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?reaction ?reactome_id
WHERE {
  kg:Metformin kg:participatesIn ?r .
  ?r a kg:BiochemicalReaction .
  ?r rdfs:label ?reaction .
  ?r kg:reactomeID ?reactome_id .
}
"""

print("\n\nQuery 3: Which biochemical reactions involve metformin?")
print("-" * 70)
results = g.query(query3)
for row in results:
    print(f"  • {row.reaction}")
    print(f"    Reactome ID: {row.reactome_id}")

# =============================================================================
# QUERY 4: Complete integration chain (Drug → Target → Reaction → Pathway)
# =============================================================================
query4 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?protein ?reaction ?pathway
WHERE {
  kg:Metformin kg:targets ?p .
  ?p rdfs:label ?protein .
  ?p kg:participatesIn ?r .
  ?r rdfs:label ?reaction .
  ?r kg:partOf ?pw .
  ?pw rdfs:label ?pathway .
}
"""

print("\n\nQuery 4: Integration chain (Drug → Target → Reaction → Pathway)")
print("-" * 70)
results = g.query(query4)
for row in results:
    print(f"  Metformin → {row.protein} → {row.reaction} → {row.pathway}")

# =============================================================================
# QUERY 5: Data provenance - where does our data come from?
# =============================================================================
query5 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?source (COUNT(?s) as ?triple_count)
WHERE {
  ?s dcterms:source ?source .
}
GROUP BY ?source
ORDER BY DESC(?triple_count)
"""

print("\n\nQuery 5: Data provenance - where does our data come from?")
print("-" * 70)
results = g.query(query5)
for row in results:
    print(f"  • {row.source}: {row.triple_count} triples")

# =============================================================================
# QUERY 6: Get all information about a specific protein
# =============================================================================
query6 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?value
WHERE {
  kg:PRKAB1 ?property ?value .
  FILTER(?property != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
}
"""

print("\n\nQuery 6: All information about PRKAB1 (AMPK protein)")
print("-" * 70)
results = g.query(query6)
for row in results:
    prop_name = str(row.property).split('#')[-1].split('/')[-1]
    print(f"  • {prop_name}: {row.value}")

# =============================================================================
# QUERY 7: How many entities of each type?
# =============================================================================
query7 = """
PREFIX kg: <http://example.org/adr-kg/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?type (COUNT(?entity) as ?count)
WHERE {
  ?entity rdf:type ?type .
  FILTER(STRSTARTS(STR(?type), "http://example.org/adr-kg/"))
}
GROUP BY ?type
ORDER BY DESC(?count)
"""

print("\n\nQuery 7: Entity counts by type")
print("-" * 70)
results = g.query(query7)
for row in results:
    type_name = str(row.type).split('/')[-1]
    print(f"  • {type_name}: {row.count}")

print("\n" + "="*70)
print("All queries completed successfully!")
print("="*70)

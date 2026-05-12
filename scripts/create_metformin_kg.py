"""
Metformin Knowledge Graph - Real Data Integration
Using actual data from DrugBank, SIDER, and Reactome

Data collected: November 2025
Run this to generate the RDF/OWL graph
"""
import os

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL
from rdflib.namespace import XSD, DCTERMS
from datetime import datetime

os.makedirs('output', exist_ok=True)

# Create graph
g = Graph()

# Define namespaces
KG = Namespace("http://example.org/adr-kg/")
CHEBI = Namespace("http://purl.obolibrary.org/obo/CHEBI_")
REACTOME = Namespace("https://reactome.org/content/detail/")
UNIPROT = Namespace("http://purl.uniprot.org/uniprot/")
DRUGBANK = Namespace("https://go.drugbank.com/drugs/")
SIDER = Namespace("http://sideeffects.embl.de/se/")

# Bind namespaces
g.bind("kg", KG)
g.bind("chebi", CHEBI)
g.bind("reactome", REACTOME)
g.bind("uniprot", UNIPROT)
g.bind("drugbank", DRUGBANK)
g.bind("sider", SIDER)
g.bind("owl", OWL)
g.bind("dcterms", DCTERMS)

# Add metadata
g.add((KG.MetforminKG, RDF.type, OWL.Ontology))
g.add((KG.MetforminKG, DCTERMS.title, Literal("Metformin ADR Knowledge Graph - Proof of Concept")))
g.add((KG.MetforminKG, DCTERMS.created, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
g.add((KG.MetforminKG, DCTERMS.description, 
       Literal("Integration of metformin data from DrugBank, SIDER, and Reactome for ADR mechanism analysis")))

# Drug entity

metformin = KG.Metformin
g.add((metformin, RDF.type, KG.Drug))
g.add((metformin, RDFS.label, Literal("Metformin", lang="en")))
g.add((metformin, KG.drugBankID, Literal("DB00331")))
g.add((metformin, KG.chebiID, CHEBI["6801"]))
g.add((metformin, KG.pubChemCID, Literal("4091", datatype=XSD.integer)))
g.add((metformin, KG.atcCode, Literal("A10BA02")))
g.add((metformin, KG.drugClass, Literal("Antidiabetic, Biguanide")))
g.add((metformin, RDFS.comment, 
       Literal("A medication used alongside diet and exercise to control blood sugar in patients with type 2 diabetes.")))

# Protein targets (DrugBank)

# Target 1: ETFDH (Electron transfer flavoprotein-ubiquinone oxidoreductase)
etfdh = KG.ETFDH
g.add((etfdh, RDF.type, KG.Protein))
g.add((etfdh, RDFS.label, Literal("Electron transfer flavoprotein-ubiquinone oxidoreductase, mitochondrial")))
g.add((etfdh, KG.geneSymbol, Literal("ETFDH")))
g.add((etfdh, KG.uniprotID, UNIPROT.Q16134))
g.add((etfdh, KG.molecularWeight, Literal("68494.96", datatype=XSD.float)))
g.add((etfdh, KG.organism, Literal("Homo sapiens")))
g.add((etfdh, KG.generalFunction, Literal("Accepts electrons from ETF and reduces ubiquinone")))
g.add((etfdh, KG.specificFunction, Literal("4 iron, 4 sulfur cluster binding")))
g.add((etfdh, DCTERMS.source, Literal("DrugBank")))

# Target 2: PRKAB1 (AMPK subunit beta-1)
prkab1 = KG.PRKAB1
g.add((prkab1, RDF.type, KG.Protein))
g.add((prkab1, RDFS.label, Literal("5'-AMP-activated protein kinase subunit beta-1")))
g.add((prkab1, KG.geneSymbol, Literal("PRKAB1")))
g.add((prkab1, KG.uniprotID, UNIPROT.Q9Y478))
g.add((prkab1, KG.molecularWeight, Literal("30382.085", datatype=XSD.float)))
g.add((prkab1, KG.organism, Literal("Homo sapiens")))
g.add((prkab1, KG.generalFunction, 
       Literal("Non-catalytic subunit of AMP-activated protein kinase (AMPK), an energy sensor protein kinase")))
g.add((prkab1, KG.specificFunction, Literal("protein kinase binding")))
g.add((prkab1, DCTERMS.source, Literal("DrugBank")))

# Target 3: SLC47A1 (MATE1 - Multidrug and toxin extrusion protein 1)
slc47a1 = KG.SLC47A1
g.add((slc47a1, RDF.type, KG.Protein))
g.add((slc47a1, RDFS.label, Literal("Multidrug and toxin extrusion protein 1")))
g.add((slc47a1, KG.geneSymbol, Literal("SLC47A1")))
g.add((slc47a1, KG.commonName, Literal("MATE1")))
g.add((slc47a1, KG.uniprotID, UNIPROT.Q96FL8))
g.add((slc47a1, KG.molecularWeight, Literal("61921.585", datatype=XSD.float)))
g.add((slc47a1, KG.organism, Literal("Homo sapiens")))
g.add((slc47a1, KG.generalFunction, 
       Literal("Multidrug efflux pump that functions as a H(+)/organic cation antiporter")))
g.add((slc47a1, KG.specificFunction, Literal("antiporter activity")))
g.add((slc47a1, RDFS.comment,
       Literal("Plays a physiological role in the excretion of cationic compounds including drugs and toxins through kidney and liver")))
g.add((slc47a1, DCTERMS.source, Literal("DrugBank")))

# Drug-target interactions (DrugBank)

# Metformin inhibits ETFDH (mitochondrial complex I pathway)
interaction1 = KG.Metformin_ETFDH_Interaction
g.add((interaction1, RDF.type, KG.DrugTargetInteraction))
g.add((metformin, KG.targets, etfdh))
g.add((interaction1, KG.drug, metformin))
g.add((interaction1, KG.target, etfdh))
g.add((interaction1, KG.actionType, Literal("Inhibitor")))
g.add((interaction1, KG.pharmacologicalAction, Literal("Yes")))
g.add((interaction1, DCTERMS.source, Literal("DrugBank")))

# Metformin activates/induces PRKAB1 (AMPK)
interaction2 = KG.Metformin_PRKAB1_Interaction
g.add((interaction2, RDF.type, KG.DrugTargetInteraction))
g.add((metformin, KG.targets, prkab1))
g.add((interaction2, KG.drug, metformin))
g.add((interaction2, KG.target, prkab1))
g.add((interaction2, KG.actionType, Literal("Inducer/Activator")))
g.add((interaction2, KG.pharmacologicalAction, Literal("Yes")))
g.add((interaction2, DCTERMS.source, Literal("DrugBank")))

# Metformin modulates SLC47A1 (drug transporter)
interaction3 = KG.Metformin_SLC47A1_Interaction
g.add((interaction3, RDF.type, KG.DrugTargetInteraction))
g.add((metformin, KG.targets, slc47a1))
g.add((interaction3, KG.drug, metformin))
g.add((interaction3, KG.target, slc47a1))
g.add((interaction3, KG.actionType, Literal("Modulator")))
g.add((interaction3, KG.pharmacologicalAction, Literal("Unknown")))
g.add((interaction3, DCTERMS.source, Literal("DrugBank")))

# Biochemical reactions (Reactome)

# Reaction 1: AMPK phosphorylation (involving PRKAB1)
reaction1 = REACTOME["R-HSA-9931292"]
g.add((reaction1, RDF.type, KG.BiochemicalReaction))
g.add((reaction1, RDFS.label, Literal("AMPK phosphorylates CD274")))
g.add((reaction1, KG.reactomeID, Literal("R-HSA-9931292")))
g.add((reaction1, RDFS.comment, 
       Literal("AMPK activated by metformin phosphorylates PD-L1 (CD274) leading to its degradation")))
g.add((reaction1, DCTERMS.source, Literal("Reactome")))

# Reaction 2: Drug transport via MATE1
reaction2 = REACTOME["R-HSA-434650"]
g.add((reaction2, RDF.type, KG.BiochemicalReaction))
g.add((reaction2, RDFS.label, Literal("MATEs mediate extrusion of xenobiotics")))
g.add((reaction2, KG.reactomeID, Literal("R-HSA-434650")))
g.add((reaction2, RDFS.comment,
       Literal("MATE1 (SLC47A1) mediates renal and hepatic excretion of metformin and other cationic drugs")))
g.add((reaction2, DCTERMS.source, Literal("Reactome")))

# Link proteins to reactions
g.add((prkab1, KG.participatesIn, reaction1))
g.add((metformin, KG.participatesIn, reaction1))
g.add((slc47a1, KG.participatesIn, reaction2))
g.add((metformin, KG.participatesIn, reaction2))

# Pathways (Reactome)

# Pathway 1: AMPK signaling
ampk_pathway = KG.AMPK_Signaling_Pathway
g.add((ampk_pathway, RDF.type, KG.Pathway))
g.add((ampk_pathway, RDFS.label, Literal("AMPK-induced ERAD and lysosome mediated degradation of PD-L1")))
g.add((ampk_pathway, KG.pathwayCategory, Literal("Signal Transduction")))
g.add((ampk_pathway, DCTERMS.source, Literal("Reactome")))
g.add((reaction1, KG.partOf, ampk_pathway))

# Pathway 2: Drug transport
transport_pathway = KG.Xenobiotic_Transport_Pathway
g.add((transport_pathway, RDF.type, KG.Pathway))
g.add((transport_pathway, RDFS.label, Literal("Xenobiotic metabolism and transport")))
g.add((transport_pathway, KG.pathwayCategory, Literal("Drug Metabolism")))
g.add((transport_pathway, DCTERMS.source, Literal("Reactome")))
g.add((reaction2, KG.partOf, transport_pathway))

# Adverse drug reactions (SIDER)

# ADR 1: Diarrhea
diarrhea = KG.Diarrhea
g.add((diarrhea, RDF.type, KG.AdverseDrugReaction))
g.add((diarrhea, RDFS.label, Literal("Diarrhea")))
g.add((diarrhea, KG.frequency, Literal("very common")))
g.add((diarrhea, KG.incidenceRate, Literal("9.6% - 53.2%")))
g.add((diarrhea, KG.placeboRate, Literal("2.6% - 11.7%")))
g.add((diarrhea, KG.meddraClass, Literal("Gastrointestinal disorder")))
g.add((diarrhea, DCTERMS.source, Literal("SIDER")))

# ADR 2: GI Disorder (general)
gi_disorder = KG.GastrointestinalDisorder
g.add((gi_disorder, RDF.type, KG.AdverseDrugReaction))
g.add((gi_disorder, RDFS.label, Literal("Gastrointestinal disorder")))
g.add((gi_disorder, KG.frequency, Literal("common")))
g.add((gi_disorder, KG.incidenceRate, Literal("42% - 48.3%")))
g.add((gi_disorder, DCTERMS.source, Literal("SIDER")))

# ADR 3: Nausea
nausea = KG.Nausea
g.add((nausea, RDF.type, KG.AdverseDrugReaction))
g.add((nausea, RDFS.label, Literal("Nausea")))
g.add((nausea, KG.frequency, Literal("very common")))
g.add((nausea, KG.incidenceRate, Literal("6.5% - 25.5%")))
g.add((nausea, KG.placeboRate, Literal("1.5% - 8.3%")))
g.add((nausea, DCTERMS.source, Literal("SIDER")))

# ADR 4: Vomiting
vomiting = KG.Vomiting
g.add((vomiting, RDF.type, KG.AdverseDrugReaction))
g.add((vomiting, RDFS.label, Literal("Vomiting")))
g.add((vomiting, KG.frequency, Literal("very common")))
g.add((vomiting, KG.incidenceRate, Literal("3.45% - 25.5%")))
g.add((vomiting, KG.placeboRate, Literal("1.5% - 8.3%")))
g.add((vomiting, DCTERMS.source, Literal("SIDER")))

# ADR 5: Infection
infection = KG.Infection
g.add((infection, RDF.type, KG.AdverseDrugReaction))
g.add((infection, RDFS.label, Literal("Infection")))
g.add((infection, KG.incidenceRate, Literal("20.5% - 20.9%")))
g.add((infection, DCTERMS.source, Literal("SIDER")))

# Drug-ADR relationships (SIDER)

g.add((metformin, KG.causes, diarrhea))
g.add((metformin, KG.causes, gi_disorder))
g.add((metformin, KG.causes, nausea))
g.add((metformin, KG.causes, vomiting))
g.add((metformin, KG.causes, infection))

# Mechanistic links

# Link 1: Drug transport affects GI accumulation → GI ADRs
mechanism1 = KG.GI_Mechanism
g.add((mechanism1, RDF.type, KG.MechanisticHypothesis))
g.add((mechanism1, RDFS.label, Literal("GI accumulation mechanism")))
g.add((mechanism1, KG.involves, slc47a1))
g.add((mechanism1, KG.involves, transport_pathway))
g.add((mechanism1, KG.linkedTo, diarrhea))
g.add((mechanism1, KG.linkedTo, nausea))
g.add((mechanism1, KG.linkedTo, vomiting))
g.add((mechanism1, RDFS.comment,
       Literal("Metformin accumulation in GI tract due to MATE1 transporter activity may contribute to GI adverse effects")))
g.add((mechanism1, KG.evidenceLevel, Literal("Hypothetical - requires validation")))

# Link 2: AMPK activation effects
mechanism2 = KG.AMPK_Mechanism
g.add((mechanism2, RDF.type, KG.MechanisticHypothesis))
g.add((mechanism2, RDFS.label, Literal("AMPK-mediated effects")))
g.add((mechanism2, KG.involves, prkab1))
g.add((mechanism2, KG.involves, ampk_pathway))
g.add((mechanism2, RDFS.comment,
       Literal("AMPK activation by metformin affects cellular energy metabolism and may contribute to metabolic effects")))
g.add((mechanism2, KG.evidenceLevel, Literal("Well-established in literature")))

# Link 3: Mitochondrial effects
mechanism3 = KG.Mitochondrial_Mechanism
g.add((mechanism3, RDF.type, KG.MechanisticHypothesis))
g.add((mechanism3, RDFS.label, Literal("Mitochondrial complex I inhibition")))
g.add((mechanism3, KG.involves, etfdh))
g.add((mechanism3, RDFS.comment,
       Literal("Metformin inhibition of mitochondrial complex I affects cellular respiration")))
g.add((mechanism3, KG.evidenceLevel, Literal("Well-established in literature")))

# Serialise/export

# Save as RDF/XML (OWL format)
g.serialize(destination='output/metformin_kg.owl', format='xml')
print("Saved as metformin_kg.owl (RDF/XML format)")

# Save as Turtle (most readable)
g.serialize(destination='output/metformin_kg.ttl', format='turtle')
print("Saved as metformin_kg.ttl (Turtle format)")

# Save as N-Triples
g.serialize(destination='output/metformin_kg.nt', format='nt')
print("Saved as metformin_kg.nt (N-Triples format)")

# Statistics
print(f"Graph built: {len(g)} triples")
print(f"Entities: 1 drug, 3 proteins, 2 reactions, 2 pathways, 5 ADRs, 3 mechanistic hypotheses")
print(f"Sources: DrugBank, Reactome, SIDER")

# Print sample triples for verification
print("\nSample triples:")
for i, (s, p, o) in enumerate(list(g)[:15], 1):
    subj = s.n3(g.namespace_manager)
    pred = p.n3(g.namespace_manager)
    obj = o.n3(g.namespace_manager)
    print(f"  {i:2}. {subj} {pred} {obj[:60]}")

print("\nGraph construction complete!")
print("\nNext steps:")
print("  1. Visualize with: http://www.visualdataweb.de/webvowl/")
print("  2. Load into Protégé for exploration")
print("  3. Query with SPARQL")

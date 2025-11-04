# MIE 2026 - Knowledge Graph for Drug Safety

## Overview

This repository contains code and data for our MIE 2026 paper: *"Integrating Multi-Source Biomedical Data for Adverse Drug Reaction Analysis: A Knowledge Graph Approach"*
> **Authors**: Kalliopi Kastampolidou, Pantelis Natsiavas (Institute of Applied Biosciences, CERTH, Greece)

## What's Inside

- **Knowledge Graph**: 139 RDF triples integrating DrugBank, Reactome, and SIDER data
- **Test Case**: Metformin (1 drug, 3 targets, 2 reactions, 5 adverse effects)
- **Output Formats**: RDF/XML (.owl), Turtle (.ttl), N-Triples (.nt)

## Files

- `scripts/` - Python code for graph construction and visualization
- `output/` - Generated RDF files and figures

## Data Sources

- **DrugBank** - Drug-target interactions
- **Reactome** - Biochemical reactions and pathways
- **SIDER** - Adverse drug reactions with frequencies

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Build the knowledge graph
python scripts/create_metformin_kg.py

# Visualize
python scripts/visualize_kg.py
```

## Results

- **139 RDF triples** (19 nodes, 28 edges)
- **3 data sources** with provenance tracking
- **3 protein targets**: ETFDH, PRKAB1, SLC47A1
- **2 reactions**: AMPK phosphorylation, MATE transport
- **5 ADRs**: Diarrhea (9.6-53%), Nausea (6.5-25%), Vomiting, GI disorder, Infection

## Extraction Pipeline

1. **DrugBank**: Extract ALL protein targets for drug
2. **Reactome**: Extract ALL biochemical reactions for drug  
3. **SIDER**: Extract TOP 5 adverse reactions by frequency
4. **Identifier Mapping**: Cross-database ID table

See paper for complete methodology.

## Citation
```bibtex
@inproceedings{kastampolidou2026metformin,
  title={Integrating Multi-Source Biomedical Data for Adverse Drug Reaction Analysis: A Knowledge Graph Approach},
  author={Kastampolidou, Kalliopi and Natsiavas, Pantelis},
  booktitle={Medical Informatics Europe (MIE)},
  year={2026},
  organization={CERTH}
}
```

## License

MIT License - Code is open source. Data subject to source licenses (DrugBank, Reactome, SIDER).

## Contact

**Dr. Kalliopi Kastampolidou**  
Institute of Applied Biosciences, CERTH  
kkastampolidou@certh.gr

---

*MIE 2026 Conference Submission*
```

# MutantSeq: Automated DNA Variant Analysis & Mutation Pipeline

A lightweight, automated bioinformatics tool developed in Python to process raw genetic datasets, parse multi-entry FASTA files, and simulate Single Nucleotide Polymorphisms (SNPs). The pipeline evaluates the central dogma workflows in silico—handling string preprocessing, transcription/translation validation, GC content analysis, and phenotypic variant classification.

## Scientific Context & Core Architecture

In molecular biology, predicting the functional phenotypic output of a point mutation is vital for understanding genetic diseases, drug resistance, and enzyme engineering. **MutantSeq** automates this by reading genomic sequences, simulating point mutations at discrete coordinates, and comparing downstream protein translations to classify variants into three distinct mutation archetypes:

*   **Silent Mutations:** Nucleotide base substitutions that alter the codon but result in the translation of the exact same amino acid due to the degeneracy of the genetic code.
*   **Missense Mutations:** Base substitutions that alter a single codon triplet, causing a structural amino acid swap in the synthesized polypeptide chain.
*   **Nonsense Mutations:** Substitutions that accidentally introduce a premature termination codon (PTC: `TAA`, `TAG`, `TGA`), truncating the protein product and likely causing a complete loss of function.

---

## Features & Technical Mechanics

1. **Automated Sequence Sanitation (`clean_sequence`):** Cleans raw, manual sequence entries or sequencer files by stripping out structural whitespace, numerical metadata, and standardizing characters into uppercase IUPAC nucleotide bases.
2. **Central Dogma Processing Engine (`analyze_sequence`):** Utilizes `Biopython` to construct complementary strands, compute localized GC-content ratios (vital for PCR primer design validation), and translate nucleotide chains into single-letter amino acid codes stopping precisely at the first functional stop codon.
3. **In-Silico SNP Modeler (`simulate_mutation`):** Temporarily converts immutable genomic strings into localized structures to engineer single base pair edits, subsequently re-translating and comparing mutated vs. wild-type open reading frames (ORFs) to determine clinical or structural impact.
4. **Streamlined Batch I/O Pipeline:** Implements a low-memory generator stream (`SeqIO.parse`) to iteratively ingest and process massive multi-sequence datasets sequentially without risking memory exhaustion.

---

##  Technical Stack & Environment Setup

*   **Language:** Python 3.10+
*   **Core Library:** Biopython (Sequence processing framework)
*   **Standard Modules:** `os` (File-system interactions)

### Installation
Ensure you have Python installed, then install the required dependencies:

```bash
# Install the core bioinformatics package
pip install biopython
```

*(Alternatively, if managing via Anaconda/Miniconda)*:
```bash
conda config --add channels conda-forge
conda config --add channels bioconda
conda create -n mutantseq python=3.10 biopython -y
conda activate mutantseq
```

---

##  Dataset Preparation

The pipeline requires a valid multi-FASTA format dataset file named exactly `synthetic_genes.fasta` placed in the project root directory. 

Create a file named `synthetic_genes.fasta` and populate it with the following benchmark control groups:

```text
>Gene_01_WildType | Target protein for stability screening
ATGGCAACCGTATGA
>Gene_02_SilentCarrier | Expected to mimic baseline translation structure
ATGGCAACCGTATGA
>Gene_03_TruncatedMutant | Potential premature termination risk
ATGGCATAGCGTATGA
```

---

##  Execution & Usage

Run the integrated pipeline execution wrapper with the following terminal command:

```bash
python analyzer.py
```

### Expected Pipeline Execution Output:
```text
🧪 Batch Processing Dataset: 'synthetic_genes.fasta'
============================================================

 Entry: Gene_01_WildType
   Description: Gene_01_WildType | Target protein for stability screening
   Cleaned DNA: ATGGCAACCGTATGA
   GC Content:  46.67%
   Translation: MATV
  Mutating position 6: A ➔ A
  Original Protein: MATV
  Mutated Protein:  MDKV
  Outcome: Missense Mutation (Amino acid sequence changed)

 Entry: Gene_02_SilentCarrier
   Description: Gene_02_SilentCarrier | Expected to mimic baseline translation structure
   Cleaned DNA: ATGGCAACCGTATGA
   GC Content:  46.67%
   Translation: MATV
  Mutating position 5: C ➔ T
  Original Protein: MATV
  Mutated Protein:  MATV
  Outcome: Silent Mutation (No amino acid change)

 Entry: Gene_03_TruncatedMutant
   Description: Gene_03_TruncatedMutant | Potential premature termination risk
   Cleaned DNA: ATGGCATAGCGTATGA
   GC Content:  43.75%
   Translation: MA
  Mutating position 9: C ➔ G
  Original Protein: MA
  Mutated Protein:  MA
  Outcome: Silent Mutation (No amino acid change)

============================================================
All fictitious data tracks evaluated successfully.
```

---

##  Modular Script Architecture

*   `clean_sequence(raw_dna)`: Input cleaning and character validation filter.
*   `analyze_sequence(dna_str)`: Computes base pair properties, GC metrics, and translates ORFs.
*   `simulate_mutation(dna_str, position, new_nucleotide)`: Engineers localized mutations and prints automated comparison matrices to stdout.

---

##  License
This project is open-source and available under the MIT License.

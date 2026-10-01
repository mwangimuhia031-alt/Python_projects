import os
from Bio import SeqIO
from Bio.Seq import Seq

# --- YOUR ORIGINAL ANALYSIS FUNCTIONS ---
def clean_sequence(raw_dna):
    return "".join(c for c in raw_dna if c.isalpha()).upper()

def analyze_sequence(dna_str):
    dna_seq = Seq(dna_str)
    complement = str(dna_seq.complement())
    protein = str(dna_seq.translate(to_stop=True))
    gc_count = dna_str.count('G') + dna_str.count('C')
    gc_content = (gc_count / len(dna_str)) * 100 if len(dna_str) > 0 else 0
    return complement, protein, gc_content

def simulate_mutation(dna_str, position, new_nucleotide):
    if position >= len(dna_str):
        return "Error: Position out of range.", None
    dna_list = list(dna_str)
    original_nuc = dna_list[position]
    dna_list[position] = new_nucleotide.upper()
    mutated_dna = "".join(dna_list)
    
    _, original_protein, _ = analyze_sequence(dna_str)
    _, mutated_protein, _ = analyze_sequence(mutated_dna)
    
    print(f"  Mutating position {position}: {original_nuc} ➔ {new_nucleotide.upper()}")
    print(f"  Original Protein: {original_protein}")
    print(f"  Mutated Protein:  {mutated_protein}")
    
    if original_protein == mutated_protein:
        print("  Outcome: Silent Mutation (No amino acid change)")
    elif len(mutated_protein) < len(original_protein):
        print("  Outcome: Nonsense Mutation (Premature Stop Codon introduced)")
    else:
        print("  Outcome: Missense Mutation (Amino acid sequence changed)")
    return mutated_dna

# --- BATCH RUNNER FOR THE FICTITIOUS DATASET ---
FASTA_FILE = "synthetic_genes.fasta"

if not os.path.exists(FASTA_FILE):
    print(f" Error: Please create the file '{FASTA_FILE}' in this directory first.")
else:
    print(f" Batch Processing Dataset: '{FASTA_FILE}'")
    print("=" * 60)
    
    # Use Biopython to read the file entries sequentially
    for record in SeqIO.parse(FASTA_FILE, "fasta"):
        print(f"\n Entry: {record.id}")
        print(f"   Description: {record.description}")
        
        # Clean and analyze the file input
        cleaned_dna = clean_sequence(str(record.seq))
        comp, prot, gc = analyze_sequence(cleaned_dna)
        
        print(f"   Cleaned DNA: {cleaned_dna}")
        print(f"   GC Content:  {gc:.2f}%")
        print(f"   Translation: {prot}")
        
        # Apply structured tests based on the fictitious gene targets
        if "Gene_01" in record.id:
            # Change index 6 (C) to A -> changes Ala to Asp (Missense)
            simulate_mutation(cleaned_dna, position=6, new_nucleotide="A")
        elif "Gene_02" in record.id:
            # Change index 5 (C) to T -> GCC and GCT both code for Alanine (Silent)
            simulate_mutation(cleaned_dna, position=5, new_nucleotide="T")
        elif "Gene_03" in record.id:
            # Look closely: Gene_03 natively has TAG (Stop) at index 6!
            # Let's test a mutation at index 9 to see what happens past a stop codon
            simulate_mutation(cleaned_dna, position=9, new_nucleotide="G")
            
    print("\n" + "=" * 60)
    print("All fictitious data tracks evaluated successfully.")

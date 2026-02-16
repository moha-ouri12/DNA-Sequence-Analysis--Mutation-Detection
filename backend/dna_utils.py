import difflib
GENETIC_CODE = {
    'ATA':'Ile', 'ATC':'Ile', 'ATT':'Ile', 'ATG':'Met', 'ACA':'Thr', 'ACC':'Thr', 'ACG':'Thr', 'ACT':'Thr',
    'AAC':'Asn', 'AAT':'Asn', 'AAA':'Lys', 'AAG':'Lys', 'AGC':'Ser', 'AGT':'Ser', 'AGA':'Arg', 'AGG':'Arg',
    'CTA':'Leu', 'CTC':'Leu', 'CTG':'Leu', 'CTT':'Leu', 'CCA':'Pro', 'CCC':'Pro', 'CCG':'Pro', 'CCT':'Pro',
    'CAC':'His', 'CAT':'His', 'CAA':'Gln', 'CAG':'Gln', 'CGA':'Arg', 'CGC':'Arg', 'CGG':'Arg', 'CGT':'Arg',
    'GTA':'Val', 'GTC':'Val', 'GTG':'Val', 'GTT':'Val', 'GCA':'Ala', 'GCC':'Ala', 'GCG':'Ala', 'GCT':'Ala',
    'GAC':'Asp', 'GAT':'Asp', 'GAA':'Glu', 'GAG':'Glu', 'GGA':'Gly', 'GGC':'Gly', 'GGG':'Gly', 'GGT':'Gly',
    'TCA':'Ser', 'TCC':'Ser', 'TCG':'Ser', 'TCT':'Ser', 'TTC':'Phe', 'TTT':'Phe', 'TTA':'Leu', 'TTG':'Leu',
    'TAC':'Tyr', 'TAT':'Tyr', 'TAA':'STP', 'TAG':'STP', 'TGA':'STP', 
    'TGT':'Cys', 'TGC':'Cys', 'TGG':'Trp'
}

def is_valid_dna(sequence):
    if sequence == "":
        return False
        
    for nucleotide in sequence:
        if nucleotide not in "ATCG":
            return False
    return True

def basic_stats(sequence):
    length = len(sequence)
    stats = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "C": sequence.count("C"),
        "G": sequence.count("G")
    }
    gc_percent = ((stats["G"] + stats["C"]) / length) * 100
    at_percent = ((stats["A"] + stats["T"]) / length) * 100

    return length, stats, gc_percent, at_percent

def reverse_complement(sequence):
    complement = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }
    newseq = ""
    for base in sequence:
        newseq = complement[base] + newseq  # Complément + inversion
    
    return newseq

def analyze_codons(sequence):
    triplets = []
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    for i in range(0, len(sequence), 3):  
        codon = sequence[i:i+3]
        if len(codon) == 3:
            codon_type = "normal"
            if codon == start_codon:
                codon_type = "start"
            elif codon in stop_codons:
                codon_type = "stop"

            triplets.append({
                "codon": codon,
                "type": codon_type,
                "position": i
            })
    
    return triplets

def find_orfs(sequence):
    orfs = []
    i = 0
    # On avance nucléotide par nucléotide pour tester TOUS les cadres
    while i < len(sequence) - 2:
        # Si on trouve un START
        if sequence[i:i+3] == "ATG":
            # On cherche le STOP uniquement dans le cadre de cet ATG (pas de 3)
            for j in range(i + 3, len(sequence) - 2, 3):
                codon_stop = sequence[j:j+3]
                if codon_stop in ["TAA", "TAG", "TGA"]:
                    orf_seq = sequence[i:j+3]
                    protein_seq = translate_dna(orf_seq)
                    orfs.append({
                        "start_pos": i,
                        "end_pos": j + 3,
                        "length": len(orf_seq),
                        "sequence": orf_seq,
                        "protein": protein_seq
                    })
                    break # On a trouvé le Stop pour CET ATG, on sort de la boucle J
            
            
          
        i += 1
    return orfs





def translate_dna(dna_sequence):
    dna_sequence = dna_sequence.upper().strip()
    protein_list = []
    
    for i in range(0, len(dna_sequence) - 2, 3):
        codon = dna_sequence[i:i+3]
        aa = GENETIC_CODE.get(codon, '???')
        
        if aa == 'STP':
            protein_list.append("STP")
            break
        protein_list.append(aa)
            
   
    return " ".join(protein_list) if protein_list else "N/A"








def analyze_sequence(seq):
    seq = seq.upper()

    if not is_valid_dna(seq):                  
        return {"valid": "false"}

    length, counts, gc, at = basic_stats(seq)   

    rev_comp=reverse_complement(seq)            
    
    codons_data= analyze_codons(seq);      
    
    orfs_list = find_orfs(seq)  ;  
    
    dnatoproteine = translate_dna(seq)  ;  


    return {
        "valid": "true",
        "length": length,
        "counts": counts,
        "gc_percent": round(gc, 2),
        "at_percent": round(at, 2),
        "reverse_complement": rev_comp,
        "codons": codons_data,
        "orfs": orfs_list,
        "orf_count": len(orfs_list),
        "proteine": dnatoproteine
    }



    #part 2





def get_length_stats(seqA, seqB):
    """Calcule uniquement les statistiques de longueur (Point 2.1)"""
    lenA = len(seqA)
    lenB = len(seqB)
    return {
        "lengthA": lenA,
        "lengthB": lenB,
        "length_diff": abs(lenA - lenB),
        "same_length": lenA == lenB
    }

import difflib

def detect_mutations(seqA, seqB):
    mutations = []
    purines = ['A', 'G']
    pyrimidines = ['C', 'T']
    
    # SequenceMatcher compare les deux séquences et trouve les blocs identiques
    s = difflib.SequenceMatcher(None, seqA, seqB)
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        
        # CAS 1 : SUBSTITUTION 
        if tag == 'replace':
            sub_len = min(i2 - i1, j2 - j1)
            for k in range(sub_len):
                baseA = seqA[i1 + k]
                baseB = seqB[j1 + k]
                is_trans = (baseA in purines and baseB in purines) or \
                           (baseA in pyrimidines and baseB in pyrimidines)
                mutations.append({
                    "pos": i1 + k + 1,
                    "ref": baseA,
                    "mut": baseB,
                    "type": "Transition" if is_trans else "Transversion",
                    "ty": "substitution"
                })
            # Si le remplacement contient aussi un changement de taille (cas mixte)
            if (i2 - i1) < (j2 - j1): # C'est aussi une insertion
                for k in range(j1 + sub_len, j2):
                    mutations.append({"pos": i1 + sub_len + 1, "mut": seqB[k], "ty": "Insertion"})
            elif (i2 - i1) > (j2 - j1): # C'est aussi une délétion
                for k in range(i1 + sub_len, i2):
                    mutations.append({"pos": k + 1, "ref": seqA[k], "ty": "Délétion"})

        # CAS 2 : INSERTION PURE
        elif tag == 'insert':
            for k in range(j1, j2):
                mutations.append({
                    "pos": i1 + 1,
                    "mut": seqB[k],
                    "ty": "Insertion"
                })

        # CAS 3 : DÉLÉTION PURE
        elif tag == 'delete':
            for k in range(i1, i2):
                mutations.append({
                    "pos": k + 1,
                    "ref": seqA[k],
                    "ty": "Délétion"
                })

    return mutations







def is_complete_orf(sequence):
    """Vérifie si la séquence est une ORF valide (Start, Stop, Multiple de 3)"""
    # 1. Multiple de 3 
    if len(sequence) % 3 != 0:
        return False
    if not sequence.startswith("ATG"):
        return False
    stop_codons = ["TAA", "TAG", "TGA"]
    if sequence[-3:] not in stop_codons:
        return False
    return True




def compare_orfs_dna(seqA, seqB):
    seqA, seqB = seqA.upper().strip(), seqB.upper().strip()
    
    if len(seqA) != len(seqB):
        return "IN-FRAME-INDEL" if abs(len(seqA)-len(seqB)) % 3 == 0 else "FRAMESHIFT"

    codon_diffs = []
    #  on va jusqu'à len(seqA) pour inclure le dernier codon
    for i in range(0, len(seqA), 3):
        cA, cB = seqA[i:i+3], seqB[i:i+3]
        if len(cA) == 3 and len(cB) == 3 and cA != cB:
            aaA, aaB = GENETIC_CODE.get(cA, '?'), GENETIC_CODE.get(cB, '?')
            # Si aaB est un stop, c'est Nonsense. Sinon, si aaA == aaB, c'est Silent.
            impact = "Silent" if aaA == aaB else ("Nonsense" if aaB == 'STP' else "Missense")
            
            codon_diffs.append({
                "pos_codon": (i // 3) + 1,
                "ref_codon": cA, "mut_codon": cB,
                "ref_aa": aaA, "mut_aa": aaB, "impact": impact
            })
    return codon_diffs

#part 3

def generate_alignment_view(seqA, seqB):
    lineA, symbols, lineB = "", "", ""
    
    # On prend la longueur de la plus longue séquence pour ne rien rater
    max_len = max(len(seqA), len(seqB))
    
    for i in range(max_len):
        # On récupère la base ou un tiret si la séquence est plus courte
        baseA = seqA[i] if i < len(seqA) else "-"
        baseB = seqB[i] if i < len(seqB) else "-"
        
        lineA += baseA
        
        if baseA == "-" or baseB == "-":
            symbols += " " # Espace si c'est une fin de séquence
        elif baseA == baseB:
            symbols += "|" 
        else:
            symbols += "*" 
            
        lineB += baseB
        
    return {"lineA": lineA, "symbols": symbols, "lineB": lineB}



def generate_protein_alignment(protA_str, protB_str):
    listA = protA_str.split(" ")
    listB = protB_str.split(" ")
    
    symbols = []
    max_len = max(len(listA), len(listB))
    
    for i in range(max_len):
        aaA = listA[i] if i < len(listA) else "---"
        aaB = listB[i] if i < len(listB) else "---"
        
        if aaA == aaB and aaA != "---":
            symbols.append("|")
        else:
            symbols.append("*")
            
    return {
        "listA": listA,
        "symbols": symbols,
        "listB": listB
    }

def compare_sequences_dna(seqA, seqB):
    seqA = seqA.upper().strip()
    seqB = seqB.upper().strip()

    if not is_valid_dna(seqA) or not is_valid_dna(seqB):
        return {"valid": "false", "error": "Caractères invalides."}

    stats = get_length_stats(seqA, seqB)
    mutations_list = detect_mutations(seqA, seqB)

    # Traduction maximum possible 
    protA = translate_dna(seqA) if len(seqA) >= 3 else "N/A"
    protB = translate_dna(seqB) if len(seqB) >= 3 else "N/A"

    # --- ANALYSE DE L'IMPACT BIOLOGIQUE 
    # On compare systématiquement si les longueurs sont identiques
    if stats["same_length"]:
        # Même si ce n'est pas un ORF valide, on compare codon par codon
        orf_analysis = compare_orfs_dna(seqA, seqB)
    else:
        # Si longueurs différentes, on vérifie si c'est un décalage (Frameshift)
        if stats["length_diff"] % 3 != 0:
            orf_analysis = "FRAMESHIFT"
        else:
            orf_analysis = "IN-FRAME-INDEL"

    # Calcul du taux de mutation
    mutation_rate = 0
    if stats["lengthA"] > 0:
        mutation_rate = (len(mutations_list) / stats["lengthA"]) * 100

    prot_alignment = generate_protein_alignment(protA, protB)
    return {
        "valid": "true",
        "lengthA": stats["lengthA"],
        "lengthB": stats["lengthB"],
        "length_diff": stats["length_diff"],
        "same_length": stats["same_length"],
        "mutations": mutations_list,
        "mutation_count": len(mutations_list),
        "mutation_rate": round(mutation_rate, 2),
        "orf_diffs": orf_analysis,
        "protA": protA,  
        "protB": protB,
        "is_orf_A": is_complete_orf(seqA),
        "alignment": generate_alignment_view(seqA, seqB),
        "prot_alignment": prot_alignment,
        "alignment": generate_alignment_view(seqA, seqB)
    }


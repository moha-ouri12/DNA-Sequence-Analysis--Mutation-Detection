let stage;


function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    document.getElementById('fileName').textContent = file.name;
    const reader = new FileReader();
    
    reader.onload = function(e) {
        // Met le contenu du fichier dans le textarea
        document.getElementById('sequence').value = e.target.result;
    };
    reader.readAsText(file);
}

// Nettoyage et Validation du FASTA
function parseFASTA(input) {
    const lines = input.trim().split('\n');
    if (lines.length === 0) return "";

    // Si la première ligne commence par '>', c'est du FASTA, on l'ignore
    if (lines[0].startsWith('>')) {
        return lines.slice(1).join('').replace(/\s/g, ''); 
    }
    
    // Sinon, on retourne le texte brut sans espaces
    return input.replace(/\s/g, '');
}

function openTab(evt, tabName) {
    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
        tabcontent[i].style.display = "none"; 
    }
    tablinks = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("bg-white", "text-blue-700", "shadow");
        tablinks[i].classList.add("text-slate-600");
    }
    
    const targetTab = document.getElementById(tabName);
    targetTab.classList.add("active");
    targetTab.style.display = "block"; 
    
    evt.currentTarget.classList.add("bg-white", "text-blue-700", "shadow");
    evt.currentTarget.classList.remove("text-slate-600");

    
}

async function analyzeSequence(x) {
    const seq = document.getElementById("sequence").value;
    const cleanSeq = parseFASTA(seq);

    if (!cleanSeq) {
        document.getElementById("result").textContent = "⚠️ Séquence vide.";
        return;
    }
    const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({sequence: cleanSeq})
    });
    const result = await response.json(); 
    if (x == 1) {
        document.getElementById("result").textContent = formatResult(result);
    }
}

function formatResult(result) {
    const resElement = document.getElementById("result");
    
    if (result.valid == "false") {
        resElement.classList.add("text-red-400");
        return `⚠️ Error: DNA sequence is not valid `;
    }
   
    if (result.valid === "true") {
        resElement.classList.remove("text-red-400");

        // Analyse des Codons 
        let codonsText = "\n";
        if (result.codons.length !== 0) {
            result.codons.forEach(c => {
                codonsText += `  ${c.codon.padEnd(5)} | Type: ${c.type.padEnd(7)} | Pos: ${c.position}\n`;
            });
        } else {
            codonsText = " none\n";
        }

        let orfText = "\n";
        if (result.orfs.length !== 0) {
            result.orfs.forEach((orf, index) => {
                orfText += ` > ORF ${index + 1} \n`;
                orfText += `   Pos: ${orf.start_pos} | Len: ${orf.length} nt\n`;
                orfText += `   DNA: ${orf.sequence}\n`;
                orfText += `   PRO: ${orf.protein} \n\n`;
            });
        } else {
            orfText = " none\n";
        }

        
        return `[ BASIC STATISTICS ] 
Length : ${result.length} nt
GC%    : ${result.gc_percent}%
AT%    : ${result.at_percent}%
Counts : A:${result.counts.A} T:${result.counts.T} C:${result.counts.C} G:${result.counts.G}

[ SEQUENCES ] 
Reverse Complement : ${result.reverse_complement}
Global Translation : ${result.proteine}

[ CODON ANALYSIS ] ${codonsText}
[ DETECTED ORFS ] (Total: ${result.orf_count})  ${orfText}`;
    }
}




// part 2 comparaison

// Permet de charger un fichier dans n'importe quel champ (A ou B)
function handleCompareUpload(event, targetId, nameId) {
    const file = event.target.files[0];
    if (!file) return;

    // Affiche le nom du fichier
    const nameLabel = document.getElementById(nameId);
    if (nameLabel) nameLabel.textContent = file.name;

    const reader = new FileReader();
    reader.onload = function(e) {
        const rawContent = e.target.result;
        // On nettoie le contenu immédiatement (enlève les en-têtes FASTA)
        const cleanedContent = parseFASTA(rawContent);
        document.getElementById(targetId).value = cleanedContent;
    };
    reader.readAsText(file);
    
    // Reset l'input pour permettre de re-charger le même fichier si besoin
    event.target.value = '';
}





async function compareSequences() {
    const seqA = parseFASTA(document.getElementById("seqA").value);
    const seqB = parseFASTA(document.getElementById("seqB").value);
    const resElement = document.getElementById("result");
    const vizElement = document.getElementById("alignment-result"); 

    if (!seqA || !seqB) {
        resElement.textContent = "⚠️ Veuillez entrer deux séquences pour comparer.";
        return;
    }

    try {
        const response = await fetch("/api/compare", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ sequenceA: seqA, sequenceB: seqB })
        });
        
        const result = await response.json();
        
        resElement.textContent = formatComparisonResult(result);
        
        if (vizElement && result.alignment) {
            const { lineA, symbols, lineB } = result.alignment;

            const formatLine = (text, syms) => {
                return text.split('').map((char, i) => {
                    const s = syms[i];
                    if (s !== '|') {
                     return `<span style="color: #ff4d4f; font-weight: bold;">${char}</span>`;
                    }
                    return `<span>${char}</span>`;
                }).join(' ');
            };

            const formattedSymbols = symbols.split('').map((s, i) => {
                // On colorie le symbole lui-même s'il indique une différence
                if (s !== '|') {
                  return `<span style="color: #ff4d4f; font-weight: bold;">${s === ' ' ? '*' : s}</span>`;
                }
                return `<span style="opacity: 0.3;">|</span>`;
            }).join(' ');
            vizElement.innerHTML = `REF: ${formatLine(lineA, symbols)}\n     ${formattedSymbols}\nMUT: ${formatLine(lineB, symbols)}`;
        }
 
        //protein alignement
        const protVizElement = document.getElementById("protein-alignment-result");

        if (protVizElement && result.prot_alignment) {
            const { listA, symbols, listB } = result.prot_alignment;
            let htmlOutput = `<div style="display: flex; font-family: 'JetBrains Mono', monospace; gap: 8px; overflow-x: auto; padding-bottom: 10px;">`;
            for (let i = 0; i < symbols.length; i++) {
                const aaA = listA[i] || "---";
                const sym = symbols[i];
                const aaB = listB[i] || "---";
                const isMut = (sym === "*");
                // On crée une colonne verticale pour chaque codon
                const aaColor = isMut ? '#ff4d4f' : '#ffffff'; // Rouge si muté, Blanc si normal
                const symColor = isMut ? '#ff4d4f' : 'rgba(255, 255, 255, 0.4)'; // Rouge si muté
                const weight = isMut ? 'bold' : 'normal';
        htmlOutput += `
            <div style="display: flex; flex-direction: column; align-items: center; min-width: 40px; padding: 4px; border-radius: 4px; background: ${isMut ? 'rgba(255, 77, 79, 0.1)' : 'transparent'}">
                <span style="color: ${aaColor}; font-weight: ${weight};">${aaA}</span>
                <span style="color: ${symColor}; font-weight: bold; margin: 2px 0;">${sym}</span>
                <span style="color: ${aaColor}; font-weight: ${weight};">${aaB}</span>
            </div>`;
            }

         htmlOutput += `</div>`;
         protVizElement.innerHTML = htmlOutput;
         protVizElement.style.background = "#0f172a"; 
        }
    } catch (error) {
        resElement.textContent = "❌ Erreur de communication avec le serveur.";
    }
}


function formatComparisonResult(result) {
    if (result.valid === "false") return `❌ Erreur : ${result.error}`;

    let output = `╔══════════════════════════════════════════╗\n║       RAPPORT DE COMPARAISON         ║\n╚══════════════════════════════════════════╝\n\n`;
    
    output += `> . VALIDATION DES LONGUEURS \n  • Longueur Séquence A : ${result.lengthA} nt \n  • Longueur Séquence B : ${result.lengthB} nt \n  • Statut             : ${result.same_length ? "✅ Identiques" : "⚠️ Différentes"}\n`;

    output += `\n> . ANALYSE BIOLOGIQUE  \n`;
    output += `  [ SÉQUENCES PROTÉIQUES ] \n  Prot A : ${result.protA}\n  Prot B : ${result.protB}\n\n`;

    
    if (result.orf_diffs === "FRAMESHIFT") {
        output += `  ⚠️ IMPACT : FRAMESHIFT (Décalage critique du cadre de lecture). \n`;
    } 
    else if (result.orf_diffs === "IN-FRAME-INDEL") {
        output += `  ℹ️ IMPACT : IN-FRAME-INDEL (Insertion ou Délétion de codons entiers).\n`;
    }
    else if (Array.isArray(result.orf_diffs)) {
        if (result.orf_diffs.length > 0) {
            output += `  Codon | ADN (Ref ➔ Mut) | AA (Ref ➔ Mut) | Impact \n`;
            output += `  ------|-----------------|----------------|----------\n`;
            result.orf_diffs.forEach(o => {
                let codonComp = `${o.ref_codon} ➔ ${o.mut_codon}`.padEnd(15);
                let aaComp = `${o.ref_aa} ➔ ${o.mut_aa}`.padEnd(14);
                output += `  #${o.pos_codon.toString().padEnd(4)} | ${codonComp} | ${aaComp} | ${o.impact}\n`;
            });
        } else {
            output += `  ✅ Aucun changement détecté dans la séquence protéique.\n`;
        }
    }

    return output;
}



//     3D







async function loadStructureFromSequence() {
    const dnaInput = document.getElementById("sequence").value.toUpperCase().replace(/\s/g, '');
    const viewport = document.getElementById("viewport");
    
    if (!dnaInput || dnaInput.length < 20) {
        alert("⚠️ Colle une séquence ADN d'abord !");
        return;
    }

    if (stage) { stage.dispose(); }
    viewport.innerHTML = "<div id='loader' style='color:white; padding:20px;'>🧬 Identification de la séquence...</div>";
    stage = new NGL.Stage("viewport", { backgroundColor: "#0f172a" });

    let pdbID = "";
    let name = "";

    // Signature Hémoglobine
    if (dnaInput.includes("ATGGTGCACCTGACTCCTGAGGAGAAG")) {
        pdbID = "1HHO";
        name = "Hémoglobine Bêta";
    } 
    // Signature Insuline
    else if (dnaInput.includes("ATGGCCCTGTGGATGCGCCTCCTG")) {
        pdbID = "1TRZ";
        name = "Insuline Humaine";
    }
    // Signature Glucagon
    else if (dnaInput.includes("ATGCATTCACAGGGCACATTCACC")) {
        pdbID = "1GCN";
        name = "Glucagon";
    }

    // 3. AFFICHAGE DU RÉSULTAT
    if (pdbID !== "") {
        // Chargement depuis le serveur mondial PDB (très stable)
        stage.loadFile(`https://files.rcsb.org/download/${pdbID}.pdb`).then(function (o) {
            o.addRepresentation("cartoon", { color: "chainid" });
            o.autoView();
            document.getElementById('loader').remove();
            
            const badge = document.createElement("div");
            badge.style = "position:absolute; top:10px; left:10px; z-index:100; background:#10b981; color:white; padding:8px 15px; border-radius:10px; font-weight:bold; font-family:sans-serif;";
            badge.innerHTML = `✅ Structure détectée : ${name}`;
            viewport.appendChild(badge);
        });
    } else {
        // SI RIEN N'EST TROUVÉ
        viewport.innerHTML = `
            <div style='color:white; padding:40px; text-align:center; font-family:sans-serif;'>
                <h3 style='color:#f87171;'>❌ PROTÉINE INCONNUE</h3>
                <p>La séquence ADN ne correspond à aucune protéine enregistrée.</p>
            </div>`;
    }
}
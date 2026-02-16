# DNA-Sequence-Analysis--Mutation-Detection

BioDNA Analyzer — DNA Sequence Analysis & Mutation Detection

## Overview

BioDNA Analyzer is a bioinformatics web application for DNA sequence analysis and mutation detection. The system processes DNA sequences in FASTA format, performs biological analysis, detects mutations, and visualizes protein structures. The application supports both single sequence analysis and comparison between two sequences to study mutation effects on proteins.

## Features

### Single DNA Sequence Analysis
- DNA sequence validation (A, T, C, G)
- Sequence statistics (length, nucleotide counts, GC%, AT%)
- Reverse complement generation
- Codon detection (start and stop codons)
- ORF detection
- DNA to protein translation

### Sequence Comparison
- Detection of substitutions, insertions, and deletions
- Mutation classification (transition, transversion, insertion, deletion)
- Mutation rate calculation
- Protein comparison
- Mutation impact analysis (silent, missense, nonsense, frameshift)

### Visualization
- DNA sequence alignment view
- Mutation highlighting
- Protein alignment visualization
- 3D protein structure visualization

## Technologies Used

- **Python (Flask)** — backend processing
- **JavaScript (Vanilla JS)** — frontend logic
- **HTML**
- **Tailwind CSS** — UI styling
- **NGL Viewer** — 3D molecular visualization

## Input Format

The application accepts DNA sequences in FASTA format.

## Purpose

An academic project designed to apply theoretical bioinformatics knowledge to practical genetic sequence analysis, simulating professional workflows used in research laboratories for mutation detection and biological interpretation.

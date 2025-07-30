# auto\_HMM\_beta

**Author:** Marcin Gradowski, Marianna Krysińska

## Description

The script **auto\_HMM\_beta.py** automates the processing of protein sequences in FASTA format. It splits sequences into shorter and longer ones based on a specified length threshold, clusters similar sequences using CD-HIT, aligns them with Clustal Omega, and builds Hidden Markov Model (HMM) profiles using HMMER.

## Requirements

* Python 3.6+
* Biopython
* CD-HIT
* Clustal Omega (clustalo)
* HMMER (hmmbuild)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/auto_HMM_beta.git
   cd auto_HMM_beta
   ```
2. Install Python dependencies:

   ```bash
   pip install biopython
   ```
3. Ensure the following tools are installed and accessible in your PATH:

   ```bash
   cd-hit clustalo hmmbuild
   ```

## Usage

```bash
python auto_HMM_beta.py
```

Default parameters:

* `cutoff` (sequence length): 50
* `cd_hit_threshold` (CD-HIT similarity threshold): 0.80
* `cd_hit_word_length` (CD-HIT word length): 5

You can modify these parameters directly in the script or by specifying command-line arguments if implemented.

## Directory Structure

```
/ShortsAndLong/      # Results of sequence splitting
/Clustered/          # CD-HIT clustering outputs
/ClustalO/           # Aligned FASTA files
/HMM/                # Generated HMM profiles
HMM_names.txt        # List of HMM profile names and metadata
```

## License

BSD 2-Clause "Simplified" License

#!/usr/bin/env bash
set -euo pipefail

embeddings=${1:-data/results/nextflow/molecule_embeddings.csv}
labels=${2:-data/rawdata/HDD/colData.tsv}
outdir=${3:-data/results/nextflow}
notebook=${4:-workflow/qc/embedding_qc.ipynb}

for path in "$embeddings" "$labels" "$notebook"; do
    if [[ ! -f "$path" ]]; then
        printf 'Missing %s\nUsage: pixi run qc [embeddings.csv [colData.tsv [output-dir]]]\n' "$path" >&2
        exit 1
    fi
done

mkdir -p "$outdir"
export MOLJEPA_QC_EMBEDDINGS="$(cd "$(dirname "$embeddings")" && pwd)/$(basename "$embeddings")"
export MOLJEPA_QC_LABELS="$(cd "$(dirname "$labels")" && pwd)/$(basename "$labels")"
export MPLBACKEND=Agg
python -m jupyter nbconvert --to html --execute \
    --ExecutePreprocessor.kernel_name=python3 \
    --ExecutePreprocessor.timeout=1800 \
    --output embedding_qc.html --output-dir "$outdir" "$notebook"

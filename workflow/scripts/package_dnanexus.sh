#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p data/dnanexus
bundle=$(mktemp -d "$PWD/data/dnanexus/source.XXXXXX")
mkdir -p "$bundle/config" "$bundle/workflow/scripts" "$bundle/workflow/qc"
cp main.nf nextflow.config nextflow_schema.json "$bundle/"
cp config/downloads.yaml config/embeddings.yaml "$bundle/config/"
cp workflow/scripts/download.py workflow/scripts/construct_drug_universe.py \
    workflow/scripts/generate_embeddings.py workflow/scripts/render_qc.sh "$bundle/workflow/scripts/"
cp workflow/qc/embedding_qc.ipynb "$bundle/workflow/qc/"
COPYFILE_DISABLE=1 tar -czf "${bundle}.tar.gz" -C "$bundle" .
printf 'Source bundle: %s\n' "$bundle"
printf 'Source archive: %s.tar.gz\n' "$bundle"

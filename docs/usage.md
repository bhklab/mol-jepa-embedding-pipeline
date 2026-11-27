# Usage Guide

Start with [Running with Nextflow](README.md#running-with-nextflow) for local
runs, output paths and QC. `config/downloads.yaml` defines the source tables;
`config/embeddings.yaml` selects the compute device. To reuse downloaded
inputs, pass the directory containing the `HDD/` subdirectory as
`--raw_data`.

See [Deploying on DNAnexus](dnanexus.md) for container and applet commands.

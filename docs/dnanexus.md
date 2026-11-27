# Deploying on DNAnexus

The Docker image contains the locked Linux Pixi environment. The applet contains the Nextflow workflow, config, Python scripts, and QC notebook. Build and upload them separately.

1. Build a Linux AMD64 image and export it in Docker archive format:

   ```bash
   mkdir -p data/dnanexus
   docker build --platform linux/amd64 -t mol-jepa:v1 .
   docker save -o data/dnanexus/mol-jepa-v1.tar mol-jepa:v1
   ```

   The current Linux lockfile is CPU-only. The image does not contain the HDD inputs or Mol-JEPA weights. By default the job downloads the HDD files from Zenodo and the model from Hugging Face, which requires outbound network access.

2. Upload the archive to a DNAnexus project that can build and run Nextflow applets. Record the returned file ID:

   ```bash
   dx login
   dx mkdir -p 'project-PROJECT_ID:/containers'
   dx mkdir -p 'project-PROJECT_ID:/applets'
   dx upload data/dnanexus/mol-jepa-v1.tar \
     --path 'project-PROJECT_ID:/containers/' --brief
   ```

3. Package the source and build the applet. Replace `source.XXXXXX` with the directory printed by the packaging script:

   ```bash
   bash workflow/scripts/package_dnanexus.sh
   dx build --nextflow data/dnanexus/source.XXXXXX \
     --profile dnanexus --nextflow-version 25.10 \
     --extra-args '{"name":"mol-jepa-embedding-pipeline","title":"Mol-JEPA Embedding Pipeline","summary":"Generate Mol-JEPA embeddings for HDD compounds."}' \
     --destination 'project-PROJECT_ID:/applets/mol-jepa-embedding-pipeline'
   ```

4. Run the applet and pass the image file URI. Use a relative `outdir`. For a first test, upload a small list of eligible HDD IDs (with SMILES and PubChem CID) and pass it as `molset`:

   ```bash
   dx run applet-APPLET_ID \
     -icontainer_image='dx://project-PROJECT_ID:file-IMAGE_ID' \
     -imolset='project-PROJECT_ID:file-MOLSET_ID' \
     -ioutdir=results --destination 'project-PROJECT_ID:/'
   ```

   Check that `molecule_embeddings.csv` has exactly the test IDs once each and 512 finite values per ID. Open or download the `embedding_qc.html` output. Small runs omit panels without enough matched labels. Omit `molset` for the full universe.

See the [DNAnexus Nextflow guide](https://documentation.dnanexus.com/user/running-apps-and-workflows/running-nextflow-pipelines) for platform setup and Docker image options.

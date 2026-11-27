nextflow.enable.dsl = 2

process DOWNLOAD_INPUTS {
    cpus 1
    memory '1 GB'

    input:
    path downloads, stageAs: 'config/downloads.yaml'
    path downloader

    output:
    path 'data/rawdata', emit: raw_data

    script:
    """
    mkdir -p data/rawdata
    export DMP_PROJECT_ROOT="\$PWD"
    python '${downloader}'
    """
}


process CURATE_DRUG_UNIVERSE {
    cpus 4
    memory '8 GB'
    publishDir params.outdir, mode: 'copy', overwrite: true

    input:
    path raw_data, stageAs: 'data/rawdata'
    path curator

    output:
    path 'data/procdata/molecule_universe.txt', emit: molset


    script:
    """
    mkdir -p data/procdata
    export DMP_PROJECT_ROOT="\$PWD"
    export OMP_NUM_THREADS=${task.cpus}
    export MKL_NUM_THREADS=${task.cpus}
    python '${curator}'
    """

}


process GENERATE_EMBEDDINGS {
    cpus 4
    memory '8 GB'
    publishDir params.outdir, mode: 'copy', overwrite: true

    input:
    path raw_data, stageAs: 'data/rawdata'
    path mol_universe, stageAs: 'data/procdata/molecule_universe.txt'
    path embeddings, stageAs: 'config/embeddings.yaml'
    path scripts

    output:
    path 'molecule_embeddings.csv', emit: embeddings

    script:
    """
    mkdir -p data/results
    export DMP_PROJECT_ROOT="\$PWD"
    export OMP_NUM_THREADS=${task.cpus}
    export MKL_NUM_THREADS=${task.cpus}
    python '${scripts}/generate_embeddings.py'
    mv data/results/molecule_embeddings.csv .
    """
}

process RENDER_QC {
    cpus 4
    memory '8 GB'
    publishDir params.outdir, mode: 'copy', overwrite: true

    input:
    path embeddings, stageAs: 'molecule_embeddings.csv'
    path labels, stageAs: 'colData.tsv'
    path notebook
    path renderer

    output:
    path 'embedding_qc.html', emit: qc

    script:
    """
    export OMP_NUM_THREADS=${task.cpus}
    export MKL_NUM_THREADS=${task.cpus}
    export OPENBLAS_NUM_THREADS=${task.cpus}
    bash '${renderer}' molecule_embeddings.csv colData.tsv . '${notebook}'
    """
}


workflow {
    if (params.help) {
        log.info '''
Run: pixi run pipeline [options] [-resume]

  --raw_data DIR          Reuse downloaded HDD inputs
  --molset FILE           Reuse a prepared molecule universe
  --downloads FILE        Download configuration (default: config/downloads.yaml)
  --embeddings FILE       Model configuration (default: config/embeddings.yaml)
  --outdir DIR            Published results directory
  --container_image IMAGE Docker image or DNAnexus Docker archive URI

Local tasks use Pixi. The docker and dnanexus profiles use --container_image.
Keep data/work/ and .nextflow/ to resume local tasks.
'''
    } else {
        selected_profiles = workflow.profile.tokenize(',')
        if (selected_profiles.any { it in ['docker', 'dnanexus'] } && !params.container_image) {
            error 'Supply --container_image with a Docker image or DNAnexus Docker archive URI.'
        }
        if (selected_profiles.contains('dnanexus') &&
            (params.outdir.startsWith('/') || params.outdir.contains('://'))) {
            error 'Use a relative output path with the dnanexus profile.'
        }

        downloads = file(params.downloads, checkIfExists: true)
        embeddings = file(params.embeddings, checkIfExists: true)
        scripts = file("${projectDir}/workflow/scripts", checkIfExists: true)

        if (params.raw_data) {
            raw_data = Channel.value(file(params.raw_data, checkIfExists: true))
        } else {
            raw_data = DOWNLOAD_INPUTS(downloads, file("${projectDir}/workflow/scripts/download.py"))
        }

        if (params.molset) {
            molset = Channel.value(file(params.molset, checkIfExists: true))
        } else {
            molset = CURATE_DRUG_UNIVERSE(raw_data, file("${projectDir}/workflow/scripts/construct_drug_universe.py"))
        }

        generated = GENERATE_EMBEDDINGS(raw_data, molset, embeddings, scripts)
        labels = raw_data.map { it.resolve('HDD/colData.tsv') }
        RENDER_QC(
            generated.embeddings,
            labels,
            file("${projectDir}/workflow/qc/embedding_qc.ipynb", checkIfExists: true),
            file("${projectDir}/workflow/scripts/render_qc.sh", checkIfExists: true)
        )
    }
}

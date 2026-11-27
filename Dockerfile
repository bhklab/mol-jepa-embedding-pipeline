FROM ghcr.io/prefix-dev/pixi:0.85.0 AS build

WORKDIR /opt/mol-jepa
COPY pixi.toml pixi.lock ./
RUN pixi install --locked -e default

FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/mol-jepa/.pixi/envs/default /opt/mol-jepa/.pixi/envs/default
ENV PATH="/opt/mol-jepa/.pixi/envs/default/bin:${PATH}" \
    SSL_CERT_FILE="/opt/mol-jepa/.pixi/envs/default/ssl/cacert.pem" \
    HF_HOME="/tmp/mol-jepa-hf" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python -c 'import pandas, torch, torch_geometric, molfeat, rdkit, transformers, tqdm, yaml, damply; assert torch.version.cuda is None'
# Nextflow supplies the working directory and task command.
WORKDIR /tmp
CMD ["bash"]

# Dockerfile for piscem.build GenePattern Module
FROM python:3.11-slim

# Metadata labels
LABEL maintainer="GenePattern"
LABEL module.name="piscem.build"
LABEL module.version="0.16.2"
LABEL module.language="python"

# Set working directory
WORKDIR /module

# Install system dependencies required for Miniconda and piscem
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        curl \
        ca-certificates \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda and piscem from bioconda (with TOS acceptance)
# This follows the specific requirement to use conda and not compile from source
RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true /opt/conda/bin/conda install -y -c conda-forge -c bioconda piscem==0.16.2 && \
    ln -s /opt/conda/bin/piscem /usr/local/bin/piscem && \
    /opt/conda/bin/conda clean -a -y

# Update PATH to include conda binaries
ENV PATH="/opt/conda/bin:$PATH"

# Copy wrapper script
COPY piscem_build_wrapper.py /module/
COPY manifest /module/

# Set execute permissions on wrapper script
RUN chmod +x /module/piscem_build_wrapper.py

# Environment variables for resource management
ENV MODULE_CPU_CORES=4
ENV MODULE_MEMORY=8192
ENV MODULE_NAME=piscem.build

# Set entrypoint
CMD ["/bin/bash"]
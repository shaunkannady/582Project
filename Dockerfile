# Use a base image
FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

# Install essential packages and dependencies
RUN apt-get update && apt-get install -y \
    git \
    sudo \
    curl \
    libglew-dev libglfw3-dev libglm-dev libgl-dev libgl1-mesa-dev cmake \
    vim \
    build-essential \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Set CUDA environment variables
ENV PATH=/usr/local/cuda/bin:/opt/nsight-systems/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
ENV CUDA_HOME=/usr/local/cuda
ENV NVIDIA_VISIBLE_DEVICES=GPU-546f2736-c9ab-49ce-b280-a0e70c5d11be,
ENV NVIDIA_DRIVER_CAPABILITIES=all

# Set working directory
WORKDIR /Titan

# Clone the repository, run install commands in container after
RUN git clone https://github.com/jacobaustin123/Titan.git .

CMD ["/bin/bash"]

# Run Titan installation
RUN ./setup.sh

COPY CMakeLists.txt /Titan/CMakeLists.txt

#include <cuda_runtime.h>
#include <iostream>

int main() {
    int device_count;
    cudaGetDeviceCount(&device_count);

    if (device_count == 0) {
        std::cout << "No CUDA devices found." << std::endl;
        return 1;
    }

    for (int i = 0; i < device_count; i++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, i);
        std::cout << "GPU " << i << ": " << prop.name << std::endl;
    }
    return 0;
}

#include <CL/cl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int WIDTH =1024;
int HEIGHT =1024;
int EXTRA_ITER= 5000;
// Hata kontrol fonksiyonu
void checkError(cl_int err, const char* message) {
    if (err != CL_SUCCESS) {
        printf("OpenCL hata: %s (%d)\n", message, err);
        exit(EXIT_FAILURE);
    }
}

// OpenCL kernel: matris üzerinde yoğun hesaplama
const char* kernelSource =
"__kernel void heavy_matrix(__global float* A, __global float* B, __global float* C, int extraIter, int width) {\n"
"    int x = get_global_id(0);\n"
"    int y = get_global_id(1);\n"
"    if (x >= width || y >= width) return;\n"
"    int idx = y * width + x;\n"
"    float sum = 0.0f;\n"
"    for(int k = 0; k < extraIter; k++) {\n"
"        sum += sin(A[idx] + k*0.001f) * cos(B[idx] + k*0.001f);\n"
"    }\n"
"    C[idx] = sum;\n"
"}\n";

int main() {
    cl_int err;

    // Platform ve cihaz
    cl_uint numPlatforms;
    checkError(clGetPlatformIDs(0, NULL, &numPlatforms), "clGetPlatformIDs");
    cl_platform_id* platforms = (cl_platform_id*)malloc(sizeof(cl_platform_id) * numPlatforms);
    checkError(clGetPlatformIDs(numPlatforms, platforms, NULL), "clGetPlatformIDs");

    cl_uint numDevices;
    checkError(clGetDeviceIDs(platforms[1], CL_DEVICE_TYPE_GPU, 0, NULL, &numDevices), "clGetDeviceIDs");
    cl_device_id* devices = (cl_device_id*)malloc(sizeof(cl_device_id) * numDevices);
    checkError(clGetDeviceIDs(platforms[1], CL_DEVICE_TYPE_GPU, numDevices, devices, NULL), "clGetDeviceIDs");

    cl_device_id device = devices[1]; // 2. GPU
    char name[128]; clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(name), name, NULL);
    printf("Seçilen GPU: %s\n", name);

    cl_context context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    checkError(err, "clCreateContext");

    cl_command_queue queue = clCreateCommandQueue(context, device, 0, &err);
    checkError(err, "clCreateCommandQueue");

    // Matrisleri oluştur
    float* hA = (float*)malloc(sizeof(float) * WIDTH * HEIGHT);
    float* hB = (float*)malloc(sizeof(float) * WIDTH * HEIGHT);
    float* hC = (float*)malloc(sizeof(float) * WIDTH * HEIGHT);
    for(int i=0;i<WIDTH*HEIGHT;i++){ hA[i] = rand()%100/100.0f; hB[i] = rand()%100/100.0f; }

    cl_mem dA = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(float)*WIDTH*HEIGHT, hA, &err);
    checkError(err, "clCreateBuffer A");
    cl_mem dB = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(float)*WIDTH*HEIGHT, hB, &err);
    checkError(err, "clCreateBuffer B");
    cl_mem dC = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(float)*WIDTH*HEIGHT, NULL, &err);
    checkError(err, "clCreateBuffer C");

    cl_program program = clCreateProgramWithSource(context, 1, &kernelSource, NULL, &err);
    checkError(err, "clCreateProgramWithSource");

    err = clBuildProgram(program, 1, &device, NULL, NULL, NULL);
    if(err != CL_SUCCESS){
        size_t logSize; clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, NULL, &logSize);
        char* log = (char*)malloc(logSize);
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, logSize, log, NULL);
        printf("Build hatası:\n%s\n", log);
        free(log); exit(EXIT_FAILURE);
    }

    cl_kernel kernel = clCreateKernel(program, "heavy_matrix", &err);
    checkError(err, "clCreateKernel");

    checkError(clSetKernelArg(kernel, 0, sizeof(cl_mem), &dA), "clSetKernelArg A");
    checkError(clSetKernelArg(kernel, 1, sizeof(cl_mem), &dB), "clSetKernelArg B");
    checkError(clSetKernelArg(kernel, 2, sizeof(cl_mem), &dC), "clSetKernelArg C");
    int extra = EXTRA_ITER;
    checkError(clSetKernelArg(kernel, 3, sizeof(int), &extra), "clSetKernelArg extraIter");
    int width = WIDTH;
    checkError(clSetKernelArg(kernel, 4, sizeof(int), &width), "clSetKernelArg width");

    size_t globalSize[2] = {WIDTH, HEIGHT};
    printf("Kernel çalıştırılıyor...\n");
    err = clEnqueueNDRangeKernel(queue, kernel, 2, NULL, globalSize, NULL, 0, NULL, NULL);
    checkError(err, "clEnqueueNDRangeKernel");

    clFinish(queue);

    checkError(clEnqueueReadBuffer(queue, dC, CL_TRUE, 0, sizeof(float)*WIDTH*HEIGHT, hC, 0, NULL, NULL),
               "clEnqueueReadBuffer");

    printf("Örnek sonuçlar:\n");
    for(int i=0;i<10;i++) printf("%.4f ", hC[i]);
    printf("\n");

    // Temizlik
    free(hA); free(hB); free(hC);
    clReleaseMemObject(dA); clReleaseMemObject(dB); clReleaseMemObject(dC);
    clReleaseKernel(kernel); clReleaseProgram(program);
    clReleaseCommandQueue(queue); clReleaseContext(context);
    free(platforms); free(devices);

    return 0;
}

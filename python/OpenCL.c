#include <stdio.h>
#include <stdlib.h>
#include <CL/cl.h>

const char* kernelSource = 
"__kernel void add_one(__global float* data) {   \n"
"    int id = get_global_id(0);                   \n"
"    data[id] = data[id] + 1.0f;                  \n"
"}                                               \n";

int main() {
    const size_t count = 268435456; // 1 GB float sayısı
    float* data = (float*)malloc(sizeof(float) * count);
    if (!data) {
        printf("Bellek ayırma başarısız!\n");
        return 1;
    }

    for (size_t i = 0; i < count; i++) data[i] = (float)i;

    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_program program;
    cl_kernel kernel;
    cl_mem buffer;
    cl_int err;

    err = clGetPlatformIDs(0, &platform, NULL);
    err |= clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 0, &device, NULL);
    if (err != CL_SUCCESS) {
        printf("Platform veya GPU device bulunamadi!\n");
        free(data);
        return 1;
    }

    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    queue = clCreateCommandQueue(context, device, 0, &err);

    program = clCreateProgramWithSource(context, 1, &kernelSource, NULL, &err);
    err = clBuildProgram(program, 1, &device, NULL, NULL, NULL);
    if (err != CL_SUCCESS) {
        char log[2048];
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, sizeof(log), log, NULL);
        printf("Build error:\n%s\n", log);
        free(data);
        return 1;
    }

    kernel = clCreateKernel(program, "add_one", &err);
    buffer = clCreateBuffer(context, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, sizeof(float)*count, data, &err);

    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &buffer);

    size_t global_work_size = count;
    err = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    if (err != CL_SUCCESS) {
        printf("Kernel çalıştırma hatası: %d\n", err);
        free(data);
        return 1;
    }

    err = clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, sizeof(float)*count, data, 0, NULL, NULL);
    if (err != CL_SUCCESS) {
        printf("Sonuçları okuma hatası: %d\n", err);
        free(data);
        return 1;
    }

    for (int i = 0; i < 10; i++) {
        printf("data[%d] = %f\n", i, data[i]);
    }

    clReleaseMemObject(buffer);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    free(data);

    return 0;
}

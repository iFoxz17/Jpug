#include "dct.h"

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <vector>

#define MAX_VALUE 255

bool test_dct(double * (*dct_functor)(double*, size_t, DCTSupport*), bool verbose = true) {

    if (verbose) {
        std::cout << "Running DCT test" << std::endl;
    }

    double v[] = {231, 32, 233, 161, 24, 71, 140, 245};
    double expected[] = {401, 6.6, 109, -112, 65.4, 121, 116, 28.8};
    double eps = 1e-0;

    double * dct_v = dct_functor(v, 8, nullptr);

    if (verbose) {
        std::cout << "DCT result: ";
        for (size_t i = 0; i < 8; ++i) {
            std::cout << dct_v[i] << " ";
        }
        std::cout << std::endl;
    }

    for (size_t i = 0; i < 8; ++i) {
        if (std::abs(dct_v[i] - expected[i]) > eps) {
            delete[] dct_v;
            return false;
        }
    }
    delete[] dct_v;

    return true;
}

bool test_dct2(double ** (*dct2_functor)(double**, size_t, size_t), bool verbose = true) {

    if (verbose) {
        std::cout << "Running DCT2 test" << std::endl;
    }

    double values[8][8] = {
        {231, 32, 233, 161, 24, 71, 140, 245},
        {247, 40, 248, 245, 124, 204, 36, 107},
        {234, 202, 245, 167, 9, 217, 239, 173},
        {193, 190, 100, 167, 43, 180, 8, 70},
        {11, 24, 210, 177, 81, 243, 8, 112},
        {97, 195, 203, 47, 125, 114, 165, 181},
        {193, 70, 174, 167, 41, 30, 127, 245},
        {87, 149, 57, 192, 65, 129, 178, 228}
    };

    double expected[8][8] = {
        {1.11e+03,  4.40e+01,  7.59e+01, -1.38e+02, 3.50e+00, 1.22e+02, 1.95e+02, -1.01e+02},
        {7.71e+01,  1.14e+02, -2.18e+01, 4.13e+01, 8.77e+00, 9.90e+01, 1.38e+02, 1.09e+01},
        {4.48e+01, -6.27e+01, 1.11e+02, -7.63e+01, 1.24e+02, 9.55e+01, -3.98e+01, 5.85e+01},
        {-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01, 2.66e+01, -3.68e+01, 6.61e+01, 1.25e+02},
        {-1.09e+02, -4.33e+01, -5.55e+01, 8.17e+00, 3.02e+01, -2.86e+01, 2.44e+00, -9.41e+01},
        {-5.38e+00, 5.66e+01, 1.73e+02, -3.54e+01, 3.23e+01, 3.34e+01, -5.81e+01, 1.90e+01},
        {7.88e+01, -6.45e+01, 1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02, 3.98e+01},
        {1.97e+01, -7.81e+01, 9.72e-01, -7.23e+01, -2.15e+01, 8.13e+01, 6.37e+01, 5.90e+00}
    };

    double **v = new double*[8];

    for (int i = 0; i < 8; ++i) {
        v[i] = new double[8]();
    }
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j) {
            v[i][j] = values[i][j];
        }
    }

    double eps = 10e1;

    double ** dct2_v = dct2_functor(v, 8, 8);

    if (verbose) {
        std::cout << "DCT2 result: " << std::endl;
        for (size_t i = 0; i < 8; ++i) {
            for (size_t j = 0; j < 8; ++j) {
                std::cout << dct2_v[i][j] << " ";
            }
        std::cout << std::endl;
        }
    }

    for (size_t i = 0; i < 8; ++i) {
        for (size_t j = 0; j < 8; ++j) {
            if (std::abs(dct2_v[i][j] - expected[i][j]) > eps) {
                for (int i = 0; i < 8; ++i) {
                    delete[] v[i];
                    delete[] dct2_v[i];
                }
                delete[] v;
                delete[] dct2_v;
                return false;
            }
        }
    }

    for (int i = 0; i < 8; ++i) {
        delete[] v[i];
        delete[] dct2_v[i];
    }
    delete[] v;
    delete[] dct2_v;

    return true;
}

int main() {
    
    /*
    double * (*dct_pointer)(double*, size_t, DCTSupport*) = nullptr;
    dct_pointer = dct;

    bool passed = test_dct(dct_pointer, false);
    if (passed) {
        std::cout << "DCT test passed" << std::endl;
    } else {
        std::cout << "DCT test failed" << std::endl;
    }

    double ** (*dct2_pointer)(double**, size_t, size_t) = nullptr;
    dct2_pointer = dct2;

    passed = test_dct2(dct2_pointer);
    if (passed) {
        std::cout << "DCT2 test passed" << std::endl;
    } else {
        std::cout << "DCT2 test failed" << std::endl;
    }
    
    */
    const unsigned int N_[] = {25, 50, 100, 200, 400, 800, 1600}; 
    const unsigned int N = sizeof(N_) / sizeof(N_[0]);

    std::vector<std::chrono::milliseconds> times;

    std::srand(std::time(nullptr));

    double **v = nullptr;

    for (size_t i = 0; i < N; ++i) {
        std::cout << "Running DCT2 test for matrix of size " << N_[i] << "x" << N_[i] << std::endl;

        v = new double*[N_[i]];
        for (size_t j = 0; j < N_[i]; ++j) {
            v[j] = new double[N_[i]];
            for (size_t k = 0; k < N_[i]; ++k) {
                v[j][k] = std::rand() / static_cast<double>(RAND_MAX) * MAX_VALUE;
            }
        }

        auto start = std::chrono::steady_clock::now();
        double ** result = dct2(v, N_[i], N_[i]);
        auto end = std::chrono::steady_clock::now();

        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        times.push_back(duration);

        std::cout << "DCT2 test for matrix of size " << N_[i] << "x" << N_[i] << " completed in " << duration.count() << " ms" << std::endl;

        for (size_t j = 0; j < N_[i]; ++j) {
            delete[] result[j];
        }
        delete[] result;

        for (size_t j = 0; j < N_[i]; ++j) {
            delete[] v[j];
        }
        delete[] v;

    }

    std::cout << std::endl << "DCT2 test results:" << std::endl;
    for (size_t i = 0; i < N; ++i) {
        std::cout << "Size " << N_[i] << "x" << N_[i] << ": " << times[i].count() << " ms" << std::endl;
    }

    return 0;
}
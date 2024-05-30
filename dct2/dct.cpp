#include "dct.h"

//#define DEBUG

#ifdef DEBUG
#include <iostream>
#endif

#include <cmath>
#define PI 3.14159265358979323846

/**
 * @brief Discrete Cosine Transform of a vector
 * 
 * Perform a Discrete Cosine Transform of a vector of length N. The result is allocated on the heap.
 * Time complexity: O(N^2)
 * Space complexity: O(N)
 * 
 * @param v Vector to transform
 * @param N Length of the vector
 * @param support Support structure to avoid repeated calculations for dct2
 * 
 * @return double* Transformed vector allocated on the heap
*/
double * dct(double *v, size_t N, DCTSupport *support) {
    #ifdef DEBUG
    std::cout << "dct called" << std::endl;
    #endif

    double *result = nullptr;
    double sqrt_N = 0, sqrt_2 = 0, coeff = 0;
    
    if (support == nullptr) {
        sqrt_N = std::sqrt(N); 
        sqrt_2 = std::sqrt(2);
        coeff = PI / (2 * N);
    } else {
        result = support->result;
        sqrt_N = support->sqrt_N;
        sqrt_2 = support->sqrt_2;
        coeff = support->coeff;
    } 

    if (result == nullptr) {
        result = new double[N]();
    }

    double a_k = 0.0, coeff_k = 0.0;

    for (size_t k = 0; k < N; ++k) {
        a_k = 0.0;
        coeff_k = coeff * k;

        for (size_t i = 0; i < N; ++i) {
            a_k += std::cos(coeff_k * (2 * i + 1)) * v[i];
        }

        result[k] = a_k / sqrt_N * sqrt_2;
    }
    result[0] /= sqrt_2;

    return result;
}

/**
 * @brief Discrete Cosine Transform of a matrix
 * 
 * Perform a Discrete Cosine Transform of a matrix of size N x M. The result is allocated on the heap.
 * Time complexity: O(N^3) (for simplicity, we consider N = M)
 * Space complexity: O(N)   (for simplicity, we consider N = M)
 * 
 * @param matrix Matrix to transform
 * @param N Number of rows
 * @param M Number of columns
 * 
 * @return double** Transformed matrix allocated on the heap
*/
double ** dct2(double **matrix, size_t N, size_t M) {
    #ifdef DEBUG
    std::cout << "dct2 called" << std::endl;
    #endif

    double **result = new double*[N]();
    for (size_t i = 0; i < N; ++i) {
        result[i] = new double[M]();
    }

    DCTSupport * support = new DCTSupport;
    support->result = nullptr;
    support->sqrt_N = std::sqrt(N);
    support->sqrt_2 = std::sqrt(2);
    support->coeff = PI / (2 * N);

    for (size_t i = 0; i < N; ++i) {
        result[i] = dct(matrix[i], M, support);
    }

    double * transformed;
    double * col_v = new double[N]();
    support->result = new double[N]();

    for (size_t j = 0; j < M; ++j) {
        for (size_t i = 0; i < N; ++i) {
            col_v[i] = result[i][j];
        }

        transformed = dct(col_v, N, support);
        
        for (size_t i = 0; i < N; ++i) {
            result[i][j] = transformed[i];
        }
    }

    delete[] col_v;
    delete[] support->result;
    delete support;

    return result;
}


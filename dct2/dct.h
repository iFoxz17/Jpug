#ifndef _DCT_H
#define _DCT_H

#include <cstddef>

typedef struct {
    double * result;
    double sqrt_N;
    double sqrt_2;
    double coeff;
} DCTSupport;

double * dct(double * v, size_t N, DCTSupport *support = nullptr);
double ** dct2(double ** matrix, size_t N, size_t M);

#endif
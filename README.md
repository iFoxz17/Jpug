# Jpug
Implementation of a simple version of the ***JPG*** format.

## DCT2
The <code>dct2</code> folder contains a simple benchmark over different implementations of the ***Discrete Cosine Transform 2-dimensional***  algorithm. 

## JPUG
The <code>jpug</code> folder contains a ***CLI*** program that can be used for testing a simple version of the ***JPG*** format, whose details are described in <code>doc/project.pdf</code>. 

### Parameters
The three parameters used are:
- $F \in \mathbb{N},$ $F > 0$: dimension of the blocks;
- $d \in \mathbb{N},$ $0 < d \le 2F - 1$: first antidiagonal to exclude;
- $mode \in \{L, RGB\}$: modality used in compression. *L* represents a **gray-scale** image and *RGB* a **colored** image. 

### Format
The program defines a *custom format* called ***jpug*** which is used to save the 'compressed' files.
Images formats supported are:
- **Encoding**:
  - Input: ***bmp***
  - Output: ***jpug***
- **Decoding**:
  - Input: ***jpug***
  - Output: ***bmp***

### CLI
The usage of the ***CLI*** is:

<code>Main.py [*path* [*param_1*] [*param_2*] [*param_3*]]</code>
where:
- <code>\.Main.py </code> runs the ***CLI*** based program;
- <code>\.Main.py *path*</code> tries to **encode** or **decode** the file specified at <code>*path*</code> according to the *file extension*;
- <code>\.Main.py *path* *mode*</code> tries to **encode** or **decode** according to specified <code>*mode*</code>, which can be '***RGB***' or '***L***';
- <code>\.Main.py *path* *F* *d*</code> tries to **encode** or **decode** according to the specified *parameters* <code>*F*</code> and <code>*d*</code>, with the constraints
  - $F > 0$;
  - $0 < d \le 2F - 1$;
- <code>\.Main.py *path* *F* *d* *mode*</code> tries to **encode** or **decode** with the specified parameters <code>*F*</code> <code>*d*</code> and the specified <code>*mode*</code>.

Where not specified, the following default values are used:
- $F = 8$
- $d = 8$
- *mode = RGB*

## Dependencies
- [numpy](https://numpy.org/): Linear algebra for python;
- [PIL](https://python-pillow.org/): *Python Image Library*;
- [pickle](https://docs.python.org/3/library/pickle.html): Python object *serialization*;
- [fft](https://numpy.org/doc/stable/reference/routines.fft.html): *Fast Fourier Transform* (***dct2*** implementation)




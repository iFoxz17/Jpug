import numpy as np
from scipy.fftpack import dctn, idctn

class Encoder():
    '''
    Encoder class for encoding and decoding vectors according to the format.
    '''

    DEFAULT_FLOAT_DTYPE = np.float16

    def __init__(self, F:int=8, d:int=8, float_dtype:np.dtype=DEFAULT_FLOAT_DTYPE) -> None:
        ''' 
        Constructor of the Encoder class.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        @param float_dtype: The float dtype of the encoder. Default is np.float32.
        '''

        self.set_params(F, d)
        self.set_float_dtype(float_dtype)

    def set_params(self, F:int, d:int) -> None:
        '''
        Set the parameters of the encoder.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed). It must be between 0 <= d <= 2F - 1.
        '''

        assert F > 0, 'The size of the blocks must be greater than 0.'
        assert 0 <= d <= 2 * F - 1, f'd must be between 0 and 2F - 1 = {2 * F - 1}.' 
        
        assert type(F) == int, 'The size of the blocks must be an integer.'
        assert type(d) == int, 'The first antidiagonal to delete must be an integer.'

        self._F = F
        self._d = d

    def set_float_dtype(self, float_dtype:np.dtype) -> None:
        '''
        Set the float dtype of the encoder.

        Parameters:
        @param float_dtype: The float dtype of the encoder.
        '''

        assert np.issubdtype(float_dtype, np.floating) or float_dtype==np.int8, 'The float dtype must be a floating point type or int8.'

        self._float_dtype = float_dtype

    def get_F(self) -> int:

        return self._F
    
    def get_d(self) -> int:

        return self._d
    
    def get_params(self) -> tuple[int]:  

        return (self.get_F(), self.get_d())

    def get_float_dtype(self) -> np.dtype:
            
        return self._float_dtype


    def _compute_rearranged_shape(self, original_shape:tuple[int]) -> tuple[int]:
        '''
        Return the maximum possible shape divisible for F.

        Parameters:
        @param original_shape: The original shape of the vector.

        @return: A tuple representing the maximum possible shape divisible for F.
        '''

        return tuple([x - x % self._F for x in original_shape])

    def _rearrange_vector(self, v:np.ndarray) -> np.ndarray:
        '''
        Rearrange the vector to a shape divisible for F.

        Parameters:
        @param v: The input vector to rearrange.

        @return: The rearranged vector.
        '''

        assert v.ndim == 2, 'The input vector must be two dimensional.'

        blocks_x, blocks_y = self._compute_rearranged_shape(v.shape)
        return v[:blocks_x, :blocks_y]


    def _compute_blocks_vector(self, v:np.ndarray) -> np.ndarray:
        '''
        Return the original array divided in blocks of F x F bytes.

        Parameters:
        @param v: The input vector to divide in blocks.

        @return: A new vector representing the input vector divided in blocks.
        '''
        
        blocks_x = v.shape[0] // self._F
        blocks_y = v.shape[1] // self._F

        return v.reshape((blocks_x, self._F, blocks_y, self._F)).swapaxes(1, 2)

    def _compute_vector_from_blocks(self, blocks_v:np.ndarray) -> np.ndarray:
        '''
        Reshape a vector divided in (F x F) blocks in a two dimensional vector.

        Parameters:
        @param blocks_v: The input vector divided in blocks of F x F bytes.

        @return: A new vector representing the input vector in two dimensions.
        '''

        assert blocks_v.ndim == 4, 'The input vector must be four dimensional.'
        assert blocks_v.shape[2] == self._F, f'The blocks must have size {self._F} x {self._F}.'
        assert blocks_v.shape[3] == self._F, f'The blocks must have size {self._F} x {self._F}.'
        assert blocks_v.dtype == np.uint8, f'The input vector must be of type uint8, not {blocks_v.dtype}.'

        return blocks_v.swapaxes(1, 2).reshape((blocks_v.shape[0] * self._F, blocks_v.shape[1] * self._F))


    def _compute_compressed_n(self):
        '''
        Compute the length of the compressed vectors.

        @return: The length of the compressed vectors.
        '''

        if self._d <= self._F:
            return self._d * (self._d + 1) // 2
        else:
            return int(2 * self._F * self._d - 1/2 * self._d * self._d - self._F * self._F - 1/2 * self._d + self._F)


    def _compress(self, v:np.ndarray) -> np.ndarray:
        '''
        Compress the image performing the cut of the frequncies according to d.

        Parameters:
        @param v: The input vector to compress. It must be a four dimensional numpy array of float.

        @return: The compressed vector. It is a three dimensional array of float.
        '''

        assert v.ndim == 4, 'The input vector must be four dimensional.'

        n = self._compute_compressed_n()
        compressed_v = np.zeros((v.shape[0], v.shape[1], n), dtype=self.get_float_dtype())
        mask = np.rot90(np.triu(np.ones((self._F, self._F), dtype=bool), k = self._F - self._d), k=1)

        for i, row_block in enumerate(v):
            for j, block in enumerate(row_block):
                compressed_v[i, j] = block[mask]

        return compressed_v
    
    def _triu_secondary_mask(self, matrix, k):
        matrix[:] = 0

        N = len(matrix)
        for i in range(min(N, k)):
            matrix[i, : min(N, k - i)] = 1

        return matrix

    def _decompress(self, compressed_v:np.ndarray) -> np.ndarray:
        '''
        Decompress the image, filling the empty entries with zeros.

        Parameters:
        @param compressed_v: The input vector to decompress. It must be a three dimensional numpy array of float.

        @return: The decompressed vector. It is a four dimensional array of float.
        '''

        assert compressed_v.ndim == 3, 'The input vector must be three dimensional.'

        v = np.zeros((compressed_v.shape[0], compressed_v.shape[1], self._F, self._F), dtype=self.get_float_dtype())
        triu_secondary_idx = np.mask_indices(self._F, self._triu_secondary_mask, k = self._d)

        for i, row_block in enumerate(v):
            for j, block in enumerate(row_block):
                block[triu_secondary_idx[0], triu_secondary_idx[1]] = compressed_v[i, j]

        return v
 

    def encode(self, v:np.ndarray) -> np.ndarray:
        '''
        Perform the encoding of the input vector v.

        Parameters:
        @param v: The input vector to encode. It must be a two dimensional numpy array of uint8.

        @return: The encoded vector. It is a three dimensional array of float.
        '''

        assert v.ndim == 2, 'The input vector must be two dimensional.'
        assert v.dtype == np.uint8, 'The input vector must be of type uint8.'
        
        rearranged_v = self._rearrange_vector(v)

        blocks_v = self._compute_blocks_vector(rearranged_v)

        transformed_blocks_v = dctn(blocks_v, axes=(2, 3), type=2, norm='ortho')

        if self.get_float_dtype() == np.int8:
            transformed_blocks_v = np.round(np.clip(transformed_blocks_v, -128, 127)).astype(np.int8)

        compressed_blocks_v = self._compress(transformed_blocks_v)

        return compressed_blocks_v

    def decode(self, compressed_v:np.ndarray) -> np.ndarray:
        '''
        Perform the decoding of the input vector v.

        Parameters:
        @param v: The input vector to decode. It must be a three dimensional numpy array of float.

        @return: The decoded vector. It is a two dimensional array of uint8.
        '''

        assert compressed_v.ndim == 3, 'The input vector must be three dimensional.'
        assert compressed_v.dtype == self.get_float_dtype(), f'The input vector must be of type {self.get_float_dtype()}.'

        decompressed_blocks_v = self._decompress(compressed_v)

        blocks_v = idctn(decompressed_blocks_v, axes=(2, 3), type=2, norm='ortho')

        blocks_v = np.round(np.clip(blocks_v, 0, 255)).astype(np.uint8)

        v = self._compute_vector_from_blocks(blocks_v)

        return v

    def get_stats(self) -> float:
        '''
        Return the percentage of elements saved with the encoder parameters.

        @return: A float representing the percentage of elements saved. It does not take into account the size of the float dtype.
        '''

        if self._d <= self._F:
            return 1 - (self._d * (self._d + 1) / 2) / (self._F * self._F)
        else:
            return 1 - (4 * self._F * self._d - self._d ** 2 - 2 * self._F ** 2 - self._d + 2 * self._F) / (2 * self._F ** 2)

    def __str__(self) -> str:
        return f'Encoder(F={self._F}, d={self._d}, float_dtype={self._float_dtype})'
    
    def __repr__(self) -> str:
        return self.__str__()

    

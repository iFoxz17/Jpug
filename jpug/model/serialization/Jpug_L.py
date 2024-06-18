import numpy as np
from model.serialization.Jpug import Jpug

class Jpug_L(Jpug):
    '''
    Class to encode our version of the JPEG format for a gray-scaled image.
    '''

    def __init__(self, F:int, d:int, v:np.array) -> None:
        '''
        Constructor of the class.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        @param v: The vector to serialize.
        '''

        super().__init__(F, d)
        
        self.set_v(v)       

    def get_v(self) -> np.array:
        return self._v
    
    def set_v(self, v:np.array) -> None:
        assert type(v) == np.ndarray, 'The image must be a numpy array.'
        assert v.ndim == 3, 'The vector must be a three dimensional array.'
        assert v.shape[2] == self._compute_compressed_n(self._F, self._d), 'The third dimension of the image must be equal to d.'

        self._v = v

    def __str__(self) -> str:
        return f'Jpug_L({super().__str__()}, v_shape={self.get_v().shape}, v_type={self.get_v().dtype}'
    
    def __repr__(self) -> str:
        return self.__str__()
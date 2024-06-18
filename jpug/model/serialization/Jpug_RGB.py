import numpy as np
from model.serialization.Jpug import Jpug

class Jpug_RGB(Jpug):
    '''
    Class to encode our version of the JPEG format for a RGB image.
    '''

    def __init__(self, F:int, d:int, R:np.array, G:np.array, B:np.array) -> None:
        '''
        Constructor of the class.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        @param R: The red compoenent vector to serialize.
        @param G: The green compoenent vector to serialize.
        @param B: The blue compoenent vector to serialize.
        '''

        assert R.shape == G.shape == B.shape, 'The three RGB components must have the same shape.'

        super().__init__(F, d)
        
        self.set_R(R)
        self.set_G(G)
        self.set_B(B)
               

    def get_R(self) -> np.array:
        return self._R
    
    def get_G(self) -> np.array:
        return self._G
    
    def get_B(self) -> np.array:
        return self._B
    
    def get_RGB(self) -> np.array:
        return [self.get_R(), self.get_G(), self.get_B()]
    
    def set_R(self, R:np.array) -> None:
        assert type(R) == np.ndarray, 'The image must be a numpy array.'
        assert R.ndim == 3, 'The vector must be a three dimensional array.'
        assert R.shape[2] == self._compute_compressed_n(self._F, self._d), 'The third dimension of the image must be equal to d.'

        self._R = R

    def set_G(self, G:np.array) -> None:
        assert type(G) == np.ndarray, 'The image must be a numpy array.'
        assert G.ndim == 3, 'The vector must be a three dimensional array.'
        assert G.shape[2] == self._compute_compressed_n(self._F, self._d), 'The third dimension of the image must be equal to d.'

        self._G = G

    def set_B(self, B:np.array) -> None:
        assert type(B) == np.ndarray, 'The image must be a numpy array.'
        assert B.ndim == 3, 'The vector must be a three dimensional array.'
        assert B.shape[2] == self._compute_compressed_n(self._F, self._d), 'The third dimension of the image must be equal to d.'

        self._B = B

    def __str__(self) -> str:
        return f'Jpug_RGB({super().__str__()}, R_shape={self.get_R().shape}, G_shape={self.get_G().shape}, B_shape={self.get_B().shape}, v_type={self.get_R().dtype})'
    
    def __repr__(self) -> str:
        return self.__str__()
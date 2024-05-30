from abc import ABC

class Jpug(ABC):
    '''
    Abstract class to encode our version of the JPEG format.
    '''

    def _compute_compressed_n(self, F, d):
        '''
        Compute the length of the compressed vectors.

        @return: The length of the compressed vectors.
        '''

        if d <= F:
            return d * (d + 1) // 2
        else:
            return int(2 * F * d - 1/2 * d * d - F * F - 1/2 * d + F)


    def __init__(self, F:int, d:int) -> None:
        '''
        Constructor of the class.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        '''

        self._set_params(F, d)

    def _set_params(self, F:int, d:int) -> None:
        assert F > 0, 'The size of the blocks must be greater than 0.'
        assert 0 <= d <= 2 * F - 1, f'd must be between 0 and 2F - 1 = {2 * F - 1}.' 
        
        assert type(F) == int, 'The size of the blocks must be an integer.'
        assert type(d) == int, 'The first antidiagonal to delete must be an integer.'

        self._F = F
        self._d = d

    def get_F(self) -> int:
        return self._F
    
    def get_d(self) -> int:
        return self._d
    
    def __str__(self) -> str:
        return f'Jpug(F={self._F}, d={self._d})'
    
    def __repr__(self) -> str:
        return self.__str__()




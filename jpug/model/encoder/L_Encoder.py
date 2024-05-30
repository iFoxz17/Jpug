from PIL import Image
import numpy as np

from model.serialization.Jpug_L import Jpug_L
from model.encoder.Encoder import Encoder

class L_Encoder(Encoder):
    '''
    Encoder class for encoding and decoding gray-scaled images according to the format.
    '''

    def __init__(self, F:int=8, d:int=8, float_dtype:np.dtype=Encoder.DEFAULT_FLOAT_DTYPE) -> None:
        ''' 
        Constructor of the L_Encoder class.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        @param float_dtype: The float dtype of the encoder. Default is np.float32.
        '''
        super().__init__(F, d, float_dtype=float_dtype)


    def encode(self, image:Image.Image) -> Jpug_L:
        '''
        Encode a gray-scaled image.

        Parameters:
        @param image: PIL Image object representation of the image. If the image is not gray-scaled, it will be converted to gray-scaled.

        @return:  An object Jpug_L representing the compressed image.
        '''
        
        assert isinstance(image, Image.Image), 'The image must be a PIL Image object.'
        
        if image.mode != 'L':
            image = image.convert('L')

        image_array = np.array(image)
        
        return Jpug_L(self.get_F(), self.get_d(), super(L_Encoder, self).encode(image_array))
    
    def decode(self, jpug:Jpug_L) -> Image.Image:
        '''
        Decode an encoded image.

        Parameters:
        jpug: Jpug_L object representing the compressed image.

        @return: PIL Image object representation of the image. It is a gray-scaled image.
        '''
        F, d = self.get_params()

        self._F = jpug.get_F()
        self._d = jpug.get_d()
        image_array = super(L_Encoder, self).decode(jpug.get_v())
        
        self.set_params(F, d)

        return Image.fromarray(image_array, mode='L')
    
    def __str__(self) -> str:
        return f'L_Encoder({super().__str__()})'
    
    def __repr__(self) -> str:
        return self.__str__()


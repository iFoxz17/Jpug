from PIL import Image
import numpy as np

from model.encoder.Encoder import Encoder
from model.serialization.Jpug_RGB import Jpug_RGB

class RGB_Encoder(Encoder):
    '''
    Encoder class for encoding and decoding RGB images according to the format.
    '''

    def __init__(self, F:int=8, d:int=8, float_dtype:np.dtype=Encoder.DEFAULT_FLOAT_DTYPE) -> None:
        ''' 
        Constructor of the RGB_Encoder class.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        @param float_dtype: The float dtype of the encoder. Default is np.float32.
        '''
        super().__init__(F, d, float_dtype=float_dtype)


    def encode(self, image:Image.Image) -> Jpug_RGB:
        '''
        Encode an RGB image.

        Parameters:
        @param image: PIL Image object representation of the image. It must be a RGB image (x * y * 3).

        @return: An object Jpug_RGB representing the compressed image.
        '''
        
        assert isinstance(image, Image.Image), 'The image must be a PIL Image object.'
        assert image.mode == 'RGB', 'The image must be gray-scaled.'

        image_array_rgb = np.array(image)
        image_array_list = [np.squeeze(x) for x in np.dsplit(image_array_rgb, 3)]

        encoded_arrays_list = np.array([super(RGB_Encoder, self).encode(image_array) for image_array in image_array_list])
        return Jpug_RGB(self.get_F(), self.get_d(), *encoded_arrays_list)

    def decode(self, jpug:Jpug_RGB) -> Image.Image:
        '''
        Decode an encoded image.

        Parameters:
        @param jpug: Jpug_RGB object representing the compressed image.

        @return: PIL Image object representation of the image. It is a RGB image.
        '''

        assert isinstance(jpug, Jpug_RGB), 'The image must be a Jpug_RGB object.'

        F, d = self.get_params()

        self._F = jpug.get_F()
        self._d = jpug.get_d()

        image_array_list = [super(RGB_Encoder, self).decode(image_array) for image_array in jpug.get_RGB()]
        self.set_params(F, d)

        image_array_rgb = np.dstack(image_array_list)
        
        return Image.fromarray(image_array_rgb, mode='RGB')
    
    def __str__(self) -> str:
        return f'RGB_Encoder({super().__str__()})'
    
    def __repr__(self) -> str:
        return self.__str__()


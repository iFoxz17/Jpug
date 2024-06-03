import controller.Util as Util

from model.encoder.Encoder import Encoder
from model.encoder.L_Encoder import L_Encoder
from model.encoder.RGB_Encoder import RGB_Encoder

class Encoder_Controller:
    instance = None

    @staticmethod
    def get_instance() -> 'Encoder_Controller':
        if Encoder_Controller.instance is None:
            Encoder_Controller.instance = Encoder_Controller(Util.DEFAULT_MODE)
        return Encoder_Controller.instance

    def __init__(self, default_mode:Util.Mode) -> None:
        '''
        Constructor of the Encoder_Controller class.

        Parameters:
        @param default_mode: The default mode of the active encoder.
        '''
        self._rgb_encoder = None
        self._l_encoder = None

        self._active_encoder = None
        
        self._set_mode(default_mode)

    def _initialize_rgb_encoder(self) -> None:
        '''
        Initialize the RGB encoder.
        '''

        self._rgb_encoder = RGB_Encoder(Util.DEFAULT_F, Util.DEFAULT_D, Util.DEFAULT_FLOAT_DTYPE)

    def _initialize_l_encoder(self) -> None:
        '''
        Initialize the L encoder.
        '''

        self._l_encoder = L_Encoder(Util.DEFAULT_F, Util.DEFAULT_D, Util.DEFAULT_FLOAT_DTYPE)

    def _set_mode(self, mode:Util.Mode) -> None:
        '''
        Set the mode of the encoder.

        Parameters:
        @param mode: The mode to set.
        '''
        self._mode = mode
        self._set_active_encoder()

    def _set_active_encoder(self) -> None:
        '''
        Update the active encoder according to self._mode.
        '''
        if self._mode == Util.Mode.L:
            if self._l_encoder is None:
                self._initialize_l_encoder()
            self._active_encoder = self._l_encoder

        elif self._mode == Util.Mode.RGB:
            if self._rgb_encoder is None:
                self._initialize_rgb_encoder()
            self._active_encoder = self._rgb_encoder

    def change_mode(self) -> None:
        '''
        Switch the mode of the encoder.
        '''
        if self._mode == Util.Mode.L:
            self._set_mode(Util.Mode.RGB)
        else:
            self._set_mode(Util.Mode.L)

    def get_active_params(self) -> tuple[int]:
        '''
        Get the parameters of the active encoder.

        @return: A tuple with the active parameters of the encoder.
        '''
        return self._active_encoder.get_params()
    
    def change_active_params(self, F:int, d:int) -> None:
        '''
        Change the parameters of the active encoder.

        Parameters:
        @param F: The size of the blocks.
        @param d: The first antidiagonal of the block to delete (0-indexed).
        '''
        self._active_encoder.set_params(F, d)
    
    def get_active_mode(self) -> Util.Mode:
        '''
        Get the active mode of the encoder.

        @return: The active mode of the encoder.
        '''
        return self._mode
    
    def get_active_encoder(self) -> Encoder:
        '''
        Get the active encoder.

        @return: The active encoder.
        '''
        return self._active_encoder
    
    def get_rgb_encoder(self) -> RGB_Encoder:
        '''
        Get the RGB encoder.

        @return: The RGB encoder.
        '''

        if self._rgb_encoder is None:
            self._initialize_rgb_encoder()

        return self._rgb_encoder
    
    def get_l_encoder(self) -> L_Encoder:
        '''
        Get the L encoder.

        @return: The L encoder.
        '''

        if self._l_encoder is None:
            self._initialize_l_encoder()
        
        return self._l_encoder
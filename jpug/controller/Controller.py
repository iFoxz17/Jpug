import controller.Util as Util
from controller.Encoder_Controller import Encoder_Controller

from model.serialization.Jpug_RGB import Jpug_RGB
from model.serialization.Jpug_L import Jpug_L

from model.Parser import Parser

from PIL import Image

class Controller():

    instance = None

    @staticmethod
    def get_instance() -> 'Controller':
        if Controller.instance is None:
            Controller.instance = Controller()
        return Controller.instance
    
    def __init__(self) -> None:
        self._encoder_controller = Encoder_Controller.get_instance()

    def get_active_params(self) -> tuple[int]:
        return self._encoder_controller.get_active_params()
    
    def get_active_mode(self) -> Util.Mode:
        return self._encoder_controller.get_active_mode()

    def _retrieve_image(self, path:str) -> Image.Image:
        img = Parser.load_image(path)

        if self._encoder_controller.get_active_mode() == Util.Mode.L:
            img = img.convert('L')

        return img
    
    def _encode(self, path:str) -> None:
        img = self._retrieve_image(path)

        jpug = self._encoder_controller.get_active_encoder().encode(img)
        encoded_path = Util.compute_encoded_path(path, self._encoder_controller.get_active_mode())
        Parser.save_jpug(jpug, encoded_path)

        return encoded_path
    
    def _decode(self, path:str) -> None:
        jpug = Parser.load_jpug(path)

        if isinstance(jpug, Jpug_RGB):
            img = self._encoder_controller.get_rgb_encoder().decode(jpug)
        elif isinstance(jpug, Jpug_L):
            img = self._encoder_controller.get_l_encoder().decode(jpug)
        
        decoded_path = Util.compute_decoded_path(path)
        Parser.save_image(img, decoded_path)

        return decoded_path

    def _get_result_msg(self, operation:Util.Operation, args:list) -> str:
        '''
        Get the result message of the operation.

        Parameters:
        @param operation: The operation to execute.

        @return: The result message of the operation.
        '''
        if operation == Util.Operation.SWITCH_MODE:
            return Util.SWITCH_MODE_MSG.format(args)
        
        elif operation == Util.Operation.CHANGE_PARAMS:
            return Util.CHANGE_PARAMS_MSG.format(args[0], args[1])  

        elif operation == Util.Operation.SHOW:
            return args
        
        elif operation == Util.Operation.ENCODE:
            return Util.ENCODE_MSG.format(args)
        
        elif operation == Util.Operation.DECODE:
            return Util.DECODE_MSG.format(args)
        
        elif operation == Util.Operation.STATS:
            return Util.STATS_MSG.format(args)
        
        elif operation == Util.Operation.EXIT:
            return Util.EXIT_MSG

    def execute(self, operation:Util.Operation, args:list) -> str:
        '''
        Execute the operation.

        Parameters:
        @param operation: The operation to execute.
        '''

        if operation == Util.Operation.SWITCH_MODE:
            self._encoder_controller.change_mode()
            result = self._encoder_controller.get_active_mode().name

        elif operation == Util.Operation.CHANGE_PARAMS:
            assert len(args) == 2, Util.INVALID_ARGS_MSG
            F = args[0]
            d = args[1]

            try:
                self._encoder_controller.change_active_params(F, d) 
                result = (F, d)
            except:
                return Util.INVALID_PARAMS_MSG.format(F, d)        
        
        elif operation == Util.Operation.SHOW:
            assert len(args) == 1, Util.INVALID_ARGS_MSG
            path = args[0]
            
            try:
                result = self._retrieve_image(path)
            except FileNotFoundError:
                return Util.FILE_NOT_FOUND_MSG.format(path)
            except:
                return Util.INVALID_FORMAT_MSG
        
        elif operation == Util.Operation.ENCODE:
            assert len(args) == 1, Util.INVALID_ARGS_MSG
            path = args[0]

            try:
                result = self._encode(path)
            except FileNotFoundError:
                return Util.FILE_NOT_FOUND_MSG.format(path)
            except:
                return Util.INVALID_FORMAT_MSG

        elif operation == Util.Operation.DECODE:
            assert len(args) == 1, Util.INVALID_ARGS_MSG
            path = args[0]
            
            try:
                result = self._decode(path)
            except FileNotFoundError:
                return Util.FILE_NOT_FOUND_MSG.format(path)
            except:
                return Util.INVALID_FORMAT_MSG

        elif operation == Util.Operation.STATS:
            result = self._encoder_controller.get_active_encoder().get_stats()

        elif operation == Util.Operation.EXIT:
            result = None

        return self._get_result_msg(operation, result)
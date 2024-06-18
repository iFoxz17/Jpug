from enum import Enum
import numpy as np

class Operation(Enum):
    SWITCH_MODE = 0
    CHANGE_PARAMS = 1
    SHOW = 2
    ENCODE = 3
    DECODE = 4
    STATS = 5
    EXIT = 6

def get_enum_from_value(value:int, enum:Enum=Operation) -> Operation:
    for op in enum:
        if op.value == value:
            return op
        
    return None

SWITCH_MODE_MSG = 'Mode switched to {}'
CHANGE_PARAMS_MSG = 'Parameters changed to F={} and d={}'
ENCODE_MSG = 'Image encoded at \'{}\' successfully'
DECODE_MSG = 'Image decoded at \'{}\' successfully'
STATS_MSG = 'The percentage of elements saved is {}'
EXIT_MSG = 'Exiting...'

INVALID_PARAMS_MSG = 'Invalid parameters: F={} and D={}'
FILE_NOT_FOUND_MSG = 'File \'{}\' not found'
INVALID_FORMAT_MSG = 'File format not valid'
INVALID_ARGS_MSG = 'Invalid number of arguments'

class Mode(Enum):
    L = 'L'
    RGB = 'RGB'

DEFAULT_MODE = Mode.RGB
DEFAULT_F = 8
DEFAULT_D = 8
DEFAULT_FLOAT_DTYPE = np.float16

JPUG_EXTENSION = '.jpug'
IMAGE_EXTENSION = '.bmp'

def compute_encoded_path(path:str, mode:Mode=None) -> str:
    '''
    Compute the path for a new encoded image.
    
    Parameters:
    @param path: The path of the original image encoded.
    @param mode: The mode of the encoder. Default is None.
    
    @return: The path of the new image encoded.
    '''
    
    if mode is None:
        return path[:path.rfind(IMAGE_EXTENSION)] + JPUG_EXTENSION
    
    return path[:path.rfind(IMAGE_EXTENSION)] + f'_{mode.name}' + JPUG_EXTENSION
    
def compute_decoded_path(path:str) -> str:
    '''
    Compute the path for a new decoded image.
    
    Parameters:
    @param path: The path of the original image encoded.
    
    @return: The path of the new image decoded.
    '''

    return path[:path.rfind(JPUG_EXTENSION)] + IMAGE_EXTENSION


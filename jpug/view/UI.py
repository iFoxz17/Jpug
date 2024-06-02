import controller.Util as Util
from controller.Controller import Controller

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

class UI:

    DEFAULT_IMAGE_SIZE_THRESHOLD = 1000000

    def __init__(self, image_size_threshold:int=DEFAULT_IMAGE_SIZE_THRESHOLD) -> None:
        self._image_size_threshold = image_size_threshold

    def _show(self, result:any, path:str=None) -> None:
        '''
        Output the result of an operation

        @param result: the result of the operation. It can be a string or an image. If is an image, it will be displayed
        according to its size: image.show() creates a PNG copy of the image on the disk, so it is not recommended for large images.
        Use instead matplotlib to display large images.
        '''
        if isinstance(result, str):
            print(f'> {result}')
        elif isinstance(result, Image.Image):
            print(f'> Loading image...')
            
            width, height = result.size
            if width * height <= self._image_size_threshold:
                result.show(title=path if path is not None else 'Image')
            else:
                fig, ax = plt.subplots(figsize=(10, 5)) 

                image_array = np.array(result)
                ax.imshow(image_array)
                ax.axis('off')  

                fig.canvas.manager.set_window_title(path if path is not None else 'Image')

                plt.show(block=False)
            
    def start_ui(self) -> None:
        controller = Controller.get_instance()

        while True:
            F, d  = controller.get_active_params()
            mode = controller.get_active_mode().name
            print('-------------------------------------------------------')
            print(f'Active mode: {mode}')
            print(f'Active parameters: F = {F}, d = {d}')
            print('-------------------------------------------------------')
            print('Choose an operation:')
            print(f'\t{Util.Operation.SWITCH_MODE.value}. Switch mode')
            print(f'\t{Util.Operation.CHANGE_PARAMS.value}. Change parameters')
            print(f'\t{Util.Operation.SHOW.value}. Show an image')
            print(f'\t{Util.Operation.ENCODE.value}. Encode')
            print(f'\t{Util.Operation.DECODE.value}. Decode')
            print(f'\t{Util.Operation.STATS.value}. Show statistics')
            print(f'\t{Util.Operation.EXIT.value}. Exit')
            
            try:
                operation_val = int(input('< '))
            except ValueError:
                print('> Invalid operation')
                continue
            
            operation = Util.get_enum_from_value(operation_val)
            if operation is None:
                print('> Operation not supported')
                continue
            
            params = []
            path = None

            if operation == Util.Operation.SHOW or operation == Util.Operation.ENCODE or operation == Util.Operation.DECODE:
                path = input('< Enter path: ')
                params.append(path)

            elif operation == Util.Operation.CHANGE_PARAMS:
                try:
                    F = int(input('< Enter F: '))
                except:
                    print('> Invalid F')
                    continue
                if F <= 0:
                    print('> F must be greater than 0')
                    continue

                try:
                    d = int(input('< Enter d: '))
                except:
                    print('> Invalid d')
                    continue
                if d <= 0 or d > 2 * F - 1:
                    print(f'> d must be between 0 and 2F - 1 = {2 * F - 1}')
                    continue

                params.append(F)
                params.append(d)

            result = controller.execute(operation, params)
            self._show(result, path)
           
            if operation == Util.Operation.EXIT:
                break
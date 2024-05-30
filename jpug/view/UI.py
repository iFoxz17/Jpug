import controller.Util as Util
from controller.Controller import Controller

from PIL import Image

class UI:

    def __init__(self):
        self._view = None

    def _show(self, result:any) -> None:
        if isinstance(result, str):
            print(f'> {result}')
        elif isinstance(result, Image.Image):
            print(f'> Loading image...')
            result.show()

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
            self._show(result)
           
            if operation == Util.Operation.EXIT:
                break
import sys
from view import UI

import controller.Util as Util
import controller.Controller as Controller

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        ui = UI.UI()
        ui.start_ui()

    else:
        controller = Controller.Controller()
        path = args[0]
        F = Util.DEFAULT_F
        d = Util.DEFAULT_D
        mode = Util.DEFAULT_MODE

        if path.rfind('.') == -1:
            print(f'Invalid file format: \'\'')
            return
        
        if path[path.rfind('.') :] == Util.JPUG_EXTENSION:    
            operation = Util.Operation.DECODE
        elif path[path.rfind('.') :] == Util.IMAGE_EXTENSION:
            operation = Util.Operation.ENCODE
        else:
            print(f"Invalid file format: \'{path[path.rfind('.'):]}\'")
            return
        
        if operation == Util.Operation.ENCODE:
            if len(args) == 2:
                mode = Util.get_enum_from_value(args[1].upper(), Util.Mode)
                if mode is None:
                    print(f"Invalid mode: {args[1]}")
                    return
                
            elif len(args) > 2:
                try:
                    F = int(args[1])
                except ValueError:
                    print(f"Invalid parameter F: {args[1]}")
                    return
                if F <= 0:
                    print(f"Invalid parameter F: {F}")
                    return
                try:
                    d = int(args[2])
                except ValueError:
                    print(f"Invalid parameter d: {args[2]}")
                    return
                if d <= 0 or d > 2 * F - 1:
                    print(f"Invalid parameter d: {d}")
                    return
                if len(args) > 3:
                    mode = Util.get_enum_from_value(args[3].upper(), Util.Mode)
                    if mode is None:
                        print(f"Invalid mode: {args[3]}")
                        return
                    
            if controller.get_active_mode() != mode:
                controller.execute(Util.Operation.SWITCH_MODE, [mode])

            controller.execute(Util.Operation.CHANGE_PARAMS, [F, d])    
            
        result = controller.execute(operation, [path])    
        print(result)

if __name__ == '__main__':
    main()
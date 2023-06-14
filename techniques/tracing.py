from io import StringIO
import sys
import trace


def path_trace(code, data):
    # ================================================== #
    # For Capturing Trace Path from Terminal
    # ================================================== #

    tmp = sys.stdout
    my_result = StringIO()
    sys.stdout = my_result

    # ================================================== #
    # Path Tracing Algorithm
    # ================================================== #
    val_x = data['x']
    val_y = data['y']

    tracer = trace.Trace(count=False, trace=True)

    try:
        val_z = tracer.runfunc(code, val_x, val_y, data['inc'])
    except:
        val_z = tracer.runfunc(code, val_x, val_y)

    sys.stdout = tmp

    path = my_result.getvalue()

    splt = path.split('\n')
    arr = []

    for val in splt:
        if not '---' in val and len(val) > 0:
            arr.append(f"{val}\n")

    result = {"x": val_x, "y": val_y, "path": arr, "z": val_z, "length": len(arr)}

    return result
import cv2


def gstreamer_pipeline(
    capture_width=600,
    capture_height=400,
    display_width=600,
    display_height=400,
    framerate=20,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )



def start_capturing(**cam_params):
    cam = cv2.VideoCapture(gstreamer_pipeline(**cam_params), cv2.CAP_GSTREAMER)

    while True:
        yield cam.read()
    

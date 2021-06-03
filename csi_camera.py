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



def start_capturing(record_name=None, **cam_params):
    cam = cv2.VideoCapture(gstreamer_pipeline(**cam_params), cv2.CAP_GSTREAMER)

    if record_name is not None: 
        video_writer = cv2.VideoWriter(record_name, cv2.VideoWriter_fourcc(*'MJPG'), 60, (600, 400))
        yield video_writer

    while True:
        ret, frame = cam.read()
        if record_name is not None:
            video_writer.write(frame)

        yield ret, frame
    

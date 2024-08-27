import cv2
import serial
import time

# Set desired resolution
width = 1080
height = 720

capture = cv2.VideoCapture(0)

# Initialize serial communication with Arduino
ArduinoSerial = serial.Serial('COM3', 9600, timeout=0.1)
time.sleep(1)

# Set resolution
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Create window with specific size
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', width, height)

# Variables to store previous face position
prev_x = None
prev_y = None

def send_command(x, y):
    command = 'X{0:d}Y{1:d}'.format(x, y)
    ArduinoSerial.write(command.encode('utf-8'))
#
while True:
    isTrue, frame = capture.read()
    frame = cv2.flip(frame, 1)  # Mirror the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 8, minSize=(120, 120))


    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print("Frame Width:", frame_width)
    # print("Frame Height:", frame_height)

    frame_mid_x = frame_width // 2
    frame_mid_y = frame_height // 2

    # mid point of the frame
    cv2.circle(frame, (frame_mid_x, frame_mid_y), 2, (255, 0, 255), 2)

    if len(faces) > 0:

        x, y, w, h = faces[0]  # Consider only the first detected face
        # for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

        forehead_x = x + w // 2
        forehead_y = y + int(h * 0.3)


        # Plot the center of the face
        cv2.circle(frame, (x + w // 2, y + int(h * 0.3)), 5, (255, 0, 0), 2)

        # Display coordinates next to the circle
        # cv2.putText(frame, f'({forehead_x}, {forehead_y})', (forehead_x + 20, forehead_y), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (255, 255, 255), 2)

        # Draw line between frame mid point and forehead along x-axis
        cv2.line(frame, (frame_mid_x, frame_mid_y), (forehead_x, frame_mid_y), (0, 0, 255), 2)

        # Draw line between forehead and frame mid point along y-axis
        cv2.line(frame, (forehead_x, forehead_y), (forehead_x, frame_mid_y), (0, 0, 255), 2)

        #distance to cover along X-axis
        dist_X = frame_mid_x - forehead_x
        # distance to cover along Y-axis
        dist_Y = frame_mid_y - forehead_y


        # Display distances
        cv2.putText(frame, f'{abs(dist_X)} pxl', ((frame_mid_x + forehead_x)//2, frame_mid_y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f'{abs(dist_Y)} pxl', (forehead_x + 10, (frame_mid_y + forehead_y)//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


        if dist_X != prev_x or dist_Y != prev_y:
            send_command(dist_X, dist_Y)
            prev_x, prev_y = dist_X, dist_Y

    cv2.imshow('Video', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

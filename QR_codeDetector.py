import cv2
from pyzbar.pyzbar import decode

# Start video capture (0 = default laptop camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access the camera.")
    exit()

print("Camera is active. Showing live feed...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Decode any QR codes in the frame
    decoded_objs = decode(frame)

    # Draw rectangles and show data
    for obj in decoded_objs:
        # Draw rectangle around QR code
        points = obj.polygon
        if len(points) > 4:  # If polygon is not a quadrilateral
            hull = cv2.convexHull(points)
            points = hull
        for i in range(len(points)):
            pt1 = (points[i].x, points[i].y)
            pt2 = (points[(i+1) % len(points)].x, points[(i+1) % len(points)].y)
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

        # Decode and show the data
        qr_data = obj.data.decode('utf-8')
        print(f"QR Code detected: {qr_data}")
        cv2.putText(frame, qr_data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show frame with overlay and wait a bit
        cv2.imshow("QR Code Scanner", frame)
        cv2.waitKey(2000)  # show for 2 seconds
        cap.release()
        cv2.destroyAllWindows()
        exit(0)

    # Show the live video feed
    cv2.imshow("QR Code Scanner", frame)

    # Exit manually with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Clean up
cap.release()
cv2.destroyAllWindows()

import cv2
import face_recognition
import numpy as np
import os
from pathlib import Path

video_capture = cv2.VideoCapture(0)

db = Path("database")
known_face_encodings = {}

for person in db.glob("*"):
    if not person.is_dir():
        continue

    for image in person.glob("*.jpg"):
        if not image:
            continue

        name = person.parts[-1]
        try:  # if face is detected
            encoding = face_recognition.face_encodings(
                face_recognition.load_image_file(image)
            )[0]
            known_face_encodings[name] = encoding
        except IndexError:  # if no face detected
            continue

frame_counter = 0
while True:
    # grab one frame
    ret, frame = video_capture.read()
    frame_counter += 1

    if frame_counter % 5 == 0:  # do the detection every 5 frames
        # resize frame for faster recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # convert image from BGR (opencv) to RGB (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # find all faces and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            # see if there is known match
            matches = face_recognition.compare_faces(
                list(known_face_encodings.values()), face_encoding
            )
            # use the new face with smallest distance to detected face
            name = "Unknown"
            face_distances = face_recognition.face_distance(
                list(known_face_encodings.values()), face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = list(known_face_encodings.keys())[best_match_index]

            face_names.append(name)

    # display the results
    if frame_counter >=5:
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # scale back up face locations since the frame we detected in was scaled to 0.25% size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # cv2.rectangle(
            #     frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            # )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # display the resulting image
    cv2.imshow("Press esc to exit", frame)

    # hit escape on the keyboard to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

video_capture.release()
cv2.destroyAllWindows()

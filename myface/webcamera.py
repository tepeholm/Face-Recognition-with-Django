import os
import urllib.request

import cv2
import face_recognition
import numpy as np

from django.conf import settings

 

class YzatCamera(object):

    first_person_image = face_recognition.load_image_file("myface/media/first_person.jpg")
    first_person_face_encoding = face_recognition.face_encodings(first_person_image)[0]

    second_person_image = face_recognition.load_image_file("myface/media/second_person.jpg")
    second_person_face_encoding = face_recognition.face_encodings(second_person_image)[0]


    known_face_encodings = [first_person_face_encoding, second_person_face_encoding]
    known_face_names = ["first_person_name", "second_person_name"]
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):

        success, image = self.video.read()

        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if self.process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not self.process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        # image = cv2.flip(image,1)  # if webcamera is up and down
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

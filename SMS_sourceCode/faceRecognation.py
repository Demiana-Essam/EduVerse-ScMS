import os
import cv2
import numpy as np
import math
import face_recognition
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.known_face_encodings_List = 'faces_Encodings/encoded_Faces.npy'
        self.known_face_names_List = 'faces_Encodings/named_Faces.npy'

        # Resize frame to smaller value for faster recognition
        self.frame_resize_factor = 1.0
        self.encode_faces()

    def encode_faces(self):
        newFaces = 0
        existingFaces = 0
        if os.path.exists(self.known_face_encodings_List):
            self.known_face_encodings = list(np.load(self.known_face_encodings_List, allow_pickle=True))
            self.known_face_names = list(np.load(self.known_face_names_List, allow_pickle=True))

        for image in os.listdir('students_Faces'):
            if image not in self.known_face_names:
                face_image = face_recognition.load_image_file(f"students_Faces/{image}")
                face_encoding = face_recognition.face_encodings(face_image)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(image)
                newFaces += 1
            else:
                existingFaces += 1

        np.save(self.known_face_encodings_List, self.known_face_encodings)
        np.save(self.known_face_names_List, self.known_face_names)
        print('New Faces:', newFaces, '/ Existing Faces:', existingFaces)
        print(self.known_face_names)

    def reset_encoded_faces(self):
        if os.path.exists(self.known_face_encodings_List):
            os.remove(self.known_face_encodings_List)
        if os.path.exists(self.known_face_names_List):
            os.remove(self.known_face_names_List)

    def run_recognition(self, frame):
        # cv2.imwrite("xad.jpg", rgb_small_frame)
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resize_factor, fy=self.frame_resize_factor)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        self.face_names = []
        self.face_confidence = []
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = 'None'

            # Calculate the shortest distance to face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                name = name[:-4]
                confidence = face_confidence(face_distances[best_match_index])

            self.face_names.append(name)
            self.face_confidence.append(confidence)

        # # # Display the results
        # for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
        #     bottom+=int(bottom/6)
        #     # Create the frame with the name
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        #     cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
        #     # cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        #     cv2.imwrite("xad.jpg", frame)

        # return frame
        return self.face_locations, self.face_names
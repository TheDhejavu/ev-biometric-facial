from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


class FacialRecognition():
    def __init__(self, encodings=None):
        self.encodings = encodings

    def train_images(self, images_folder):
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(images_folder))
        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                                                         len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb,
                                                model="hog")
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)
        self.encodings = encodings
        return (print("Encodings Saved!!"))

    def save_encodings(self):
        import os
        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        cwd = os. getcwd()
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(cwd + "encodings", "wb")
        f.write(pickle.dumps(data))
        f.close()

    def test_images(self, image_url):
        from google.colab.patches import cv2_imshow
        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        cwd = os. getcwd()
        data = pickle.loads(open(cwd + "encodings", "rb").read())
        # load the input image and convert it from BGR to RGB
        image = cv2.imread(image_url)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        print("[INFO] recognizing faces...")
        boxes = face_recognition.face_locations(rgb,
                                                model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        # initialize the list of names for each face detected
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                data["encodings"], encoding)
            name = "Unknown"

        # check to see if we have found a match
        if True in matches:
          # find the indexes of all matched faces then initialize a
          # dictionary to count the total number of times each face
          # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
          # loop over the matched indexes and maintain a count for
          # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
          # determine the recognized face with the largest number of
          # votes (note: in the event of an unlikely tie Python will
          # select first entry in the dictionary)
                name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
            # show the output image
            cv2_imshow(image)
            cv2.waitKey(0)

        return name


if __name__ == "__main__":
    # load face recognition object
    fr = FacialRecognition()
    # implement an event listeer to run whenever images in the folder chages
    fr.train_images("/content/drive/MyDrive/Image Recognition/dataset")
    fr.save_encodings()

    # test new image to return the image and class label
    fr.test_images("trump.jpg")

from PIL import Image
import numpy as np
import pickle


class ImageClassifier:
    def __init__(self, database_name):
        self._database = None
        self._database_name = database_name

    def __str__(self):
        if self._database is not None:
            return ("Image Recognizer with database of " + str(len(self._database)) +
                    " different classes, each containing " + str(len(self._database[0])) + " images.")

    @staticmethod
    def create_database(image_folder, database_name):
        number_db = {}
        for i in range(10):
            number_db[i] = []

        for number in range(len(number_db.keys())):
            for index in range(10):
                image = Image.open(image_folder + "/" + str(number) + "_" + str(index) + ".jpg")
                number_db[number].append(np.array(image).tolist())

        with open(database_name + ".pkl", "wb") as db:
            pickle.dump(number_db, db)

    def open_database(self):
        with open(self._database_name + ".pkl", "rb") as db:
            self._database = pickle.load(db)

    @staticmethod
    def normalize_binary(image):
        for row in image:
            for pixel in range(len(row)):
                total_color = 0
                for color in row[pixel]:
                    total_color += color
                if total_color / 3 < 255 / 2:
                    row[pixel] = 0
                else:
                    row[pixel] = 1
        # print(image)
        return image

    @staticmethod
    def normalize_not(image):
        return image

    def normalize_database(self, norm_function):
        for number in range(len(self._database.keys())):
            for image in self._database[number]:
                image = norm_function(image)

    def classify_image(self, img, norm_function):
        test_image = Image.open(img)
        test_image = np.array(test_image).tolist()
        test_image = norm_function(test_image)

        confidence_dict = dict()

        for i in range(10):
            confidence_dict[i] = 0
        for number in range(len(self._database.keys())):
            for image in self._database[number]:
                for row in range(len(image)):
                    for pixel in range(len(image[row])):
                        if image[row][pixel] == test_image[row][pixel] == 0:
                            confidence_dict[number] += 2
                        elif image[row][pixel] == test_image[row][pixel] == 1:
                            continue
                        else:
                            confidence_dict[number] -= 1

        max_confidence = sorted(confidence_dict.values(), reverse=True)
        print(confidence_dict)
        for key, value in confidence_dict.items():
            if value == max_confidence[0]:
                return key, min(round(
                    abs(((1.0 / max_confidence[0]) * max_confidence[1]) * 100)
                    , 2), 100.00)


if __name__ == "__main__":
    ImageClassifier.create_database("images", "number_db")
    image_classifier = ImageClassifier("number_db")
    image_classifier.open_database()
    print(image_classifier)
    image_classifier.normalize_database(ImageClassifier.normalize_binary)
    for number in range(10):
        print("test_" + str(number) + ": ", end="")
        print(image_classifier.classify_image("test_images/test_" + str(number) + ".jpg",
                                              ImageClassifier.normalize_binary))


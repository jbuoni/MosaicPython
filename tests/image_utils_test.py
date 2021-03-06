# image_utils_test.py
# Jason Buoni
# jason.buoni@gatech.edu
import unittest
import numpy as np
import image_utils as utils
import cv2


# https://docs.python.org/2.7/library/unittest.html
# https://docs.python.org/3/library/unittest.html#setupclass-and-teardownclass
class TestImageUtilsMethods(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.image_1 = np.array([[1, 2, 3, 4],
                                [5, 6, 7, 8],
                                [9, 10, 11, 12],
                                [13, 14, 15, 16]], dtype=np.int16)

        self.image_2 = cv2.imread('/tests/donkey.jpg')

        self.images_1 = []
        self.images_2 = []

        for x in range(3):
            self.images_1.append(self.image_1)

        for x in range(3):
            self.images_2.append(self.image_2)

    def test_resizeImages(self):
        resize_1 = utils.resizeimages_diffheightwidth(2, 2, self.images_1)[0]
        self.assertEqual(resize_1.shape, (2, 2))

        resize_2 = utils.resizeimages_diffheightwidth(2, 3, self.images_1)[0]
        self.assertEqual(resize_2.shape, (2, 3))

        resize_3 = utils.resizeimages(2, self.images_1)[0]
        self.assertEqual(resize_3.shape, (2, 2))

        resize_4 = utils.resizeimages(2, self.images_2)[0]
        self.assertEqual(resize_4.shape, (2, 2))

    def test_convertToGrayscale(self):
        grayscale = utils.converttograyscale(self.image_2)

        imageisgrayscale = True

        h, w = grayscale.shape
        for i in range(w):
            for j in range(h):
                r, g, b = grayscale.getpixel((i, j))
                if r != g != b:
                    imageisgrayscale = False

        self.assertTrue(imageisgrayscale)

    def test_cropImage(self):
        cropped_image = utils.cropimage(self.image_1, 1, 1)

        self.assertEqual(cropped_image.shape, (3, 3))

    def test_readImages(self):
        images_read = utils.readimages('/tests/')

        self.assertEqual(images_read.shape, 1)

if __name__ == '__main__':
    unittest.main()
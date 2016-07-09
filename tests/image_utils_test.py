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
        resize_1 = utils.resizeImagesDiffHeightWidth(2, 2, self.images_1)[0]
        self.assertEqual(resize_1.shape, (2, 2))

        resize_2 = utils.resizeImagesDiffHeightWidth(2, 3, self.images_1)[0]
        self.assertEqual(resize_2.shape, (2, 3))

        resize_3 = utils.resizeImages(2, self.images_1)[0]
        self.assertEqual(resize_3.shape, (2, 2))

        resize_4 = utils.resizeImages(2, self.images_2)[0]
        self.assertEqual(resize_4.shape, (2, 2))

    def test_convertToGrayscale(self):
        grayscale = utils.convertToGrayscale(self.images_2)

        images_are_grayscale = True

        for img in range(len(grayscale)):
            h, w = grayscale[img].shape
            for i in range(w):
                for j in range(h):
                    r, g, b = grayscale[img].getpixel((i, j))
                    if r != g != b:
                        images_are_grayscale = False

        self.assertTrue(images_are_grayscale)

    def test_cropImage(self):
        cropped_image = utils.cropImage(self.image_1, 1, 1)

        self.assertEqual(cropped_image.shape, (3, 3))

    def test_readImages(self):
        images_read = utils.readImages('/tests/')

        self.assertEqual(images_read.shape, 1)

if __name__ == '__main__':
    unittest.main()
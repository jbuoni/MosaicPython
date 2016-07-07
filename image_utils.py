import numpy
import cv2
import os
import glob

"""
    Resize all images in array. Called if height
    and width are the same value

    http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#void resize(InputArray src, OutputArray dst, Size dsize, double fx, double fy, int interpolation)

    Args:
        size: Height and width of the image
        images: Array of images
    Returns:
        array of resized images
"""
def resizeImages(size, images):
    return resizeImages(size, size, images)


"""
    Resize all images in array.

    Args:
        height: Image hight as an int
        width: Image width as an int
        images: Array of images
    Returns:
        array of resized images
"""
def resizeImages(height, width, images):
    output = []
    for image in range(len(images)):
        image = cv2.resize(image, (width, height))
        output.append(image)
    return output


"""
    Converts images to grayscale
    http://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html

    Args:
        images: Array of images
    Returns:
        array of grayscale images
"""
def convertToGrayscale(images):
    output = []

    for image in range(len(images)):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        output.append(gray_image)

    return output


"""
    Crop image

    Args:
        image: Numpy 2d array representing the image
        cropX: Crop for each column
        cropY: Crop for each row

    Returns:
        Cropped image
"""
def cropImage(image, cropX, cropY):
    return image[: image.shape[0] - cropX, : image.shape[1] - cropY]

"""
    Copied from assignment 11.
    This function reads in input images from a image directory

    Note: This is implemented for you since its not really relevant to
    computational photography (+ time constraints).

    Args:
        image_dir (str): The image directory to get images from.

    Returns:
        images(list): List of images in image_dir. Each image in the list is of
                      type numpy.ndarray.

"""
def readImages(image_dir):
    extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg',
                  'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']

    search_paths = [os.path.join(image_dir, '*.' + ext) for ext in extensions]
    image_files = sorted(reduce(list.__add__, map(glob, search_paths)))
    images = [cv2.imread(f, cv2.IMREAD_UNCHANGED | cv2.IMREAD_COLOR)
              for f in image_files]

    return images
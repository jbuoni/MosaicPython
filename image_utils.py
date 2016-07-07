import numpy
import cv2
import os
import glob

"""
    Resize all images in array. Called if height
    and width are the same value

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
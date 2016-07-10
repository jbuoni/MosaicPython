import cv2
import os
from glob import glob
import numpy as np

"""
    Documentation:
    Algorithm understanding:
        http://www.drdobbs.com/understanding-photomosaics/184404848

    Other
        http://effbot.org/imagingbook/image.htm
        https://gist.github.com/olooney/1246268
        http://stackoverflow.com/questions/2270874/image-color-detection-using-python
        http://miriamposner.com/classes/medimages/3-use-opencv-to-find-the-average-color-of-an-image/
        http://stackoverflow.com/questions/2270874/image-color-detection-using-python/2270895#2270895
        https://codeyarns.com/2014/01/16/how-to-convert-between-numpy-array-and-pil-image/
        https://en.wikipedia.org/wiki/Image_histogram
        http://stackoverflow.com/questions/7563315/how-to-loop-over-histogram-to-get-the-color-of-the-picture
        http://blog.wolfram.com/2008/05/02/making-photo-mosaics/
        http://programmers.stackexchange.com/questions/254955/algorithms-for-making-image-mosaics-is-there-a-quicker-way-than-this
        http://williamedwardscoder.tumblr.com/post/84505278488/making-image-mosaics
        http://royvanrijn.com/blog/2014/04/mosaic-algorithm/
        http://miriamposner.com/classes/medimages/3-use-opencv-to-find-the-average-color-of-an-image/
"""


def resizeimages(size, images):
    """
    Resize all images in array. Called if height
    and width are the same value

    http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#void resize(InputArray src, OutputArray dst, Size dsize, double fx, double fy, int interpolation)

    :param size: Height and width of the image
    :param images: Array of images
    :return: Array of resized images
    """
    return resizeimages_diffheightwidth(size, size, images)


def resizeimages_diffheightwidth(height, width, images):
    """
        Resize all images in array.

        Args:
            height: Image hight as an int
            width: Image width as an int
            images: Array of images
        Returns:
            array of resized images
    """
    output = []
    for image in range(len(images)):
        image = resizeimage(height, width, image)
        output.append(image)
    return output


def resizeimage(height, width, image):
    """
    Resize a single image to a specified height and width

    :param height: New height.
    :param width: New width. In most cases, same as height.
    :param image: Image to resize
    :return: Resized image as array
    """
    return cv2.resize(image, (height, width))


def converttograyscale(image):
    """
    Converts images to grayscale
    http://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html

    :param image: Image to convert to grayscale
    :return: Greyscale image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def createfullimage(path, patchsize, greyscale=False):
    """
    To ensure that the image is of the correct size, we want to prevent overflow
    that we would have run into if we do not alter the size of the image. To do this, we
    want to ensure that the width and height will be divisible by the patch size.

    :param path: path to full image. Should include image file name
    :param patchsize: Size of patches for image. Used in resizing the full image
    :param greyscale: (bool) True if a greyscale
    :return:
    """
    image = None

    if greyscale:
        image = cv2.imread(path, 0)
    else:
        image = cv2.imread(path)

    height = image.shape[0]
    width = image.shape[1]

    # Divide by patch size, then increase it by the multiple of patch size.
    # I did this, because it seemed like an approach that more of the published mosaic software tools
    # used over just cropping the image to be divisible by the patch size.
    image = cv2.resize(image, (width / patchsize * patchsize, height / patchsize * patchsize))
    cv2.imwrite('output/full_image.png', image)

    return image


def cropimage(image, cropX, cropY):
    """
    Crop image. This function is deprecated. After research, it was
    determined that there is a better way to create the full image of proper size

    :param image: Numpy 2d array representing the image
    :param cropX: Crop for each column
    :param cropY: Crop for each row
    :return: Cropped image
    """
    return image[: image.shape[0] - cropX, : image.shape[1] - cropY]


def readimages(image_dir, greyscale=False):
    """
    Copied from assignment 11.
    This function reads in input images from a image directory.
    Slightly modified to fit what we are doing here.

    :param image_dir: (str) The image directory to get images from.
    :param greyscale (bool) True if a greyscale
    :return: List of images mapped to a file name in image_dir. Each image in the list is of
                      type numpy.ndarray.
    """
    extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg',
                  'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']

    search_paths = [os.path.join(image_dir, '*.' + ext) for ext in extensions]
    image_files = sorted(reduce(list.__add__, map(glob, search_paths)))

    image_objects = []

    for i in image_files:
        image = None

        if greyscale:
            image = cv2.imread(i, 0)
        else:
            image = cv2.imread(i, cv2.IMREAD_UNCHANGED | cv2.IMREAD_COLOR)

        image_obj = {}
        image_obj["path"] = os.path.join(image_dir, i)
        image_obj["image"] = image

        image_objects.append(image_obj)

    return image_objects


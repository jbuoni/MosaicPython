import numpy
import cv2
import os
import glob

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


def resizeimages(size, images):
    return resizeimages_diffheightwidth(size, size, images)


"""
    Resize all images in array.

    Args:
        height: Image hight as an int
        width: Image width as an int
        images: Array of images
    Returns:
        array of resized images
"""


def resizeimages_diffheightwidth(height, width, images):
    output = []
    for image in range(len(images)):
        image = resizeimage(height, width, image)
        output.append(image)
    return output


def resizeimage(height, width, image):
    return cv2.resize(image, (height, width))

"""
    Converts images to grayscale
    http://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html

    Args:
        images: Array of images
    Returns:
        array of grayscale images
"""


def converttograyscale(images):
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


def cropimage(image, cropX, cropY):
    return image[: image.shape[0] - cropX, : image.shape[1] - cropY]

"""
    Copied from assignment 11.
    This function reads in input images from a image directory.
    Slightly modified to fit what we are doing here.

    Note: This is implemented for you since its not really relevant to
    computational photography (+ time constraints).

    Args:
        image_dir (str): The image directory to get images from.

    Returns:
        images(list): List of images mapped to a file name in image_dir. Each image in the list is of
                      type numpy.ndarray.

"""


def readimages(image_dir):
    extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg',
                  'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']

    search_paths = [os.path.join(image_dir, '*.' + ext) for ext in extensions]
    image_files = sorted(reduce(list.__add__, map(glob, search_paths)))

    image_objects = []

    for i in image_files:
        image = cv2.imread(image_files[i], cv2.IMREAD_UNCHANGED | cv2.IMREAD_COLOR)

        image_obj = {}
        image_obj["path"] = os.path.join(image_dir, image_files[i])
        image_obj["image"] = image

        image_objects.append(image_obj)

    return image_objects


# mosaic.py
# Jason Buoni
# jason.buoni@gatech.edu
import image_utils as utils
import math
import cv2
import sys
import numpy as np
import json

"""
    Make these global to allow for repeating with more of a range.
    If these were not global, we would see more repeated images.
"""
patchimages = []
patchimages_copy = []
"""
    These probably don't need to be global, but they get passed around a lot so I made them so.
"""
patch_size = 0
width = 0
greyscale = False
channel = "rgb"


def getcolordistance_rgb(rgb1, rgb2):
    """
    Get RGB color distance. Though it appears that there are better ways start off using this
    http://stackoverflow.com/questions/8863810/python-find-similar-colors-best-way

    :param rgb1: First average
    :param rgb2: Second image average
    :return:
    """

    # Cast as int64 to ensure binary shift will work
    rmean = ((rgb1["r"] + rgb2["r"]) / 2).astype(np.int64)
    r_val = (rgb1["r"] - rgb2["r"]).astype(np.int64)
    g_val = (rgb1["g"] - rgb2["g"]).astype(np.int64)
    b_val = (rgb1["b"] - rgb2["b"]).astype(np.int64)

    return math.sqrt((((512 + rmean) * r_val * r_val) >> 8) + 4 * g_val * g_val + (((767 - rmean) * b_val * b_val) >> 8))


def calculatecolordistantance_hsv(hsv1, hsv2):
    """
    Get HSV color distance.
    http://stackoverflow.com/questions/35113979/calculate-distance-between-colors-in-hsv-space
    :param hsv1: First average
    :param hsv2: Second image average
    :return:
    """
    h_dist = min(abs(hsv2["h"] - hsv1["h"]), 360 - abs(hsv2["h"] - hsv1["h"])) / 180.0
    s_dist = abs(hsv2["s"] - hsv1["s"])
    v_dist = abs(hsv2["v"] - hsv1["v"]) / 255.0

    return math.sqrt(h_dist * h_dist + s_dist * s_dist + v_dist * v_dist)


def getclosestpatchmatch(full_color_average, patch_images):
    """
    Determine the closest match to a patch image

    :param full_color_average: average value of the full color image at the patch pixels
    :param patch_images: patch images to compare
    :return: object containing the index of the image, and the image itself that closest matches the full_color_average:
    {
        image: patch image
        index: index of image in patchimage array
    }
    """
    min_distance = sys.maxint
    return_image = {}
    for i in range(len(patch_images)):
        image = patch_images[i]

        if greyscale:
            distance = (full_color_average["greyscale"] - image["color_averages"]["greyscale"]).astype(np.uint8)
        elif channel == "rgb":
            distance = getcolordistance_rgb(full_color_average, image["color_averages"])
        elif channel == "hsv":
            distance = calculatecolordistantance_hsv(full_color_average, image["color_averages"])

        if distance < min_distance:
            min_distance = distance
            return_image["image"] = image["resized_image"]
            # Save the index so we can remove the image if repeat == false
            return_image["index"] = i

    if min_distance == sys.maxint:
        print "Out of images..."

    return return_image


def generatepathimages(image_dir, size=None, forjson=False):
    """
    Create the patch images. Grab the image from the image directory and resize it to match
    patch_size.

    :param image_dir: Directory that contains all patch images
    :param greyscale: (bool) Converts image to greyscale if true
    :return: List of all patch image objects:
    {
        path: Image path
        image: Full image
        resized_image: Image of size patch_size * patch_size
        color_averages: r, g, b channel color averages
    }
    """
    #Read all images
    images = utils.readimages(image_dir, greyscale)

    # Create patch image object
    output = []

    # For file generator only
    if size is not None:
        global patch_size
        patch_size = size

    #Create array of patch image objects
    for i in range(len(images)):
        patch_image = {}

        # Get image
        image_obj = images[i]
        image = image_obj["image"]

        #Create patch image object
        patch_image["path"] = image_obj["path"]
        if not forjson:
            patch_image["image"] = image
            patch_image["resized_image"] = utils.resizeimage(patch_size, patch_size, image)

        patch_image["color_averages"] = getchannelcoloraverages(image, forjson)

        output.append(patch_image)

    return output


def generatepathimagesfromjson(data):
    """
    Create the patch images. Grab the image from the image directory and resize it to match
    patch_size.
    http://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file-in-python

    :param data: json data
    :return: List of all patch image objects:
    {
        path: Image path
        image: Full image
        resized_image: Image of size patch_size * patch_size
        color_averages: r, g, b channel color averages
    }
    """

    #Read all images
    images = utils.readimages(data['image_dir'], greyscale)

    # Create patch image object
    output = []

    #Create array of patch image objects
    for i in range(len(images)):
        patch_image = {}

        # Get image
        image_obj = images[i]
        image = image_obj["image"]

        #Create patch image object
        patch_image["path"] = image_obj["path"]
        patch_image["image"] = image
        patch_image["resized_image"] = utils.resizeimage(patch_size, patch_size, image)
        patch_image["color_averages"] = data["images"][i]["color_averages"]

        output.append(patch_image)

    return output

def getaveragechannelcolor(image, channel, rng=256):
    """
    Get the average color of an image. Through some digging I determined that using a
    histogram was the best way to do this. Create a histogram, then get the sum and divide it by
    the height and width of the image.

    Documentation:
        https://en.wikipedia.org/wiki/Image_histogram
        http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/histogram_calculation/histogram_calculation.html
        http://docs.opencv.org/2.4/modules/imgproc/doc/histograms.html?highlight=calchist#calchist
        http://stackoverflow.com/questions/7563315/how-to-loop-over-histogram-to-get-the-color-of-the-picture

    :param image: Image to get average
    :param channel: Color channel (R, G, B)
    :param rng: Channel boundries. 256 unless specified
    :return: Float value representing the average color
    """

    height = image.shape[0]
    width = image.shape[1]

    histogram = cv2.calcHist([image], [channel], None, [rng], [0, rng])
    color_sum = sum(idx * histogram[idx] for idx in range(len(histogram)))

    return (color_sum / (width * height)).astype(float)


def getgreyscaleaverage(image):
    """
    Get average greyscale value

    :param image: Image to get average
    :return: Float value representing the average greyscale value
    """
    total_sum = sum(map(sum, image))

    return (total_sum / (image.shape[1] * image.shape[0])).astype(np.uint8)


def getchannelcoloraverages(image, forjson=False):
    """
    Get the channel averages for an image.
    http://stackoverflow.com/questions/23202132/splitting-an-rgb-image-to-r-g-b-channels-python

    :param image: Image to get RGB average
    :return:
    """
    output = {}

    if greyscale:
        output["greyscale"] = getgreyscaleaverage(image)
    else:
        if channel == "rgb" or forjson:
            # According to the split in the SO post b is at 0, g at 1, r at 2
            output["b"] = getaveragechannelcolor(image, 0)[0]
            output["g"] = getaveragechannelcolor(image, 1)[0]
            output["r"] = getaveragechannelcolor(image, 2)[0]

        if channel == "hsv" or forjson:
            # Convert image to HSV
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Range of h should be 180
            output["h"] = getaveragechannelcolor(image, 0, 180)[0]
            output["s"] = getaveragechannelcolor(image, 1)[0]
            output["v"] = getaveragechannelcolor(image, 2)[0]
    return output


def createpatchline(idx, full_image, repeat):
    """
    For each "line" of the image, which is the same height of the patch, we want to
    replace what is displayed in the full image, with patch images. This function will
    go through each portion of that line, and replace the full image with patches.

    :param idx: Height index. Will be in intervals of size.
    :param full_image: Image to be patched
    :param patch_size: Size of patched images
    :return:
    """
    # Divide by patch size so that we
    for w in range(width / patch_size):
        # Create a "patch" of the image using the full image. Used to compare colors
        full_image_patch = full_image[idx * patch_size:(idx + 1) * patch_size, w * patch_size:(w + 1) * patch_size]
        full_color_average = getchannelcoloraverages(full_image_patch)
        #Get closest match
        patch = getclosestpatchmatch(full_color_average, patchimages)
        #Add patch
        full_image[idx * patch_size:(idx + 1) * patch_size, w * patch_size:(w + 1) * patch_size] = patch["image"]

        if not repeat:
            patchimages.remove(patchimages[patch["index"]])

        if len(patchimages) == 0:
            global patchimages
            patchimages = list(patchimages_copy)

    return full_image

def generatemosaic(full_img_dir, image_dir, size, greyscale_val=False, repeat=True, channelparam="rgb"):
    """
    Generate the full mosaic image

    :param full_img_dir: File path (file name included) of full image. Will be patched with smaller images
    :param image_dir: Directory of images used to create patches.
    :param greyscale: True or False, depending on if the output should be a greyscale or not
    :param size: size of patches
    :param repeat: Default is true. Set to false if we want to not repeat images.
        ** NOTE: Not repeating images decreases the quality of the mosaic. Also, if we run out of images
            when generating the mosaic, the program will recreate the patched image array, meaning that there
            will be repeating images, though the the number of duplicates will be less.
    :return: Mosaic image as np array
    """

    print "Generating full image"

    usedjsonfile = False

    if image_dir == 'patched_images.json':
        print "Reading images from json"
        with open('patched_images.json') as data_file:
            data = json.load(data_file)
        size = data['size']
        image_dir = data['image_dir']
        usedjsonfile = True


    global channel
    channel = channelparam

    global patch_size
    patch_size = size

    global greyscale
    greyscale = greyscale_val

    fullimage = utils.createfullimage(full_img_dir, patch_size, greyscale)

    print "Generating patch images"
    if usedjsonfile:
        global patchimages
        patchimages = generatepathimagesfromjson(data)
    else:
        global patchimages
        patchimages = generatepathimages(image_dir)

    # For repeating. Typically, we run out if images unless there are a ton for smaller patches
    # http://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list-in-python
    global patchimages_copy
    patchimages_copy = list(patchimages)

    global width
    height = fullimage.shape[0]
    width = fullimage.shape[1]

    print "Generating mosaic image of size ", height, " by ", width

    for i in range(height / size):
        fullimage = createpatchline(i, fullimage, repeat)

    print "Finished processing of image"

    return fullimage


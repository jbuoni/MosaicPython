import image_utils as utils
import math
import cv2
import sys

"""
    Get RGB color distance. Though it appears that there are better ways start off using this
    http://stackoverflow.com/questions/8863810/python-find-similar-colors-best-way
"""
def getcolordistance_rgb(rgb1, rgb2):

    rmean = (rgb1["r"] + rgb2["r"]) / 2
    r = rgb1["r"] - rgb2["r"]
    g = rgb1["g"] - rgb2["g"]
    b = rgb1["b"] - rgb2["b"]

    return math.sqrt((((512 + rmean) * r * r) >> 8) + 4 * g * g + (((767 - rmean) * b * b) >> 8))

def getclosestpatchmatch(full_color_average, patch_images):

    min_distance = sys.maxint
    return_image = {}
    for i in range(len(patch_images)):
        image = patch_images[i]

        distance = getcolordistance_rgb(full_color_average, image["color_averages"])

        if distance < min_distance:
            min_distance = distance
            return_image = image["resized_image"]

    return return_image

def generatepathimages(image_dir, size):
    #Read all images
    images = utils.readimages(image_dir)

    # Create patch image object
    patchimages = []

    #Create array of patch image objects
    for i in range(len(images)):
        patch_image = {}

        # Get image
        image_obj = images[i]
        image = image_obj["image"]

        #Create patch image object
        patch_image["path"] = image_obj["path"]
        patch_image["image"] = image
        patch_image["resized_image"] = utils.resizeimage(size, size, image)
        patch_image["color_averages"] = getChannelColorAverages(image)

        patchimages.append(patch_image)

    return patchimages


"""
    Returns the average color for a specific channel using a histogram.

    Documentation:
        https://en.wikipedia.org/wiki/Image_histogram
        http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/histogram_calculation/histogram_calculation.html
        http://docs.opencv.org/2.4/modules/imgproc/doc/histograms.html?highlight=calchist#calchist
        http://stackoverflow.com/questions/7563315/how-to-loop-over-histogram-to-get-the-color-of-the-picture
"""
def getaveragechannelcolor(image, index, rng):

    height, width, colorRange = image.shape

    histogram = cv2.calcHist(image, index, None, rng, [0, rng])
    color_sum = sum(idx * histogram[idx] for idx in range(len(histogram)))

    return color_sum / (width * height)


def getChannelColorAverages(image):
    output = {}

    output["b"] = getaveragechannelcolor(image, 0, 256)
    output["g"] = getaveragechannelcolor(image, 1, 256)
    output["r"] = getaveragechannelcolor(image, 2, 256)

    return output

def createfullimage(path, patchsize):
    image = cv2.imread(path)
    height, width, colorRange = image.shape

    image = cv2.resize(image, (width / patchsize * patchsize, height / patchsize * patchsize))
    return image


def createpatchline(idx, width, patchimages, full_image, patch_size):
    for j in range(width / patch_size):
        # Create a "patch" of the image using the full image. Used to compare colors
        full_image_patch = full_image[idx * patch_size:(idx + 1) * patch_size, j * patch_size:(j + 1) * patch_size]
        full_color_average = getChannelColorAverages(full_image_patch)
        #Get closest match
        patch = getclosestpatchmatch(full_color_average, patchimages)
        #Add patch
        full_image[idx * patch_size:(idx + 1) * patch_size, j * patch_size:(j + 1) * patch_size] = patch

        return full_image

def generatemosaic(full_img_dir, image_dir, greyscale, size):
    patchimages = generatepathimages(image_dir, size)

    fullimage = createfullimage(full_img_dir, size)

    height, width, colorRange = fullimage.shape

    print "Generating mosaic image of size ", height, " by ", width

    for i in range(height / size):
        fullimage = createpatchline(i, width, patchimages, fullimage, size)

    print "Finished processing of image"

    cv2.imwrite("mosaic.jpg", fullimage)


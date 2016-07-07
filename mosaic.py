import image_utils as utils


def generateMosaic(full_image, images, greyscale, height, width):
    # Resize images
    images_resized = utils.resizeImages(images, height, width)

    if greyscale == True:
        images_resized = utils.convertToGrayscale(images_resized)
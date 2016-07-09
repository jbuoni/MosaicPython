import mosaic
import image_utils as utils
import sys
import cv2


# http://williamedwardscoder.tumblr.com/post/84505278488/making-image-mosaics
def main():
    if len(sys.argv) != 4:
        print "Arguments cannot equal 0. Please pass in, image directory, full image, greyscale, height, and width"

    # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    image_dir = sys.argv[0]
    full_img_dir = sys.argv[1]
    greyscale = sys.argv[2]
    height = sys.argv[3]
    width = sys.argv[4]

    result = mosaic.generatemosaic(full_img_dir, utils.readimages(image_dir), greyscale, height, width)

    cv2.imwrite('mosaic.png', result)

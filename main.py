import mosaic
import image_utils as utils
import os
import cv2


# http://williamedwardscoder.tumblr.com/post/84505278488/making-image-mosaics
def main():
    # if len(sys.argv) != 4:
    #     print "Arguments cannot equal 0. Please pass in, image directory, full image, greyscale, height, and width"

    # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    # image_dir = sys.argv[0]
    # full_img_dir = sys.argv[1]
    # greyscale = sys.argv[2]
    # height = sys.argv[3]
    # width = sys.argv[4]

    # image_dir = "/source/patches"
    full_img_dir = "source/full/donkey.JPG"
    greyscale = False
    size = 20

    image_dir = os.path.join("source", "patches")

    result = mosaic.generatemosaic(full_img_dir, image_dir, greyscale, size)

    cv2.imwrite('mosaic.png', result)

if __name__ == "__main__":
    main()

import mosaic
import sys
import os
import cv2


def main():
    """
    Main function

    Documentation:
        http://williamedwardscoder.tumblr.com/post/84505278488/making-image-mosaics
        https://github.com/cinemast/OpenMosaic
    """
    print "Running Mosaic Image Generator. Possible args (all optional) size, greyscale, repeat." \
          "If not specified, the defaults are 20, False, True."

    size = 20
    greyscale = False
    repeat = True

    # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    if len(sys.argv) > 2:
        greyscale = bool(sys.argv[2])

    if len(sys.argv) > 3:
        repeat = bool(sys.argv[3])

    full_img_dir = "source/full/yunghumma.png"
    image_dir = os.path.join("source", "patches")

    result = mosaic.generatemosaic(full_img_dir, image_dir, size, greyscale, repeat)

    cv2.imwrite('mosaic.png', result)

if __name__ == "__main__":
    main()

# main.py
# Jason Buoni
# jason.buoni@gatech.edu
import mosaic
import sys
import os
import cv2
import ntpath
import ast

def main():
    """
    Main function

    Documentation:
        http://williamedwardscoder.tumblr.com/post/84505278488/making-image-mosaics
        https://github.com/cinemast/OpenMosaic
        http://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
    """
    print "Running Mosaic Image Generator. Possible args (all optional) size, greyscale, repeat." \
          "If not specified, the defaults are 20, False, True."

    size = 20
    greyscale = False
    repeat = True
    full_img_dir = "source/full/yunghumma.png"
    image_dir = os.path.join("source", "patches")
    channel = "rgb"

    if len(sys.argv) > 1:
        full_img_dir = sys.argv[1]

    if len(sys.argv) > 2:
        image_dir = sys.argv[2]

    if len(sys.argv) > 3:
        size = int(sys.argv[3])

    if len(sys.argv) > 4:
        greyscale = ast.literal_eval(sys.argv[4])

    if len(sys.argv) > 5:
        repeat = ast.literal_eval(sys.argv[5])

    if len(sys.argv) > 6:
        channel = sys.argv[6]

    filename = "output/" + ntpath.basename(full_img_dir).replace(".", "_") + "_" + str(size) + "_" + channel

    if greyscale:
        filename += "_greyscale"

    if repeat:
        filename += "_repeat"
    else:
        filename += "_no_repeat"

    filename += ".png"

    print filename

    result = mosaic.generatemosaic(full_img_dir, image_dir, size, greyscale, repeat, channel)

    cv2.imwrite(filename, result)

if __name__ == "__main__":
    main()

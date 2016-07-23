import json
import io
import sys
import mosaic as pyMosaic

"""
    The FileGenerator will be responsible for generating a JSON file of the patch images using
    a specified directory. This will reduce the time it takes for the application to run
    as it creates the patch images, which reduces a lot of up front costs when running the image
    generator multiple times.

    http://stackoverflow.com/questions/10252010/serializing-python-object-instance-to-json
    http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
    http://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
"""

def main():

    if len(sys.argv) > 1:
        image_dir = sys.argv[1]
    else:
        print "Cannot generate file. Please specify input path as the first argument."
        return

    if len(sys.argv) > 2:
        size = int(sys.argv[2])
    else:
        print "Cannot generate file. Please specify patch size as the second argument."
        return

    print "Generating patched images."
    patched_images = pyMosaic.generatepathimages(image_dir, size, True)

    print "Saving as json."
    with open('patched_images.json', 'w') as output_file:
        json.dump({'image_dir': image_dir, 'size': size, 'images': patched_images}, output_file)


if __name__ == "__main__":
    main()
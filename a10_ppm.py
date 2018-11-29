######################################################################
# Author: Dr. Scott Heggen      TODO: Ela Jamali & Emely Alfaro
# Username: heggens             TODO: Jamalie & Alfarozavale
#
# Assignment: A11: PPM
#
# Purpose: To learn more about lists of lists and deep copies and also
# to enhance a larger module (ppm.py)
# ######################################################################
# Acknowledgements:
#
# Original code written by Dr. Jan Pearce
#
# Ben Stephenson: http://pages.cpsc.ucalgary.ca/~jacobs/Courses/cpsc217/W10/code/Topic7/ppm.py
# working from a class: http://bytes.com/topic/python/answers/520360-trouble-displaying-image-tkinter
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

from ppm import *
# HINT: Be sure you work with a single ppm object at a time


def main():
    # The following interaction is just for testing.  You will improve this.

    wn = PPM_set_up()   # To use the PPM class, this must appear at the beginning of your program. You'll pass wn into
                        # the class init method when creating new PPM objects

    print("\nWelcome to the PPM introduction!\n")

    # Example using the default file
    ppmdefault = PPM(wn)
    ppmdefault.PPM_display()            # NOTE: This displays the image, but it's really small! It may be hard to find.
    print("---")

    # Example using a user-defined file
    filename = input("Please input name of PPM-P3 file: ")
    ppmobject = PPM(wn, filename)
    ppmobject.PPM_make_red()
    ppmobject.PPM_grayscale()
    ppmobject.PPM_flip_horizontal()
    ppmobject.PPM_rotateclockwise()
    ppmobject.PPM_negative_scale()
    ppmobject.PPM_display()
    # TODO Add your own method calls for the methods you are completing/creating from scratch

    print("\nPush the Quit button to exit all files.")

    PPM_render(wn)  # needed to render all of the images you have instantiated


main()

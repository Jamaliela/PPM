######################################################################
# Author: Dr. Scott Heggen      TODO: Change this to your names
# Username: heggens             TODO: Change this to your usernames
#
# Assignment: A11: PPM
#
# Purpose:  A module for loading and displaying PPM-P3 files using Python
######################################################################
# Usage Instructions:
#
# To use you must call a helper function:
# wn = PPM_set_up()
#
# Following this, you may use the class methods which reads an input PPM-P3 file in the constructor.
# It never writes to the input file, instead creating two output files with
# "-asc" and "-bin", respectively appended to the input filename.
# These are intended for the user's use and to display respectively.
#
# to render the image:
# PPM_render(wn)   # needed to render all of the images you have instantiated where the argument is that which
#                  # was returned from PPM_set_up()
#
# The image data is stored in the following member variables:
# self.magic
# self.width
# self.height
# self.colormax
# self.pixellist
#
# # Constructor usage examples:
# df = PPM()
# df = PPM("bc-flowers.ppm")
#
#
# Display image example:
# df.PPM_display()
#
#
# Change image by changing pixellist:
# bc.PPM_updatefrompixellist(mylist)
#
######################################################################
# Acknowledgements:
#
# Original code written by Dr. Jan Pearce, Berea College
#
# Attributions:
    # Ben Stephenson: http://pages.cpsc.ucalgary.ca/~jacobs/Courses/cpsc217/W10/code/Topic7/ppm.py
    # working from a class: http://bytes.com/topic/python/answers/520360-trouble-displaying-image-tkinter
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import tkinter as tk    # for display of the PPM image
import copy             # You might need this later...

####################
# This section represents helper functions which are needed by the PPM class.
global tkintertoggle        # Needed as global to ensure a single Tkinter instance
tkintertoggle = False


def PPM_set_up(): # This must be called at the beginning of any program which uses the PPM class
    """
    Sets up the Tkinter root instance which allows for image windows

    :return: a Tk tkinter object
    """
    master = tk.Tk()
    return master           # save and send to all PPM methods which need it, including the initializer


def PPM_render(master):
    """
    Renders all PPM instances

    :param master: a Tk tkinter object
    :return: None
    """
    master.mainloop()
# End helper functions section
####################


class PPM_Exception(Exception):
    """
    Create a Python class to enable meaningful error messages on exceptions.
    """
    def __init__(self, value):
        """
        Initializer method for the PPM_Exception class.

        :param value: the exception value
        """
        self.value = value

    def __str__(self):
        """
        Modifies the str method to return more meaningful error messages
        :return: a string representing the error message
        """
        return repr(self.value) # allows a meaningful error message to be displayed

# End PPM_Exception class


class PPM:
    """
    Class which can be used to open, close, and display PPM P3 (ASCII) files.
    """

    PPMDEFAULT = '''P3
# Created by OOM class, by Dr. Jan Pearce, Berea College
8 10
255
140 140 140 120 120 120 100 100 100 80 80 80 60 60 60 40 40 40 20 20 20 0 0 0
120 120 120 63 72 204 63 72 204 63 72 204 63 72 204 252 252 255 255 255 255 15 15 15
105 105 105 255 255 255 63 72 204 255 255 255 63 72 204 255 255 255 255 255 255 30 30 30
90 90 90 255 255 255 63 72 204 63 72 204 63 72 204 255 255 255 255 255 255 45 45 45
75 75 75 255 255 255 63 72 204 255 255 255 63 72 204 63 72 204 63 72 204 60 60 60
60 60 60 63 72 204 63 72 204 63 72 204 63 72 204 255 255 255 63 72 204 75 75 75
45 45 45 255 255 255 255 255 255 63 72 204 255 255 255 254 254 254 255 255 255 90 90 90
30 30 30 255 255 255 255 255 255 63 72 204 255 255 255 255 255 255 63 72 204 105 105 105
15 15 15 252 252 253 255 255 255 63 72 204 63 72 204 63 72 204 63 72 204 120 120 120
0 0 0 20 20 20 40 40 40 60 60 60 80 80 80 100 100 100 120 120 120 140 140 140'''
    def __init__(self, master, inasciifile = "default.ppm"):
        """
        Opens or creates a PPM P3 file named inasciifile to construct a PPM object

        :param master: a Tk tkinter object
        :param inasciifile: the input ascii file representing the image
        """
        global tkintertoggle            # This must be global to allow multiple PPM objects but make only a single Quit button on the Tkinter canvas.
        self.root = master
        self.root.title("PPM Quit")

        if tkintertoggle == False:
            tk.Button(self.root, text="QUIT", fg="red", command=self.root.quit).pack()
            tkintertoggle = True

        if inasciifile == "": # makes default.ppm as input file if none exists
            inasciifile = "default.ppm"

        self.inasciifile = inasciifile                  # This file is used only for reading
        self.outasciifile = inasciifile[:-4]+"-asc.ppm" # created to store modifications
        self.outbinfile = inasciifile[:-4]+"-bin.ppm"   # binary ppm filename needed for viewing
        self.title = inasciifile                        # used for the title of the display window
        self.magic = "P3"                               # ppm file type
        self.comment = "# Created by ppm-class, by Dr. Jan Pearce\n"
        self.width = 0
        self.height = 0
        self.colormax = 255         # should be set to 255
        self.ascii = ""             # will store the color intensities in P3 format
        self.pixellist = []         # will store nested list containing pixel colors
        self.image = ""             # It is necessary that this be a member variable for Tk to display image correctly
        # If there is no filename given, make a file to work with
        self.label = ""             # Used to place image in window
        if self.inasciifile == "default.ppm" :
            self.ascii = self.PPMDEFAULT
            tmpfile = open(self.inasciifile, "w")
            tmpfile.write(self.ascii)
            tmpfile.close()
        print("PPM object created from {0}".format(self.inasciifile))
        self.PPM_makeoutputfiles()  # Makes ascii and binary output files

    def PPM_makeoutputfiles(self):
        """
        Given self.inasciifile, sets self.ascii and creates both ascii and binary files for output

        :return: None
        """
        outtmpfile = open(self.outasciifile, "w")
        intempfile = open(self.inasciifile, 'r')        # self.inasciifile must have data
        self.ascii = intempfile.read()
        outtmpfile.write(self.ascii)
        intempfile.close()
        outtmpfile.close()
        self.PPM_load(self.inasciifile)
        self.PPM_convert2bin()

    def PPM_partition(self, strng, ch):
        """
        Returns a triple with all characters before the delimiter, the delimiter itself if present,
        and all of the characters after the delimiter (if any)

        :param strng: a string to partition
        :param ch: the character to use as the delimiter
        :return: a tuple containing 1) the string, 2) the delimiter, and 3) all characters after the delimiter
        """
        if ch in strng:
            i = strng.index(ch)
            return (strng[0:i], strng[i], strng[i+1:])
        else:
            return (strng, None, None)

    def PPM_clean(self, strng):
        """
        Removes all single line comments present in a string, including all white space at the end,
        the newline, and linefeed characters.

        :param strng: an input string
        :return: A string with all characters after the comment character removed.
        """
        (retval, junk1, junk2) = self.PPM_partition(strng, "#")
        return retval.rstrip(" \t\n\r")

    def PPM_load(self, inasciifile):
        """
        Input parameter inasciifile is a string containing the name of the file to load
        Assumes an ASCII PPM-P3 (non-binary) file.
        Loads the named image file from disk, and stores the image data in member variables.

        :param inasciifile: the name of the file to load
        :return: None
        """

        # Open the input file
        infile = open(self.inasciifile,"r")

        # Read the magic number out of the top of the file and verify that we are
        # reading from an ASCII PPM-P3 file
        tmpln = infile.readline()
        self.ascii += tmpln
        self.magic = self.PPM_clean(tmpln)
        if (self.magic != "P3"):
            raise PPM_Exception('The file being loaded does not appear to be a valid ASCII PPM-P3 file')

        # Get the image dimensions
        tmpln = infile.readline()
        while tmpln[0] == '#':          # Dump full comment lines
            tmpln = infile.readline()
        self.ascii += tmpln
        imgdimensions = self.PPM_clean(tmpln)

        # Unpack dimensions
        (width, sep, height) = self.PPM_partition(imgdimensions," ")
        self.width = int(width)
        self.height = int(height)
        if (self.width <= 0) or (self.height <= 0):
            raise PPM_Exception("The file being loaded does not appear to have valid dimensions ({0} x {1})".format(str(width), str(height)))

        # Get the maximum color value, which is assumed to be 255
        tmpln = infile.readline()
        self.ascii += tmpln
        self.colormax = int(self.PPM_clean(tmpln))
        if (self.colormax != 255):
            raise PPM_Exception("Warning: PPM file does not have a maximum intensity value of 255.  Image may not be handled correctly.")

      # Create a list of the color intensities
        color_list = []                     # hold intensity data temporarily in a list of intensity strings
        for line in infile:
            self.ascii += line
            line = self.PPM_clean(line)
            color_list += line.split(" ")
        infile.close()                      # Close input file since done
        self.PPM_makepixellist(color_list)  # Creates self.pixellist, a nested list of rows of [red, green, blue] pixels

    def PPM_makepixellist(self, color_list):
        """
        Creates self.pixellist, a nested list of rows of [red, green, blue] pixels
        from a color_list which contains an unnested list of strings

        :param color_list: a list of strings representing the colors
        :return: None
        """
        rcount = 0
        gcount = 1
        bcount = 2
        self.pixellist = []
        for row in range(self.height):
            self.pixellist.append([])
            for col in range(self.width):
                self.pixellist[row].append([int(color_list[rcount]), int(color_list[gcount]), int(color_list[bcount])])
                rcount += 3     # move to next red
                gcount += 3     # move to next green
                bcount += 3     # move to next blue

    def PPM_updatefrompixellist(self, pixellist, title="from_pixellist"):
        """
        Updates image object data and related files from input pixellist

        :param pixellist: a list of pixels
        :param title: the title of the window
        :return: None
        """
        strout = ""
        self.magic = "P3"
        self.colormax = 255
        self.width = len(pixellist[0])
        self.height = len(pixellist)
        header = self.magic+"\n"
        header += self.comment
        header += str(self.width) + " " + str(self.height)+"\n"+str(self.colormax)+"\n" # header is in ASCII
        for rowlist in pixellist:
            for pixel in rowlist:
                for color in pixel:
                    strout += str(color)+" "
            strout += "\n"
        self.ascii = header + strout
        self.pixellist = pixellist
        tmpfile = open(self.outasciifile, "w")
        tmpfile.write(self.ascii)
        tmpfile.close() #close tmpfile when done
        print("PPM object changed based upon list.")
        if self.title == "default.ppm":
            self.title = title
        self.PPM_convert2bin()

    def PPM_convert2bin(self):
        """
        Converts PPM-P3 to PPM-P6 using self.pixellist

        [04/07/2017] Credit to Conner Bondurant for fixing this function to work correctly Python 3

        :return: None
        """
        header = "P6\n"
        header += self.comment
        header += str(self.width) + " " + str(self.height)+"\n" + "255\n" # header is in ASCII
        strout = bytes()

        for rowlist in self.pixellist:
            for pixel in rowlist:
                for color in pixel:
                    strout += color.to_bytes(1, byteorder='big')

        # First write the header as ascii
        tmpfile = open(self.outbinfile, "w", newline="\n")
        tmpfile.write(header)
        tmpfile.close()         #close tmpfile when done
        # Then, write the image as binary
        tmpfile = open(self.outbinfile, "ab")
        tmpfile.write(strout)
        tmpfile.close()         #close tmpfile when done

    def PPM_set_title(self, title):
        """
        Setter for self.title (title of display window.)

        :param title: The title of the display window
        :return: None
        """
        self.title = title

    def PPM_display(self):
        """
        Displays PPM-P3 binary file using Tkinter

        :return: None
        """
        self.mywindow = tk.Toplevel(self.root)
        self.mywindow.geometry(str(self.width) + "x" + str(self.height)) # sets correct window size
        self.mywindow.wm_title(self.title)
        self.image = tk.PhotoImage(file = self.outbinfile)
        self.label = tk.Label(self.mywindow, image = self.image)
        self.label.place(x = 0, y = 0, height = self.height, width = self.width)


    def PPM_make_red(self):
        """
        Colorizes current image to red by using self.pixellist

        :return: None
        """
        newpixellist = self.pixellist
        self.width = len(newpixellist[0])
        self.height = len(newpixellist)
        row = 0
        for rowlist in newpixellist:
            col = 0
            for pixel in rowlist:
                newpixellist[row][col][1] = 0 # update green
                newpixellist[row][col][2] = 0 # update blue
                col += 1
            row += 1
        print(self.outasciifile + " output file turned red.")
        self.PPM_updatefrompixellist(newpixellist)      # This call will update all member attributes appropriately.

    def PPM_grayscale(self):
        """
        Converts image to grayscale

        :return: None
        """
        newpixellist = self.pixellist
        # Hint: What needs to be done here is to convert newpixellist to the equivalent greyscale image.
        # The final call to self.PPM_updatefrompixellist(newpixellist) is essential for updating member attribute appropriately.

        # TODO FIX ME: write the needed changes to newpixellist here

        self.PPM_updatefrompixellist(newpixellist)      # This call will update all member attributes appropriately.

    def PPM_flip_horizontal(self):
        """
        Flips image horizontally

        :return: None
        """
        newpixellist = self.pixellist

        # Hint 1: What needs to be done here is to convert newpixellist to the equivalent horizontally flipped image.
        # Hint 2: You might want a new object of the correct size or a deep copy.
        # The final call to self.PPM_updatefrompixellist(newpixellist) is essential for updating member attribute appropriately.

        # TODO FIX ME: write the needed changes to newpixellist here

        self.PPM_updatefrompixellist(newpixellist) # This call will update all member apttributes appropriately.

    def PPM_rotateclockwise(self):
        """
        Rotates image clockwise

        :return: None
        """
        newpixellist = self.pixellist

        # Hint 1: What needs to be done here is to convert newpixellist to the equivalent rotated image.
        # Hint 2: It might be helpful to make a new object of the correct size
        # The final call to self.PPM_updatefrompixellist(newpixellist) is essential for updating member attribute appropriately.

        # TODO FIX ME: write the needed changes to newpixellist here

        self.PPM_updatefrompixellist(newpixellist) # This call will update all member attributes appropriately.

    # TODO FIX ME: write at least one additional PPM class method

# End of PPM Class


# See a11-ppm.py for code that uses the PPM class.

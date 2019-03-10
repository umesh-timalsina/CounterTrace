import math
import numpy as np
from PIL import Image
import logging
import argparse
from matplotlib import pyplot as plt


class ContourTracer(object):
    """
    A Class That Implements the moore's
    Counter Tracing Algorithm
    """
    def __init__(self, image_path, width, height):
        """
        Initialize an image with image paths
        """
        self.logger = logging.getLogger("ContourTracer")
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        # im = Image.open(image_path).convert('L')
        self.tess = np.fromfile(image_path, dtype='uint8', sep="")
        self.tess = self.tess.reshape((width, height))
        self.tess = self.tess.clip(min=0)
        self.image_dims = self.tess.shape 
        self.logger.info("Loaded Image from {0} as {1}*{2} numpy array"
                            .format(image_path, self.tess.shape[0], self.tess.shape[1]))
        # plt.imshow(self.tess)
        # plt.show()

    def count_contours(self, pixel_intensity):
        """
        Counts the number of closed contours with the given pixel intensity

        -- Arguments:
            pixel_intensity(int) -- The intensity of the contour

        -- Returns:
            count -- The number of closed contours

        Note:
            This method uses the Moore's Contour Detection Algorithm
            More details are available here:
                http://www.imageprocessingplace.com/
                downloads_V3/root_downloads/tutorials/
                contour_tracing_Abeer_George_Ghuneim/ray.html
        """
        # Try 1: Looped Implementation
        count = 0
        B = [(0, 0)]
        self.already_checked = []
        for i in range(self.image_dims[0]):
            for j in range(self.image_dims[1]):
                if self.tess[i, j] == pixel_intensity and (i, j) not in self.already_checked:
                    B = self.check_closed_contour((i, j), B[0], pixel_intensity)
                    count = count+1
                    break
        print(pixel_intensity + " " + count)
        return count

    def check_closed_contour(self, bpixel_coordinates, e, pixel_intensity):
        """
        Check if there's a closed contour around this pixel

        Arguments:
            -- pixel_coordinates(tuple): (x,y) starting pixel of the contour
            -- pixel_intensity(int): intensity of the pixel

        Returns:
            -- B : Boundary array
        """
        print("Method Call")
        s = bpixel_coordinates
        B = []
        B.append(s)
        p = s
        Mp = ContourTracer.moores_boundary(bpixel_coordinates, self.image_dims)
        c = Mp[0]
        i = 1
        while c != s:
            if self.tess[c[0], c[1]] == pixel_intensity:
                B.append(c)
                p = c
                c = e
            else:
                c = Mp[i]
                i = i + 1
        return B

    def intensity(self, start):
        """Returns the intensity of the start pixel"""
        return self.tess[start[0], start[1]]

    def find_boundary(self, intense):
        """Find Contour around the pixel""" 
        B = []
        for i in range(self.image_dims[0]):
            for j in range(self.image_dims[1]):
                neigh = ContourTracer.moores_boundary((i, j), self.image_dims)
                for k in neigh:
                    if self.tess[i, j] != self.tess[k[0], k[1]] and self.tess[i, j] == intense and (j, i) not in B:
                        B.append((j, i))
        return B

    def count_lines(self, arr):
        """
        Count the number of lines through boundaries Array

        Arguments:
            -- arr: A list of array boundaries

        Returns:
            -- count: The number of lines through the array
        """
        arr.sort()
        count = 0
        while len(arr) != 0:
            count += 1
            i = 0
            for l in arr:
                if(l[0] == 0 
                        or l[1] == 0 
                        or l[0] == self.image_dims[0]-1
                        or l[1] == self.image_dims[0]-1
                        or l[0] == self.image_dims[1]-1
                        or l[1] == self.image_dims[1]-1):
                    st = l
                    break
                else:
                    st = l
            arr.remove(st)
            while i < len(arr):
                if math.sqrt(((arr[i][0]-st[0])**2)+((arr[i][1]-st[1])**2)) == 1:
                    st = arr.pop(i)
                    i = 0
                else:
                    i += 1
        return count

    @staticmethod
    def moores_boundary(pixel_coordinates, image_dims):
        """
        Takes the pixel coordinates and returns the moore's boundary
        of the pixel

        Arguments:
            -- pixel_coordinates: tuple (x, y) representing x and y coordinates 
            -- image_dims: tuple (width, height) representing image size

        Returns:
            -- moores_boundary: A List of tuples 
                    [(x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y),
                     (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]
        """

        assert(isinstance(pixel_coordinates, tuple))
        x, y = pixel_coordinates
        p_1 = (x, y+1)
        p_2 = (x-1, y+1)
        p_3 = (x-1, y)
        p_4 = (x-1, y-1)
        p_5 = (x, y-1)
        p_6 = (x+1, y-1)
        p_7 = (x+1, y)
        p_8 = (x+1, y+1)
        boundary_list = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8]
        moores_boundary = [x for x in boundary_list if
                            ((x[0] >= 0 and x[0] < image_dims[0])
                                and (x[1] >= 0 and x[1] < image_dims[1]))]
        return moores_boundary

    def count_intensities(self):
        """
        Return the number of pixel values through the array

        Returns:
            int_arr : A list of intensities in the image
        """
        int_arr = []
        for i in range(self.image_dims[0]):
            for j in range(self.image_dims[1]):
                if self.tess[i, j] not in int_arr:
                    self.logger.info("Found Pixel With intensity {}".format(
                        self.tess[i, j]))
                    int_arr.append(self.tess[i, j])
        return int_arr


def parse_arguments():
    """
    Parse the program arguments in the following form:
        count-areas <input-filename> --shape <height>,<width>
    """
    parser = argparse.ArgumentParser("Count the number of contours in a binary image")
    parser.add_argument("file_path", type=str, help='Input Image Path')
    parser.add_argument("--shape", "-s", type=list, help="Shape of the original image width, height", default=[256, 256])
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    ct = ContourTracer(args.file_path, args.shape[0], args.shape[1])
    pixel_frequency = [0]*256
    intensities = ct.count_intensities()
    for i in intensities:
        B = ct.find_boundary(i)
        count = ct.count_lines(B)
        # print(i, count)
        pixel_frequency[i] = count
    print("__________________________")
    print("|Intesity >>>>> Frequency|")
    for intensity, frequency in enumerate(pixel_frequency):
        print("|________________________|")
        print("|   " + str(intensity) + "\t >>>>>\t" + "  " + str(frequency) + "      |")
    print("|________________________|")   

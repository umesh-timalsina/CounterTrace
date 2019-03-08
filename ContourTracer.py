import numpy as np
from PIL import Image
import logging


class ContourTracer(object):
    """
    A Class That Implements the moore's
    Counter Tracing Algorithm
    """
    def __init__(self, image_path):
        """
        Initialize an image with image paths
        """
        self.logger = logging.getLogger("ContourTracer")
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        im = Image.open(image_path).convert('L')
        self.tess = np.asarray(im)
        self.image_dims = self.tess.shape
        self.logger.info("Loaded Image from {0} as {1}*{2} numpy array"
                            .format(image_path, self.tess.shape[0], self.tess.shape[1]))
        pass

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
        self.already_checked = []
        for i in range(self.image_dims[0]):
            for j in range(self.image_dims[1]):
                if self.tess[i, j] == pixel_intensity and (i, j) not in self.already_checked:
                    self.already_checked.append((i, j))
                    if self.check_closed_contour((i, j), pixel_intensity):
                        count += 1
        return count
    

    def check_closed_contour(self, pixel_coordinates, pixel_intensity):
        """
        Check if there's a closed contour around this pixel

        Arguments:
            -- pixel_coordinates(tuple): (x,y) starting pixel of the contour
            -- pixel_intensity(int): intensity of the pixel
        
        Returns:  
        """
        B = []
        B.append(pixel_coordinates)
        next_pixel = (-1, -1)
        next_pixel_boundaries = ContourTracer.moores_boundary(pixel_coordinates, self.image_dims)
        while (pixel_coordinates[0] != next_pixel[0]) and (pixel_coordinates[1] != next_pixel[1]):
            for pixel in next_pixel_boundaries:
                if self.tess[pixel[0], pixel[1]] == pixel_intensity:
                    self.already_checked.append(pixel)
                    B.append(pixel)
                    next_pixel = pixel
                    break
            if(pixel_coordinates[0] == next_pixel[0] and pixel_coordinates[1] == next_pixel[1]):
                print(next_pixel)
            next_pixel_boundaries =  ContourTracer.moores_boundary(next_pixel, self.image_dims)
        return True


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
        p_1 = (x-1, y-1)
        p_2 = (x, y-1)
        p_3 = (x+1, y-1)
        p_4 = (x+1, y)
        p_5 = (x+1 , y+1)
        p_6 = (x, y+1)
        p_7 = (x-1, y+1)
        p_8 = (x-1, y)
        boundary_list = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8]
        moores_boundary = [ x for x in boundary_list if ((x[0] >= 0 and x[0] < image_dims[0])
                            and (x[1] >= 0 and x[1] < image_dims[1]))]
        return moores_boundary


if __name__ == "__main__":
    ct = ContourTracer("./images/shades-of-grey.png")
    print(ContourTracer.moores_boundary((3, 3), (640, 640)))
    print(ct.count_contours(200))

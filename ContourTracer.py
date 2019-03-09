import numpy as np
from PIL import Image
import logging
from matplotlib import pyplot as plt
import argparse



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
        # im = Image.open(image_path).convert('L')
        self.tess = np.fromfile(image_path, dtype='uint8', sep="")
        new_size = int(np.sqrt(self.tess.size))
        self.tess = self.tess.reshape((new_size, new_size))
        self.tess = self.tess.clip(min=0)
        self.image_dims = self.tess.shape 
        self.logger.info("Loaded Image from {0} as {1}*{2} numpy array"
                            .format(image_path, self.tess.shape[0], self.tess.shape[1]))
       
        plt.imshow(self.tess)
        plt.show()
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
                if self.tess[i][j] == pixel_intensity and (i, j) not in self.already_checked:
                    self._check_closed_contour((i, j), pixel_intensity)
                    break
        return count
    

    def _check_closed_contour(self, pixel_coordinates, pixel_intensity):
        """
        Check if there's a closed contour around this pixel

        Arguments:
            -- pixel_coordinates(tuple): (x,y) starting pixel of the contour
            -- pixel_intensity(int): intensity of the pixel
        
        Returns:  
        """
        print("Method Call")
        B = []
        B.append(pixel_coordinates)
        self.already_checked.append(pixel_coordinates)
        current_pixel = pixel_coordinates
        next_pixel_itr = iter(ContourTracer.moores_boundary(current_pixel, self.image_dims))
        next_pixel = next(next_pixel_itr)
        while next_pixel != pixel_coordinates:
            if self.tess[next_pixel[0], next_pixel[1]] == pixel_intensity and next_pixel not in B[1:]:
                B.append(next_pixel)
                print(pixel_coordinates, next_pixel, pixel_intensity)
                current_pixel = next_pixel
                next_pixel_itr = iter(ContourTracer.moores_boundary(next_pixel, self.image_dims))
                next_pixel = next(next_pixel_itr)
            else:
                try:
                    next_pixel = next(next_pixel_itr)
                except:
                    next_pixel = current_pixel
                    next_pixel_itr = iter(ContourTracer.moores_boundary(next_pixel, self.image_dims))
        else:
            return True
        return False

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
        p_5 = (x , y-1)
        p_6 = (x+1, y-1)
        p_7 = (x+1, y)
        p_8 = (x+1, y+1)
        boundary_list = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8]
        moores_boundary = [ x for x in boundary_list if ((x[0] >= 0 and x[0] < image_dims[0])
                            and (x[1] >= 0 and x[1] < image_dims[1]))]
        return moores_boundary


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
    ct = ContourTracer(args.file_path)
    print(ContourTracer.moores_boundary((3, 3), (640, 640)))
    print(ct.count_contours(0))

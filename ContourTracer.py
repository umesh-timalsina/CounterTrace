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
        im = Image.open(image_path)
        self.tess = np.asarray(im)
        self.image_dims = self.tess.shape
        self.logger.info("Loaded Image from {0} as {1}*{2} numpy array"
                            .format(image_path, self.tess.shape[0], self.tess.shape[1]))
        pass


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
        (x, y) = pixel_coordinates
        p1 = (x-1, y-1) 
        p2 = (x, y-1)
        p3 = (x+1, y-1)
        p4 = (x+1, y)
        p5 = (x+1 , y+1)
        p6 = (x, y+1)
        p7 = (x-1, y+1)
        p8 = (x-1, y)
        boundary_list = [p1, p2, p3, p4, p5, p6, p7, p8]
        moores_boundary = [ x for x in boundary_list if ((x[0] >= 0 and x[0] < image_dims[0])
                            and (x[1] >= 0 and x[1] < image_dims[1]))]
        return moores_boundary


if __name__ == "__main__":
    ct = ContourTracer("./images/shades-of-grey.png")
    print(ContourTracer.moores_boundary((3, 3), (640, 640)))
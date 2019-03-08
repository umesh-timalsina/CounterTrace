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
        self.logger.info("Loaded Image from {0} as {1}*{2} numpy array"
                            .format(image_path, self.tess.shape[0], self.tess.shape[1]))
        pass

    @staticmethod
    def moores_boundary(pixel_coordinates, image_dims):
        """
        Takes the pixel coordinates and returns the moore's boundary
        """

if __name__ == "__main__":
    ct = ContourTracer("./images/shades-of-grey.png")
        
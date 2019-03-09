import math
import numpy as np
from PIL import Image
import logging
from matplotlib import pyplot as plt



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
#        plt.show()
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
        B = [(0,0)]
        self.already_checked = []
        for i in range(self.image_dims[0]):
            for j in range(self.image_dims[1]):
                if self.tess[i, j] == pixel_intensity and (i, j) not in self.already_checked:
                    B = self.check_closed_contour((i, j),B[0], pixel_intensity)
                    count = count+1
                    break
        print(pixel_intensity + " "+ count)
        return count
    

    def check_closed_contour(self, bpixel_coordinates, e, pixel_intensity):
        """
        Check if there's a closed contour around this pixel

        Arguments:
            -- pixel_coordinates(tuple): (x,y) starting pixel of the contour
            -- pixel_intensity(int): intensity of the pixel
        
        Returns:  
        """
        print("Method Call")
        s = bpixel_coordinates
        B = []
        B.append(s)
        p = s
        #next_pixel = (-1, -1)
        Mp = ContourTracer.moores_boundary(bpixel_coordinates, self.image_dims)
        #p = start_pixel
        c = Mp[0]
        i = 1
        while c != s:
           # print(pixel_coordinates, next_pixel)
            # print(next_pixel_boundaries)
            if self.tess[c[0],c[1]] == pixel_intensity:
                B.append(c)
                p=c
                c=e
            else:
                c = Mp[i]
                i=i+1
        return B

    @staticmethod
    def intensity(start):
        return self.tess[start[0],start[1]]

    def find_boundary(self,start):
        B = []
        intense=self.tess[start[0],start[1]]
        for i in range(1,self.image_dims[0]):
                for j in range(1,self.image_dims[1]):
                    #neigh = ContourTracer.moores_boundary((i,j),self.image_dims)
                        if self.tess[i-1,j-1] != self.tess[i,j]:
                            if self.tess[i-1,j-1] == intense:
                                B.append((j-1,i-1))
                            if self.tess[i,j] == intense:
                                B.append((j,i))
        return B

    def count_lines(self,arr):
        arr.sort()
        count = 0
        while len(arr) != 0:
            count +=1
            i = 0
            st = arr.pop(0)
            while i < len(arr):
                if math.sqrt(((arr[i][0]-st[0])**2)+((arr[i][1]-st[1])**2)) == 1:
                    st = arr.pop(0)
                    print(st)
                    i = 0
                else:
                    i +=1
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
        p_5 = (x , y-1)
        p_6 = (x+1, y-1)
        p_7 = (x+1, y)
        p_8 = (x+1, y+1)
        boundary_list = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8]
        moores_boundary = [ x for x in boundary_list if ((x[0] >= 0 and x[0] < image_dims[0])
                            and (x[1] >= 0 and x[1] < image_dims[1]))]
        return moores_boundary


if __name__ == "__main__":
    ct = ContourTracer("./images/sample.bin")
    #print(ContourTracer.moores_boundary((3, 3), (640, 640)))
    #print(ct.count_contours(0))
    B = ct.find_boundary((0,0))
    print(len(B))
    plt.scatter(*zip(*B))
    plt.show()
    print(ct.count_lines(B))

import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image
import urllib
from io import BytesIO
from random import choice
import cv2


def read_array_from_image_url(url):
    '''
    Returns array of an image given the url of the image

    Parameters: 
        url(str) - url of the image to be processed

    Returns: 
        R(numpy array) - array of pixels (R,G,B)
    '''
           
    #pass headers to stop site blocking (without these can give HTTP Error: Forbidden
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    img = Image.open(BytesIO(resp.read()))
    R = np.array(img)
    
    return R
    

def select_dark_pixels(image_array, threshold = None, ratio = None):
    '''
    Extract the black pixels from an array. Either take the % darkest pixels, or those darker than a threshold

    Parameters: 
        image_array (numpy array) - pixels from image
        threshold (float) - threshold below which to count as a black pixel. If None - will try and use ratio
        ratio (float) - ratio of darkest points to take. If None - will try and use threshold

    Returns: 
        coords (numpy array: shape (n,2) - coordinates of 'black' pixels
    '''

    #convert to grayscale
    grsc = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    if ratio:
        number_darkest = int(len(image_array.ravel())*ratio)
        dark_i = np.unravel_index(grsc.ravel().argsort()[::-1][-number_darkest:], grsc.shape)

    elif threshold:
        #take pixels which are darker than the threshold
        dark_i = np.where(grsc<threshold)
        
    else:
        return None

    coords = np.column_stack((dark_i[1], -dark_i[0]))
    return coords

def get_edge_coords(image_array, lower = 100, upper = 200):
    '''
    Use edge detection to find image edges, and return coords

    Parameters: 
        image_array (numpy array) - pixels from image
        lower (int) - lower hysteresis threshold. Optional - default 100
        upper (int) - upper hysteresis threshold. Optional - defaul 200

    Returns: 
        coords (numpy array: shape (n,2) - edge coordinates
    '''
    
    edges = cv2.Canny(image_array,lower,upper)
    dark_i = np.where(edges>0) #should only be 255 or 0

    coords = np.column_stack((dark_i[1], -dark_i[0]))

    return coords


def return_reduced_points(coords, plot_original = False, number_of_points = None, exact_number = True):
    '''
    Thin out the number of items in a list to the desired number. This thins by taking every nth point
    where it's possible to divide to get the required number, and then by removing points at random
    if the exact number is required

    Parameters: 
       coords (list) - original list
       plot_original (bool) default False - plot the original coordinates
       number_of_points (int) default None - required number of points. None will set no limit
       exact_number (bool) default True - exact number required? If false will just try and reduce by multiples

    Returns: 
        coord_strip (numpy array: shape (n,2)) - thinned list of coords
    '''    
    
    if plot_original:    
        plt.axes().set_aspect('equal', 'datalim')
        plt.plot([i[0] for i in coords], [i[1] for i in coords],'o',markersize=0.2)
        plt.show()
    
    if number_of_points == None or number_of_points>len(coords):
        step_size = 1
        exact_number = False
    else:
        step_size = int(len(coords)/number_of_points)
    
    coord_strip = coords[::step_size]
    if exact_number:
        while len(coord_strip) > number_of_points:
            coord_strip = np.delete(coord_strip, choice(range(len(coord_strip))), axis = 0)
    print('Original number of points: {0:,}\nNew number of points: {1:,}'.format(len(coords), len(coord_strip)))
    
    return coord_strip


def get_coords_from_url_image(url, number_points = None, colour_threshold = None, ratio = None, lower_edge = 100, upper_edge = 200):
    '''
    Take an image url and give a thinned number of coordinates of black pixels

    Parameters: 
        url(str) - url of the image to be processed
        number_of_points (int) default None - required number of points. None will set no limit
        colour_threshold (float) - threshold below which to count as a black pixel

    Returns: 
        points_reduced (list) - thinned list of coords
    '''    
    R = read_array_from_image_url(url)
    points = get_edge_coords(R, lower = lower_edge, upper = upper_edge)
    #points = select_dark_pixels(R, threshold = colour_threshold, ratio = ratio)
    points_reduced = return_reduced_points(points, number_of_points = number_points)
    
    return points_reduced

if __name__ == '__main__':
    
    url = r'https://vignette.wikia.nocookie.net/sonic/images/2/2d/TSR_Sonic.png/revision/latest/top-crop/width/360/height/360?cb=20191020043348'
    
    points = get_coords_from_url_image(url, number_points = 5000)
    
    plt.axes().set_aspect('equal', 'datalim')
    plt.plot([i[0] for i in points], [i[1] for i in points],'o',markersize=0.2,color = 'k')
    plt.show()


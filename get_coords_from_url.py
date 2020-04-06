import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image
import urllib
from io import BytesIO
from random import choice




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
    

def select_pixels(image_array, threshold = 0):
    '''
    Extract the black pixels from an array

    Parameters: 
        image_array (numpy array) - pixels from image
        threshold (float) - threshold below which to count as a black pixel

    Returns: 
        coords (list) - list of coordinates of 'black' pixels
    '''

    coords = []
    for row in range(len(image_array)):
        for pix in range(len(image_array[row])):  
            if (image_array[row][pix][:2] == threshold).all():
                coords.append((pix,-row))
    coords.sort(key = lambda x:x[1])
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
        coord_strip (list) - thinned list of coords
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
            coord_strip.remove(choice(coord_strip))
    print('Original number of points: {0:,}\nNew number of points: {1:,}'.format(len(coords), len(coord_strip)))
    
    return coord_strip


def get_coords_from_url_image(url, number_points = None, colour_threshold = 0):
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
    points = select_pixels(R, threshold = colour_threshold)
    points_reduced = return_reduced_points(points, number_of_points = number_points)
    
    return points_reduced

if __name__ == '__main__':
    
    url = r'https://i.pinimg.com/originals/6a/ea/63/6aea63e74b246450eab8a90d38d2bb5b.jpg'
    
    #points = get_coords_from_url_image(url, number_points = 5000)

    R = read_array_from_image_url(url)
    plt.axes().set_aspect('equal', 'datalim')
    plt.plot([i[0] for i in points], [i[1] for i in points],'o',markersize=0.2,color = 'k')
    plt.show()
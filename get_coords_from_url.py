import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image
import urllib
from io import BytesIO
from random import choice




def read_array_from_image_url(url):
            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    img = Image.open(BytesIO(resp.read()))
    R = np.array(img)
    
    return R
    

def select_pixels(image_array, threshold = 0):
    
    coords = []
    for row in range(len(image_array)):
        for pix in range(len(image_array[row])):  
            if (image_array[row][pix][:2] == threshold).all():
                coords.append((pix,-row))
    coords.sort(key = lambda x:x[1])
    return coords

def return_reduced_points(coords, plot_original = False, number_of_points = None, exact_number = True):
                
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
    R = read_array_from_image_url(url)
    points = select_pixels(R, threshold = colour_threshold)
    points_reduced = return_reduced_points(points, number_of_points = number_points)
    
    return points_reduced

if __name__ == '__main__':
    
    url = r'https://i.pinimg.com/originals/6a/ea/63/6aea63e74b246450eab8a90d38d2bb5b.jpg'
    
    points = get_coords_from_url_image(url, number_points = 5000)


    plt.axes().set_aspect('equal', 'datalim')
    plt.plot([i[0] for i in points], [i[1] for i in points],'o',markersize=0.2,color = 'k')
    plt.show()
import numpy as np
import cv2

import argparse
from argparse import ArgumentParser
import os
from PIL import Image as im

enc_path = "map_big.jpg"  # os.path.join(ile)

# try block to handle the exception
try:
    # take path of image as a input
    path = enc_path

    # taking decryption key as input
    key = 45

    # print path of image file and decryption key that we are using
    print('The path of file : ', path)
    print('Note : Encryption key and Decryption key must be same.')
    print('Key for Decryption : ', key)

    # open file for reading purpose
    fin = open(path, 'rb')

    # storing image data in variable "image"
    image = fin.read()
    fin.close()

    # converting image into byte array to perform decryption easily on numeric data
    image = bytearray(image)

    # performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ key

    # opening file for writing purpose
    fin = open("eec.jpg", 'wb')

    # writing decryption data in image
    fin.write(image)
    fin.close()
    print('Decryption Done...')


except Exception:
    print('Error caught : ', Exception.__name__)

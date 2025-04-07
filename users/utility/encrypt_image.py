import os
import random
from django.conf import settings


def encrypt_input_image(file, xorKey):
    path = os.path.join(settings.MEDIA_ROOT, 'plain_image', file)
    enc_path = os.path.join(settings.MEDIA_ROOT, 'encrypted_image', file)
    # try block to handle exception
    try:
        key = random.randint(1, 256)
        print('The path of file : ', path)
        print('Key for encryption : ', key)
        print("XorShiftKey is:", xorKey)
        # open file for reading purpose
        fin = open(path, 'rb')
        image = fin.read()
        fin.close()
        image = bytearray(image)
        for index, values in enumerate(image):
            image[index] = values ^ key
        fin = open(enc_path, 'wb')
        fin.write(image)
        fin.close()
        print('Encryption Done...')
        return key
    except Exception as ex:
        print('Error caught : ', ex)

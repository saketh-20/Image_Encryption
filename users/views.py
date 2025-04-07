# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel, EncryptionModels,ImageSharingModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
import random
import os
from django.db.models import Q

# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def generateXorShiftAnd():
    x = random.randint(100000000, 999999999)
    y = random.randint(100000000, 999999999)
    z = random.randint(100000000, 999999999)
    w = random.randint(10000000, 99999999)
    t = x ^ ((x << 11) & 0xFFFFFFFF)
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w


def XorShiftAndKey(request):
    randomKey = generateXorShiftAnd()
    return render(request, 'users/xorshiftkey.html', {'key': randomKey})


def EncryptionImage(request):
    if request.method == 'POST':
        image_file = request.FILES['file']
        # let's check if it is a csv file
        # if not image_file.name.endswith('.png'):
        #     messages.error(request, 'THIS IS NOT A PNG  FILE')
        fs = FileSystemStorage(location="media/plain_image/")
        filename = fs.save(image_file.name, image_file)
        # detect_filename = fs.save(image_file.name, image_file)
        uploaded_file_url = "/media/plain_image/" + filename  # fs.url(filename)
        encypted_image = "/media/encrypted_image/" + filename

        from .utility.encrypt_image import encrypt_input_image
        key = generateXorShiftAnd()
        nkey = encrypt_input_image(filename, key)
        loginid = request.session['loginid']
        EncryptionModels.objects.create(loginid=loginid, imageName=filename, xorShiftKey=key, byteKey=nkey)
        print(f"Original Image {uploaded_file_url} Encrypted Image {encypted_image} XorKey: {key}")
        return render(request, "users/UploadForm.html", {'path': uploaded_file_url, 'encPath': encypted_image})
    else:
        return render(request, "users/UploadForm.html", {})
    return HttpResponse('working')


def DecryptionImage(request):
    loginid = request.session['loginid']
    data = EncryptionModels.objects.filter(loginid=loginid)
    usrs = UserRegistrationModel.objects.filter(~Q(loginid=loginid), status='activated')
    # from itertools import chain
    # result_list = list(chain(data, usrs))
    return render(request, "users/dec_images.html", {'data': data,'usrs': usrs})


def DecryptProcess(request):
    id = request.GET.get('uid')
    data = EncryptionModels.objects.get(id=id)
    # encypted_image = "/media/encrypted_image/" + data.imageName
    encypted_image = os.path.join(settings.MEDIA_ROOT, 'encrypted_image', data.imageName)
    down_path = os.path.join(settings.MEDIA_ROOT, 'encrypted_image', data.imageName)
    xorShiftKey = data.xorShiftKey
    byteKey = data.byteKey
    # open file for reading purpose
    fin = open(encypted_image, 'rb')

    # storing image data in variable "image"
    image = fin.read()
    fin.close()

    # converting image into byte array to perform decryption easily on numeric data
    image = bytearray(image)

    # performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ byteKey
    fin = open(down_path, 'wb')

    # writing decryption data in image
    fin.write(image)
    fin.close()

    with open(down_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


def ShareToUsers(request):
    if request.method == 'POST':
        imgId = request.POST.get('imgId')
        sharefrom = request.POST.get('sharefrom')
        imageName = request.POST.get('imageName')
        xorShiftKey = request.POST.get('xorShiftKey')
        byteKey = request.POST.get('byteKey')
        recipientUser = request.POST.get('recipientUser')
        ImageSharingModel.objects.create(imgId=imgId,sharefrom=sharefrom,imageName=imageName,xorShiftKey=xorShiftKey,byteKey=byteKey,recipientUser=recipientUser,)
        print(f"imgId: {imgId} Share From {sharefrom} Image Name: {imageName} xorShiftKey {xorShiftKey} recepent User: {recipientUser}")
        return render(request, 'users/UserHomePage.html', {})
    if request.method=='GET':
        loginid = request.session['loginid']
        id = request.GET.get('uid')
        data = EncryptionModels.objects.get(id=id)
        usrs = UserRegistrationModel.objects.filter(~Q(loginid=loginid), status='activated')
        return render(request, "users/share_images.html", {'data': data, 'usrs': usrs})

def ViewSharedImages(request):
    loginid = request.session['loginid']
    data = ImageSharingModel.objects.filter(recipientUser=loginid)
    usrs = UserRegistrationModel.objects.filter(~Q(loginid=loginid), status='activated')
    # from itertools import chain
    # result_list = list(chain(data, usrs))
    return render(request, "users/view_shared_images.html", {'data': data, 'usrs': usrs})

def DecryptProcess_1(request):
    id = request.GET.get('uid')
    data = EncryptionModels.objects.get(id=id)
    # encypted_image = "/media/encrypted_image/" + data.imageName
    encypted_image = os.path.join(settings.MEDIA_ROOT, 'encrypted_image', data.imageName)
    down_path = os.path.join(settings.MEDIA_ROOT, 'encrypted_image', data.imageName)
    xorShiftKey = data.xorShiftKey
    byteKey = data.byteKey
    # open file for reading purpose
    fin = open(encypted_image, 'rb')

    # storing image data in variable "image"
    image = fin.read()
    fin.close()

    # converting image into byte array to perform decryption easily on numeric data
    image = bytearray(image)

    # performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ byteKey
    fin = open(down_path, 'wb')

    # writing decryption data in image
    fin.write(image)
    fin.close()

    with open(down_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")
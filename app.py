import os
from flask import Flask
import requests
import cv2
import w3storage
from PIL import Image

path = (os.getcwd())
path = os.path.join(path, 'static')
#print(path)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/copy')
def img():
    os.chdir(path)
    mean_height = 0
    mean_width = 0

    images = [img for img in os.listdir('.')
    if img.endswith(".jpg") or
        img.endswith(".jpeg") or
        img.endswith("png")]

    num_of_images = len(images)
    print(num_of_images)

    for file in os.listdir('.'):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
            im = Image.open(os.path.join(path, file))
            width, height = im.size
            mean_width += width
            mean_height += height
            # im.show() # uncomment this for displaying the image

    # Finding the mean height and width of all images.
    # This is required because the video frame needs
    # to be set with same width and height. Otherwise
    # images not equal to that width height will not get
    # embedded into the video
    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)

    # print(mean_height)
    # print(mean_width)

    # Resizing of the images to give
    # them same width and height
    for file in os.listdir('.'):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
            # opening image using PIL Image
            im = Image.open(os.path.join(path, file))

            # im.size includes the height and width of image
            width, height = im.size
            #print(width, height)

            # resizing
            imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)
            imResize.save( file, 'JPEG', quality = 95) # setting quality
            # printing each resized image name
            #print(im.filename.split('\\')[-1], " is resized")

    # Copying the image multiple time to
    # set video timestamp = 20 sec
    # Limitation max image = 10
    Required_num_of_images = 20
    if(Required_num_of_images > num_of_images):
        copy_num =int((Required_num_of_images - num_of_images)/ num_of_images)
        rem_num = Required_num_of_images % num_of_images 
        if(copy_num):
            for file in os.listdir('.'):
                if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
                    # opening image using PIL Image
                    im = Image.open(os.path.join(path, file))

                    for x in range(copy_num):
                        temp = file.split('.')
                        temp[0]= temp[0]+'_'+ str(x)
                        filename = temp[0]+'.'+temp[1]
                        im.save(filename, 'JPEG', quality= 95)
                        #print(filename)
                        if (x == copy_num -1):
                            if(rem_num):
                                temp = file.split('.')
                                temp[0]= temp[0]+'_'+ str(copy_num)
                                filename = temp[0]+'.'+temp[1]
                                im.save(filename, 'JPEG', quality= 95)
                                #print(filename)
                                rem_num = rem_num -1  
    return "Multiple images generated"

def down(img_url, filename):
    #image_url = "https://bafybeiefgd4fur5pjpbrcdlbncjvbyjvd7okph2mpz66bdkaj25zuz4xru.ipfs.w3s.link/3d_1515.jpg"
    filename = filename + '.jpg'
    save_path = os.path.join(path, filename)
  
    # URL of the image to be downloaded is defined as img_url
    r = requests.get(img_url) # create HTTP response object
    
    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open(save_path,'wb') as f:
    
        # Saving received content as a jpg file in
        # binary format
    
        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)


# Video Generating function
@app.route('/vdo')
def generate_video():
    image_folder = '.' # make sure to use your folder
    video_name = 'video.avi'
    os.chdir(path)
    
    images = [img for img in os.listdir(image_folder)
            if img.endswith(".jpg") or
                img.endswith(".jpeg") or
                img.endswith("png")]
    
    # Array images should only consider
    # the image files ignoring others if any
    print(images)

    frame = cv2.imread(os.path.join(image_folder, images[0]))

    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    # Appending the images to the video one by one
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    
    # Deallocating memories taken for window creation
    #cv2.destroyAllWindows()
    video.release() # releasing the video generated
    return "video generated"


def up(filename):
    w3 = w3storage.API(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGNDMGJCMWI4Yzc5MkVDMjYzODE5NjNGOWYwNGJlRWFBZmExMTY3NmYiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NjQ0MzA5ODQzNzMsIm5hbWUiOiJweWFwaSJ9.QHfc2DXkoXwai9qGXFXxsh2QZXm64QP4ie1Uyrk4tlg')

    some_uploads = w3.user_uploads(size=25)

    # limited to 100 MB
    
    media_cid = w3.post_upload((filename, open(os.path.join(path,filename), 'rb')))
    print(media_cid)
    return media_cid

    # larger files can be uploaded by splitting them into .cars.



@app.route('/img')
def aim():
    image_url = "https://bafybeiefgd4fur5pjpbrcdlbncjvbyjvd7okph2mpz66bdkaj25zuz4xru.ipfs.w3s.link/3d_1515.jpg"

    down(image_url, "photo")
    return "Image Downloaded"

@app.route('/up')
def upl():
    cid= up("video.avi")

    return "video uploaded successfully \n cid = " + str(cid)

@app.route('/image')
def photos():
    os.chdir(path)
    images = [img for img in os.listdir('.')
    if img.endswith(".jpg") or
        img.endswith(".jpeg") or
        img.endswith("png") or
        img.endswith(".avi")]
        
        # Array images should only consider
        # the image files ignoring others if any
    #print(images)
    #im = Image.open(os.path.join(path, images[0]))
    return "image list - " + str(images) 


if __name__=="__main__":
    app.run(debug=True)
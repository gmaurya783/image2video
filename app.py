import os
from flask import Flask
import requests
import cv2

path = (os.getcwd())
path = os.path.join(path, 'static')
print(path)

app = Flask(__name__)

@app.route('/')
def hello():
    print("Hello Gaurav")
    return "Hello World"

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


@app.route('/img')
def aim():
    image_url = "https://bafybeiefgd4fur5pjpbrcdlbncjvbyjvd7okph2mpz66bdkaj25zuz4xru.ipfs.w3s.link/3d_1515.jpg"

    down(image_url, "photo")
    return "Image Downloaded"

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
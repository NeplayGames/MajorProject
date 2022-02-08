import io

from flask import Flask, request, render_template, Response
import base64
from io import BytesIO
import pickle
from torchvision import transforms
import torch
from PIL import Image
import enchant
from CheckForSquareImage import Main

app = Flask(__name__)

# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

img_src = None

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # route and function to handle the home page
# @app.route('/', methods=['GET', 'POST'])
# def home_page():
#     return render_template('index.html')

# route and function to handle the upload page
@app.route('/read', methods=['GET', 'POST'])
def read_image():
    if request.method == 'POST':
        data = request.get_json(force=True)
        im = Image.open(BytesIO(base64.b64decode(data['img'])))
        print("decode image", im)
        im.save('accept.jpg', 'PNG')
        extracted_text = Main()
        arr = extracted_text.split()
        d = enchant.Dict("en_US")

        for a in arr:
            if not d.check(a):
                arr.remove(a)

        # data

        extracted_text = listToString(arr)
        response = Response(
            extracted_text)
        print(extracted_text)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    else:
        return "Post has not yet been called <h1>GET</h1>"


@app.route("/see", methods=['GET', 'POST'])
def scan_env():
    if request.method == "POST":
        datas = request.get_json(force=True)
        im = Image.open(BytesIO(base64.b64decode(datas['img'])))
        print("decode image", im)
        im.save('accept.jpg', 'PNG')

        device = torch.device("cpu")
        transform_test = transforms.Compose([
            transforms.Resize(256),  # smaller edge of image resized to 256
            transforms.RandomCrop(224),  # get 224x224 crop from random location
            transforms.RandomHorizontalFlip(),  # horizontally flip image with probability=0.5
            transforms.ToTensor(),  # convert the PIL Image to a tensor
            transforms.Normalize((0.485, 0.456, 0.406),  # normalize image for pre-trained model
                                 (0.229, 0.224, 0.225))])

        encoder = torch.load('encoder1.pt')
        encoder.eval()
        decoder = torch.load('decoder1.pt')
        decoder.eval()

        encoder.to(device)
        decoder.to(device)

        PIL_image = Image.open('accept.jpg').convert('RGB')
        final_image = transform_test(PIL_image)
        final_image = final_image.unsqueeze(0)
        print(final_image.shape)
        final_image = final_image.to(device)

        caption = get_prediction(image=final_image, encoder=encoder, decoder=decoder)
        print(caption)
        # p = Translator()
        # caption = p.translate(caption, dest='nepali')
        # print(caption.pronunciation)

        resp = Response(
            caption)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return "Post has not yet been called <h1>GET</h1>"


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return str1.join(s)


def clean_sentence(output):
    with open('vocab.pkl', 'rb') as f:
        vocab = pickle.load(f)
        idx2word = vocab.idx2word
    sentence = ''
    for each_caption_index in output:
        each_caption_word = idx2word[each_caption_index]
        if each_caption_word == '<start>':
            continue
        if each_caption_word == '<end>':
            break

        sentence += ' ' + each_caption_word
    return sentence


def get_prediction(image, encoder, decoder):
    features = encoder(image).unsqueeze(1)
    output = decoder.sample(features)
    sentence = clean_sentence(output)
    return sentence


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

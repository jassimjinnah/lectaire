from flask import Flask, render_template, send_file, request, redirect, send_from_directory
import cv2
import requests
from bs4 import BeautifulSoup
import os
from IPython.display import display, Image
import openai
import pyttsx3
from mtranslate import translate
import threading
import time
import io
import base64
import jsonify
from gtts import gTTS 
import os 
import speech_recognition as sr
app = Flask(__name__)
VIDEO_FOLDER = 'images'
##################################################################
# Initialize the text-to-speech engine outside the functions
engine = pyttsx3.init()
def jas(text):
  mytext = text
  language = 'en'
  myobj = gTTS(text=mytext, lang=language, slow=False) 
  myobj.save("welcome.mp3") 
  os.system("mpg321 welcome.mp3") 

def translate_and_speak(engine, text, target_language='ta'):
    sentences = text.split(".")
    audio_subtitles = []

    # Initialize start time
    start_time = 0

    for sentence in sentences:
        if not sentence.strip():
            continue
        
        translated_sentence = translate(sentence.strip(), target_language)

        # Add subtitle with start time
        audio_subtitles.append({'english': sentence.strip(), 'translated': translated_sentence, 'start_time': start_time})
        
        # Increment start time
        start_time += len(sentence.split()) * 0.5  # Adjust this value based on your preference

        time.sleep(0.01)  # Add a short delay between sentences
    
    return audio_subtitles


# Function to scrape images from Bing based on a search query
def scrape_images(query, num_images=5):
    search_url = f"https://www.bing.com/images/search?q={query}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = []
        for img in soup.find_all('img', {'class': 'mimg'}):
            image_url = img.get('src')
            if image_url:
                image_urls.append(image_url)
            if len(image_urls) >= num_images:
                break
        return image_urls
    else:
        print("Failed to fetch search results")

# Function to download and save an image
def download_image(image_url, download_path, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        # Ensure the file extension is .jpg
        filename = os.path.splitext(filename)[0] + ".jpg"
        with open(os.path.join(download_path, filename), 'wb') as f:
            f.write(response.content)
        return filename
    else:
        print(f"Failed to download image from {image_url}")
@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
    print(transcript)
    return render_template('view.html', transcript=transcript)


@app.route('/generate_video', methods=['POST'])
def generate_video():
   # Define the content to be used for generation
    input_text = request.form['content']
    # client = openai.OpenAI(api_key="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")
    # # Generate content
    # arr=[]
    # y=""
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "give in one word the topic about which paragraph is discussed"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # x=response.choices[0].message.content
    # print(x)
    # print("-------------------------")
    # ###########################################################################################################################################
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": f"give a short introduction about {x}"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)
    # y+=response.choices[0].message.content
    # print("***")
    # input_text=response.choices[0].message.content
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant.You should respond only the phrase."},
    #     {"role": "user", "content": "give one search key phrase from the input for which image should be generated to clarify the content of the paragraph"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)

    # arr.append(response.choices[0].message.content)
    # print("***")
    # print("************")
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": f"explain the working of {x}"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)
    # y+=response.choices[0].message.content
    # print("***")
    # input_text=response.choices[0].message.content
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant.You should respond only the phrase."},
    #     {"role": "user", "content": "give one search key phrase from the input for which image should be generated to clarify the content of the paragraph"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)

    # arr.append(response.choices[0].message.content)
    # print("***")
    # print("************")
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": f"explain the classification of {x}"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)
    # y+=response.choices[0].message.content
    # print("***")
    # input_text=response.choices[0].message.content
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant.You should respond only the phrase."},
    #     {"role": "user", "content": "give one search key phrase from the input for which image should be generated to clarify the content of the paragraph"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)

    # arr.append(response.choices[0].message.content)
    # print("***")
    # print("************")
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": f"explain the applications of {x}"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)
    # y+=response.choices[0].message.content
    # print("***")
    # input_text=response.choices[0].message.content
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant.You should respond only the phrase."},
    #     {"role": "user", "content": "give one search key phrase from the input for which image should be generated to clarify the content of the paragraph"},
    #     {"role": "assistant", "content": input_text },

    #   ]
    # )
    # print(response.choices[0].message.content)

    # arr.append(response.choices[0].message.content)
    # print("***")
    # def download_image(image_url, download_path, filename):
    #   response = requests.get(image_url)
    #   if response.status_code == 200:
    #     # Ensure the file extension is .jpg
    #     filename = os.path.splitext(filename)[0] + ".jpg"
    #     with open(os.path.join(download_path, filename), 'wb') as f:
    #       f.write(response.content)
    #     return filename
    #   else:
    #     print(f"Failed to download image from {image_url}")
    # # Define the directory path where the images are stored
    # download_path = "images/"

    # # Create the directory if it doesn't exist
    # if not os.path.exists(download_path):
    #     os.makedirs(download_path)

    # # Loop through each query text and scrape images
    # for i, query_text in enumerate(arr):
    #     image_urls = scrape_images(query_text, 5)
    #     if image_urls:
    #         # Select the first image URL
    #         image_url = image_urls[0]
    #         # Download the image directly into Google Drive
    #         download_image(image_url, download_path, f"image_{i+1}")
    #     else:
    #         print(f"No images found for query: {query_text}")

    # print("Images downloaded successfully into Google Drive.")
    text = """the mobility of electrons is higher than that of the holes. It is mainly because of their different band structures and scattering mechanisms.

Electrons travel in the conduction band, whereas holes travel in the valence band. When an electric field is applied, holes cannot move as freely as electrons due to their restricted movement. The elevation of electrons from their inner shells to higher shells results in the creation of holes in semiconductors. Since the holes experience stronger atomic force by the nucleus than electrons, holes have lower mobility."""
    audio_subtitles = translate_and_speak(engine,text)
    jas(text)
    return render_template('video.html', num_images=4, audio_subtitles=audio_subtitles)
    # # Get the list of image files
    # image_files = [os.path.join(download_path, f"image_{i}.jpg") for i in range(1, 5)]

    # # Define the output video path
    # output_video_path = "videos/video.mp4"

    # # Define function to generate video from images
    # def generate_video(image_files, output_video_path):
    #     # Get dimensions of the first image
    #     first_image = cv2.imread(image_files[0])
    #     height, width, _ = first_image.shape

    #     # Define the duration of each image in seconds
    #     image_duration_secs = 10

    #     # Define the duration of the video in seconds
    #     total_duration_secs = 120  # 2 minutes

    #     # Calculate the number of frames based on the desired frame rate
    #     frame_rate = 30  # frames per second
    #     num_frames_per_image = image_duration_secs * frame_rate
    #     num_frames_total = total_duration_secs * frame_rate

    #     # Define video writer
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    #     # Generate video frames
    #     for i in range(num_frames_total):
    #         # Calculate the index of the image to display
    #         image_index = (i // num_frames_per_image) % len(image_files)
    #         image_file = image_files[image_index]

    #         # Read image
    #         frame = cv2.imread(image_file)

    #         # Write frame to video
    #         out.write(frame)

    #     # Release video writer
    #     out.release()

    #     print(f"Video generated successfully at {output_video_path}")

    # # Generate video
    # generate_video(image_files, output_video_path)

    # return redirect('/show_video')
@app.route('/show_video')
def show_video():
    return render_template('video.html', num_images=4)
  

@app.route('/videos/video.mp4')
def serve_generated_video():
    video_path = "videos/video.mp4"
    return send_file(video_path, mimetype='video.mp4')

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

import torch
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

# model = T5ForConditionalGeneration.from_pretrained('t5-small')
# tokenizer = T5Tokenizer.from_pretrained('t5-small')
# device = torch.device('cpu')

# def generate_summary(input_text):
#     t5_prepared_text = "summarize:" + input_text
#     tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt").to(device)
#     summary_gen = model.generate(tokenized_text,
#                                  num_beams=4,
#                                  no_repeat_ngram_size=2,
#                                  min_length=20,
#                                  max_length=100,
#                                  early_stopping=True)

#     output = tokenizer.decode(summary_gen[0], skip_special_tokens=True)
#     return output

# import spacy
# def generate_keyword(input_text):
#   nlp = spacy.load("en_core_web_sm")
#   doc = nlp(input_text)
#   return doc.ents[0].text

import os
import time
import urllib
import requests
import magic
import progressbar
from urllib.parse import quote

class simple_image_download:
    def __init__(self):
        pass

    def urls(self, keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        i = 0
        links = []

        things = len(keyword_to_search) * limit

        # bar = progressbar.ProgressBar(maxval=things, \
                                      # widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()

        while i < len(keyword_to_search):
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode(
                    'utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = self._download_page(url)

            end_object = -1;
            google_image_seen = False;
            j = 0

            while j < limit:
                while (True):
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffor = raw_html.find('\\', new_line + 1, end_object)
                        if buffor != -1:
                            object_raw = (raw_html[new_line + 1:buffor])
                        else:
                            object_raw = (raw_html[new_line + 1:end_object])

                        if any(extension in object_raw for extension in extensions):
                            break

                    except Exception as e:
                        break


                try:
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    if('html' not in str(r.content)):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension == '.png' and not google_image_seen:
                            google_image_seen = True
                            raise ValueError();
                        links.append(object_raw)
                        # bar.update(bar.currval + 1)
                    else:
                        j -= 1
                except Exception as e:
                    j -= 1
                j += 1

            i += 1

        # bar.finish()
        return(links)


    def download(self, keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        main_directory = "static/"
        i = 0

        things = len(keyword_to_search) * limit

        # bar = progressbar.ProgressBar(maxval=things, \
                                      # widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        # bar.start()

        while i < len(keyword_to_search):
            self._create_directories(main_directory, keyword_to_search[i])
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode('utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = self._download_page(url)

            end_object = -1;
            google_image_seen = False;
            j = 0
            while j < limit:
                while (True):
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffor = raw_html.find('\\', new_line + 1, end_object)
                        if buffor != -1:
                            object_raw = (raw_html[new_line+1:buffor])
                        else:
                            object_raw = (raw_html[new_line+1:end_object])

                        if any(extension in object_raw for extension in extensions):
                            break

                    except Exception as e:
                        break
                path = main_directory + keyword_to_search[i].replace(" ", "_")

                try:
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    if('html' not in str(r.content)):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension not in extensions:
                            raise ValueError()
                        if file_extension == '.png' and not google_image_seen:
                            google_image_seen = True
                            raise ValueError()
                        file_name = str(keyword_to_search[i]) + "_" + str(j + 1) + file_extension
                        with open(os.path.join(path, file_name), 'wb') as file:
                            file.write(r.content)
                        # bar.update(bar.currval + 1)
                    else:
                        j -= 1
                except Exception as e:
                    j -= 1
                j += 1

            i += 1
        # bar.finish()


    def _create_directories(self, main_directory, name):
        name = name.replace(" ", "_")
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.2)
                path = (name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                path = (name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)

        except OSError as e:
            if e.errno != 17:
                raise
            pass
        return

    def _download_page(self,url):

        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData

        except Exception as e:
            print(e)
            exit(0)

def convert_summary_to_audio(summary, filename):
  from google.cloud import texttospeech
  client = texttospeech.TextToSpeechClient()
  synthesis_input = texttospeech.SynthesisInput(text=summary)
  voice = texttospeech.VoiceSelectionParams(
      language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
  )
  audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.MP3
  )
  response = client.synthesize_speech(
      input=synthesis_input, voice=voice, audio_config=audio_config
  )
  with open("static/"+filename+".mp3", "wb") as out:
      out.write(response.audio_content)



# from flask_ngrok import run_with_ngrok
import json
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# run_with_ngrok(app)   #starts ngrok when the app is run

summaries=[['Democratic candidate Joe Biden Wednesday said he was optimistic of a win in the US presidential elections and thanked his supporters for their patience.  Both Trump and Biden have made expected gains in smaller states','../static/trump.jpeg','../static/trump.mp3'],
           ['However, while the victory ensured the Hyderabad team got a spot in the playoffs, it also knocked Kolkata Knight Riders out of the tournament. However, with a victory needed to qualify, Sunrisers Hyderabad skipper David Warner and Wriddhiman Saha ensured the team chased down a total of 150 at a canter without losing a single wicket','../static/srh.jpeg','../static/srh.mp3'],
           ['PayPal  this week laid out its vision for the future of its digital wallet platform and its PayPal and Venmo  apps.  What’s more, PayPal put timeline on the Honey integrations and the other updates it plans to roll out over the course of the next year','../static/paypal.jpeg','../static/paypal.mp3'],
           ['Scientists have developed a vaccine candidate for COVID-19 that produces "extremely high levels" of protective antibodies in animal models, an advance that may lead to a novel therapeutic to curb the pandemic.  According to the study, the molecular structure of the vaccine roughly mimics that of a virus, which may account for its enhanced ability to provoke an immune response','../static/covid.jpeg','../static/covid.mp3']]
images=['../static/trump.jpeg','../static/srh.jpeg','../static/paypal.jpeg','../static/covid.jpeg']
audios=['../static/trump.mp3','../static/srh.mp3','../static/paypal.mp3','../static/covid.mp3']

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(password)
        print(email)
        return redirect('home')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def index():
    # if request.method == 'POST':
    #     summary = generate_summary(request.form['summary'])
    #     keyword=generate_keyword(request.form['summary'])
    #     print(summary)
    #     print(keyword)
    #     generate_image = simple_image_download
    #     generate_image().download(keyword, 1,extensions={'.png'})
    #     keyword = keyword.replace(" ", "_")
    #     image="../static/"+keyword.replace(" ", "_")+"/"+keyword+"_1.png"
    #     convert_summary_to_audio(summary,keyword.replace(" ", "_"))
    #     filename="../static/"+keyword.replace(" ", "_")+".mp3"
    #     return redirect(url_for('summary', summary=summary, image=image, audio=filename))s
    return render_template('index.html')


@app.route('/summary', methods=['POST', 'GET'])
def summary():
    # if request.method == 'POST':
    #     return redirect('posts')
    # summary=request.args['summary']
    # image=request.args['image']
    # audio=request.args['audio']
    # summaries.insert(0,[summary,image,audio])
    # images.insert(0,image)
    # audios.insert(0,audio)
    return render_template('summary.html', summary=summary, image=image, audio=audio)


@app.route('/posts', methods=['POST', 'GET'])
def posts():
    return render_template('posts.html',summaries=summaries,images=images)

# app.run()

if __name__ == '__main__':
    app.run()

# app.run()

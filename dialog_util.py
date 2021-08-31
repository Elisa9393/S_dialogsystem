import requests

from google.cloud import speech
import io
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
from scipy.io.wavfile import write
sr = 16000  # Sample rate
seconds = 3  # Duration of recording
filename = 'myfile.wav'
import pickle
vaccinations = pickle.load( open( "C:/Users/elisa/Seminare_Python/S_dialogsystem/vaccination_data.pkl", "rb" ) )

phrases = {'hello':'Guten Tag! Sie können mir Fragen zu den Impfungen in Deutschland stellen.', 
    'continue':'Sprechen Sie weiter!', 
    'goodbye':'Danke, dass Sie die Impfauskunft genutzt haben!  Auf Wiedersehen!', 
    'done':'fertig', 
    'done':'tschüss'}




states_d = {'schleswig':'SH', 'hamburg':'HH', 'berlin':'BE', 'bayern':'BY', 
            'niedersachsen': 'NI', 'bremen': 'HB', 
            'nordrhein':'NW', 'hessen':'HE', 'rheinland':'RP', 'baden':'BW', 
            'saarland': 'SL', 'brandenburg':'BB', 'mecklenburg':'MV', 'sachsen':'SN',
            'anhalt':'ST', 'thüringen':'TH', 'deutschland':'DE', 'hier':'DE'}
state_names = {'SH':'Schleswig-Hostein', 'HH':'Hamburg', 'BE':'Berlin', 'BY':'Bayern', 
            'NI':'Niedersachsen', 'HB':'Bremen', 
            'NW': 'Nordrhein Westphalen', 'HE':'Hessen', 'RP':'Rheinland Pfalz', 'BW':'Baden Würthenberg', 
            'SL':'Saarland', 'BB':'Brandenburg', 'MV':'Mecklenburg Vorpommern', 
            'SN': 'Sachsen', 'ST':'Sachsen-Anhalt', 'TH':'Thüringen', 'DE':'Deutschland'}
vaccines_d = {'biontech':'biontech', 'biontec':'biontech', 
              'moderna':'moderna', 'moderner':'moderna',
              'janssen':'janssen', 'jansen':'janssen',
              'delta':'delta',
              'astraZeneca':'astraZeneca', 'astra':'astraZeneca', 'zeneca':'astraZeneca'}
vaccine_names = {'biontech':'Biontech', 'moderna':'Moderna', 'janssen':'Janssen', 'delta':'Delta',
              'astraZeneca':'Astra Zeneca'}

def init_google():
    credentials='C:\\Users\\elisa\\Seminare_Python\\S_dialogsystem\\dialogsystem-1627986561247-c6ec7c426248.json'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials

def transcribe():
    client = speech.SpeechClient()
    with io.open(filename, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content = content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="de-DE",
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        for index, alternative in enumerate(result.alternatives):
            print("Transcript {}: {}".format(index, alternative.transcript))
            return alternative.transcript
    
#formantsysthese
import pyttsx3
def tts(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'german')
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()


def speech_input():
    record_file()
    text = transcribe()
    return text

def do_input():
    return speech_input()



def record_file():
    data = sd.rec(int(seconds * sr), samplerate=sr, channels=1)
    sd.wait()  # Wait until recording is finished
    # Convert `data` to 16 bit integers:
    y = (np.iinfo(np.int16).max * (data/np.abs(data).max())).astype(np.int16) 
    write(filename, sr, y)

def normalize(in_s):
    return in_s.lower()


def semantic(input_s):
    semantics = {'state':'', 'vaccine':''}
    for key in states_d.keys():
        if key in input_s:
            semantics['state'] = states_d[key]
    for key in  vaccines_d.keys():
        if key in input_s:
            semantics['vaccine'] =  vaccines_d[key]
    return semantics

# expects semantics: semantics[0] == bundesland, semantics[1] == impfstoff 
# vaccinations = requests.get('https://api.corona-zahlen.org/vaccinations')
def data(semantics, vaccinations):
    s = semantics['state']
    v = semantics['vaccine']
    if s: # state given
        if s != 'DE':
            if v: # and vaccine given
                vacc_number = vaccinations["data"]["states"][s]['vaccination'][v]
            else: # all vaccines for state
                vacc_number = vaccinations["data"]["states"][s]['vaccinated']
        else:
            if v: # and vaccine given
                vacc_number = vaccinations["data"]['vaccination'][v]
            else: # all vaccines for Germany
                vacc_number = vaccinations['data']['vaccinated']
    else: # no state
        if v: # but vaccine
            vacc_number = vaccinations["data"]['vaccination'][v]
        else: # nothing given
            vacc_number = None
    return vacc_number

def output(semantics, results, inputs, eliza):
    ret = ''
    s = semantics['state']
    v = semantics['vaccine']
    if s: # state given
        s = state_names[semantics['state']]
        if v: # and vaccine given
            v = vaccine_names[semantics['vaccine']]
            ret = 'Die Impfungen für {} mit {} sind {}'.format(s, v, results)
        else: # all vaccines for state
            ret = 'Die Impfungen für {} sind {}'.format(s, results)
    else: # no state
        if v: # but vaccine
            v = vaccine_names[semantics['vaccine']]
            ret = 'Die Impfungen in Deutschland mit {} sind {}'.format(v, results)
        else: # nothing given
            ret = eliza.respond(inputs)
    return ret

from eliza import eliza

#load deutsch.txt (Text)
def init_eliza():
    root = "C:/Users/elisa/Seminare_Python/S_dialogsystem"
    elz = eliza.Eliza() #Instanz von Eliza Klasse
    elz.load(root+"/eliza/deutsch.txt") #use german version of Eliza
    return elz
elz = init_eliza()

def dialogmanager(eliza):
    tts(phrases['hello'])    
    input_s = do_input()
    input_s = normalize(input_s)
    while input_s and input_s != phrases['done']:
        semantics = semantic(input_s)
        result = data(semantics, vaccinations)
        out_string = output(semantics, result, input_s, eliza)
        tts(out_string)
        tts(phrases['continue'])    
        input_s = do_input()
    tts(phrases['goodbye'])   

def main():
    init_google()
    dialogmanager(elz)

if __name__ == "__main__":
    main()


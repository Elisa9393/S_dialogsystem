# S_dialogsystem
Programming a spoken dialog system

You can find [my dialog here](Corona_Dialog_mit_Sprache_Eliza_und_Emotion_Seyfried.ipynb)

The uploaded spoken dialog system can interact vie speech with the user and also recognizes the mood the user is in. When implementing this systen, I learned how a dialog system is constituted and how the different components are connected to each other. Our dialog system consists of the modules dialogmanager, input, output, semantic parsing and data and emotional analyses. About Each of the parts I will explain briefly what I learned about them in this seminar.

The module dialogmanager is the organisational unit which connects all the other components. It gives a meaning to the received spoken input and is planing the next steps. It also has to decide which response should be replied and to the TTS. 

In the input the system records an audio file and transcribes this via Automatic Speech Recognition. The ASR tries to find for each phoneme probabilities and the most probabilistic option gets recognized. In the modern speech recognition neural networks are used for this purpose. Neural networks are statistical models that consist of several perceptron layers.There is an input layer, a hidden layer that we cannot see during training and an output layer.  A part of the input is also the Speech Recognition. There are several methods to do speech recognition.  In my script I used the Google Speech Recognition by the Google Cloud. I recognizes speech from languages.

The module semantic parsing is translating human language into logical expressions that can be read by the computer. Therefore, it derives the meaning of an utterance and translates this for the machine.

In order to be able to give out the information the user asked for, the dialog system needs a data connection. This data connection can be an API, which means application programming interface. These can be accessed via json.file and contain the data. In the project in this course we used the api of the Robert-Koch-Institut. It consists of dictionaries defining the vaccination numbers for the states.

Another neccessary module is the text-to-speech. It is the reverse operation on the speech recognition and translates machine language into natural spoken language. in this course I used pytts from espeak. The voice, the language and the speech rate can be chosen.

Except understanding and executing the code programmed in the course, I also learned how to implement own code. Since the uploaded script only either takes the RKI api about vaccinations as data input or connects to the deutsch.txt to give out the eliza-responses, it is not possible to ask other questions about corona. This is why I worked on a script, that takes the data of the website https://www.deutsche-familienversicherung.de/krankenhauszusatzversicherung/ratgeber/artikel/coronavirus-symptome-verlauf-behandlung/ and generates an answer to questions about the Coronavirus, like symptoms and how contagious it is. You can find the script  [here](Corona_Information.ipynb). The script searches the input and returns sections from the article on the website that are similar to the strings in the input. It would be possible to include this script into the dialog instead of eliza, if the greetings are left out. But the version included here functions as independent script.

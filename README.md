# pdfTTS

A Python application to convert text to speech using AWS Polly.

Supports converting text from PDF files or strings to speech, with various customization
options for voice, audio format, and sample rate.

Throughout the application effort is made to ensure exiting on critical errors
so the user is aware of issues preventing the application from functioning.

Application retrieves random text to convert to speech in order to provide an
engaging experience with varied output on each run when neither PDF nor plain
text inputs are not provided.

Relevant Libraries and Services:

- [Python](https://www.python.org/)

- [AWS Polly](https://aws.amazon.com/polly/)

- [AWS SDK for Python (Boto3)](https://github.com/boto/boto3)

- [pypdf](https://pypdf.readthedocs.io/en/stable/)

- [Harvard Sentences](https://en.wikipedia.org/wiki/Harvard_sentences)

Completed for Professional Portfolio Project: Assignment 10, Angela Yu 100 Days of
Code -- "HTTP Requests & APIs: Convert PDF to Audiobook"

_MIT License: Copyright (c) 2024 Andrew Blais_

---

Future updates will include:

- More efficient and detailed use of AWS Polly's features and options.

- More robust error-handling.

- Create Python unit tests.

- More...

---

### Documentation:

_Printed via `help(pdfTTS)` in `main.py`:_

```
Help on class PollyTTS in module __main__:

class PollyTTS(builtins.object)
 |  PollyTTS(access_key: str, secret_access_key: str, pdf_input_path: str = '', str_input: str = '', use_temp_dir: bool = False, user_filename: str = '')
 |
 |  A class to convert text to speech using AWS Polly.
 |
 |  This class supports converting text from PDF files or strings to speech, with
 |   various customization options for voice, audio format, and sample rate.
 |
 |  Throughout the application effort is made to ensure exiting on critical errors
 |   so the user is aware of issues preventing the application from functioning.
 |
 |  Application retrieves random text to convert to speech in order to provide an
 |   engaging experience with varied output on each run when neither PDF nor plain
 |   text inputs are not provided.
 |
 |  :param access_key: AWS access key ID.
 |  :type access_key: str
 |  :param secret_access_key: AWS secret access key.
 |  :type secret_access_key: str
 |  :param pdf_input_path: Path to the input PDF file. Optional.
 |  :type pdf_input_path: str
 |  :param str_input: Direct string input for conversion. Optional.
 |  :type str_input: str
 |  :param use_temp_dir: Flag to use a temporary directory for output files. Optional.
 |  :type use_temp_dir: bool
 |  :param user_filename: Prefix for the output filename. Optional.
 |  :type user_filename: str
 |
 |  Methods defined here:
 |
 |  __init__(self, access_key: str, secret_access_key: str, pdf_input_path: str = '', str_input: str = '', use_temp_dir: bool = False, user_filename: str = '')
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  choose_eng_accent(self, eng_language_code)
 |      Allows the user to choose a specific English accent for speech synthesis.
 |
 |      Valid accents codes:
 |       "en-AU": "Australian", "en-IN": "Indian", "en-IE": "Irish",
 |       "en-NZ": "New Zealander Kiwi", "en-ZA": "South African", "en-GB": "English",
 |       "en-US": "American", "en-GB-WLS": "Welsh"
 |
 |      :param eng_language_code: The language code representing the desired accent.
 |      :type eng_language_code: str
 |
 |  choose_output_format(self, output_format)
 |      Allows the user to specify the audio format for the output file.
 |
 |      Available formats:
 |       "json", "mp3", "ogg_vorbis" and "pcm"
 |
 |      :param output_format: The desired audio format (e.g., "mp3").
 |      :type output_format: str
 |
 |  choose_sample_rate(self, sample_rate)
 |      Allows the user to specify the sample rate for the audio output.
 |
 |      Available sample rates:
 |       "8000", "16000", "22050" and "24000"
 |
 |      :param sample_rate: The desired sample rate (e.g., "16000").
 |      :type sample_rate: str
 |
 |  choose_voice_id(self, voice_id)
 |      Allows the user to choose a specific voice ID from available AWS Polly voices.
 |
 |      User can choose from valid AWS Free Tier voices:
 |       "Aditi", "Amy", "Astrid", "Bianca", "Brian", "Camila", "Carla", "Carmen",
 |       "Celine", "Chantal", "Conchita", "Cristiano", "Dora", "Emma", "Enrique",
 |       "Ewa", "Filiz", "Gabrielle", "Geraint", "Giorgio", "Gwyneth", "Hans",
 |       "Ines", "Ivy", "Jacek", "Jan", "Joanna", "Joey", "Justin", "Karl",
 |       "Kendra", "Kevin", "Kimberly", "Lea", "Liv", "Lotte", "Lucia", "Lupe",
 |       "Mads", "Maja", "Marlene", "Mathieu", "Matthew", "Maxim", "Mia", "Miguel",
 |       "Mizuki", "Naja", "Nicole", "Olivia", "Penelope", "Raveena", "Ricardo",
 |       "Ruben", "Russell", "Salli", "Seoyeon", "Takumi", "Tatyana", "Vicki",
 |       "Vitoria", "Zeina" and "Zhiyu"
 |
 |      :param voice_id: The desired voice ID.
 |      :type voice_id: str
 |
 |  complete_tts(self)
 |      Final method to be called by the user to synthesize speech and create the output file.
 |      This method should be called after initializing the PollyTTS object and optionally
 |       setting customization methods.
 |
 |  random_eng_accent(self)
 |      Selects a random English accent for speech synthesis. This method is optional and can
 |       be called explicitly to override the default or chosen language code.
 |
 |  random_voice_id(self)
 |      Selects a random voice ID for speech synthesis. This method is optional and can
 |       be called explicitly to override the default or chosen voice ID.
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
```

---

## Created in completing an assignment for Angela Yu's Course:

### **Day 91, Professional Portfolio Project [HTTP Requests & APIs]**

#### **_Assignment 10, "Convert PDF to Audiobook"_**

Write a Python script that takes a PDF file and converts it into speech.

- _assignment
  for [Angela Yu 100 Days of Code](https://www.udemy.com/course/100-days-of-code/)_

### **Assignment instructions:**

Too tired to read? Build a python script that takes a PDF file, identifies the text and
converts the text to speech. Effectively creating a free audiobook.

AI text-to-speech has come so far. They can sound more lifelike than a real audiobook.

Using what you've learnt about HTTP requests, APIs and Python scripting, create a program
that can convert PDF files to speech.

You right want to choose your own Text-To-Speech (TTS) API. But here are some you can
consider:

- http://www.ispeech.org/api/#introduction

- https://cloud.google.com/text-to-speech/docs/basics

- https://aws.amazon.com/polly/

---

### My Submission:

Try it out: https://github.com/andrewblais/pdfTTS.

---

### **Questions for this assignment**

#### _Reflection Time:_

_This is a place to journal your experience of completing this project. This will help
you figure out how to improve as a developer._

**_Write down how you approached the project._**

It took a little time, but I settled on using AWS Polly to to the speechifying. I also
decided to write the application as a class with a separate file for data/options.

**_What was hard?_**

The hardest part was conquering my fear of using AWS, both because I've found it a
bit intimidating, but also I was trepidatious about trying to make sure I could use
the free tier without triggering any charges. I decided to use the web interface
rather than the CLI, and will leave that challenge for a later date.

**_What was easy?_**

I'm confident at this point in creating a class from scratch and populating it with
necessary attributes and useful methods. This is even fun for me at this point.

**_How might you improve for the next project?_**

Once again, my priority has to be on core-functionality over making cool features.
I tend to get ahead of myself in this respect, and need to concentrate on planning the
simplest possible roadmap when creating a new project -- then adding interesting/
creative features later.

**_What was your biggest learning from today?_**

Learning about AWS and Polly. I was pleasantly surprised, after getting my feet wet,
that it's not quite as difficult to use as I thought it would be.

**_What would you do differently if you were to tackle this project again?_**

Make sure to not waste time writing unnecessary methods: getting things clear in my
head or on paper to see the direction the application should take, then following that
plan -- but remaining flexible at the same time.
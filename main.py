# Import necessary libraries and modules:
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing  # For safely closing resources
from dotenv import load_dotenv  # To load environment variables from a .env file
import os
from pypdf import PdfReader  # For reading PDF files
import random
import secrets  # For generating secure random strings
import sys  # For accessing system-specific parameters and functions
from tempfile import gettempdir  # For accessing the temporary directory

# Import local data:
from static.options import *

load_dotenv()  # Load environment variables from a .env file


class PollyTTS:
    """
    A class to convert text to speech using AWS Polly.

    This class supports converting text from PDF files or strings to speech, with
     various customization options for voice, audio format, and sample rate.

    Throughout the application effort is made to ensure exiting on critical errors
     so the user is aware of issues preventing the application from functioning.

    Application retrieves random text to convert to speech in order to provide an
     engaging experience with varied output on each run when neither PDF nor plain
     text inputs are not provided.

    :param access_key: AWS access key ID.
    :type access_key: str
    :param secret_access_key: AWS secret access key.
    :type secret_access_key: str
    :param pdf_input_path: Path to the input PDF file. Optional.
    :type pdf_input_path: str
    :param str_input: Direct string input for conversion. Optional.
    :type str_input: str
    :param use_temp_dir: Flag to use a temporary directory for output files. Optional.
    :type use_temp_dir: bool
    :param user_file_prefix: Prefix for the output filename. Optional.
    :type user_file_prefix: str
    """

    def __init__(self, access_key: str, secret_access_key: str,
                 pdf_input_path: str = "", str_input: str = "",
                 use_temp_dir: bool = False, user_file_prefix: str = ""):
        # Initialize instance variables:
        self.pdf_input_path = pdf_input_path
        self.str_input = str_input
        # Placeholder for the final text to be converted to speech:
        self.aws_client_str = ""

        # Output filename management:
        self.user_file_prefix = user_file_prefix
        self.output_filename = ""

        # Default AWS Polly settings:
        self.voice_id = "Joanna"
        self.output_format = "mp3"
        self.sample_rate = "16000"
        self.language_code = "en-US"

        # Temporary directory usage flag:
        self.use_temp_dir = use_temp_dir

        # AWS client and response placeholders:
        self.client = None
        self.response = None
        # AWS credentials:
        self._access_key = access_key
        self._secret_access_key = secret_access_key

        # Initial methods to get things rolling:
        self._initialize_client()  # Initialize AWS Polly client
        self._determine_output_filename()  # Determine or generate output filename
        self._process_input_text()  # Process input text for speech synthesis

    def _initialize_client(self):
        """
        Initializes the AWS Polly client with provided credentials.
        """
        try:
            # Initialize AWS Polly client with US East (N. Virginia) region;
            #  adjust as necessary for your needs:
            self.client = boto3.client(
                "polly",
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_access_key,
                region_name="us-east-1"
            )
            print("AWS-Polly client successfully initiated.")
        except (BotoCoreError, ClientError) as e:
            # Exit on failure to initialize the client:
            sys.exit(f"Failed to initialize AWS Polly client: {e}")

    def _process_input_text(self):
        """
        Processes the input text from either a PDF file or a string. If neither is available,
         generates random text.
        """
        # Fallback to string input if PDF is not found or invalid, and to random text
        #  if neither input is provided:
        if self.pdf_input_path:
            # Create a PDF reader object
            try:
                reader = PdfReader(self.pdf_input_path)
                text_from_pdf = ""
                for page in reader.pages:
                    text_from_pdf += page.extract_text() + "\n"
                self.aws_client_str = text_from_pdf
                print("PDF input file processed successfully.")
            except FileNotFoundError as fnfe:
                print(f"Path not valid. Going to string input. Error: {fnfe}")
                # Initialize empty string to hold extracted text:
                if self.str_input:
                    self.aws_client_str = self.str_input
                    print("String input processed successfully.")
                else:
                    print("No valid input string input.")
                    print("Using random text to tide you over...")
                    self._random_text_input()
        # Use string input in no PDF file input:
        elif self.str_input:
            print("Using string input.")
            self.aws_client_str = self.str_input
        # Opt for random text if no user text input:
        else:
            self._random_text_input()

    def _determine_output_filename(self):
        """
        Determines the output filename based on the user_file_prefix parameter or generates
         a random filename if none is provided.
        """
        if not self.user_file_prefix:
            random_filename = secrets.token_urlsafe(6)
            print(f"Generated random file name: {random_filename}")
            self.user_file_prefix = f"pdf_tts_{random_filename}"
        # Append the audio format extension to the output filename to ensure proper
        #  file handling:
        self.output_filename = f"{self.user_file_prefix}.{self.output_format}"

    def _get_synthesized_speech(self):
        """
        Calls AWS Polly to synthesize speech from the processed text input.
        """
        try:
            self.response = self.client.synthesize_speech(
                VoiceId=self.voice_id,
                OutputFormat=self.output_format,
                Text=self.aws_client_str,
                LanguageCode=self.language_code,
                SampleRate=self.sample_rate
            )
            print("Speech successfully synthesized.")
        except (BotoCoreError, ClientError) as e:
            print(f"`_get_synthesized_speech` error: {e}")
            sys.exit(-1)

    def _write_audio_file(self):
        """
        Writes the synthesized speech to an audio file in the specified format.
        """
        if "AudioStream" in self.response:
            with closing(self.response["AudioStream"]) as audio_stream:
                # Determine output path based on temp directory flag:
                if self.use_temp_dir:
                    # Use the system's temporary directory for output if specified,
                    #  allowing for cleaner file management:
                    output_path = os.path.join(gettempdir(), self.output_filename)
                else:
                    output_path = self.output_filename
                try:
                    # Write the audio stream to file:
                    with open(output_path, "wb") as audio_file:
                        audio_file.write(audio_stream.read())
                    print(f"Audio file successfully written to {output_path} ")
                except IOError as e:
                    # Handle file writing errors:
                    print(f"`_write_audio_file` error: {e}")
                    sys.exit(-1)
        else:
            print("`_write_audio_file` error: 'AudioStream' not in response.")
            sys.exit(-1)

    def _random_text_input(self):
        """
        Generates random sample text for speech synthesis if no input text is provided.
        This method is optional and can be called explicitly to set random text.
        """
        """
        Optional. User can assert this method to generate random sample text.
        Also runs if no pdf or string input upon initialization.
        """
        random_sample_text = random.choice(sample_sentences)
        print(f"Random text generated: {random_sample_text}")
        self.aws_client_str = random_sample_text

    def random_voice_id(self):
        """
        Selects a random voice ID for speech synthesis. This method is optional and can
         be called explicitly to override the default or chosen voice ID.
        """
        random_voice = random.choice(voice_ids)
        print("Retrieved random voice.")
        self.voice_id = random_voice
        print(f"Using voice {self.voice_id}")

    def random_eng_accent(self):
        """
        Selects a random English accent for speech synthesis. This method is optional and can
         be called explicitly to override the default or chosen language code.
        """
        random_language_code = random.choice(list(eng_language_code_dict.keys()))
        accent_name = eng_language_code_dict[random_language_code]
        print(f"Using random accent: {accent_name}.")
        self.language_code = random_language_code

    def choose_voice_id(self, voice_id):
        """
        Allows the user to choose a specific voice ID from available AWS Polly voices.

        User can choose from valid AWS Free Tier voices:
         "Aditi", "Amy", "Astrid", "Bianca", "Brian", "Camila", "Carla", "Carmen",
         "Celine", "Chantal", "Conchita", "Cristiano", "Dora", "Emma", "Enrique",
         "Ewa", "Filiz", "Gabrielle", "Geraint", "Giorgio", "Gwyneth", "Hans",
         "Ines", "Ivy", "Jacek", "Jan", "Joanna", "Joey", "Justin", "Karl",
         "Kendra", "Kevin", "Kimberly", "Lea", "Liv", "Lotte", "Lucia", "Lupe",
         "Mads", "Maja", "Marlene", "Mathieu", "Matthew", "Maxim", "Mia", "Miguel",
         "Mizuki", "Naja", "Nicole", "Olivia", "Penelope", "Raveena", "Ricardo",
         "Ruben", "Russell", "Salli", "Seoyeon", "Takumi", "Tatyana", "Vicki",
         "Vitoria", "Zeina" and "Zhiyu"

        :param voice_id: The desired voice ID.
        :type voice_id: str
        """
        try:
            if voice_id in voice_ids:
                self.voice_id = voice_id
            else:
                print(f"`select_voice_id` error: {voice_id} not available.")
                print("Using default voice 'Joanna' instead.")
        except TypeError as te:
            raise TypeError(f"Missing `voice_id`: {te}. Defaulting to 'Joanna'.")
        except (Exception,) as e:
            print(f"`choose_voice_id` error: {e}.")
        finally:
            print(f"Setting `voice_id` to: {self.voice_id}.")

    def choose_output_format(self, output_format):
        """
        Allows the user to specify the audio format for the output file.

        Available formats:
         "json", "mp3", "ogg_vorbis" and "pcm"

        :param output_format: The desired audio format (e.g., "mp3").
        :type output_format: str
        """
        try:
            if self.output_format not in output_formats:
                print(f"You entered an invalid output format: {self.output_format}.")
                print("Going with 'mp3' instead.")
                self.output_format = "mp3"
            else:
                self.output_format = output_format
        except TypeError as te:
            raise TypeError(f"Invalid `output_format`: {te}. Defaulting to 'mp3'.")
        except (Exception,) as e:
            print(f"`choose_output_format` error: {e}.")
        else:
            self.output_format = "16000"
        finally:
            print(f"Setting `output_format` to: {self.output_format}.")

    def choose_sample_rate(self, sample_rate):
        """
        Allows the user to specify the sample rate for the audio output.

        Available sample rates:
         "8000", "16000", "22050" and "24000"

        :param sample_rate: The desired sample rate (e.g., "16000").
        :type sample_rate: str
        """
        try:
            if self.sample_rate not in sample_rates:
                print(f"You entered an invalid output sample rate: {self.sample_rate}.")
                print("Going with '16000' instead.")
                self.sample_rate = "16000"
            else:
                self.sample_rate = sample_rate
        except TypeError as te:
            raise TypeError(f"Invalid `sample_rate`: {te}. Defaulting to '16000'.")
        except (Exception,) as e:
            print(f"`choose_sample_rate` error: {e}.")
        else:
            self.sample_rate = "16000"
        finally:
            print(f"Setting `sample_rate` to: {self.sample_rate}.")

    def choose_eng_accent(self, eng_language_code):
        """
        Allows the user to choose a specific English accent for speech synthesis.

        Valid accents codes:
         "en-AU": "Australian", "en-IN": "Indian", "en-IE": "Irish",
         "en-NZ": "New Zealander Kiwi", "en-ZA": "South African", "en-GB": "English",
         "en-US": "American", "en-GB-WLS": "Welsh"

        :param eng_language_code: The language code representing the desired accent.
        :type eng_language_code: str
        """
        try:
            if eng_language_code in eng_language_code_dict:
                self.language_code = eng_language_code
            else:
                print(f"`choose_eng_accent` error: {eng_language_code} not available.")
                print("Using default accent instead.")
        except (TypeError, Exception) as error:
            self.language_code = "en-US"
            raise TypeError(
                f"`choose_eng_accent` error: {error}. Defaulting to 'en-US'.")
        finally:
            print(f"Speech will be in {eng_language_code_dict[self.language_code]}.")

    def complete_tts(self):
        """
        Final method to be called by the user to synthesize speech and create the output file.
        This method should be called after initializing the PollyTTS object and optionally
         setting customization methods.
        """
        self._get_synthesized_speech()
        self._write_audio_file()


if __name__ == "__main__":
    # Example instantiation and execution of the PollyTTS class to demonstrate uage:
    pdf_path = "pdf_samples/hope_emily_dickinson.pdf"
    pdf_tts = PollyTTS(
        access_key=os.environ.get("AWS_ACCESS_KEY"),
        secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        pdf_input_path=pdf_path,
        user_file_prefix="dickinson_hope"
    )
    pdf_tts.random_voice_id()
    pdf_tts.complete_tts()

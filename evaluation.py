import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Load API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

def prompt_answer(line, model=None):
    """

    :param line: JSON record
    :param model: gemini X model
    :return: Picture answering the prompt question
    """

    prompt = "Your task is to generate an image which describes the following: " + line
    print("The prompt is: \n" + prompt)
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('gemini-native-image.png')
            image.show()




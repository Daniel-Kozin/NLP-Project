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

def prompt_answer(prompt, idx=1, max_index=150, model="gemini-2.0-flash-preview-image-generation"):
    """


    :param prompt: gemini prompt
    :param idx:  index of JSON record
    :param max_index: total amount of records in the data set.
    :param model: gemini X model
    :return: Picture answering the prompt question
    """
    print("\033[91mImage Generation\033[0m")
    print("The prompt is: \n" + prompt)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    # --- SAFETY CHECK ---
    if not response or not getattr(response, "candidates", None):
        print(f"⚠ No candidates returned for record {idx}/{max_index}")
        return

    if not response.candidates[0].content or not getattr(response.candidates[0].content, "parts", None):
        print(f"⚠ Empty content for record {idx}/{max_index}")
        return
    # --------------------

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f'gemini_img/{idx}_out_of_{max_index}.png')
            #image.show()

def model_answer(prompt, img_path, model="gemini-2.5-flash"):

    print("\033[91mImage Evaluation\033[0m")
    print("The prompt is: \n" + prompt)

    with open(img_path, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            prompt
        ]
    )

    print(response.text)
    return response.text



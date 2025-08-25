# NLP Project: Testing Google's Gemini Model
This project demonstrates how Google's Gemini model struggles to generate accurate images
from prompts containing unseen or unusual data. The focus is on testing the model with
unusual human features, atypical objects, or other challenging scenarios.

## Main Idea
The goal of this project is to explore the limitations of AI image generation. Specifically:
- Identify prompts where Gemini fails to produce accurate images.
- Analyze performance on unusual or unseen inputs.
- Provide insights into model weaknesses for research or debugging purposes.

Example:
> Your task is to generate a person with 5 legs.

of course the prompt itself is much more detailed. 
## Dataset
The dataset contains entries describing challenging prompts. Each entry has the following fields:

| Field       | Description                                          |
|------------|------------------------------------------------------|
| description | Text describing the object to generate.              |
| data_type   | Type of the prompt, e.g., "person" or "clock".       |
| difficulty  | Estimated difficulty of the prompt for the AI model. |

> The dataset can be expanded with any prompts you want to test, allowing flexible experimentation.

## How to Run
Follow these steps to test prompts with Gemini:

### 1. Set up your API key
Create a `.env` file in the project root with the following content:

```
GEMINI_API_KEY=your_key
```

You need a valid Google Gemini API key. You can get one from:
[Gemini API Key & Usage](https://aistudio.google.com/apikey)

### 2. Run the evaluation script
Run the main script with:

```
python run_eval.py
```

The results (and accuracy) will appear directly in your terminal, and the generated images will be saved in the `gemini_img` folder.

## References
- Image understanding guide: [Gemini Image API](https://ai.google.dev/gemini-api/docs/image-understanding)  
- Official API documentation: [Gemini API](https://ai.google.dev/gemini-api/docs/api-key)  
- API usage and billing: [Gemini Usage & Billing](https://aistudio.google.com/usage?project=gen-lang-client-0672115561)


# NLP Project
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

| Field       | Description                                         |
|------------|-----------------------------------------------------|
| description | Text describing the object to generate.             |
| data_type   | Type of the prompt, e.g., "person"       |
| difficulty  | Estimated difficulty of the prompt for the AI model. |

> The dataset can be expanded with any prompts you want to test, allowing flexible experimentation.

## How to Run
Follow these steps to test prompts with Gemini:
### 1. create a folder named `gemini_img`
### 2. Set up your API key
Create a `.env` file in the project root with the following content:

```
GEMINI_API_KEY=your_key
```

You need a valid Google Gemini API key. You can get one from:
[Gemini API Key & Usage](https://aistudio.google.com/apikey)

### 3. Run the evaluation script
Run the main script with:

```
python run_eval.py
```

The results (and accuracy) will appear directly in your terminal, and the generated images will be saved in the
`gemini_img` folder.

## Data Generation

We have implemented a flexible way to generate an **infinite amount of data** using the script [`generate_data.py`](./generate_data.py).  
There are two main approaches you can use:

1. **Expanding the count arrays**  
   Each item has its own count array (e.g., `eye_count`). By simply increasing the range of these arrays, you can generate as many variations as needed.

2. **Using `person_data_example`**  
   The function `person_data_example` accepts the number of items to generate as its second argument.  
   By increasing this value (e.g., to `3` or `4`), you can quickly generate a large volume of data.  
   This method can also be combined with the first approach for even greater flexibility.

The code also ensures that **no duplicate lines are generated** — every entry will be unique.

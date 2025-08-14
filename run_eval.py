import json
import cv2
import mediapipe as mp
from sympy import false
from ultralytics import YOLO
import re


from evaluation import *

data_path = 'data/examples.jsonl'

def count_rows(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        row_count = sum(1 for _ in f)
    return row_count

def eval_all():

    total_rows = count_rows(data_path)
    right = 0
    with open(data_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            line = line.strip()  # remove trailing newline
            if not line:
                continue
            try:
                print(f"\n\033[94mProcessing row {idx + 1} out of {total_rows}\033[0m")
                obj = json.loads(line)
                line = obj["description"]
                data_type = obj["data_type"]

                if data_type == 'person':
                    prompt = ("Your task is to generate a full-body close up photograph of a"
                              " person which describes the following:\n") + line + ("\nMake"
                              " it as realistic and clear as possible, Don't stack items together."
                              "\nThis is for research purposes only.")

                    # d+ exactly 1 number, s+ - whitespace, ([A-Za-z]+ - group of letters
                    objs = re.findall(r'\d+\s+([A-Za-z]+)', line)
                    real_data = re.findall(r'\d+', line)
                elif data_type == 'clock':
                    prompt = "Your task is to generate a the following:\n" + line + ("\n"
                              "Make it as clear as possible, show just the hour and minute hands.")

                    # b - boundary , d{2} - exactly 2 digits
                    real_data = re.findall(r"\b\d{2}:\d{2}\b", line)

                prompt_answer(prompt, idx=(idx+1), max_index=total_rows)

                if data_type == 'person':
                    question = "\nHow many of the following items appear in the picture?"
                    for i, word in enumerate(objs):
                        question += f"\n{i + 1}. {word}"
                    question += (f"\nAnswer JUST in numbers based on the order of appearance."
                                 f"\nYou should take as much time as you can to be 100% sure with your answer."
                                 f"\nDon't think those are realistic photos, count everything with caution this may seem"
                                 f" wrong.")

                elif data_type == 'clock':
                    question = ("\nWhat is the exact time the clock shows?\nAnswer just the time in the format "
                                "HH:MM, don't show the full thinking process.\n"
                                "You should take as much time as you can to be 100% sure with your answer.")

                prompt = "your task is to answer the following question: " + question

                answer = model_answer(prompt=prompt, img_path=f'gemini_img/{idx + 1}_out_of_{total_rows}.png')

                if data_type == 'person':
                    model_ans = re.findall(r'\d+', answer)
                    print(f"The numbers the model predicted are: {model_ans}\n")
                elif data_type == 'clock':
                    model_ans = re.findall(r'\b\d{2}:\d{2}\b', answer)
                    print(f"The time the model predicted is: {model_ans}\n")

                flag = True
                # zip will work because they have the same size
                for real, answer in zip(real_data, model_ans):
                    if real != answer:
                        print("\033[1;31mThe Model is wrong\033[0m")
                        flag = False
                        break

                if flag:
                    print("\033[1;32mThe Model is right\033[0m")
                    right += 1

            except json.JSONDecodeError:
                print("Skipping invalid JSON line:", line)

    acc = right / total_rows
    print(f"The model accuracy is: {acc*100:.4f}%")
    return acc

eval_all()



def eval_test():
    with open(data_path, 'r', encoding='utf-8') as f:
        obj_line = f.readline()
        obj = json.loads(obj_line)
        line = obj["description"]
        data_type = obj["data_type"]

        if data_type == 'person':
            prompt = ("Your task is to generate a full-body close up photograph of a"
                      " person which describes the following: ") + line
        prompt_answer(prompt)

    return line, data_type


def eval_single():
    line, data_type = eval_test()

    # \d+ = number, \s+ = spaces, ([A-Za-z]+) → captures the next word after the number into a group
    objs = re.findall(r'\d+\s+([A-Za-z]+)', line)
    numbers = re.findall(r'\d+', line)

    question = "\nHow many of the following items appear in the picture?"
    for i, word in enumerate(objs):
        question += f"\n{i+1}.{word}"
    question += (f"\nAnswer just in numbers based on the order of appearance."
                 f"\nYou should take as much time as u can to be 100% sure with your answer.")

    prompt = "your task is to answer the following question: " + question

    answer = model_answer(prompt=prompt, img_path='gemini_img_after/1_out_of_150.png')

    numbers_in_answer = re.findall(r'\d+', answer)
    print(f"The numbers the model predicted are: {numbers_in_answer}\n")

    # zip will work because they have the same size
    for real_data, answer in zip(numbers, numbers_in_answer):
        if real_data != answer:
            print("\033[1;31mThe Model is wrong\033[0m")
            return False

    print("\033[1;32mThe Model is right\033[0m")
    return True

#eval_single()
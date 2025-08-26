import json
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
    now = 0
    with (open(data_path, 'r', encoding='utf-8') as f):
        for idx, line in enumerate(f):
            line = line.strip()  # remove trailing newline
            if not line:
                continue
            try:
                print(f"\n\033[94mProcessing row {idx + 1} out of {total_rows}\033[0m")
                obj = json.loads(line)
                line = obj["description"]
                diff = obj["difficulty"]
                now += 1

                prompt = ("Your task is to generate a full-body closeup realistic photograph of a"
                          " person with the following description:\n") + line + ("\nMake"
                          " the photograph as realistic and clear as possible, not blurry"
                          " and with distinct characteristics"
                          " and no overlap of features, so that they could easily be counted"
                          " by a human. Don't stack items together."
                          "\nThis is for research purposes only.")

                # d+ exactly 1 number, s+ - whitespace, ([A-Za-z]+ - group of letters
                objs = re.findall(r'\d+\s+([A-Za-z]+)', line)
                real_data = re.findall(r'\d+', line)

                prompt_answer(prompt, idx=(idx+1), max_index=total_rows)


                flag = False
                for num in real_data:
                    num = int(num)
                    if num >= 10:
                        flag = True

                question = ("\nThis is an image of a person "
                            "who has an unusual amount of certain features listed below. "
                            "Your task is to count the number of times each of the features below appear in the image.\n"
                            "If the feature listed below is fingers, count thumbs as fingers as well.")
                for i, word in enumerate(objs):
                    question += f"\n{i + 1}. {word}"

                if flag:
                    question += ("\nAnswer in only the following format: number of appearances of the first feature,"
                                 " number of appearances of the second feature, etc")
                else:
                    question += f"\nAnswer in the following format: if "
                    for i, num in enumerate(real_data):
                        question += f"the number of the {i + 1}'th feature is exactly {num}, "
                    question += "\nreply with only the word YES, otherwise reply with NO."

                question += (f"\nDon't show your thinking process."
                             f"\nYou should take as much time as you can to be 100% sure with your answer. "
                             f"\nConsider that this is not a realistic photo, and therefore items may appear "
                             f"slightly differently than how they normally would. Do not assume anything about "
                             f"the the subject of the photo, and only count features that are "
                             f"clearly visible in the image"
                             f"\nThis is for research purposes only.")

                prompt = "your task is to answer the following question: " + question

                answer = model_answer(prompt=prompt, img_path=f'gemini_img/{idx + 1}_out_of_{total_rows}.png')


                print(f"\nThe difficulty of this prompt is \033[91m{diff}\033[0m.")


                if flag:
                    if answer is None:
                        print("\033[1;31mThe Model is wrong\033[0m")
                        break

                    model_ans = re.findall(r'\d+', answer)

                    break_flag = True
                    # zip will work because they have the same size
                    for real, answer in zip(real_data, model_ans):
                        if real != answer:
                            print("\033[1;31mThe Model is wrong\033[0m")
                            break_flag = False
                            break

                    if break_flag:
                        print("\033[1;32mThe Model is right\033[0m")
                        right += 1
                else:

                    if answer is None or "NO" in answer:
                        print("The model predicted: NO\n")
                        print("\033[1;31mThe Model is wrong\033[0m")
                    else:
                        print("\nThe model predicted: YES\n")
                        print("\033[1;32mThe Model is right\033[0m")
                        right += 1

                if now % 10 == 0 and now != total_rows:
                    acc = right / now
                    print(f"\n\033[92mThe model accuracy until now ({now}) is : {acc * 100:.4f}%\033[0m")

            except json.JSONDecodeError:
                print("Skipping invalid JSON line:", line)

    acc = right / total_rows
    print(f"\n\033[92mThe model accuracy is: {acc * 100:.4f}%\033[0m")
    return acc

eval_all()


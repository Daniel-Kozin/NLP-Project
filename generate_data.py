import random
import json
import os

eye_count = [i for i in range(5,11)]
glasses_count = [i for i in range(5,11)]
fingers_count = [i for i in range(8,16)]
ears_count = [i for i in range(5,16)]
objs = ["eye", "glasses", "fingers", "ears"]


different_times = []

data_path = 'data/examples.jsonl'

def person_data(x, count=None):
    if x == "eye":
        random_item = random.choice(eye_count)
        if count is None:
            count = random_item
        return f"{count} eyes"

    elif x == "glasses":
        random_item = random.choice(glasses_count)
        if count is None:
            count = random_item
        return f"{count} glasses"

    elif x == "fingers":
        random_item = random.choice(fingers_count)
        if count is None:
            count = random_item
        return f"{count} fingers on one hand"

    elif x == "ears":
        random_item = random.choice(ears_count)
        if count is None:
            count = random_item
        return f"{count} ears"

    return ""

def line_exists(file_path, line):
    """Check if a given description already exists in a JSONL file."""

    with open(file_path, "r", encoding="utf-8") as f:
        for existing_line in f:
            try:
                obj = json.loads(existing_line)
                if obj.get("description") == line:
                    return True
            except json.JSONDecodeError:
                pass
    return False

def person_data_example(amount_of_items: int, item=None):
    n = int(amount_of_items)
    if n < 1:
        return None


    with open(data_path, "a", encoding="utf-8") as f:
        # single objects in a prompt
        if n == 1:
            if item is None:
                print("\033[91mYou forgot to specify an item?\033[0m")
                item = random.choice(objs)
            line = "a person with " + person_data(item) + "."
        # 2 objects in a prompt
        elif n == 2:
            result = random.sample(objs, n)
            line = "a person with " + person_data(result[0]) + " and " + person_data(result[1]) + "."

        # more than 2 object in a prompt
        else:
            if n - 1 > len(objs):
                raise "Not enough descriptions"
            result = random.sample(objs, n)
            line = "a person with " + person_data(result[0])
            for i in range(n - 2):
                line += ", " + person_data(result[i + 1])
            line += " and " + person_data(result[n - 1])

            line += "."
        print(line)

        if not line_exists(data_path, line):
            json_obj = {"description": line, "data_type": "person"}
            f.write(json.dumps(json_obj) + "\n")
        if line_exists(data_path, line):
            print("\033[94mThis line already exists\033[0m")



for i in range(15):
    person_data_example(1)
for i in range(2):
    person_data_example(2)

person_data_example(3)
person_data_example(4)


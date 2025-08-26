import random
import json
import os

eye_count = [i for i in range(1,30)]
glasses_count = [i for i in range(1,30)]
fingers_count = [i for i in range(1,30)]
ears_count = [i for i in range(1,30)]
hands_count = [i for i in range(2,30)]
legs_count = [i for i in range(2,30)]
heads_count = [i for i in range(2,30)]
feet_count = [i for i in range(2,30)]

items = ["eyes", "glasses", "fingers", "ears"]
general_items = ["hands", "legs", "heads", "feet"]

data_path = 'data/examples.jsonl'

def sen_create(x, count=None):
    diff = None

    if x == "eyes":
        random_item = random.choice(eye_count)
        if count is None:
            count = random_item

        if count == 2:
            diff = "Easy"
        elif count <= 6:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} eyes", diff

    elif x == "glasses":
        random_item = random.choice(glasses_count)
        if count is None:
            count = random_item

        if count == 1:
            diff = "Easy"
        elif count <= 5:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} glasses", diff

    elif x == "fingers":
        random_item = random.choice(fingers_count)
        if count is None:
            count = random_item

        if count == 5:
            diff = "Easy"
        elif count <= 10:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} fingers (including thumbs) on one hand", diff

    elif x == "ears":
        random_item = random.choice(ears_count)
        if count is None:
            count = random_item

        if count == 2 or count == 1:
            diff = "Easy"
        elif count <= 6:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} ears", diff

    elif x == "hands":
        random_item = random.choice(hands_count)
        if count is None:
            count = random_item

        if count == 2:
            diff = "Easy"
        elif count <= 6:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} hands", diff

    elif x == "legs":
        random_item = random.choice(legs_count)
        if count is None:
            count = random_item

        if count == 2:
            diff = "Easy"
        elif count <= 6:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} legs", diff

    elif x == "heads":
        random_item = random.choice(heads_count)
        if count is None:
            count = random_item

        if count == 1:
            diff = "Easy"
        elif count <= 5:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} heads", diff

    elif x == "feet":
        random_item = random.choice(feet_count)
        if count is None:
            count = random_item

        if count == 2:
            diff = "Easy"
        elif count <= 6:
            diff = "Medium"
        else:
            diff = "Hard"

        return f"{count} feet", diff

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

def person_data_example(objs, amount_of_items: int, item=None, count=None):
    n = int(amount_of_items)
    if n < 1:
        return None


    with open(data_path, "a", encoding="utf-8") as f:
        # single objects in a prompt
        diff = "Hard+"
        if n == 1:
            if item is None:
                print("\033[91mYou forgot to specify count?\033[0m")
                item = random.choice(objs)
            sen, diff = sen_create(item, count)
            line = "A person with " + sen + "."
        # 2 objects in a prompt
        elif n == 2:
            while True:
                result = random.sample(objs, n)
                # Resample if both "heads" and "legs" are picked
                if not ("heads" in result and "legs" in result):
                    break

            line = "A person with " + sen_create(result[0])[0] + " and " + sen_create(result[1])[0] + "."

        # more than 2 object in a prompt
        else:
            if n - 1 > len(objs):
                raise "Not enough descriptions"

            result = random.sample(objs, n)

            line = "A person with " + sen_create(result[0])[0]
            for i in range(n - 2):
                line += ", " + sen_create(result[i + 1])[0]
            line += " and " + sen_create(result[n - 1])[0]

            line += "."
        print(line)

        if not line_exists(data_path, line):
            json_obj = {"description": line, "difficulty": diff}
            f.write(json.dumps(json_obj) + "\n")
        if line_exists(data_path, line):
            print("\033[94mThis line already exists\033[0m")

# How we generated our data
"""
for i in range(1,21):
    for item in items:
        person_data_example(items, 1,item=item, count=i)

for i in range(1,21):
    for item in general_items:
        person_data_example(general_items, 1,item=item, count=i)

for i in range(25):
    person_data_example(items, 2)

for i in range(25):
    person_data_example(general_items, 2)

"""
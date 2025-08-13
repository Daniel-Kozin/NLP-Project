import random
import json
import os

eye_count = [i for i in range(5,11)]
glasses_count = [i for i in range(5,11)]
fingers_count = [i for i in range(8,16)]
ears_count = [i for i in range(5,16)]
hands_count = [i for i in range(4,9)]
legs_count = [i for i in range(4,9)]
heads_count = [i for i in range(3,7)]


items = ["eyes", "glasses", "fingers", "ears"]
general_items = ["hands", "legs", "heads"]

hours = list(range(0, 10)) + list(range(11, 24))
minutes = list(range(0, 60))

data_path = 'data/examples.jsonl'

def sen_create(x, count=None):
    if x == "eyes":
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

    elif x == "hands":
        random_item = random.choice(hands_count)
        if count is None:
            count = random_item
        return f"{count} hands"

    elif x == "legs":
        random_item = random.choice(legs_count)
        if count is None:
            count = random_item
        return f"{count} legs"

    elif x == "heads":
        random_item = random.choice(heads_count)
        if count is None:
            count = random_item
        return f"{count} heads"

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

def person_data_example(objs, amount_of_items: int, item=None):
    n = int(amount_of_items)
    if n < 1:
        return None


    with open(data_path, "a", encoding="utf-8") as f:
        # single objects in a prompt
        if n == 1:
            if item is None:
                print("\033[91mYou forgot to specify an item?\033[0m")
                item = random.choice(objs)
            line = "A person with " + sen_create(item) + "."
        # 2 objects in a prompt
        elif n == 2:
            result = random.sample(objs, n)
            line = "A person with " + sen_create(result[0]) + " and " + sen_create(result[1]) + "."

        # more than 2 object in a prompt
        else:
            if n - 1 > len(objs):
                raise "Not enough descriptions"
            result = random.sample(objs, n)
            line = "A person with " + sen_create(result[0])
            for i in range(n - 2):
                line += ", " + sen_create(result[i + 1])
            line += " and " + sen_create(result[n - 1])

            line += "."
        print(line)

        if not line_exists(data_path, line):
            json_obj = {"description": line, "data_type": "person"}
            f.write(json.dumps(json_obj) + "\n")
        if line_exists(data_path, line):
            print("\033[94mThis line already exists\033[0m")


def time_example(hour, minute):

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None
    if hour < 10:
        hour = f"0{hour}"
    if minute < 10:
        minute = f"0{minute}"

    date_type = "clock"
    time = f"{hour}:{minute}"
    line = "A clock which shows the time " + time + "."

    print(line)

    with open(data_path, "a", encoding="utf-8") as f:

        if not line_exists(data_path, line):
            json_obj = {"description": line, "data_type": date_type}
            f.write(json.dumps(json_obj) + "\n")
        if line_exists(data_path, line):
            print("\033[94mThis line already exists\033[0m")

for i in range(5):
    min = random.choice(minutes)
    hour = random.choice(hours)
    time_example(hour, min)


for i in range(15):
   person_data_example(general_items, 1)
for i in range(2):
   person_data_example(general_items, 2)

person_data_example(general_items, 3)
#person_data_example(items, 4)


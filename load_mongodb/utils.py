# utils.py

import json

def append_jsonl(path, obj):
    with open(path, 'a') as f:
        json.dump(obj, f)
        f.write('\n')

def convert_jsonl_to_json_streaming(jsonl_path, json_path):
    with open(jsonl_path, 'r') as infile, open(json_path, 'w') as outfile:
        outfile.write('[')

        first = True
        for line in infile:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            if not first:
                outfile.write(',')
            else:
                first = False

            obj = json.loads(line)
            json.dump(obj, outfile)

        outfile.write(']')

    # print(f"✅ Successfully converted {jsonl_path} to {json_path} without memory overflow.")
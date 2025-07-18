import json
import argparse

def read_jsonl(file_path):
    """Yield one JSON object per line from a JSONL file."""
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line)


def extract_func(content):
    import re
    res = re.findall(r"\[{.*?}\]", content, re.DOTALL)
    return res[0] if len(res) > 0 else ''


def process_wmdata_to_ftdata_by_task(obj):
    assert len(obj['expert_obs']) == len(obj['expert_acts']) == len(obj['explore_obs']) == len(obj['explore_acts'])
    conversations = []
    for expert_observation, expert_action, explore_observations, explore_actions in zip(obj['expert_obs'], obj['expert_acts'], obj['explore_obs'], obj['explore_acts']):
        wrapping_prompt = '''You are having a conversation with a user to help resolve a retail-relevant request. The previous message you receive is:\n{expert_observation}\n\nNow you have decided to respond with\n{response}.\n\n Please predict the next message that you will receive.'''
        if len(explore_observations) != len(explore_actions):
            continue
        expert_action_func = extract_func(expert_action['content'])
        for explore_observation, explore_action in zip(explore_observations, explore_actions):
            action = explore_action['content']
            action_func = extract_func(action)
            if action_func and expert_action_func:
                try:
                    if json.loads(expert_action_func) == json.loads(action_func):
                        continue
                except Exception as e:
                    # if there is any error on getting the func call structure, we skip it, even though it might be potention duplication
                    print(e)
                    print("1", expert_action_func)
                    print("2", action_func)
                    print("------")

            sft_user = {
                "from": "human",
                "value": wrapping_prompt.format(expert_observation=json.dumps(expert_observation, indent=4), response=action if not extract_func(action) else extract_func(action))
            }
            sft_response = {
                "from": "gpt",
                "value": json.dumps(explore_observation, indent=4)
            }
            conversations.append({"conversations": [sft_user, sft_response]})
    return conversations


def main(input_file='data/wm_datas.jsonl', output_file='data/wm_sft.json'):
    conversations = []
    count = 0
    for obj in read_jsonl(input_file):
        count += len(obj['expert_obs'])
        conversations.extend(process_wmdata_to_ftdata_by_task(obj))

    print(count)  # wm data action/obs pair
    json.dump(conversations, open(output_file, 'w'), indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert WM data to WM-SFT data format')
    parser.add_argument('--input', type=str, default='data/wm_datas.jsonl', help='Input JSONL file path')
    parser.add_argument('--output', type=str, default='data/wm_sft.json', help='Output JSON file path')
    args = parser.parse_args()
    
    main(args.input, args.output)
import argparse
import os
from openai import AzureOpenAI


def main():
    parser = argparse.ArgumentParser(description="Make a request to Azure OpenAI API.")
    parser.add_argument("--model", required=True, help="The model name to use.", default="gpt-4o")
    args = parser.parse_args()

    client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_API_ENDPOINT"],
        api_key=os.environ["AZURE_API_KEY"],
        api_version=os.environ["AZURE_API_VERSION"],
    )

    print(f"querying model {args.model}")

    completion = client.chat.completions.create(
        model=args.model,
        messages=[
            {
                "role": "user",
                "content": "Write a one-sentence bedtime story about a unicorn."
            }
        ]
    )

    print(completion.choices[0].message.content)



if __name__ == "__main__":
    main()
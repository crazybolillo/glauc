import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TextIO

from openai import OpenAI


def main() -> int:
    return run(sys.argv[1:])


def run(args: list[str], out: TextIO = sys.stdout) -> int:
    parser = ArgumentParser(prog="glauc", description="Process text files with the help of AI.")
    parser.add_argument("file", help="Input file to be processed")
    params = parser.parse_args(args)

    target = Path(params.file)
    if not target.is_file():
        print(f"File '{target}' does not exist", file=out)
        return 1

    prompt = input("Prompt:\n> ")

    client = OpenAI()
    with open(target, "r", encoding="utf-8") as fd:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": fd.read()},
            ],
        )

    with open(target.with_name("glauc").with_suffix(target.suffix), "w", encoding="utf-8") as fd:
        fd.write(completion.choices[0].message.content)

    return 0

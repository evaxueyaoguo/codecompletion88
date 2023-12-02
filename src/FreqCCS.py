import os
import ast
from collections import defaultdict
from operator import itemgetter

# Function to get all python files in a directory
def collect_code_examples(directory):
    code_examples = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code_examples.append(f.read())

    return code_examples

def parse_code(code):
    tree = ast.parse(code)
    methods = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return methods

def build_frequency_dict(code_examples):
    frequency_dict = defaultdict(int)

    for code in code_examples:
        methods = parse_code(code)
        for method in methods:
            frequency_dict[method] += 1

    return frequency_dict

def rank_methods_by_frequency(frequency_dict):
    ranked_methods = sorted(frequency_dict.items(), key=itemgetter(1), reverse=True)
    return ranked_methods

def some_function():
    pass

# Function to suggest code completions based on how many times a method shows up in the codebase/ dataset
def suggest_code_completions(directory, code_to_complete):
    code_examples = collect_code_examples(directory)
    frequency_dict = build_frequency_dict(code_examples)
    ranked_methods = rank_methods_by_frequency(frequency_dict)

    # Display code completion suggestions
    suggestions = [method for method, _ in ranked_methods]
    print("Code Completion Suggestions:")
    for suggestion in suggestions:
        if suggestion.startswith(code_to_complete.lower()):
            print(suggestion)


def main():
    directory_path = "./"
    code_to_complete = "so"
    suggest_code_completions(directory_path, code_to_complete)

if __name__ == "__main__":
    main()
    
# TODO: Dataset
# TODO: ArCCS.py
# TODO: BNN
# TODO: integrate with VSCode
# TODO: evaluation
# TODO: GPT? Copilot?

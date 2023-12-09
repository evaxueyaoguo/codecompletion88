import os
import javalang
import openai
import re

def remove_line_from_file(code, lineNum):
    # Split the code into lines
    lines = code.split('\n')

    # Check if the lineNum is valid
    if 1 <= lineNum <= len(lines):
        # Remove the specified line
        del lines[lineNum]

        # Join the lines back into code
        updated_code = '\n'.join(lines)
        return updated_code
    else:
        print(f"Invalid line number: {lineNum}")
        return code
      
# Function to read and return the content of a Java file.
def get_code_from_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
      
# Function to parse Java code into an Abstract Syntax Tree (AST).   
def parse_to_ast(code):
    try:
        ast_tree = javalang.parse.parse(code)
        return ast_tree
    except javalang.parser.JavaSyntaxError as e:
        # print(f"Error parsing Java code: {e}")
        pass
      
def get_var_name_from_line(line):
    return remove_whitespace(line.split(" ").pop())

def remove_whitespace(input_string):
    # Use regular expression to replace tabs, newlines, and spaces with an empty string
    cleaned_string = re.sub(r'[\t\n\s]', '', input_string)
    return cleaned_string

def get_var_name_from_openai(line):
    # TODO: implement
    # if there is one: return var name
    # if there is none: return ""
    openai.api_key = "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"

    # Customize the prompt to instruct the model
    # TODO: imporve the prompt so that correct variable names are returned more often
    # prompt = line +  "\nget the name of the variable from the line of java code above. The line of java code may be complete or incomplete. If there is one: return var name. If there is none: return \"\" The line may be variable declaration, method call, method definition, or class definition."

    prompt = line +  "\nget a name of a variable from the line of java code above. The line of java code may be complete or incomplete. If no variable name can be found, return a space"

    variable_name = " "
    try: 
    # Call the OpenAI API
      response = openai.Completion.create(
          engine="text-davinci-003",  # Choose the engine based on your requirements
          prompt=prompt,
          max_tokens=50,  # Adjust max_tokens based on your desired output length
          n=1,  # Number of completions
          stop=None,  # You can customize the stop criteria if needed
      )
      # Extract and return the generated variable name
      variable_name = response.choices[0].text.strip()
    except Exception as e:
      print(e)
      pass
    return variable_name
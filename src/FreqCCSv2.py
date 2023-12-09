import javalang
import os
import numpy as np
import BMNCCS
import json
  
def context_list_to_method_frequency(context_list):
  method_frequency = {}
  for context in context_list:
    method_calls = context[0]
    declared_type = context[1]
    enclosing_methods = context[2]
    # if not declared_type == None:
    if not declared_type in method_frequency:
      type_method_frequency = {}
      for method_call in method_calls:
        type_method_frequency[method_call] = 1
      method_frequency[declared_type] = type_method_frequency
    else:
      type_method_frequency = method_frequency[declared_type]
      for method_call in method_calls:
        if method_call in type_method_frequency:
          type_method_frequency[method_call] += 1
        else:
          type_method_frequency[method_call] = 1
      method_frequency[declared_type] = type_method_frequency
  return method_frequency

def save_method_frequency_to_file(method_frequency, file_path):
  with open(file_path, 'w') as file:
    json.dump(method_frequency, file)
        
def get_method_frequency_from_file(file_path):
  with open(file_path, 'r') as file:
    data = json.load(file)
  return data

def get_recommendations_from_method_frequency(curr_context_dict_processed, method_frequency, n):
  var_type = curr_context_dict_processed[1]
  if var_type in method_frequency:
    options = method_frequency[var_type]
    sorted_options = sorted(options.items(), key=lambda x: x[1], reverse=True)
    return [option[0] for option in sorted_options[:n]]
  else:
    return []

def main():
    root_directory = "/Users/xueyaoguo/Desktop/DS_project/codecompletion88/"
    current_directory = os.path.join(root_directory, "src")
    data_path = os.path.join(current_directory, "data") # 2236 asts
    # print(current_directory)
    
    data_code = BMNCCS.collect_code_examples(data_path) # list of file strings
    ast_trees = BMNCCS.parse_to_ast(data_code) # list of ast trees
    context_list = list()
    # print(len(ast_trees))

    for ast in ast_trees: 
        local_variable_set = set()
        enclosing_methods_dict = BMNCCS.extract_classes_methods_variables(ast)

        for _, node in ast:
            BMNCCS.extract_local_variables(node, local_variable_set)

        context_dict = {}

        for variable in local_variable_set:
            method_calls, declared_type = BMNCCS.get_method_calls_and_type_on_local_variable(ast, variable)
            enclosing_methods = BMNCCS.get_enclosing_methods_from_dict(variable, enclosing_methods_dict)
            context_dict[variable] = [method_calls, declared_type, enclosing_methods]

        # add in: to the enclosing methods to distinguish them from method calls
        context_dict_processed = BMNCCS.process_context_dict(context_dict)
        # print("context_dict_processed")
        # print(context_dict_processed)
        
        for variable, data in context_dict_processed.items():
            # print(variable, data)
            # context_list.add(tuple(data))
            context_list.append(data)
        
        method_frequency = context_list_to_method_frequency(context_list)
        # print(method_frequency)
        
# code comletion starts here
 
    curr_directory_path = os.path.join(current_directory, "curr_file")
    curr_code = BMNCCS.collect_code_examples(curr_directory_path) # list of file strings
    print(curr_code)
    curr_ast = BMNCCS.parse_to_ast(curr_code)[0] # context ast tree
    curr_variable = "y"
    # print(curr_ast)
    # context_vec = get_context(curr_ast, curr_variable)
    # TODO: retvist how to get current context
    
    curr_context_dict = {}
    enclosing_methods_dict = BMNCCS.extract_classes_methods_variables(curr_ast)
    method_calls, declared_type = BMNCCS.get_method_calls_and_type_on_local_variable(curr_ast, curr_variable)
    enclosing_methods = BMNCCS.get_enclosing_methods_from_dict(curr_variable, enclosing_methods_dict)
    curr_context_dict[curr_variable] = [method_calls, declared_type, enclosing_methods]
    
    curr_context_dict_processed = BMNCCS.process_context_dict(curr_context_dict)
    print(curr_context_dict_processed)
    
    # recommendations
    recommendations = get_recommendations_from_method_frequency(curr_context_dict_processed[curr_variable], method_frequency, 5)
    print(recommendations)

if __name__ == "__main__":
  main()
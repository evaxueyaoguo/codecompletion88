import os
import sys
import argparse
import BMNCCS
import random
import csv
import FreqCCSv2 as FreqCCS

def split_list(input_list, percentage=90):
    # Calculate the number of elements to select based on the percentage
    num_elements_to_select = int(len(input_list) * (percentage / 100.0))

    # Randomly select elements
    selected_elements = random.sample(input_list, num_elements_to_select)

    # Create a list of unselected elements
    unselected_elements = [elem for elem in input_list if elem not in selected_elements]

    return selected_elements, unselected_elements
  
def save_matrix_to_file(matrix, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)
        
def save_encoding_format_to_txt(encoding_format, filename):
    with open(filename, 'w') as file:
        for item in encoding_format:
            file.write(f"{item}\n")
  

def main():
    print("Preprocessing...")
    data_directory = "/Users/xueyaoguo/Desktop/DS_project/codecompletion88/data/eclipse.platform.swt"
    # print(current_directory)

    # FIXME: handle multiple ast trees --> context matrix
    # right now only the last context matrix is saved
    
    data_code = BMNCCS.collect_code_examples(data_directory) # list of file strings
    ast_trees = BMNCCS.parse_to_ast(data_code) # list of ast trees
    train_context_list = []
    train_encoding_format = []
    train_context_matrix = []
    print(len(ast_trees)) #2235 asts, 2011 for training, 224 for testing
    
    print("Splitting into training and test sets...")
    training_set, test_set = split_list(ast_trees)
    print("Training set size: " + str(len(training_set)))
    print("Test set size: " + str(len(test_set)))
    # print(training_set[0])
    
    print("Generating context matrix from the training set...")
    ast_counter = 0
    for ast in training_set: 
        print("Processing training AST " + str(ast_counter) + "...")
        try: 
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
              print(variable, data)
              # context_list.add(tuple(data))
              train_context_list.append(data)
          
        except TypeError as e:
          # Catch TypeError and continue with the next iteration
          print(f"Caught TypeError: {e}")
          continue       
        
        print(str(len(train_context_list)) + " contexts added")
        ast_counter += 1
          
        
        # for variable, data in context_dict.items():
        #     print(variable, data)
    
    # context_matrix, encoding_format = context_dict_to_matrix(context_dict_processed)
    train_context_matrix, train_encoding_format = BMNCCS.context_set_to_matrix(train_context_list)
    train_unique_context_matrix = BMNCCS.remove_duplicate_rows(train_context_matrix)
    save_matrix_to_file(train_unique_context_matrix, "training_context_matrix.csv")
    save_encoding_format_to_txt(train_encoding_format, "training_encoding_format.txt")

    print(len(train_context_matrix))
    print(len(train_unique_context_matrix))
    print(train_encoding_format)
        
        
        
    print("Generating context vectors for the test set...")
    test_context_list = []
    test_encoding_format = []
    test_context_matrix = []
    ast_counter = 0
    for ast in test_set: 
        print("Processing test AST " + str(ast_counter) + "...")
        try: 
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
              print(variable, data)
              # context_list.add(tuple(data))
              test_context_list.append(data)
          
        except TypeError as e:
          # Catch TypeError and continue with the next iteration
          print(f"Caught TypeError: {e}")
          continue       
        
        print(str(len(test_context_list)) + " contexts added")
        ast_counter += 1
        
    # context_matrix, encoding_format = context_dict_to_matrix(context_dict_processed)
    test_context_matrix, test_encoding_format = BMNCCS.context_set_to_matrix(test_context_list)
    test_unique_context_matrix = BMNCCS.remove_duplicate_rows(test_context_matrix)
    save_matrix_to_file(test_unique_context_matrix, "test_context_matrix.csv")
    save_encoding_format_to_txt(test_encoding_format, "test_encoding_format.txt")

    print(len(test_context_matrix))
    print(len(test_unique_context_matrix))
    print(test_encoding_format)
    
    train_method_frequency = FreqCCS.context_list_to_method_frequency(train_context_list)
    test_method_frequency = FreqCCS.context_list_to_method_frequency(test_context_list)
    FreqCCS.save_method_frequency_to_file(train_method_frequency, "train_method_frequency.txt")
    FreqCCS.save_method_frequency_to_file(test_method_frequency, "test_method_frequency.txt")
    
    
if __name__ == '__main__':
    main()
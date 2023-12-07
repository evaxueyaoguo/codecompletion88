import os
import sys
import argparse
import BMNCCS
import random

def split_list(input_list, percentage=90):
    # Calculate the number of elements to select based on the percentage
    num_elements_to_select = int(len(input_list) * (percentage / 100.0))

    # Randomly select elements
    selected_elements = random.sample(input_list, num_elements_to_select)

    # Create a list of unselected elements
    unselected_elements = [elem for elem in input_list if elem not in selected_elements]

    return selected_elements, unselected_elements
  

def main():
    print("Preprocessing...")
    data_directory = "/Users/xueyaoguo/Desktop/DS_project/codecompletion88/data/eclipse.platform.swt"
    # print(current_directory)

    # FIXME: handle multiple ast trees --> context matrix
    # right now only the last context matrix is saved
    
    data_code = BMNCCS.collect_code_examples(data_directory) # list of file strings
    ast_trees = BMNCCS.parse_to_ast(data_code) # list of ast trees
    encoding_format = []
    context_matrix = []
    print(len(ast_trees)) #2235 asts, 2011 for training, 224 for testing
    
    print("Splitting into training and test sets...")
    training_set, test_set = split_list(ast_trees)
    print("Training set size: " + str(len(training_set)))
    print("Test set size: " + str(len(test_set)))
    print(training_set[0])
    
    
    
if __name__ == '__main__':
    main()
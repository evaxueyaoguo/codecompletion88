from mypy import api
import javalang
import os
import numpy as np

# Function to get all java files in a directory
def collect_code_examples(directory):
    code_examples = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    code_examples.append(f.read())

    return code_examples

def parse_to_ast(code_examples):
    ast_list = []

    for code_example in code_examples:
        try:
            ast_tree = javalang.parse.parse(code_example)
            ast_list.append(ast_tree)
        except javalang.parser.JavaSyntaxError as e:
            print(f"Error parsing Java code: {e}")

    return ast_list

def traverse_ast(node, indent=0, visited=set()):
    if id(node) in visited:
        return
    visited.add(id(node))

    if isinstance(node, javalang.tree.ClassDeclaration):
        print(f"{' ' * indent}Class: {node.name}")
    elif isinstance(node, javalang.tree.MethodDeclaration):
        print(f"{' ' * indent}Method: {node.name}")
    elif isinstance(node, javalang.tree.BlockStatement):
        print(f"{' ' * indent}Block Statement")
        for statement in node.statements:
            print(f"{' ' * (indent + 2)}{statement}")

    if isinstance(node, (javalang.tree.ClassDeclaration, javalang.tree.MethodDeclaration)):
        for _, child_node in node:
            traverse_ast(child_node, indent + 2, visited)
            
def extract_local_variables(node, local_variables, indent=0, visited=set()):
    if id(node) in visited:
        return
    visited.add(id(node))
    
    if isinstance(node, javalang.tree.LocalVariableDeclaration):
        for declarator in node.declarators:
            local_variables.add(declarator.name)

    for _, child_node in node:
        extract_local_variables(child_node, local_variables)

def is_variable_used_in_method(node, variable_name, indent=0, visited=set()):
    if id(node) in visited:
        return False
    visited.add(id(node))
    # for _, node in javalang.traverse.iterate(method_node):
    if isinstance(node, javalang.tree.LocalVariableDeclaration):
        for declarator in node.declarators:
            if declarator.name == variable_name:
                return True
    elif isinstance(node, javalang.tree.VariableDeclarator) and node.name == variable_name:
        return True
        # Add more cases as needed based on your requirements 
    # elif isinstance(node, (javalang.tree.ClassDeclaration, javalang.tree.MethodDeclaration)):
    for _, child_node in node:
        if is_variable_used_in_method(child_node, variable_name, indent + 2, visited):
            return True

    return False
    
    
def find_parent(tree, target_node):
    for path, node in tree:
        for _, child_node in node:
            if child_node == target_node:
                return node
    return None

def get_method_calls_and_type_on_local_variable(ast, local_variable_name, visited=set()):
    method_calls = []
    var_type = ""
    enclosing_methods = set() # FIXME
    
    def encode_local_variables(node, enclosing_method=None, visited=set()):
        if id(node) in visited:
            return
        visited.add(id(node))

        if isinstance(node, javalang.tree.MethodInvocation):
            if node.qualifier == local_variable_name:
                method_calls.append(node.member)
                
        elif isinstance(node, javalang.tree.LocalVariableDeclaration):
            if node.declarators[0].name == local_variable_name:
                nonlocal var_type 
                var_type = node.type.name
                # enclosing_method = find_parent(ast, node)
                # print(type(enclosing_method))
                # print(node.type.name)
                # print(node.parent)
        elif isinstance(node, javalang.tree.MethodDeclaration):
            print("calling is_variable_used_in_method for var: " + local_variable_name)
            if is_variable_used_in_method(node, local_variable_name):
                enclosing_methods.add(node.name)

    for _, node in ast:
        encode_local_variables(node)
        
    return method_calls, var_type, enclosing_methods

def context_dict_to_matrix(context_dict):
    # Extract information from the input dictionary
    variable_names = list(context_dict.keys())
    method_contexts = set()
    methods_called = set()

    for data in context_dict.values():
        methods_called.update(data[0])
        method_contexts.add(data[2])

    method_contexts = list(method_contexts)
    methods_called = list(methods_called)

    # Initialize a binary matrix with zeros
    binary_matrix = np.zeros((len(variable_names), len(method_contexts) + len(methods_called)), dtype=int)

    # Fill in the matrix based on the rules
    for idx, variable_name in enumerate(variable_names):
        methods_called_on_variable, variable_type, enclosing_methods = context_dict[variable_name]

        # Set 1 for the method context
        method_context_idx = method_contexts.index(enclosing_methods)
        binary_matrix[idx, method_context_idx] = 1

        # Set 1 for each method called on the variable
        for method_called in methods_called_on_variable:
            method_called_idx = len(method_contexts) + methods_called.index(method_called)
            binary_matrix[idx, method_called_idx] = 1

    return binary_matrix

def find_enclosing_function(node, variable_name, parent=None, visited=set()):
    if id(node) in visited:
        return None
    visited.add(id(node))
    
    if isinstance(node, javalang.tree.MethodDeclaration):
        # Check if the variable is declared in the method's parameters
        for parameter in node.parameters:
            if parameter.name == variable_name:
                return node.name

        # Check if the variable is declared in the method's body
        for path, child_node in node:
            if find_enclosing_function(child_node, variable_name, parent=node, visited=visited):
                return node.name

    for _, child_node in node:
        result = find_enclosing_function(child_node, variable_name, parent=parent, visited=visited)
        if result:
            return result

    return None

def encode_ast_context(ast):
  # TODO: takes an ast from a file, should return a 2-D matrix of the context of each local variable
  # num rows = num local variables
  # num cols = num method contexts in the training code base + 
  #            num all callable methods on all framework types ??
  # return context_matrix
  pass

def find_best_matching_neighbors(observation, context_matrix):
  # TODO: user Hamming distance to find the best matching neighbors
  pass

def synthesize_recommendation(best_matching_neighbors):
  # TODO: synthesize a recommendation based on the best matching neighbors
  pass
        
def main():
  directory_path = "./data"
  
  code = collect_code_examples(directory_path) # list of file strings
  ast_trees = parse_to_ast(code) # list of ast trees
  
  for ast in ast_trees:    
        local_variable_set = set()

        for _, node in ast:
            extract_local_variables(node, local_variable_set)

        context_dict = {}

        for variable in local_variable_set:
            method_calls, declared_type, enclosing_method = get_method_calls_and_type_on_local_variable(ast, variable)
            # enclosing_method = find_enclosing_function(ast, variable) # FIXME: THIS IS NOT WORKING
            
            # context_dict[variable] = [method_calls, enclosing_method]
            context_dict[variable] = [method_calls, declared_type, enclosing_method]
            
        for variable, data in context_dict.items():
            print(variable, data)
            
        # context_matrix = context_dict_to_matrix(context_dict)
        # print(context_matrix)


if __name__ == "__main__":
    main()
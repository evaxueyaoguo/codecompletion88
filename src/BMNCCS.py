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
     
def find_parent(tree, target_node):
    for path, node in tree:
        for _, child_node in node:
            if child_node == target_node:
                return node
    return None

def get_method_calls_and_type_on_local_variable(ast, local_variable_name, visited=set()):
    method_calls = []
    var_type = ""
    # enclosing_methods = set() # FIXME
    
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

    for _, node in ast:
        encode_local_variables(node)
        
    return method_calls, var_type

def context_dict_to_matrix(context_dict):
# returns a 2-D matrix of the context of each local variable
  # num rows = num local variables
  # num cols = num method contexts in the training code base + 
  #            num all callable methods on all framework types ??
  # return context_matrix
# Extract information from the input dictionary
    variable_names = list(context_dict.keys())
    method_contexts = set()
    methods_called = set()
    encoding_format = list()

    for data in context_dict.values():
        methods_called.update(data[0])
        method_contexts.update(data[2])

    # these 2 lists are the encoding format. i.e. which column is which in the binary matrix
    method_contexts = list(method_contexts)
    methods_called = list(methods_called)
    encoding_format = method_contexts + methods_called
    # Initialize a binary matrix with zeros
    binary_matrix = np.zeros((len(variable_names), len(method_contexts) + len(methods_called)), dtype=int)

    # Fill in the matrix based on the rules
    for idx, variable_name in enumerate(variable_names):
        methods_called_on_variable, variable_type, enclosing_methods = context_dict[variable_name]

        # Set 1 for the method context
        for method_context in enclosing_methods:
            method_context_idx = method_contexts.index(method_context)
            binary_matrix[idx, method_context_idx] = 1

        # Set 1 for each method called on the variable
        for method_called in methods_called_on_variable:
            method_called_idx = len(method_contexts) + methods_called.index(method_called)
            binary_matrix[idx, method_called_idx] = 1

    return binary_matrix, encoding_format

def get_context(ast, variable):
    pass

def encode_context(context, encoding_format):
    pass

def find_best_matching_neighbors(observation, context_matrix):
  # TODO: user Hamming distance to find the best matching neighbors
  pass

def synthesize_recommendation(best_matching_neighbors):
  # TODO: synthesize a recommendation based on the best matching neighbors
  pass

        
def extract_classes_methods_variables(ast):
    result_dict = {}

    for path, node in ast:
        if isinstance(node, javalang.tree.ClassDeclaration):
            class_name = node.name
            method_dict = {}

            for member in node.body:
                if isinstance(member, javalang.tree.MethodDeclaration):
                    method_name = member.name
                    variables = []

                    for local_variable in member.body:
                        if isinstance(local_variable, javalang.tree.LocalVariableDeclaration):
                            for declarator in local_variable.declarators:
                                variables.append(declarator.name)

                    method_dict[method_name] = variables if variables else None

            result_dict[class_name] = method_dict

    return result_dict       
        
def get_enclosing_methods_from_dict(variable_name, enclosing_methods_dict):
    enclosing_methods = set()
    for class_name, method_dict in enclosing_methods_dict.items():
        for method_name, variables in method_dict.items():
            if variables and variable_name in variables:
                enclosing_methods.add(method_name)
    return list(enclosing_methods)

def main():
    data_directory_path = "./data"

    data_code = collect_code_examples(data_directory_path) # list of file strings
    ast_trees = parse_to_ast(data_code) # list of ast trees

    for ast in ast_trees:    
        local_variable_set = set()
        enclosing_methods_dict = extract_classes_methods_variables(ast)

        for _, node in ast:
            extract_local_variables(node, local_variable_set)

        context_dict = {}

        for variable in local_variable_set:
            method_calls, declared_type = get_method_calls_and_type_on_local_variable(ast, variable)
            enclosing_methods = get_enclosing_methods_from_dict(variable, enclosing_methods_dict)
            context_dict[variable] = [method_calls, declared_type, enclosing_methods]
            
        for variable, data in context_dict.items():
            print(variable, data)
        context_matrix, encoding_format = context_dict_to_matrix(context_dict)
        print(context_matrix)
        print(encoding_format)
        
 # code comletion starts here
    curr_directory_path = "./"
    curr_code = collect_code_examples(curr_directory_path) # list of file strings
    curr_ast = parse_to_ast(curr_code)[0] # context ast tree
    curr_variable = "display"
    # context_vec = get_context(curr_ast, curr_variable)
    # TODO: retvist how to get current context
    
    curr_context_dict = {}
    enclosing_methods_dict = extract_classes_methods_variables(curr_ast)
    method_calls, declared_type = get_method_calls_and_type_on_local_variable(curr_ast, curr_variable)
    enclosing_methods = get_enclosing_methods_from_dict(curr_variable, enclosing_methods_dict)
    curr_context_dict[curr_variable] = [method_calls, declared_type, enclosing_methods]
    for variable, data in curr_context_dict.items():
        print(variable, data)
    
    # TODO: encode context to vector
    
    # TODO: find best matching neighbors using Hamming distance
    
    # TODO: add type infomration to the recommendation
    
    # TODO: synthesize a recommendation based on the best matching neighbors
    
    # TODO: integrate with VSCode
    
    
    # print(curr_ast)

if __name__ == "__main__":
    main()
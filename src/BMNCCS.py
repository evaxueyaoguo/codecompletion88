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
            # print(f"Error parsing Java code: {e}")
            continue

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
    enclosing_class = ""
    # enclosing_methods = set() # FIXME
    
    def encode_local_variables(node, enclosing_method=None, visited=set()):
        if id(node) in visited:
            return
        visited.add(id(node))

        if isinstance(node, javalang.tree.MethodInvocation):
            if node.qualifier == local_variable_name:
                nonlocal enclosing_class
                method_calls.append(enclosing_class + "." + node.member)
                
        elif isinstance(node, javalang.tree.LocalVariableDeclaration):
            if node.declarators[0].name == local_variable_name:
                nonlocal var_type 
                var_type = node.type.name
                
        elif isinstance(node, javalang.tree.ClassDeclaration):
            enclosing_class = node.name

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
    var_types = set()
    encoding_format = list()

    for data in context_dict.values():
        methods_called.update(data[0])
        var_types.add(data[1])
        method_contexts.update(data[2])
        

    # these 2 lists are the encoding format. i.e. which column is which in the binary matrix
    method_contexts = list(method_contexts)
    var_types = list(var_types)
    methods_called = list(methods_called)
    encoding_format = method_contexts + var_types + methods_called
    # Initialize a binary matrix with zeros
    binary_matrix = np.zeros((len(variable_names), len(method_contexts) + len(var_types) + len(methods_called)), dtype=int)

    # Fill in the matrix based on the rules
    for idx, variable_name in enumerate(variable_names):
        methods_called_on_variable, variable_type, enclosing_methods = context_dict[variable_name]

        # Set 1 for the method context
        for method_context in enclosing_methods:
            method_context_idx = method_contexts.index(method_context)
            binary_matrix[idx, method_context_idx] = 1
            
        # Set 1 for the variable type
        if variable_type in var_types:
            var_type_idx = len(method_contexts) + var_types.index(variable_type)
            binary_matrix[idx, var_type_idx] = 1

        # Set 1 for each method called on the variable
        for method_called in methods_called_on_variable:
            method_called_idx = len(method_contexts) + len(var_types)+ methods_called.index(method_called)
            binary_matrix[idx, method_called_idx] = 1
    return binary_matrix, encoding_format

def context_set_to_matrix(context_set):
        # returns a 2-D matrix of the context of each local variable
    # num rows = num local variables
    # num cols = num method contexts in the training code base + 
    #            num all callable methods on all framework types ??
    # return context_matrix
    # Extract information from the input dictionary
    # variable_names = list(context_dict.keys())
    method_contexts = set()
    methods_called = set()
    var_types = set()
    encoding_format = list()

    for data in context_set:
        methods_called.update(data[0])
        var_types.add(data[1])
        method_contexts.update(data[2])
        

    # these 2 lists are the encoding format. i.e. which column is which in the binary matrix
    method_contexts = list(method_contexts)
    var_types = list(var_types)
    methods_called = list(methods_called)
    encoding_format = method_contexts + var_types + methods_called
    # Initialize a binary matrix with zeros
    binary_matrix = np.zeros((len(context_set), len(method_contexts) + len(var_types) + len(methods_called)), dtype=int)

    # Fill in the matrix based on the rules
    for idx, data in enumerate(context_set):
        methods_called_on_variable, variable_type, enclosing_methods = data

        # Set 1 for the method context
        for method_context in enclosing_methods:
            method_context_idx = method_contexts.index(method_context)
            binary_matrix[idx, method_context_idx] = 1
            
        # Set 1 for the variable type
        if variable_type in var_types:
            var_type_idx = len(method_contexts) + var_types.index(variable_type)
            binary_matrix[idx, var_type_idx] = 1

        # Set 1 for each method called on the variable
        for method_called in methods_called_on_variable:
            method_called_idx = len(method_contexts) + len(var_types)+ methods_called.index(method_called)
            binary_matrix[idx, method_called_idx] = 1
    return binary_matrix, encoding_format
    
def process_context_dict(context_dict):
    context_dict_processed = {}
    for variable, data in context_dict.items():
        # method_calls, declared_type, enclosing_methods = data
        method_calls = data[0]
        declared_type = data[1]
        enclosing_methods = data[2]
        enclosing_methods_processed = []
        if not len(enclosing_methods) == 0:
            for enclosing_method in enclosing_methods:
                enclosing_methods_processed.append("in:" + enclosing_method)
        context_dict_processed[variable] = [method_calls, declared_type, enclosing_methods_processed]
    return context_dict_processed
    
def get_context(ast, variable):
    pass

def get_context_list(context):
    context_list = []
    for item in context:
        if isinstance(item, list):
            context_list.extend(item)
        else:
            context_list.append(item)
    return context_list
            
def get_context_vector(context, encoding_format):
    # returns a vector of the context of the current local variable
    context_list = get_context_list(context)
    context_vector = list(len(encoding_format) * [0])
    for idx, format in enumerate(encoding_format):
        if format in context_list:
            context_vector[idx] = 1
    return context_vector

def get_hamming_distance(vector1, vector2):
    # Calculate the Hamming distance between two binary vectors
    return sum(bit1 != bit2 for bit1, bit2 in zip(vector1, vector2))

def find_best_matching_neighbors(n, context_vec, context_matrix):
    #use Hamming distance to find the best matching neighbors
    # Calculate Hamming distances for all vectors in the matrix
    distances = [(i, get_hamming_distance(context_vec, row)) for i, row in enumerate(context_matrix)]

    # Sort the vectors based on Hamming distance and return the top n
    sorted_distances = sorted(distances, key=lambda x: x[1])
    best_n_neighbors = [index for index, _ in sorted_distances[:n]]
    best_n_neighbors = [context_matrix[index] for index in best_n_neighbors]
    return best_n_neighbors

def get_method_calls_from_encoding_format(encoding_format):
    method_calls = []
    for idx, format in enumerate(encoding_format):
        if "." in format and not "in:" in format:
            method_calls.append(format)
    return method_calls
    
def subset_matrix(matrix, column_encodings, subset_encodings):
    # Find indices of the subset encodings in the column encodings
    subset_indices = [column_encodings.index(encoding) for encoding in subset_encodings]

    # Extract the subset of columns from the matrix
    subset_matrix = np.array([row[subset_indices] for row in matrix])

    return subset_matrix

def calculate_likelihood(matrix, column_encodings):
    likelihoods = {}

    # Convert the matrix to a NumPy array for easy calculations
    matrix_array = np.array(matrix)

    # Iterate over each column and calculate the likelihood
    for i, encoding in enumerate(column_encodings):
        ones_count = np.sum(matrix_array[:, i])
        total_rows = matrix_array.shape[0]

        # Calculate the likelihood as the percentage of ones in the column
        likelihood = (ones_count / total_rows) * 100

        likelihoods[encoding] = likelihood

    return likelihoods

def filter_methods_by_threshold(method_likelihoods, threshold):
    # Filter methods based on the threshold
    selected_methods = [method for method, likelihood in method_likelihoods.items() if likelihood > threshold]

    # Sort the selected methods based on likelihood in descending order
    sorted_methods = sorted(selected_methods, key=lambda x: method_likelihoods[x], reverse=True)

    return sorted_methods

def synthesize_recommendation(best_matching_neighbors, encoding_format):
  # TODO: synthesize a recommendation based on the best matching neighbors
  method_calls = get_method_calls_from_encoding_format(encoding_format)
  method_calls_matrix = subset_matrix(best_matching_neighbors, encoding_format, method_calls)
  likelihoods = calculate_likelihood(method_calls_matrix, method_calls)
  recommendations = filter_methods_by_threshold(likelihoods, 0)
  return recommendations
        
def extract_classes_methods_variables(ast):
    result_dict = {}

    for path, node in ast:
        if isinstance(node, javalang.tree.ClassDeclaration):
            class_name = node.name
            method_dict = {}

            for member in node.body:
                if isinstance(member, javalang.tree.MethodDeclaration):
                    method_name = class_name + "." + member.name
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

def remove_duplicate_rows(matrix):
    seen_rows = set()
    unique_matrix = []

    for row in matrix:
        # Convert the row to a tuple to make it hashable
        row_tuple = tuple(row)

        # Check if the row is not in the set of seen rows
        if row_tuple not in seen_rows:
            # Add the row to the set and the unique_matrix
            seen_rows.add(row_tuple)
            unique_matrix.append(list(row))

    return unique_matrix

def main():
    # FIXME: is each column a local variable or a method context?
    # e.g. 'shell': [['HelloWorld.setText', 'HelloWorld.setLayout', 'HelloWorld.setDefaultButton', 'HelloWorld.setSize', 'HelloWorld.computeSize', 'HelloWorld.open', 'HelloWorld.isDisposed', 'HelloWorld.setText', 'anotherClass.setText'], 'Shell', ['in:HelloWorld.main', 'in:anotherClass.anotherMethodInAnotherClass', 'in:HelloWorld.anotherMethod']]
    # [1 1 1 0 0 0 0 0 1 0 0 1 0 1 1 1 0 1 1 1 0 0 0 1 0]
    # and {'shell': [['HelloWorld.setText'], 'Shell', ['in:HelloWorld.anotherMethod']]}
    # [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # this needs to be fixed
    root_directory = "/Users/xueyaoguo/Desktop/DS_project/codecompletion88/"
    current_directory = os.path.join(root_directory, "src")
    data_path = os.path.join(current_directory, "data") # 2236 asts
    # print(current_directory)
    
    data_code = collect_code_examples(data_path) # list of file strings
    ast_trees = parse_to_ast(data_code) # list of ast trees
    context_list = list()
    encoding_format = []
    context_matrix = []
    # print(len(ast_trees))

    # TODO; accomondate multiple ast trees
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

        # add in: to the enclosing methods to distinguish them from method calls
        context_dict_processed = process_context_dict(context_dict)
        # print("context_dict_processed")
        # print(context_dict_processed)
        
        for variable, data in context_dict_processed.items():
            print(variable, data)
            # context_list.add(tuple(data))
            context_list.append(data)
        
        # for variable, data in context_dict.items():
        #     print(variable, data)
        
    # context_matrix, encoding_format = context_dict_to_matrix(context_dict_processed)
    context_matrix, encoding_format = context_set_to_matrix(context_list)
    unique_context_matrix = remove_duplicate_rows(context_matrix)

    print(len(unique_context_matrix))
    print(len(unique_context_matrix))
    print(encoding_format)
        
 # code comletion starts here
 
    # TODO: handle Error parsing Java code: 
    curr_directory_path = current_directory
    curr_code = collect_code_examples(curr_directory_path) # list of file strings
    curr_ast = parse_to_ast(curr_code)[0] # context ast tree
    curr_variable = "display"
    # print(curr_ast)
    # context_vec = get_context(curr_ast, curr_variable)
    # TODO: retvist how to get current context
    
    curr_context_dict = {}
    enclosing_methods_dict = extract_classes_methods_variables(curr_ast)
    method_calls, declared_type = get_method_calls_and_type_on_local_variable(curr_ast, curr_variable)
    enclosing_methods = get_enclosing_methods_from_dict(curr_variable, enclosing_methods_dict)
    curr_context_dict[curr_variable] = [method_calls, declared_type, enclosing_methods]
    # for variable, data in curr_context_dict.items():
    #     print(variable, data)
    
    curr_context_dict_processed = process_context_dict(curr_context_dict)
    # print(curr_context_dict_processed)
    
    # encode context to vector
    context = curr_context_dict_processed[curr_variable]
    curr_context_vector = get_context_vector(context, encoding_format)
    # print(curr_context_vector)
    
    #find best n matching neighbors using Hamming distance
    n = 5
    best_matching_neighbors = find_best_matching_neighbors(n, curr_context_vector, context_matrix)
    # print(best_matching_neighbors)
    
    # TODO: synthesize a recommendation based on the best matching neighbors
    recommendations = synthesize_recommendation(best_matching_neighbors, encoding_format)
    print(recommendations)
    
    # TODO: integrate with VSCode
    
if __name__ == "__main__":
    main()
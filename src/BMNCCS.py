from mypy import api
import javalang
import os

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
        

    
def get_method_calls_and_type_on_local_variable(ast, local_variable_name, visited=set()):
    method_calls = []
    var_type = ""

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
                print(node.type.name)

    for _, node in ast:
        encode_local_variables(node)
        
    return method_calls, var_type

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
            # print(variable+ ": ")
            method_calls, declared_type= get_method_calls_and_type_on_local_variable(ast, variable)
            enclosing_method = ""
            
            context_dict[variable] = [method_calls, declared_type, enclosing_method]
            # Display the context
        for c in context_dict:
            print(c, '', context_dict[c])


if __name__ == "__main__":
    main()
import FreqCCSv2 as FreqCCS
import BMNCCS
import argparse
import util
import predict

def get_recommendaions_FreqCCS(context_path, lineNum, line):
    code = util.get_code_from_file(context_path)
    code = util.remove_line_from_file(code, lineNum)
    ast = util.parse_to_ast(code)
    
    # curr_variable = util.get_var_name_from_openai(line)
    curr_variable = util.get_var_name_from_line(line)
    curr_variable = curr_variable.split(".")[0]
    method_frequency = FreqCCS.get_method_frequency_from_file("/Users/xueyaoguo/Desktop/DS_project/codecompletion88/train_method_frequency.txt")
    
    curr_context_dict = {}
    enclosing_methods_dict = BMNCCS.extract_classes_methods_variables(ast)
    method_calls, declared_type = BMNCCS.get_method_calls_and_type_on_local_variable(ast, curr_variable)
    enclosing_methods = BMNCCS.get_enclosing_methods_from_dict(curr_variable, enclosing_methods_dict)
    curr_context_dict[curr_variable] = [method_calls, declared_type, enclosing_methods]
    
    curr_context_dict_processed = BMNCCS.process_context_dict(curr_context_dict)
    
    # recommendations
    recommendations = FreqCCS.get_recommendations_from_method_frequency(curr_context_dict_processed[curr_variable], method_frequency, 5)
    recommendations_processed = []
    for item in recommendations:
      recommendations_processed.append(f"{curr_variable}{item}")
    return recommendations_processed
  
def get_recommendaions_BMNCCS(context_path, lineNum, line):
    code = util.get_code_from_file(context_path)
    code = util.remove_line_from_file(code, lineNum)
    ast = util.parse_to_ast(code)
    
    # curr_variable = util.get_var_name_from_openai(line)
    curr_variable = util.get_var_name_from_line(line)
    curr_variable = curr_variable.split(".")[0]
    
    curr_context_dict = {}
    enclosing_methods_dict = BMNCCS.extract_classes_methods_variables(ast)
    method_calls, declared_type = BMNCCS.get_method_calls_and_type_on_local_variable(ast, curr_variable)
    enclosing_methods = BMNCCS.get_enclosing_methods_from_dict(curr_variable, enclosing_methods_dict)
    curr_context_dict[curr_variable] = [method_calls, declared_type, enclosing_methods]
    
    curr_context_dict_processed = BMNCCS.process_context_dict(curr_context_dict)
    
    training_context_matrix = predict.read_binary_matrix_from_csv("/Users/xueyaoguo/Desktop/DS_project/codecompletion88/training_context_matrix.csv")
    training_encoding_format = predict.read_text_file("/Users/xueyaoguo/Desktop/DS_project/codecompletion88/training_encoding_format.txt")
    
    
    # encode context to vector
    context = curr_context_dict_processed[curr_variable]
    curr_context_vector = BMNCCS.get_context_vector(context, training_encoding_format)
    
    best_matching_neighbors = BMNCCS.find_best_matching_neighbors(curr_context_vector, training_context_matrix)
    
    recommendations = BMNCCS.synthesize_recommendation(best_matching_neighbors, training_encoding_format)
    recommendations_processed = []
    for item in recommendations:
      recommendations_processed.append(f"{curr_variable}{item}")
    return recommendations_processed

def get_recommendaions(mode, context_path, lineNum, line):
  if mode == "BMNCCS":
    return get_recommendaions_BMNCCS(context_path, lineNum, line)
  elif mode == "FreqCCS":
    return get_recommendaions_FreqCCS(context_path, lineNum, line)
  else:
    # print("Error: Invalid mode")
    return None


def main():
  parser = argparse.ArgumentParser(description='CCS Controller')

  # Add command-line arguments
  parser.add_argument('mode', type=str, help='FreqCCS or BMNCCS')
  parser.add_argument('context_path', type=str, help='context file path')
  parser.add_argument('lineNum', type=int, help='line number')
  parser.add_argument('line', type=str, help='line text')
  # parser.add_argument('--optional_arg', type=str, default='default_value', help='Description of an optional argument')

  # Parse the command-line arguments
  args = parser.parse_args()

  # Access the parsed arguments
  recommendations = get_recommendaions(args.mode, args.context_path, args.lineNum, args.line)
  print(recommendations)


if __name__ == "__main__":
    main()
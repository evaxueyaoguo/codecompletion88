import FreqCCSv2 as FreqCCS
import BMNCCS
import argparse
import util

def get_recommendaions_FreqCCS(context_path, lineNum, line):
    # print("get_recommendaions_FreqCCS")
    # print(line)
    # context = context[0]
    
    # curr_ast = BMNCCS.parse_to_ast(curr_code)[0]
    code = util.get_code_from_file(context_path)
    code_with_line_removed = util.remove_line_from_file(code, lineNum)
    ast = util.parse_to_ast(code_with_line_removed)
    
    curr_variable = util.get_var_name_from_openai(line)
    # print(curr_variable)
    # print(curr_ast)
    # context_vec = get_context(curr_ast, curr_variable)
    # TODO: retvist how to get current context
    method_frequency = FreqCCS.get_method_frequency_from_file("/Users/xueyaoguo/Desktop/DS_project/codecompletion88/train_method_frequency.txt")
    
    curr_context_dict = {}
    enclosing_methods_dict = BMNCCS.extract_classes_methods_variables(ast)
    method_calls, declared_type = BMNCCS.get_method_calls_and_type_on_local_variable(ast, curr_variable)
    enclosing_methods = BMNCCS.get_enclosing_methods_from_dict(curr_variable, enclosing_methods_dict)
    curr_context_dict[curr_variable] = [method_calls, declared_type, enclosing_methods]
    
    curr_context_dict_processed = BMNCCS.process_context_dict(curr_context_dict)
    # print(curr_context_dict_processed)
    
    # recommendations
    recommendations = FreqCCS.get_recommendations_from_method_frequency(curr_context_dict_processed[curr_variable], method_frequency, 5)
    return recommendations
  
def get_recommendaions_BMNCCS(context_path, lineNum, line):
  pass

def get_recommendaions(mode, context_path, lineNum, line):
  if mode == "BMNCCS":
    return get_recommendaions_BMNCCS(context_path, lineNum, line)
  elif mode == "FreqCCS":
    return get_recommendaions_FreqCCS(context_path, lineNum, line)
  else:
    # print("Error: Invalid mode")
    return None


def main():
  # print("CCS Controller")
    # Create ArgumentParser object
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
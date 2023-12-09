import csv
import random
import preprocess
import BMNCCS
import FreqCCSv2 as FreqCCS

def read_binary_matrix_from_csv(file_path):
    matrix = []

    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            for row in reader:
                # Convert each element in the row to integers
                row = [int(element) for element in row]
                matrix.append(row)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return matrix
  
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read all lines from the file into a list
            lines = file.readlines()
            
            # Remove newline characters from each line
            lines = [line.strip() for line in lines]
            
            return lines

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def transform_context_vector(train_context_matrix, test_context_matrix, train_encoding_format, test_encoding_format):
    # Combine the encoding formats while preserving the order
    combined_encoding_format = train_encoding_format + [feature for feature in test_encoding_format if feature not in train_encoding_format]

    # Find the indices of overlapping items in both encoding formats
    overlap_indices_train = [train_encoding_format.index(feature) for feature in test_encoding_format if feature in train_encoding_format]
    overlap_indices_test = [test_encoding_format.index(feature) for feature in test_encoding_format if feature in train_encoding_format]

    # Extend the train_context_matrix with zeros for the new features
    train_context_matrix_processed = [row + [0] * (len(test_encoding_format) - len(overlap_indices_test)) for row in train_context_matrix]

    # Extend the test_context_matrix with zeros for the new features
    test_context_matrix_processed = [row + [0] * (len(train_encoding_format) - len(overlap_indices_train)) for row in test_context_matrix]

    return train_context_matrix_processed, test_context_matrix_processed, combined_encoding_format
  
def transform_test_context_vector(test_context_vectors, test_encoding_format, combined_encoding_format):
    # Create a mapping of indices for the combined encoding format
    combined_encoding_indices = {feature: index for index, feature in enumerate(combined_encoding_format)}

    # Initialize the processed test context vectors with zeros for new features
    test_context_vectors_processed = [[0] * len(combined_encoding_format) for _ in range(len(test_context_vectors))]

    # Fill in the values from the original test context vectors based on the mapping
    for row_idx, row in enumerate(test_context_vectors):
        for feature, value in zip(test_encoding_format, row):
            combined_index = combined_encoding_indices[feature]
            test_context_vectors_processed[row_idx][combined_index] = value

    return test_context_vectors_processed
  
def count_different_elements(vector1, vector2):
    if len(vector1) != len(vector2):
        print("Error: Vectors must be of the same length.")
        return

    # Count the number of differing elements
    differing_elements = sum(1 for elem1, elem2 in zip(vector1, vector2) if elem1 != elem2)

    return differing_elements

def get_relevant_recommendations(label, test_context_vector_degraded, encoding_format):
    # relevant_recommendations = [element for element, label_bit, test_bit in zip(encoding_format, label, test_context_vector_degraded) if label_bit == 1 and not element.startswith("in:") and "." in element"]
    relevant_recommendations = []
    for idx, format in enumerate(encoding_format):
        if label[idx] == 1 and not format.startswith("in:") and "." in format:
            relevant_recommendations.append(format)
    return relevant_recommendations

def get_intersection(list1, list2):
    return list(set(list1) & set(list2))

def get_precision(recommendations_made, recommendations_relevant):
    if len(recommendations_made) == 0:
        return 0
    return len(get_intersection(recommendations_made, recommendations_relevant)) / len(recommendations_made)

def get_recall(recommendations_made, recommendations_relevant):
    if len(recommendations_relevant) == 0:
        return 0
    return len(get_intersection(recommendations_made, recommendations_relevant)) / len(recommendations_relevant)

def get_f1_score(precision_val, recall_val):
    if precision_val == 0 and recall_val == 0:
        return 0
    return 2 * (precision_val * recall_val) / (precision_val + recall_val)

def get_average(list):
    return sum(list) / len(list)
  
def main():
  print("Reading training context from files...")
  training_context_matrix = read_binary_matrix_from_csv("training_context_matrix.csv")
  training_encoding_format = read_text_file("training_encoding_format.txt")
  print("Training test size: " + str(len(training_context_matrix)))
  print("Training encoding format size: " + str(len(training_encoding_format)))
  
  print("Reading testing context vectors from files...")
  test_context_vectors_degraded = read_binary_matrix_from_csv("test_context_matrix_degraded.csv")
  test_context_vectors = read_binary_matrix_from_csv("test_context_matrix.csv")
  test_encoding_format = read_text_file("test_encoding_format.txt")
  print("Test context size: " + str(len(test_context_vectors)))
  
#   train_type_count = 0
#   test_type_count = 0
#   for format in training_encoding_format:
#     if not format.startswith("in:") and not "." in format:
#         train_type_count += 1
#         print(format)
#   print("Training types: " + str(train_type_count))
#   for format in test_encoding_format:
#     if not format.startswith("in:") and not "." in format:
#         test_type_count += 1
#         print(format)
#   print("Test types: " + str(test_type_count))
  print("Combining training and test encoding formats...")
  train_context_matrix_processed, test_context_vectors_processed, combined_encoding_format = transform_context_vector(training_context_matrix, test_context_vectors, training_encoding_format, test_encoding_format)
  test_context_vectors_degraded_processed =  transform_test_context_vector(test_context_vectors_degraded, test_encoding_format, combined_encoding_format)
  print("Combined encoding format size: " + str(len(combined_encoding_format)))
  print("Combined training context size: " + str(len(train_context_matrix_processed)) + " x " + str(len(train_context_matrix_processed[0])))
  print("Combined test degraded context size: " + str(len(test_context_vectors_degraded_processed)) + " x " + str(len(test_context_vectors_degraded_processed[0])))
  print("Combined test context size: " + str(len(test_context_vectors_processed)) + " x " + str(len(test_context_vectors_processed[0])))
  print("Combined encoding format: " + str(combined_encoding_format))
#   combined_type_count = 0
#   for format in combined_encoding_format:
#     if not format.startswith("in:") and not "." in format:
#         combined_type_count += 1
#         print(format)
#   print("Test types: " + str(combined_type_count))
  
  
                                                
  print("Predicting...")
  BMNCCS_precision_values = []
  BMNCCS_recall_values = []
  BMNCCS_f1_values = []
  FreqCCS_precision_values = []
  FreqCCS_recall_values = []
  FreqCCS_f1_values = []
  for idx, test_context_vector in enumerate(test_context_vectors_degraded_processed[:100]):
#   for idx, test_context_vector in enumerate(test_context_vectors_degraded_processed[:10]):
    print("Predicting for test context vector " + str(idx) + "...")
    #find best matching neighbors using Hamming distance
    best_matching_neighbors_BMNCCS = BMNCCS.find_best_matching_neighbors(test_context_vector, train_context_matrix_processed)
    recommendations_made_BMNCCS = BMNCCS.synthesize_recommendation(best_matching_neighbors_BMNCCS, combined_encoding_format)
    # print(len(recommendations_made_BMNCCS)) # this seems to be the same for all test context vectors
    # FIXME: need to work on model accuracy
    
    # get variable type
    print("Getting variable type...")
    method_frequency = FreqCCS.get_method_frequency_from_file("/Users/xueyaoguo/Desktop/DS_project/codecompletion88/train_method_frequency.txt")
    var_type = FreqCCS.get_var_type_from_context_vector(test_context_vector, combined_encoding_format)
    # best_matching_neighbors_FreqCCS = BMNCCS.find_best_matching_neighbors(test_context_vector, train_context_matrix_processed)
    recommendations_made_FreqCCS = FreqCCS.get_recommendations_from_method_frequency_with_var_type(var_type, method_frequency, 5)
    
    # recommendations
    # recommendations = FreqCCS.get_recommendations_from_method_frequency(curr_context_dict_processed[curr_variable], method_frequency, 5)
    # recommendations_processed = []
    # for item in recommendations:
    #   recommendations_processed.append(f"{curr_variable}{item}")
    # for item in recommendations_processed:
    #   print(item)
    
    print(str(len(recommendations_made_BMNCCS)) + " recommendations made BMNCCS:" + str(recommendations_made_BMNCCS))
    print(str(len(recommendations_made_FreqCCS)) + " recommendations made FreqCCS:" + str(recommendations_made_FreqCCS))
    
    # label = test_context_vectors_processed[idx] # TODO: need to look into this, returning recs, just not the correct ones 
    # for i in range(len(label)):
    #     if label[i] == 1:
    #         print(combined_encoding_format[i])
    label = test_context_vectors[idx]
    recommendations_relevant = get_relevant_recommendations(label, test_context_vector, test_encoding_format)
    print(str(len(recommendations_relevant)) + "Recommendations relevant: " + str(recommendations_relevant))
    
    BMNCCS_precision_values.append(get_precision(recommendations_made_BMNCCS, recommendations_relevant))
    BMNCCS_recall_values.append(get_recall(recommendations_made_BMNCCS, recommendations_relevant))
    BMNCCS_f1_values.append(get_f1_score(BMNCCS_precision_values[-1], BMNCCS_recall_values[-1]))
    print("BMNCCS_Precision: " + str(BMNCCS_precision_values[-1]))
    print("BMNCCS_Recall: " + str(BMNCCS_recall_values[-1]))
    print("BMNCCS_F1 score: " + str(BMNCCS_f1_values[-1]))
    
    FreqCCS_precision_values.append(get_precision(recommendations_made_FreqCCS, recommendations_relevant))
    FreqCCS_recall_values.append(get_recall(recommendations_made_FreqCCS, recommendations_relevant))
    FreqCCS_f1_values.append(get_f1_score(FreqCCS_precision_values[-1], FreqCCS_recall_values[-1]))
    print("BMNCCS_Precision: " + str(FreqCCS_precision_values[-1]))
    print("BMNCCS_Recall: " + str(FreqCCS_recall_values[-1]))
    print("BMNCCS_F1 score: " + str(FreqCCS_f1_values[-1]))

    # FIXME: giving recommendationsm just not the correct ones
    # FIXME: precision and recall are 0.0
    # FIXME: f1 score is 0.0
    
    print("Average BMNCCS_precision: " + str(get_average(BMNCCS_precision_values)))
    print("Average BMNCCS_recall: " + str(get_average(BMNCCS_recall_values)))
    print("Average BMNCCS_f1 score: " + str(get_average(BMNCCS_f1_values)))
    
    print("Average FreqCCS_precision: " + str(get_average(FreqCCS_precision_values)))
    print("Average FreqCCS_recall: " + str(get_average(FreqCCS_recall_values)))
    print("Average FreqCCS_f1 score: " + str(get_average(FreqCCS_f1_values)))

if __name__ == '__main__':
  main()
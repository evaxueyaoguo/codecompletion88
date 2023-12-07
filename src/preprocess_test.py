import csv
import random
import preprocess

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
      
def get_method_called_idx(encoding_format):
    for index, item in enumerate(encoding_format):
        # Check if the item does not start with "in:" and contains "."
        if not item.startswith("in:") and "." in item:
            return index

    # Return None if no matching item is found
    return None
  
def degrade_context_vectors(context_vectors, encoding_format, method_called_idx):
    degraded_matrix = []

    # Find the index range corresponding to the method called section
    method_called_section = encoding_format[method_called_idx:]

    for row in context_vectors:
        degraded_row = row.copy()

        # Iterate over the method called section
        for i in range(len(method_called_section)):
            if random.choice([True, False]):
                # Randomly decide to change half of the 1s to 0
                method_called_idx_in_row = i + method_called_idx
                if degraded_row[method_called_idx_in_row] == 1:
                    degraded_row[method_called_idx_in_row] = 0

        degraded_matrix.append(degraded_row)

    return degraded_matrix

def main():
  test_context_vectors = read_binary_matrix_from_csv("test_context_matrix.csv")
  test_encoding_format = read_text_file("test_encoding_format.txt")
  method_called_idx = get_method_called_idx(test_encoding_format)
  # print(test_context_vectors)
  # print(test_encoding_format)
  print(method_called_idx)
  test_context_vectors_degraded = degrade_context_vectors(test_context_vectors, test_encoding_format, method_called_idx)
  # print(len(test_context_vectors))
  # print(len(test_context_vectors_degraded))
  preprocess.save_matrix_to_file(test_context_vectors_degraded, "test_context_matrix_degraded.csv")
  
  pass

if __name__ == '__main__':
  main()
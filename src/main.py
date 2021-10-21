import parser as parser
from os import listdir
from os.path import isfile, join, splitext

################################################################
# Define a "demo.txt" with simple expressions in the src folder
################################################################

input_dir = "test_programs"
output_dir = "output"



java_programs = [file for file in listdir(input_dir) if isfile(join(input_dir, file)) and splitext(file)[1] in [".java", ".txt"]]

for input_file in java_programs:  
  input_path = join(input_dir, input_file)
  output_path = join(output_dir, f"{splitext(input_file)[0]}_tokens.txt")
  
  print(f"\nScanning {input_path}")

  text = open(input_path, "r+")
  result, error = parser.run(input_path, text.read())

  if error: 
    print(error.as_string())
    
  else: 
    print(f"Output > {output_path}\n")
    
    with open(output_path, "w+") as file:
      file.write(str(result))
from os import listdir
from os.path import isfile, join
import scanner

##########
# Define a "demo.txt" with simple expressions in the src folder
##########

input_dir = "JavaToPython/example_programs"
output_dir = "JavaToPython/output"

example_progs = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

for input_file in example_progs:  
  input_path = join(input_dir, input_file)
  output_path = join(output_dir, f"{input_file}_tokens.txt")

  text = open(input_path, "r+")
  result, error = scanner.run(input_path, text.read())

  print(f"\nReading from file path {input_path} ")
  if error: 
    print(error.as_string())
  else: 
    print(f"Output path -> {output_path}\n")
    with open(output_path, "w+") as file:
      file.write(str(result))
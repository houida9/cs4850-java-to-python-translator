import scanner
import os

##########
# Define a "demo.txt" with simple expressions in the src folder
##########

input_dir = "JavaToPython/example_programs"
output_dir = "JavaToPython/output"

input_name = "demo.txt"
input_path = os.path.join(input_dir, input_name)

output_name = f"{input_name}_tokens.txt"
output_path = os.path.join(output_dir, output_name)

text = open(input_path, "r+")
result, error = scanner.run(input_path, text.read())

print("Reading from file: " + input_path + "\n")
if error: 
  print(error.as_string())
else: 
  with open(output_path, "w+") as file:
    file.write(str(result))
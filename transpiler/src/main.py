from transpiler.src.scanner import run
from transpiler.src.scanner import Error
from os import listdir
from os.path import isfile, join, splitext
from pathlib import Path

################################################################
# Define a "demo_file.txt" with simple expressions in the src folder
################################################################


input_dir = Path("../test_programs").resolve()
output_dir = Path("../output").resolve()

java_programs = [file for file in listdir(input_dir)
                 if isfile(join(input_dir, file)) and splitext(file)[1] in [".java", ".txt"]]

for input_file in java_programs:
    try:
        input_path = join(input_dir, input_file)
        output_path = join(output_dir, f"{splitext(input_file)[0]}_tokens.txt")

        print(f"\nScanning {input_path}")

        text = open(input_path, "r+")
        result = run(input_path, text.read())  # scanner.run
        text.close()

    except Error as e:
        print(f"Error > {output_path}\n")
        print(e)
        with open(output_path, "w+") as file:
            file.write(str(e))
        continue

    else:
        print(f"Output > {output_path}\n")
        with open(output_path, "w+") as file:
            file.write(str(result))

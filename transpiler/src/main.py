from transpiler.src.translator import run
from transpiler.src.scanner import Error
from os import listdir, makedirs
from os.path import isfile, join, splitext, exists
from pathlib import Path

################################################################
# Define all of the Java files under transpiler/test_programs
################################################################

def run_java_files():
    import time
    timestr = time.strftime("%Y%m%d_%H%M%S")
    
    input_dir = Path("transpiler/test_programs").resolve()
    output_dir = Path(f"transpiler/output/translated_{timestr}").resolve()
    
    if not exists(output_dir):
        makedirs(output_dir)

    java_programs = [file for file in listdir(input_dir)
                    if isfile(join(input_dir, file)) and splitext(file)[1] in [".java", ".txt"]]

    for input_file in java_programs:
        try:
            input_path = join(input_dir, input_file)

            output_path = join(output_dir, f"{splitext(input_file)[0]}.py")

            # print(f"\nScanning {input_path}")

            text = open(input_path, "r+")
            
            # run the interpreter
            run(input_path, text.read(), output_path)
            text.close()

        except Error as e:
            print(f"Error > {output_path}\n")
            print(e)
            with open(output_path, "w+") as file:
                file.write(str(e))
            continue

        else:
            print(f"Output > {output_path}")
            
    print("\nCheck the transpiler/output directory for the translated file(s)\n")

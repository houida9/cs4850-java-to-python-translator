from django.shortcuts import render
from transpiler.src.translator import run
from transpiler.src.scanner import Error
from transpiler.src.main import run_java_files


def home(request):
    if request.method == 'POST':
        try:
            submitted = request.POST.get("translate")
            java_code = request.POST.get('javaTextArea', "")
            
            # run the demo files
            # comment out the line below to translate all of the Java programs under transpiler/test_programs
            # run_java_files()

            # run the interpreter
            import time
            timestr = time.strftime("%Y%m%d_%H%M%S")
            output_dir = f"transpiler/output/translated_{timestr}"
            output_file = f"transpiler/output/translated_{timestr}/front_end_output.py"
            
            from os.path import exists
            from os import makedirs
            if not exists(output_dir):
                makedirs(output_dir)
                
            run("front_end_java_input", java_code, output_file)
            
            
            python_code = ''
            with open(output_file) as file:
                for line in file:
                    python_code += line
                    
        except Error as error:
            return render(request, 'main.html',
                          {'python_code': str(error), 'java_code': str(java_code), 'submitted': submitted})
        except Exception as general_exception:
            return render(request, 'main.html',
                          {'python_code': general_exception, 'java_code': str(java_code), 'submitted': submitted})

        try:
            python_code = ''.join(str(e) if e != 'EOF' and e != '\r' else '' for e in python_code)

        except Exception as error:
            python_code = str(error)
        finally:
            return render(request, 'main.html',
                          {'python_code': str(python_code), 'java_code': str(java_code), 'submitted': submitted})

    return render(request, 'main.html')

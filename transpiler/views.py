from django.shortcuts import render
from transpiler.src.scanner import run
from transpiler.src.scanner import Error


def home(request):
    if request.method == 'POST':
        try:
            submitted = request.POST.get("translate")
            java_code = request.POST.get('javaTextArea', "")
            
            # run the interpreter
            run("filename", java_code)
            
            python_code = ''
            with open('transpiler/python_output/output.py') as file:
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

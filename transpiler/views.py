from django.shortcuts import render
from .src.scanner import run
from .src.scanner import Error


def home(request):
    if request.method == 'POST':
        try:
            submitted = request.POST.get("translate")
            java_code = request.POST.get('javaTextArea', "")

            python_code = run("filename", java_code)
            print("backend scanner run")
            print(python_code)
        except Error as error:
            return render(request, 'main.html',
                          {'python_code': str(error), 'java_code': str(java_code), 'submitted': submitted})
        except Exception as general_exception:
            return render(request, 'main.html',
                          {'python_code': general_exception, 'java_code': str(java_code), 'submitted': submitted})

        try:
            python_code = ''.join(str(e) if e != 'EOF' and e != '\r' else '' for e in python_code)

            print("Front end translation")
            print(python_code)
        except Exception as error:
            python_code = str(error)
        finally:
            return render(request, 'main.html',
                          {'python_code': str(python_code), 'java_code': str(java_code), 'submitted': submitted})

    return render(request, 'main.html')

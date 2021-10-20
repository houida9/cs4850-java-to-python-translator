from django.shortcuts import render
from .src.scanner import run

def home(request):
  if request.method == 'POST':
    submitted= request.POST.get("translate")
    java_code = request.POST.get('javaTextArea', "")
    python_code, error = run("filename", java_code)
    python_code = ''.join(str(e) for e in python_code)
    
    print(python_code)
    if error:
      python_code = error.as_string()
    return render(request, 'main.html', {'python_code': str(python_code), 'java_code': str(java_code), 'submitted': submitted})

  return render(request, 'main.html')
  

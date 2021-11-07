from django.shortcuts import render
from .src.scanner import run

def home(request):
  if request.method == 'POST':
    submitted= request.POST.get("translate")
    java_code = request.POST.get('javaTextArea', "")
    
    python_code, error = run("filename", java_code)
    print("backend scanner run")
    print(python_code)
    if error:
      return render(request, 'main.html', {'python_code': "ERROR", 'java_code': str(java_code), 'submitted': submitted})
    
    python_code = ''.join(str(e) if e != 'EOF' and e != '\r' else '' for e in python_code)
    
    print("Front end translation")
    print(python_code)
    if error:
      python_code = error.as_string()
    return render(request, 'main.html', {'python_code': str(python_code), 'java_code': str(java_code), 'submitted': submitted})

  return render(request, 'main.html')
  

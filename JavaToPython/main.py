import scanner

##########
# Define a "demo.txt" with simple expressions in the src folder
##########
text = open("demo.txt", "r")
result, error = scanner.run('demo.txt', text.read())

if error: print(error.as_string())
else: print(result)
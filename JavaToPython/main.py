import scanner

##########
# Define a "demo.txt" with simple expressions in the src folder
##########
fileName = "demo.txt"
text = open(fileName, "r")
result, error = scanner.run('demo.txt', text.read())

print("Reading from file: " + fileName + "\n")
if error: print(error.as_string())
else: print(result)
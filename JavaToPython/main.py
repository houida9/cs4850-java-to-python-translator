import scanner

##########
# Define a "demo.txt" with simple expressions in the src folder
##########
fileName = "demo2.txt"
text = open(fileName, "r")
result, error = scanner.run(fileName, text.read())

print("Reading from file: " + fileName + "\n")
if error: print(error.as_string())
else: print(result)
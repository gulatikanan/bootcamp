person = {'name': 'Alice'}

# EAFP: Just try it and handle the error if it occurs
try:
    print("Age:", person['age'])
except KeyError:
    print("Age key not found (EAFP)")

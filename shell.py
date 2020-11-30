import ProjectMorpheus
while True:
    text = input('Result > ')
    result, error = ProjectMorpheus.run(text)
    if error:print(error.log())
    elif result: print(result)
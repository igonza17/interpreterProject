import ProjectMorpheus3
while True:
    text = input('Result > ')
    result, error = ProjectMorpheus3.run(text)
    if error:print(error.log())
    elif result: print(result)
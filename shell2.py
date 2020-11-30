import ProjectMorpheus2
while True:
    text = input('Result > ')
    result, error = ProjectMorpheus2.run(text)
    if error:print(error.log())
    elif result: print(result)




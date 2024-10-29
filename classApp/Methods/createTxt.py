def createTXT(content, title = None):
    with open('output.txt', 'a') as f:
        if title:
            f.write(f'\n------------------------------------------{title}------------------------------------------')
        if isinstance(content, list):
            f.write('\n')
            for item in content:
                f.write(f'{item}\n')
        else:
            f.write('\n')
            f.write(content)
    
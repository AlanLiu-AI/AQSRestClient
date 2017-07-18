def print_file_before(file, separator):
    f = open(file)
    for line in f:
        if separator in line:
            break
        print(line)
    f.close()


def print_file_after(file, separator):
    f = open(file)
    found_separator = False
    for line in f:
        if separator in line:
            found_separator = True

        if found_separator:
            print(line)
    f.close()


def print_file_between(file, start_token, end_token):
    f = open(file)
    is_between = False
    for line in f:
        if end_token in line:
            is_between = False

        if is_between:
            print(line)

        if start_token in line:
            is_between = True
    f.close()


print_file_before('target/pom.tpl.xml', '<!--DEPENDENCIES BEGIN-->')
print_file_between('target/integration-test.xml', '<dependencies>', '</dependencies>')
print_file_after('target/pom.tpl.xml', '<!--DEPENDENCIES END-->')


def section_a():
    lst = []
    input_from_user = input("Enter a number (if you want to stop write stop): ")
    while input_from_user != "stop":
        input_from_user = int(input_from_user)
        lst.append(input_from_user)
        input_from_user = input("Enter a number (if you want to stop write stop): ")

    print(sum(lst))


def section_b():
    input_string = input("Enter list of numbers separated by comma: ")
    lst = [int(i) for i in input_string.split(",")]
    print(sum(lst))


def main():
    section_a()
    section_b()


if __name__ == '__main__':
    main()

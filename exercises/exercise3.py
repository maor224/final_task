def compress_string(string):

    letter = string[0]
    compressed_string = ""
    count_letter = 1

    for i in range(1, len(string)):
        if string[i] == letter:
            count_letter += 1
        else:
            compressed_string += letter + str(count_letter)
            count_letter = 1
            letter = string[i]

    compressed_string += letter + str(count_letter)

    return compressed_string


def main():
    string_to_compress = input("Enter the string you want to compress: ")
    print(compress_string(string_to_compress))

if __name__ == '__main__':
    main()
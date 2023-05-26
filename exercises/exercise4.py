def check_id(user_id):
    if user_id.isdigit():
        last_digit = int(user_id[-1])
        id_to_check = user_id[:-1]
        id_sum = 0

        for i in range(len(id_to_check)):
            if i % 2 == 0:
                id_sum += int(id_to_check[i])
            else:
                if int(id_to_check[i]) > 4:
                    res = int(id_to_check[i]) * 2
                    id_sum += (res % 10) + (res // 10 % 10)
                else:
                    id_sum += int(id_to_check[i]) * 2

        if id_sum % 10 >= 5:
            check_last_digit = (10 * ((id_sum // 10 % 10) + 1)) - id_sum
        else:
            check_last_digit = (10 * (id_sum // 10 % 10)) - id_sum

        return check_last_digit == last_digit

    else:
        return False


def main():
    id_number = input("Enter your id: ")
    if check_id(id_number):
        print("The id is legal")
    else:
        print("The id is illegal")


if __name__ == '__main__':
    main()

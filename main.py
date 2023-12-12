def compress(input_file):
    data_string = input_file.read()
    unique_symbols = list(set(data_string))
    unique_symbols.sort()

    dictionary = {elem: i for i, elem in enumerate(unique_symbols)}
    initial_dictionary = dict(dictionary)
    dictionary_size = len(dictionary)

    record_string = ""

    result_encode = []

    for symbol in data_string:
        new_string = record_string + symbol
        if new_string in dictionary:
            record_string = new_string
        else:
            result_encode.append(dictionary[record_string])
            dictionary[new_string] = dictionary_size
            dictionary_size += 1
            record_string = symbol

    if record_string:
        result_encode.append(dictionary[record_string])

    with open(f'{input_file.name.split(".")[0]}.lzw', 'w', encoding='utf-8') as file:
        for key in initial_dictionary:
            file.write(str(key) + '=' + str(dictionary[key]) + ', ')
        file.write('\n\n')
        for number in result_encode:
            file.write(str(number) + ' ')


def decompress(input_file):
    data = input_file.read().split('\n\n')
    dictionary_non_sorted = data[0].split(', ')[:-1]
    dictionary = {int(element.split('=')[-1]): element.split('=')[0] for element in dictionary_non_sorted}
    dictionary_size = len(dictionary)

    result_encode = [int(x) for x in data[-1].split()]

    result_decode = []
    first_code = int(result_encode.pop(0))
    result_decode.append(dictionary[first_code])

    for code in result_encode:
        if int(code) in dictionary:
            entry = dictionary[int(code)]
            result_decode.append(entry)
            dictionary[dictionary_size] = dictionary[first_code] + entry[0]
            dictionary_size += 1
            first_code = int(code)
        else:
            entry = dictionary[int(code - 1)][-1] * 2
            result_decode.append(entry)
            dictionary[dictionary_size] = dictionary[first_code] + entry[0]
            dictionary_size += 1
            first_code = int(code)

    result_decode = ''.join(result_decode)
    initial_data = open('text.txt', encoding='utf-8').read()
    if initial_data == result_decode:
        print('Архивация прошла успешно')
    else:
        print('Декодированный файл отличается от начального файла')


input_file_initial = open('text.txt', encoding='utf-8')
compress(input_file_initial)
input_file = open('text.lzw', encoding='utf-8')
decompress(input_file)
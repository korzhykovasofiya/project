from filemanager import read_file, write_file, FileError
from anonymizer1 import anonymize

input_path = input("Який файл анонімізувати? ").strip('"')
output_path = input("Куди зберегти результат? ").strip('"')

try:
    text = read_file(input_path)
    result = anonymize(text, {})
    write_file(result, output_path)
except FileError as e:
    print(e)
else:
    print("Готово! Результат збережено у", output_path)

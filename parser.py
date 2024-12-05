import re
import json

def parse_value(text):
    if text.isdigit():
        return int(text)
    elif text[0] == '(' and text[-1] == ')':
        return list(map(parse_value, text[1:-1].replace(' ', '').split(',')))
    elif text[0] == '$' and text[-1] == ']':
        items = re.findall(r'(\w+): (\(.*?\)|\d+|"[^"]*")', text[1:-1])
        return {name: parse_value(value) for name, value in items}
    elif text.startswith('"') and text.endswith('"'):
        return text[1:-1]  # Удаление кавычек для строк
    else:
        return text

def parse_constant(text):
    if text.startswith('@{') and text.endswith('}'):
        expression = text[2:-1]
        # Исправление синтаксиса для max и sort
        expression = expression.replace('max(', 'max(').replace('sort(', 'sorted(')
        result = eval(expression)
        return result
    return text

def parse_file(input_path, output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_dict = data
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('var '):
            var_name, var_value = line[4:].split(' = ')
            current_dict[var_name.strip()] = parse_value(var_value.strip())
        else:
            key, value = line.split(' = ')
            current_dict[key.strip()] = parse_constant(value.strip())

    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python parser.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parse_file(input_file, output_file)
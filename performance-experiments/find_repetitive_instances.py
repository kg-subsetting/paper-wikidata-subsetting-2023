import sys

def find_repetitive_lines(filename):
    with open(filename, 'r') as file:
        contents = file.read()

    lines = contents.splitlines()
    line_count = {}
    repetitions = 0
    distinct_count = 0

    for line in lines:
        if line in line_count:
            line_count[line] += 1
            repetitions += 1
        else:
            line_count[line] = 1
            distinct_count += 1

    repetitive_lines = [line for line, count in line_count.items() if count > 1]

    return repetitive_lines, repetitions, distinct_count


filename = sys.argv[1]
repetitive_lines, repetitions, distinct_count = find_repetitive_lines(filename)

if repetitive_lines:
    print("Repetitive lines found:")
    for line in repetitive_lines:
        print(line)

print(f"Total number of repetitions: {repetitions}")
print(f"Total distinct lines: {distinct_count}")


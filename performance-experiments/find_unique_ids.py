import sys

def get_unique_items(file1, file2):
    with open(file1, 'r') as f1:
        items1 = f1.read().splitlines()

    with open(file2, 'r') as f2:
        items2 = f2.read().splitlines()

    set1 = set(items1)
    set2 = set(items2)

    unique_items_file1 = list(set1 - set2)
    unique_items_file2 = list(set2 - set1)

    return unique_items_file1, unique_items_file2

def write_items_to_file(items, output_file):
    with open(output_file, 'w') as f:
        for item in items:
            f.write(item + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python program.py <file1> <file2> <output_prefix>')
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_prefix = sys.argv[3]

    output_file1 = output_prefix + '_unique_items_file1.txt'
    output_file2 = output_prefix + '_unique_items_file2.txt'

    unique_items1, unique_items2 = get_unique_items(file1, file2)

    write_items_to_file(unique_items1, output_file1)
    write_items_to_file(unique_items2, output_file2)

    print('Unique items written to files:')
    print('\t',output_file1)
    print('\t',output_file2)

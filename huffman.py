import ordered_list
import huffman_bit_writer
import huffman_bit_reader


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # stored as an integer - the ASCII character code value
        self.freq = freq  # the freqency associated with the node
        self.left = None  # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if type(self) == type(other) and self.freq == other.freq and self.char == other.char:
            return True
        else:
            return False

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        elif self.freq > other.freq:
            return False
        elif self.freq == other.freq:
            if self.char > other.char:
                return False
            else:
                return True


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    asciilist = [0] * 256
    f = open(filename, "r")
    for line in f:
        for char in line:
            asciilist[ord(char)] += 1
    f.close()
    return asciilist


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    huff_node = ordered_list.OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            huff_node.add(HuffmanNode(i, char_freq[i]))
    if huff_node.size() == 0:
        return None
    elif huff_node.size() == 1:
        huff_tree = huff_node.pop(0)
        return huff_tree
    while huff_node.size() > 1:
        left_node = huff_node.pop(0)
        right_node = huff_node.pop(0)
        new_node = HuffmanNode(min(left_node.char, right_node.char), left_node.freq + right_node.freq)
        new_node.left = left_node
        new_node.right = right_node
        huff_node.add(new_node)
    return huff_node.pop(0)


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    array = [''] * 256
    code = ''
    return helper_code(array, code, node)


def helper_code(array, code, node):
    empty_string = ''
    x = '0'
    y = '1'
    if node is None:
        return empty_string
    elif node.left is None and node.right is None:
        array[node.char] = code
    else:
        helper_code(array, code + x, node.left)
        helper_code(array, code + y, node.right)
    return array


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    # header = ascii + freq
    header = ''
    for i in range(len(freqs)):
        if freqs[i] != 0:
            ascii = str(i)
            header += ascii + ' ' + str(freqs[i]) + ' '
    return header[0:-1]


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    f = open(in_file)
    out = open(out_file, 'w')
    x = cnt_freq(in_file)
    node = create_huff_tree(x)
    code = create_code(node)
    header = create_header(x)
    header = header + '\n'
    split = out_file.split(".")
    new = split[0] + '_compressed.' + split[1]
    writer = huffman_bit_writer.HuffmanBitWriter(new)
    writer.write_str(header)
    out.write(header)
    for x in f.read():
        writer.write_code(code[ord(x)])
        out.write(code[ord(x)])
    f.close()
    out.close()
    writer.close()


def huffman_decode(encoded_file, decoded_file):
    try:
        file = huffman_bit_reader.HuffmanBitReader(encoded_file)
    except FileNotFoundError:
        raise FileNotFoundError
    out = open(decoded_file, 'w')
    read = file.read_str()
    tree = create_huff_tree(parse_header(read))
    code = ''
    if tree is None:
        file.close()
        return
    while tree.freq > len(code):
        code += helper_decord(file, tree)
    out.write(code)
    file.close()
    out.close()


def helper_decord(file, node):
    if node.left is None and node.right is None:
        return chr(node.char)
    elif file.read_bit() is False:
        return helper_decord(file, node.left)
    else:
        return helper_decord(file, node.right)


def parse_header(header_string):
    list = [0] * 256
    head_list = header_string.split()
    for n in range(0, len(head_list), 2):
        list[int(head_list[n])] = int(head_list[n + 1])
    return list
#script for finding matching symbols between files
import argparse

def load_symbols(file_path):
    symbols = {}
    with open(file_path, 'r') as f:
        for line in f:
            if '=' in line:
                symbol_name = line.split('=')[0].strip()
                symbols[symbol_name] = line.strip()
    return symbols

def find_matching_symbols(input_sym, reference_sym, output_file):
    """Find and save matching symbols between input and reference .sym files."""
    input_symbols = load_symbols(input_sym)
    reference_symbols = load_symbols(reference_sym)
    
    matched_symbols = [reference_symbols[symbol] for symbol in input_symbols if symbol in reference_symbols]
    missing_symbols = [symbol for symbol in input_symbols if symbol not in reference_symbols]
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(matched_symbols) + '\n')
        f.write('\n# Missing Symbols\n')
        f.write('\n'.join(missing_symbols) + '\n')
    
    print(f"Results saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find matching symbols in a reference .sym file.')
    
    parser.add_argument('reference_sym', help='Path to the main .sym file')
    parser.add_argument('input_sym', help='Path to the ref .sym file')
    parser.add_argument('output_file', help='Path to save the output file')
    
    args = parser.parse_args()
    find_matching_symbols(args.input_sym, args.reference_sym, args.output_file)

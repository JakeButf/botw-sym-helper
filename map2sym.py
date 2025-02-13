#credits to https://github.com/fruityloops1/zeldar/blob/master/scripts/convertMapToSym.py
#i just cleaned the script up

import argparse

symbol_matchers = ["", "_ZN", "_ZNK", "_ZTVN"]

def convert_map_to_sym(map_file_path, sym_file_path, symbol_filter=None, start_name="__main_start"):
    sym_entries = []
    
    with open(map_file_path, 'r') as map_file:
        lines = map_file.readlines()
        
        # Find the start of the symbol table
        try:
            start_index = next(i for i, line in enumerate(lines) if 'Address         Publics by Value' in line) + 2
        except StopIteration:
            print("Error: Symbol table not found in the map file.")
            return
        
        # Parse symbol entries
        for line in lines[start_index:]:
            line = line.strip()
            if not line:
                break
            
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            
            address, symbol = parts
            
            if not address.startswith('00000000:00000071'): # Filter out unimportant addresses
                continue;

            address = address.replace('00000000:00000071', '0x')
            
            if symbol_filter:
                for matcher in symbol_matchers:
                    filt = f'{matcher}{len(symbol_filter)}{symbol_filter}'
                    if symbol.startswith(filt):
                        if not symbol.endswith("_0"):  # Exclude exported nn defs
                            sym_entries.append(f'{symbol} = {start_name} + {address};')
                        break
            else:
                if not symbol.endswith("_0"):  # Exclude exported nn defs
                    sym_entries.append(f'{symbol} = {start_name} + {address};')
    
    # Write output file
    with open(sym_file_path, 'w') as sym_file:
        sym_file.write('\n'.join(sym_entries) + '\n')
    
    print(f"Symbol file saved as {sym_file_path}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a map file to a sym file.')
    parser.add_argument('input', help='Path to the input map file')
    parser.add_argument('output', help='Path to the output sym file')
    parser.add_argument('-f', '--filter', dest='symbol_filter', help='Filter symbols by prefix')
    parser.add_argument('-s', '--start', dest='start_name', default='__main_start', help='Use something other than __main_start')
    
    args = parser.parse_args()
    convert_map_to_sym(args.input, args.output, args.symbol_filter, args.start_name)
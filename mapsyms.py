#How to use:
# python mapsyms.py main.csv sdk.csv subsdk0.csv --output botw16.map <- will map all symbols
# python mapsyms.py main.csv sdk.csv subsdk0.csv --filter Function --output botw16.map <- will map just function symbols

import pandas as pd
import argparse

def load_symbols(file_paths):
    symbol_map = {}
    address_map = {}
    preferred_prefixes = ("_ZN", "_ZNK", "_ZTVN")
    
    for file in file_paths:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            name, location, sym_type = row['Name'], row['Location'], row['Type']
            
            if location == "External[ ? ]":
                location = None
            
            if location:
                if location in address_map:
                    existing_name = address_map[location]
                    if existing_name.startswith(preferred_prefixes) and not name.startswith(preferred_prefixes):
                        continue
                    elif name.startswith(preferred_prefixes) and not existing_name.startswith(preferred_prefixes):
                        address_map[location] = name
                        symbol_map[name] = (location, sym_type)
                    else:
                        symbol_map[name] = (location, sym_type)
                else:
                    address_map[location] = name
                    symbol_map[name] = (location, sym_type)
            elif name not in symbol_map:
                symbol_map[name] = (None, sym_type)
    
    return symbol_map

def filter_symbols(symbol_map, filter_type):
    if filter_type:
        return {k: v for k, v in symbol_map.items() if v[1] == filter_type}
    return symbol_map

def write_mem_regions(): #hard coding in mem regions. this is acquired from ghidramapexport.py which you can find in this repo
    f.write(" Start         Length     Name                   Class")
    f.write(" 0000:0000007100000000 0000000002127F90H .text                    CODE")
    f.write(" 0000:0000007102127F90 0000000000001AD0H .plt                     CONST")
    f.write(" 0000:0000007102129A60 0000000000000144H .text.1                  CODE")
    f.write(" 0000:000000710212A000 0000000000000050H .rodata                  CONST")
    f.write(" 0000:000000710212A050 00000000004D7720H .rela.dyn                CONST")
    f.write(" 0000:0000007102601770 0000000000002838H .rela.plt                CONST")
    f.write(" 0000:0000007102603FA8 0000000000000F08H .hash                    CONST")
    f.write(" 0000:0000007102604EB0 0000000000000098H .gnu.hash                CONST")
    f.write(" 0000:0000007102604F48 0000000000002D00H .dynsym                  CONST")
    f.write(" 0000:0000007102607C48 0000000000005446H .dynstr                  CONST")
    f.write(" 0000:000000710260D08E 000000000045FD3AH .rodata.1                CONST")
    f.write(" 0000:0000007102A6D000 0000000000211A78H .data                    DATA")
    f.write(" 0000:0000007102C7EA78 0000000000000180H .dynamic                 DATA")
    f.write(" 0000:0000007102C7EBF8 0000000000000D80H .got.plt                 CONST")
    f.write(" 0000:0000007102C7F978 0000000000008468H .got                     CONST")
    f.write(" 0000:0000007102C87DE0 0000000000001F88H .init_array              CONST")
    f.write(" 0000:0000007102C89E00 00000000000DBE80H .bss                     DATA")
    f.write(" 0000:0000007102D66008 0000000000000E50H EXTERNAL                 DATA")

def write_map_file(symbol_map, output_file):
    with open(output_file, 'w') as f:
        f.write("  Address         Publics by Value\n\n")
        for name, (location, sym_type) in sorted(symbol_map.items(), key=lambda x: x[1][0] or "ZZZ"):
            if location:
                formatted_location = f"00000000:000000{location.upper()}" #format address
                f.write(f" {formatted_location}       {name}\n")

def main():
    parser = argparse.ArgumentParser(description='Convert multiple CSV symbol tables into a .map file.')
    parser.add_argument('csv_files', nargs='+', help='CSV files to process')
    parser.add_argument('--filter', type=str, help='Filter symbols by type (e.g., Function)')
    parser.add_argument('--output', type=str, default='output.map', help='Output map file')
    args = parser.parse_args()
    
    symbol_map = load_symbols(args.csv_files)
    symbol_map = filter_symbols(symbol_map, args.filter)
    write_map_file(symbol_map, args.output)
    print(f"Map file '{args.output}' generated successfully.")

if __name__ == "__main__":
    main()


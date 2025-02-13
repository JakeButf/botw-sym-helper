#script to filter through .sym file and move stubs to another file
#assumes ghidra default prefixes
import os
import sys

def process_sym_file(sym_file_path):
    if not os.path.isfile(sym_file_path):
        print(f"Error: File '{sym_file_path}' not found.")
        return

    base_filename = os.path.splitext(os.path.basename(sym_file_path))[0]
    stubs_filename = f"{base_filename}-stubs.sym"

    with open(sym_file_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    stub_lines = [line for line in lines if line.startswith(("DAT_", "FUN_", "LAB_", "switchD", "caseD"))]
    non_stub_lines = [line for line in lines if not line.startswith(("DAT_", "FUN_", "LAB_", "switchD", "caseD"))]

    with open(stubs_filename, "w", encoding="utf-8") as stub_file:
        stub_file.writelines(stub_lines)

    with open(sym_file_path, "w", encoding="utf-8") as original_file:
        original_file.writelines(non_stub_lines)

    print(f"Stubs extracted to: {stubs_filename}")
    print(f"Original file updated, stubs removed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.sym>")
    else:
        process_sym_file(sys.argv[1])

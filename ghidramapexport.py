#FOR USE IN GHIDRA ONLY!!!
#Import this script into the ghidra script manager and run it

#this will create a map file of the symbols, including the memory regions at the top
from ghidra.program.model.symbol import SymbolType
from ghidra.program.model.listing import Program

output_file = r"C:\Users\jacob\Documents\botwdump.map"  # Change this path as needed

with open(output_file, "w") as f:
    
    ### MEMORY REGIONS HEADER ###
    f.write(" Start         Length     Name                   Class\n")
    
    print("Getting memory regions...")
    memory = currentProgram.getMemory()
    blocks = memory.getBlocks()
    
    for block in blocks:
        start_addr = block.getStart().getOffset()
        length = block.getSize()
        name = block.getName()
        
        # Weirdly .plt returns as CONST. In a TOTK example it returns as CODE. Not sure why
        if block.isExecute():
            section_class = "CODE"
        elif block.isRead() and not block.isWrite():
            section_class = "CONST"
        elif block.isWrite():
            section_class = "DATA"
        else:
            section_class = "BSS"
        
        f.write(" 0000:{:016X} {:016X}H {:<24} {}\n".format(start_addr, length, name, section_class))

    print("Getting symbols...")
    f.write("\n\n  Address         Publics by Value\n\n")
    
    sym_table = currentProgram.getSymbolTable()
    symbols = sym_table.getAllSymbols(True)
    
    for sym in symbols:
        if sym.getSymbolType() in [SymbolType.FUNCTION, SymbolType.LABEL]:
            address = sym.getAddress()
            name = sym.getName()
            formatted_address = "00000000:000000{:012X}".format(address.getOffset())
            f.write(" {}       {}\n".format(formatted_address, name))

print("Successfully exported to:", output_file)

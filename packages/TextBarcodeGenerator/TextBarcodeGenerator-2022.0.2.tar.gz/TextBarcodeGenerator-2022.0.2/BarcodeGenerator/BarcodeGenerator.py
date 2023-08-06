"""Generate barcodes!!!"""

CODES = {
    "*": "█  █ ██ ██ █ ",
    "0": "█ █  ██ ██ █ ",
    "1": "██ █  █ █ ██ ",
    "2": "█ ██  █ █ ██ ",
    "3": "██ ██  █ █ █ ",
    "4": "█ █  ██ █ ██ ",
    "5": "██ █  ██ █ █ ",
    "6": "█ ██  ██ █ █ ",
    "7": "█ █  █ ██ ██ ",
    "8": "██ █  █ ██ █ ",
    "9": "█ ██  █ ██ █ ",
}


def generate_barcode(code: any) -> str:
    """Generate a barcode for a given code."""
    barcode = CODES["*"]
    for char in str(code):
        barcode += CODES[char]
    barcode += CODES["*"]
    barcode += "\n" + barcode + "\n" + barcode + "\n" + barcode + "\n" + \
               barcode + "\n" + barcode + "\n" + barcode + "\n" + barcode
    return barcode

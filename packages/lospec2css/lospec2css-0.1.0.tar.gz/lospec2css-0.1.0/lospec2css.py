from sys import argv


# lospec2css is a simple script to convert a downloaded lospec color palette
# into a CSS file with each color set as a variable. You will have to manually
# name the colors, unfortunately.
#
# You can download the file needed from a specific palette page. Under the
# "Download" section, click the "HEX File" option. This will be your input file.
#
# Usage:
#   python lospec2css.py input.txt output.css
def main(input: str, output: str):
    # If the input file extension wasn't provided, we can add it.
    if not input.endswith(".hex"):
        input += ".hex"

        # Convert the hex values into a list of CSS property-value pairs.
    with open(input, 'r') as file:
        palette = file.read().splitlines()
        colors = [f"    --color-{i}: #{color};" for i, color in enumerate(palette)]

    # If the output file extension wasn't provided, we can add it.
    if not output.endswith(".css"):
        output += ".css"

    # Write out to a .css file. The user can then copy & paste the content into
    # their own file, or just use the file itself.
    with open(output, 'w') as file:
        file.write(":root {\n")
        file.write("\n".join(colors))
        file.write("\n}")

    print("Complete! ✨")



if __name__ == "__main__":
    if argv[1] == "-h" or argv[1] == "--help" or len(argv) != 3:
        print("Usage: css-paint.py <palette file> <output file>")

    main(argv[1], argv[2])
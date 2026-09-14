#CAVA
import subprocess
import sys
import threading

# ================ PARAMETERS ===================

scaling = "manual"    # Auto scales width of bars (in characters). Mode: auto/manual

# // Output range, unit in characteres //
height = 8
width = 40          #IGNORED IN MANUAL

# //        Shadow properties         //
shadow = False       #Create an after-image of the bar

# //                                  //
bars = 32           #IGNORED IN AUTO
thickness = 2       # Bar thickness
spacing = 0         # In character, space between each bar
font = "angled_top"      # Add fonts below, heights ranging from low to high

# =================== FONT =====================

fonts = {
"block":["⠀","▁","▂","▃","▄","▅","▆","▇","█"], #Pretty choppy and unstyalized, original cava would be better
"dot":["⠀",".",".",".",":",":",":","⋮","⋮","⋮"], #Preferrably 32 bars manual
"angled_top":["⠀","/","/","/","/","/","/","/","/","⋮"], #Preferrably 2 bar thickness
"hollow":["⋮","⋮","⋮",":",":",":","⠀"] #I don't like this
}

# ==============================================

# --- Verify font
inifont = font
for f in fonts.keys():
    if font == f:
        font = fonts[f]

if font == inifont:
    print("Error: No font chosen")
    sys.exit()

# --- Bars info
size = thickness + spacing
spaces = 0
if scaling == "auto":
    bars = width // size
    bars += (width) // thickness # --- adds another bar if another bar can be fit in the overflow
elif scaling == "manual":
    spaces = bars - 1
else:
    print("Error: Invalid scaling mode")
    sys.exit()

datarange = 128 // bars # --- range of data to calc avg
bheight = 255 / (height * (len(font) - 1)) # --- height of bits/character
fullheight = 75 / height

# --- Command process
proc = subprocess.Popen("cava", stdout=subprocess.PIPE)
for line in proc.stdout:
    # --- returns bars heights as an array

    set = line.decode()
    strheights = set.split(";")
    strheights.pop(-1)
    heights = [int(i) for i in strheights]

    # --- height medium for n bars

    medium = []
    for i in range(0,128,datarange):
        total = sum(heights[i : i + datarange])
        avg = total/datarange
        medium.append(avg / bheight)
    #print(height)
    #print(bheight)
    #print(medium)

    # --- Output processing

    output = []     #The output
    #print(shade)
    for i in range(height):
        string = ""
        for b in range(bars):
            if medium[b] >= fullheight * (i + 1):       # - if height exceeds character height, use the brightest character
                string += font[-1] * thickness
            elif medium[b] - fullheight * i >= 0:       # - if height is within the character range, use characters depending on height
                overflow = medium[b] - fullheight * i
                char = int(overflow / bheight)
                string += font[char] * thickness
            else:                                       # - if height is not in range, use blank. If shadow is enabled, blank will be swapped with the secondary layer
                string += font[0] * thickness
        output.insert(0,string)

    print("\n".join(output))
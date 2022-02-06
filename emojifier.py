from PIL import Image
from math import sqrt
from glob import glob

#prints a simple one line progress bar (argument [0.0 -> 1.0])
def progress(progress): #progress [0.0 -> 1.0]
    barLength = 50 
    pos = progress*barLength
    print( f"Progress: [{'#'*int(pos)}{'-'*(barLength-int(pos))}]  {int(progress * 100)} %", end='\r') 

#returns the distance between two 3D points (used to get the most similar emoji color in the <os>.txt file to current pixel)
def dist(x,y,z,x1,y1,z1): 
    return sqrt( (x-x1)**2 + (y-y1)**2 + (z-z1)**2 )
    
def main():
    #Prints all the files available in the folder images and asks for input which one to convert
    path     = "images/"
    os_emoji = "windows"
    for idx, file in enumerate(glob(f"{path}*")):
        print(f"{idx}. {file[7:]}")   
    name = glob(f"{path}*") [int(input("\nSelect image to convert: "))] [7:]

    #Loads the image and resizes it according to input (input is width "col")
    img_raw = Image.open(f"{path}{name}").convert("RGB")
    width     = int(input("Input image size: "))
    img_raw = img_raw.resize( (width, int(img_raw.size[1] / (img_raw.size[0] / width))) )
    #loads image pixels to pix and creates a 2d list img containing pixels
    pix     = img_raw.load()
    width   = img_raw.size[0]
    height  = img_raw.size[1]
    img     = [[pix[x, y] for x in range(width)] for y in range(height)]

    #Opens the html result file and prints the heading for "utf-8" and "black background"
    out = open(f"{name.split('.')[0]}.html", "w")
    out.write('<meta charset="UTF-8">\n')
    out.write('<body style="background-color:black;">\n')

    #Saves data from file in a dictionary {"name.png", [r,g,b], "&#xUNICODE"}
    with open(f"data\{os_emoji}.txt", "r") as inp:
        data = {line.split(":")[0] : (list(map(int, line.split(":")[1].split(","))), line.split(":")[2][:-1]) for line in inp}
    rgb = list(data.values()) #turns rgb values in a list from dictionary data

    #Iterates through the image pixel by pixel from top to bottom
    print(f"\nConverting image: {name}")
    for count, row in enumerate(img):
        progress((count+1)/height)
        for item in row:
            distances = [dist(item[0], item[1], item[2], rgb[i][0][0], rgb[i][0][1], rgb[i][0][2]) for i in range(len(rgb))]
            out.write(rgb[distances.index(min(distances))][1])
        out.write("<br>")
    print("\nDone")

if __name__ == '__main__':
    main()

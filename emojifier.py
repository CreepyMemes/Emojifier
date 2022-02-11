from PIL import Image
from math import sqrt
from glob import glob

#prints a simple one line progress bar (argument [0.0 -> 1.0])
def progress(progress): #progress [0.0 -> 1.0]
    barLen = 50 
    pos    = progress*barLen
    print( f"Progress: [{'#'*int(pos)}{'-'*(barLen-int(pos))}]  {int(progress * 100)} %", end='\r')

#returns the distance between two 3D points (used to get the most similar emoji color in the <os>.txt file to current pixel)
def dist(p1, p2): 
    return sqrt( sum((a-b)**2 for a,b in zip(p1, p2)) ) #sqrt( (x-x1)**2 + (y-y1)**2 + (z-z1)**2 )
      
def main():
    #Prints all the files available in the folder images and asks for input which one to convert
    path     = "images/"
    os_emoji = "windows"
    for idx, file in enumerate(glob(f"{path}*")):
        print(f"{idx}. {file[7:]}")   
    name = glob(f"{path}*") [int(input("\nSelect image to convert: "))] [7:]

    #Loads the image and resizes it according to input (input is width "col")
    img   = Image.open(f"{path}{name}").convert("RGB")
    width = int(input("Input image size: "))
    img   = img.resize( (width, int(img.size[1] / (img.size[0]/width))) )

    #Loads image pixels to imgPix and creates a 2d list containing pixels
    width, height   = img.size
    imgPix          = img.load() 
    imgPix          = [[imgPix[x, y] for x in range(width)] for y in range(height)]
    
    #Opens the html result file and prints the heading for "utf-8" and "black background"
    out = open(f"{name.split('.')[0]}.html", "w")
    out.write('<meta charset="UTF-8">\n')
    out.write('<body style="background-color:black;">\n')

    #Saves data from file in a dictionary {"name.png", [r,g,b], "&#xUNICODE"}
    with open(f"data\{os_emoji}.txt", "r") as inp:
        data = {line.split(":")[0] : (tuple(map(int, line.split(":")[1].split(","))), line.split(":")[2][:-1]) for line in inp}
    rgb = list(data.values()) #turns rgb values in a list from dictionary data

    #Iterates through the image pixel by pixel from top to bottom
    print(f"\nConverting image: {name}")
    for count, row in enumerate(imgPix):
        progress((count+1)/height)
        for pixel in row:
            distances = [ dist(pixel, rgb[i][0]) for i in range(len(rgb)) ]
            out.write(rgb[distances.index(min(distances))][1])
        out.write("<br>")   

    print("\nDone")

if __name__ == '__main__':
    main()

#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <filesystem>
//including @nothings's image processing libraries https://github.com/nothings/stb
#define STB_IMAGE_IMPLEMENTATION
#include "lib/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "lib/stb_image_write.h"
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "lib/stb_image_resize.h"
namespace fs = std::filesystem; //this only works in C++17 or higher
using namespace std;

//gets the n substring from s split by c ex: s = "a.b.c" -> getSubstr(s, '.', 1) = "b"
string getSubstr(string s, char c, int n){
    string r{}; int count{};
    for(char i: s){
        if(i==c)     {count++; continue;}
        if(count==n) {r+=i;}
    }
    return r;
}
//prints a simple one line progress bar (argument [0.0 -> 1.0])
void progress(double progress){
    int barLength = 50, pos = progress*barLength;
    cout << "Progress: [";
    for(int i = 0; i < barLength; i++){
        if(i < pos) cout << "#";
        else        cout << "-";
    }
    cout << "]  " << int(progress * 100.0) << " %\r";
}
//returns the distance between two 3D points (used to get the most similar emoji color in the <os>.txt file to current pixel)
int dist (int x,int y,int z,int x1,int y1,int z1){
    return sqrt((x-x1)*(x-x1) + (y-y1)*(y-y1) + (z-z1)*(z-z1));
}
string getImg (string s)         {return getSubstr(s, ':', 0);}
int    getRgb (string s, char c) {return stoi(getSubstr(getSubstr(s, ':', 1), ',', c));}
string getCod (string s)         {return getSubstr(s, ':', 2);}
string getName(string s)         {return getSubstr(s, '.', 0);}

int main(){
    //Prints all the files available in the folder images and asks for input which one to convert
    string path = "images", files[1000]{};
    int found{};
    for (const auto &entry: fs::directory_iterator(path)) {
        string file = entry.path().string().erase(0,7); //.string() converts to string .erase(0,7) deletes first 7 character from string
        cout << found << ". " << file << "\n";    
        files[found++] = file;
    }
    cout << "\nSelect image to convert: "; int sel;    cin >> sel;
    cout << "Input image size: ";          int rwidth; cin >> rwidth;

    //loads the image
    int width, height, channels;
    unsigned char *img = stbi_load( ("images\\" + files[sel]).c_str() , &width, &height, &channels, 0);
    if(img == NULL) {cout << "Error in loading the image\n"; exit(1);}
    //resizes the image
    int rheight = float(height)/(float(width)/float(rwidth));
    stbir_resize_uint8(img , width , height , 0, img, rwidth, rheight, 0, channels);
    
    //Opens the data file and the html result file printing the heading and "utf-8" with "black background"
    ifstream in("data\\windows.txt");
    ofstream out(getName(files[sel])+".html"); out<<"<meta charset=\"UTF-8\">\n<body style=\"background-color:black;\">\n";

    //declares data variables
    int tot = 4000; //max emojis available in .txt file
    string name[tot]{};
    int    r[tot]{},g[tot]{},b[tot]{};
    string cod[tot]{};

    //iterates through the txt file line by line asigning the data variables
    string line; 
    for(int i=0; getline(in, line); tot=i++){
	name[i] = getImg(line);
        r[i]    = getRgb(line, 0);
        g[i]    = getRgb(line, 1);
        b[i]    = getRgb(line, 2);
        cod[i]  = getCod(line);
    }
	
    //iterates through the image pixel by pixel while calculating the most similar emoji per current pixel
    cout << "\nConverting image: " << files[sel] << "\n";
    size_t img_size = rwidth * rheight * channels, i{}, count{};
    for(unsigned char *p = img; p != img+img_size; p += channels){
        int dmin = 1000, imin{};
        for(int j=0; j<tot; j++){
            int temp = dist(*p, *(p+1), *(p+2), r[j], g[j], b[j]);
            if(dmin > temp){
                dmin = temp;
                imin = j;
            }
        }     
        out<<cod[imin];
        if(++i==rwidth) {out << "<br>"; progress(double(++count)/double(rheight)); i=0;}
    }
    stbi_image_free(img);
    cout<<"\nDone\n";
}

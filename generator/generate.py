import urllib.request
import zipfile
import os
import shutil

joinpath = os.path.join

def make_dir( path ):
	if not os.path.exists( path ):
		os.makedirs( path  )

raylib_url             = "https://github.com/raysan5/raylib/releases/download/3.0.0/raylib-3.0.0-Win64-msvc15.zip"
raylib_zip_name        = os.path.basename(raylib_url)
raylib_zip_folder_name = os.path.splitext(raylib_zip_name)[0]

#download to file
response = urllib.request.urlopen(raylib_url)
file_data = response.read()
with open( raylib_zip_name , 'wb') as f:
	f.write( file_data )

#unzip to path
with zipfile.ZipFile(raylib_zip_name, 'r') as zip_ref:
    zip_ref.extractall('raylib')


raylib_h   = joinpath( "raylib", raylib_zip_folder_name , "include" , "raylib.h" )
raylib_lib = joinpath( "raylib", raylib_zip_folder_name , "lib" , "raylib.lib" )
raylib_dll = joinpath( "raylib", raylib_zip_folder_name , "bin" , "raylib.dll" )

# generate precompiled raylib headers
os.system('cat {} | grep -v "#include " | gcc -E - -o - | grep -v "# " > raylib.h'.format(raylib_h))

# odin bindgen failed at multiple var declaration
# hack to solve this until the bug is fixed!
# https://github.com/Breush/odin-binding-generator/issues/13

file = open("raylib.h",'r')
text = file.read()
file.close()

text = text.replace("float m0, m4, m8, m12;", "float m0; float m4; float m8; float m12;") \
.replace("float m1, m5, m9, m13;", "float m1; float m5; float m9; float m13;") \
.replace("float m2, m6, m10, m14;", "float m2; float m6; float m10; float m14;") \
.replace("float m3, m7, m11, m15;", "float m3; float m7; float m11; float m15;")

file = open("raylib.h",'w+')
file.write(text);
file.close()

# call odin binding generator
os.system("odin run odin_bindgen.odin")

# add the missing colors from the bindings

file = open("raylib.odin",'a')
text = file.write("""
LIGHTGRAY	:: Color{ 200, 200, 200, 255 };   // Light Gray
GRAY		:: Color{ 130, 130, 130, 255 };   // Gray
DARKGRAY	:: Color{ 80, 80, 80, 255 };      // Dark Gray
YELLOW		:: Color{ 253, 249, 0, 255 };     // Yellow
GOLD		:: Color{ 255, 203, 0, 255 };     // Gold
ORANGE		:: Color{ 255, 161, 0, 255 };     // Orange
PINK		:: Color{ 255, 109, 194, 255 };   // Pink
RED			:: Color{ 230, 41, 55, 255 };     // Red
MAROON		:: Color{ 190, 33, 55, 255 };     // Maroon
GREEN		:: Color{ 0, 228, 48, 255 };      // Green
LIME		:: Color{ 0, 158, 47, 255 };      // Lime
DARKGREEN	:: Color{ 0, 117, 44, 255 };      // Dark Green
SKYBLUE		:: Color{ 102, 191, 255, 255 };   // Sky Blue
BLUE		:: Color{ 0, 121, 241, 255 };     // Blue
DARKBLUE	:: Color{ 0, 82, 172, 255 };      // Dark Blue
PURPLE		:: Color{ 200, 122, 255, 255 };   // Purple
VIOLET		:: Color{ 135, 60, 190, 255 };    // Violet
DARKPURPLE	:: Color{ 112, 31, 126, 255 };    // Dark Purple
BEIGE		:: Color{ 211, 176, 131, 255 };   // Beige
BROWN		:: Color{ 127, 106, 79, 255 };    // Brown
DARKBROWN	:: Color{ 76, 63, 47, 255 };      // Dark Brown

WHITE		:: Color{ 255, 255, 255, 255 };   // White
BLACK		:: Color{ 0, 0, 0, 255 };         // Black
BLANK		:: Color{ 0, 0, 0, 0 };           // Blank (Transparent)
MAGENTA		:: Color{ 255, 0, 255, 255 };     // Magenta
RAYWHITE	:: Color{ 245, 245, 245, 255 };   // My own White (raylib logo)
""")
file.close()

# TODO: there is a function with va_list that odin bindgen can´t handle.

# move results to template path

if os.path.exists( joinpath("../","template" ) ):
	shutil.rmtree( joinpath("../","template" ) )

make_dir( joinpath("../", "template", "src", "raylib") )
make_dir( joinpath("../", "template", "lib") )
make_dir( joinpath("../", "template", "bin") )


shutil.move( "raylib.odin", joinpath("../", "template", "src", "raylib", "raylib.odin") ) 
shutil.move( raylib_lib,    joinpath("../", "template", "lib", "raylib.lib") ) 
shutil.move( raylib_dll,    joinpath("../", "template", "bin", "raylib.dll") ) 

shutil.copy( "main.odin", joinpath("../", "template", "src", "main.odin") ) 
shutil.copy( "run.bat",   joinpath("../", "template", "run.bat") ) 

# clear the mess
os.remove(raylib_zip_name);
os.remove("raylib.h");
shutil.rmtree("raylib");


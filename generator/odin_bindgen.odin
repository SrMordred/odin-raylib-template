package main
import "odin_bindgen/bindgen"

main :: proc() {
    options : bindgen.GeneratorOptions;

    bindgen.generate(
        packageName = "raylib",
        foreignLibrary = "system:raylib.lib",
        outputFile = "raylib.odin",
        headerFiles = []string{"./raylib.h"},
        options = options,

    );
}
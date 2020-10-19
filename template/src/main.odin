package main;

import "raylib"
import "core:fmt" //compiler bug ?? 

main :: proc()
{
    using raylib;

    screen_width :i32 = 800;
    screen_height :i32 = 450;

    InitWindow(screen_width, screen_height, "game");
    defer CloseWindow();

    SetTargetFPS(60);

    for !WindowShouldClose()
    {
        {
            BeginDrawing();
            defer EndDrawing();
            ClearBackground(RAYWHITE);

            DrawText("Congrats! You created your first window!", 190, 200, 20, LIGHTGRAY);
        }
    }
}
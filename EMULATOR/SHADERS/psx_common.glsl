vec2 VRAM(vec2 uv)
{
    return texture(s_texture, uv).rg;
}

vec3 PSX_DITHER(ivec2 dc)
{
    mat4 dither = mat4(
        -4.0, +0.0, -3.0, +1.0,
        +2.0, -2.0, +3.0, -1.0,
        -3.0, +1.0, -4.0, +0.0,
        +3.0, -1.0, +2.0, -2.0) / 255.0;

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            if (i == dc.x && j == dc.y)
            {
                return vec3(dither[i][j]);
            }
        }
    }
    return vec3(0.0);
}

vec4 PSX_DECODE(float color_16)
{
    return fract(floor(color_16 / vec4(1.0, 32.0, 1024.0, 32768.0)) / 32.0);
}

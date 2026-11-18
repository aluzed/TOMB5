#version 450
layout(set = 0, binding = 0) uniform sampler2D s_texture;

layout(push_constant) uniform Push
{
    mat4 Projection;
    vec2 Screen;
    float Dither;
} pc;

layout(location = 0) in vec4 v_texcoord;
layout(location = 1) in vec4 v_color;
layout(location = 2) in vec4 v_page_clut;
layout(location = 0) out vec4 fragColor;

#include "psx_common.glsl"

void main()
{
    vec2 uv = (v_texcoord.xy * vec2(0.25, 1.0) + v_page_clut.xy) * vec2(1.0 / 1024.0, 1.0 / 512.0);
    vec2 comp = VRAM(uv);
    int index = int(fract(v_texcoord.x / 4.0 + 0.0001) * 4.0);

    float v = 0.0;
    if (index / 2 == 0)
        v = comp[0] * (255.0 / 16.0);
    else
        v = comp[1] * (255.0 / 16.0);

    float f = floor(v);
    vec2 c = vec2((v - f) * 16.0, f);

    vec2 clut_pos = v_page_clut.zw;
    clut_pos.x += mix(c[0], c[1], fract(float(index) / 2.0) * 2.0) / 1024.0;
    vec2 color_rg = VRAM(clut_pos);

    float color_16 = (color_rg.y * 256.0 + color_rg.x) * 255.0;
    if (color_16 == 0.0)
        discard;

    fragColor = PSX_DECODE(color_16);
    fragColor *= v_color;
    /* Vulkan a l'origine des fragments en haut : on repasse en coordonnees
     * ecran PSX (origine en bas) pour retrouver exactement la matrice de
     * dithering du backend OpenGL. */
    ivec2 dc = ivec2(fract(vec2(gl_FragCoord.x, pc.Screen.y - gl_FragCoord.y) / 4.0) * 4.0);
    fragColor.xyz += PSX_DITHER(dc) * v_texcoord.w * pc.Dither;
}

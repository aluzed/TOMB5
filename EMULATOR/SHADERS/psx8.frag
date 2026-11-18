#version 450
layout(set = 0, binding = 0) uniform sampler2D s_texture;

layout(location = 0) in vec4 v_texcoord;
layout(location = 1) in vec4 v_color;
layout(location = 2) in vec4 v_page_clut;
layout(location = 0) out vec4 fragColor;

#include "psx_common.glsl"

void main()
{
    vec2 uv = (v_texcoord.xy * vec2(0.5, 1.0) + v_page_clut.xy) * vec2(1.0 / 1024.0, 1.0 / 512.0);
    vec2 comp = VRAM(uv);

    vec2 clut_pos = v_page_clut.zw;
    int index = int(mod(v_texcoord.x, 2.0));
    if (index == 0)
        clut_pos.x += comp[0] * 255.0 / 1024.0;
    else
        clut_pos.x += comp[1] * 255.0 / 1024.0;

    vec2 color_rg = VRAM(clut_pos);
    float color_16 = (color_rg.y * 256.0 + color_rg.x) * 255.0;
    if (color_16 == 0.0)
        discard;

    fragColor = PSX_DECODE(color_16);
    fragColor *= v_color;
    ivec2 dc = ivec2(fract(gl_FragCoord.xy / 4.0) * 4.0);
    fragColor.xyz += PSX_DITHER(dc) * v_texcoord.w;
}

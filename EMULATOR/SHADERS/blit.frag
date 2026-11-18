#version 450
layout(set = 0, binding = 0) uniform sampler2D s_texture;

layout(location = 0) in vec4 v_texcoord;
layout(location = 0) out vec4 fragColor;

#include "psx_common.glsl"

void main()
{
    vec2 color_rg = VRAM(v_texcoord.xy);
    float color_16 = (color_rg.y * 256.0 + color_rg.x) * 255.0;
    fragColor = PSX_DECODE(color_16);
}

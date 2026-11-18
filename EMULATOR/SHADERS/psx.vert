#version 450
layout(location = 0) in ivec4 a_position;
layout(location = 1) in uvec4 a_texcoord;
layout(location = 2) in vec4 a_color;

layout(push_constant) uniform Push
{
    mat4 Projection;
} pc;

layout(location = 0) out vec4 v_texcoord;
layout(location = 1) out vec4 v_color;
layout(location = 2) out vec4 v_page_clut;

void main()
{
    float pz = float(a_position.z);
    float pw = float(a_position.w);

    v_texcoord = vec4(a_texcoord);
    v_color = a_color;
    v_color.xyz *= float(a_texcoord.z);

    v_page_clut.x = fract(pz / 16.0) * 1024.0;
    v_page_clut.y = floor(pz / 16.0) * 256.0;
    v_page_clut.z = fract(pw / 64.0);
    v_page_clut.w = floor(pw / 64.0) / 512.0;

    gl_Position = vec4(vec2(a_position.xy) / vec2(512.0, 240.0) * 2.0 - 1.0, 0.0, 1.0);
}

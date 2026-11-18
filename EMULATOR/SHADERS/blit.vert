#version 450
layout(location = 0) in ivec4 a_position;
layout(location = 1) in uvec4 a_texcoord;

layout(location = 0) out vec4 v_texcoord;

void main()
{
    v_texcoord = vec4(a_texcoord) * vec4(8.0 / 1024.0, 8.0 / 512.0, 0.0, 0.0);
    gl_Position = vec4(vec2(a_position.xy), 0.0, 1.0);
}

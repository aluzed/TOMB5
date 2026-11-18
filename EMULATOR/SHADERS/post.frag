#version 450

/*
 * Passe de post-traitement de la scene PSX (RMIG-014).
 *
 * La scene est rendue hors-ecran (couleur + profondeur). La profondeur est
 * un indice de bucket d'ordering table : 0 = le plus eloigne, 1 = le plus
 * proche. Elle ne permet pas un SSR physique (pas de normales ni de
 * profondeur view-space), mais elle sert a masquer/attenuer le reflet pour
 * qu'il n'apparaisse que sur les surfaces lointaines (sol, eau, murs bas).
 *
 * Param.x = intensite du reflet (0 = pas de reflet, simple copie exacte).
 */

layout(set = 0, binding = 0) uniform sampler2D s_scene;
layout(set = 0, binding = 1) uniform sampler2D s_depth;

layout(push_constant) uniform Push
{
    vec4 Params;   /* x = intensite, y = distorsion, z/w reserves */
} pc;

layout(location = 0) out vec4 fragColor;

void main()
{
    ivec2 size = textureSize(s_scene, 0);
    ivec2 p = clamp(ivec2(gl_FragCoord.xy), ivec2(0), size - 1);

    vec3 color = texelFetch(s_scene, p, 0).rgb;

    float strength = pc.Params.x;
    if (strength > 0.001)
    {
        float depth = texelFetch(s_depth, p, 0).r;

        /* Miroir vertical autour du milieu de l'ecran, avec une legere
         * distorsion horizontale qui depend de la profondeur : imite une
         * surface reflective (flaque, eau, sol mouille). */
        float distortion = (depth - 0.5) * pc.Params.y * float(size.x);
        int mirrorY = size.y - 1 - p.y;
        int sx = clamp(p.x + int(distortion), 0, size.x - 1);
        int sy = clamp(mirrorY, 0, size.y - 1);
        vec3 reflected = texelFetch(s_scene, ivec2(sx, sy), 0).rgb;

        /* Les surfaces proches (depth eleve) refletent moins : le reflet
         * reste sur les zones lointaines (fond, sol). */
        float mask = 1.0 - smoothstep(0.10, 0.90, depth);
        /* Pas de reflet tout en haut de l'ecran (ciel/plafond lointain). */
        float vfade = smoothstep(0.30, 0.65, float(p.y) / float(size.y));
        float amount = clamp(strength * mask * vfade, 0.0, 0.85);

        color = mix(color, reflected, amount);
    }

    fragColor = vec4(color, 1.0);
}

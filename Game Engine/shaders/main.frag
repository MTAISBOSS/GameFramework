#version 330 core
out vec4 FragColor;
uniform float time;
void main() {
    // Animated gradient
    vec2 uv = gl_FragCoord.xy/vec2(512.0);
    vec3 col = 0.5 + 0.5*cos(time+uv.xyx+vec3(0,2,4));
    FragColor = vec4(col, 1.0);
}
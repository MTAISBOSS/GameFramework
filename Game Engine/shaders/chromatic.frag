#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;
uniform float offset;

void main() {
    float r = texture(screenTexture, TexCoords + vec2(offset, 0.0)).r;
    float g = texture(screenTexture, TexCoords).g;
    float b = texture(screenTexture, TexCoords - vec2(offset, 0.0)).b;
    
    FragColor = vec4(r, g, b, 1.0);
}
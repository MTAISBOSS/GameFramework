#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;
uniform float threshold;
uniform float intensity;

void main() {
    vec3 color = texture(screenTexture, TexCoords).rgb;
    
    // Brightness threshold
    float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722));
    if(brightness > threshold) {
        color *= intensity;
    }
    
    FragColor = vec4(color, 1.0);
}
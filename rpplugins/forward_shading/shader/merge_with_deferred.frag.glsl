/**
 *
 * RenderPipeline
 *
 * Copyright (c) 2014-2016 tobspr <tobias.springer1@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

#version 430

#pragma include "render_pipeline_base.inc.glsl"

uniform sampler2D ShadedScene;
uniform sampler2D SceneDepth;
uniform sampler2D ForwardDepth;
uniform sampler2D ForwardColor;

out vec4 result;

void main() {
    vec2 texcoord = get_texcoord();

    vec4 deferred_result = textureLod(ShadedScene, texcoord, 0);
    vec4 forward_result = textureLod(ForwardColor, texcoord, 0);

    float deferred_depth = textureLod(ForwardDepth, texcoord, 0).x;
    float forward_depth = textureLod(SceneDepth, texcoord, 0).x;
    forward_result = mix(forward_result, deferred_result, forward_result.a);
    result = deferred_depth > forward_depth ? deferred_result : forward_result;
    result.a = deferred_result.a;
}

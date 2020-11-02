"""

RenderPipeline

Copyright (c) 2014-2016 tobspr <tobias.springer1@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from panda3d.core import LVecBase2i, Vec2
from rpcore.render_stage import RenderStage


class AOStage(RenderStage):

    required_inputs = []
    required_pipes = ["GBuffer", "DownscaledDepth", "PreviousFrame::AmbientOcclusion",
                      "CombinedVelocity", "PreviousFrame::SceneDepth"]

    @property
    def produced_pipes(self):
        return {"AmbientOcclusion": self.target_resolve.color_tex}

    def _create_blur_pass(self, i, tex):
        target_blur_v = self.create_target("BlurV-" + str(i))
        target_blur_v.add_color_attachment(bits=(8, 0, 0, 0))
        target_blur_v.prepare_buffer()

        target_blur_h = self.create_target("BlurH-" + str(i))
        target_blur_h.add_color_attachment(bits=(8, 0, 0, 0))
        target_blur_h.prepare_buffer()

        target_blur_v.set_shader_inputs(
            SourceTex=tex,
            blur_direction=LVecBase2i(0, 1),
            pixel_stretch=self.pixel_stretch)

        target_blur_h.set_shader_inputs(
            SourceTex=target_blur_v.color_tex,
            blur_direction=LVecBase2i(1, 0),
            pixel_stretch=self.pixel_stretch)

        self.blur_targets += [target_blur_v, target_blur_h]

        return target_blur_h.color_tex

    def _create_target_resolve(self, tex):
        self.target_resolve = self.create_target("ResolveAO")
        self.target_resolve.add_color_attachment(bits=(8, 0, 0, 0))
        self.target_resolve.prepare_buffer()
        self.target_resolve.set_shader_input("CurrentTex", tex)

    def create(self):
        self.target = self.create_target("Sample")
        self.target.size = -2
        self.target.add_color_attachment(bits=(8, 0, 0, 0))
        self.target.prepare_buffer()

        self.target_upscale = self.create_target("Upscale")
        self.target_upscale.add_color_attachment(bits=(8, 0, 0, 0))
        self.target_upscale.prepare_buffer()

        self.target_upscale.set_shader_inputs(
            SourceTex=self.target.color_tex,
            upscaleWeights=Vec2(0.001, 0.001))

        self.tarrget_detail_ao = self.create_target("DetailAO")
        self.tarrget_detail_ao.add_color_attachment(bits=(8, 0, 0, 0))
        self.tarrget_detail_ao.prepare_buffer()
        self.tarrget_detail_ao.set_shader_input("AOResult", self.target_upscale.color_tex)

        self.debug("Blur quality is", self.quality)

        # Low
        self.pixel_stretch = 2.0
        self.blur_passes = 1

        if self.quality == "MEDIUM":
            self.pixel_stretch = 1.0
            self.blur_passes = 2
        elif self.quality == "HIGH":
            self.pixel_stretch = 1.0
            self.blur_passes = 3
        elif self.quality == "ULTRA":
            self.pixel_stretch = 1.0
            self.blur_passes = 5

        self.blur_targets = []
        self.target_resolve = None

        current_tex = self.tarrget_detail_ao.color_tex

        for i in range(self.blur_passes):
            current_tex = self._create_blur_pass(i, current_tex)
        self._create_target_resolve(current_tex)

    def reload_shaders(self):
        self.target.shader = self.load_plugin_shader("ao_sample.frag.glsl")
        self.target_upscale.shader = self.load_plugin_shader(
            "/$$rp/shader/bilateral_upscale.frag.glsl")
        blur_shader = self.load_plugin_shader(
            "/$$rp/shader/bilateral_blur.frag.glsl")
        for target in self.blur_targets:
            target.shader = blur_shader
        self.tarrget_detail_ao.shader = self.load_plugin_shader("small_scale_ao.frag.glsl")
        if self.target_resolve:
            self.target_resolve.shader = self.load_plugin_shader("resolve_ao.frag.glsl")

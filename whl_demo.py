import os
import sys

from direct.showbase.ShowBase import ShowBase


class Application(ShowBase):
    def __init__(self):
        cwd = os.path.abspath(os.getcwd())
        if cwd in sys.path:
            sys.path.remove(cwd)

        path = 'dist'
        for i in os.listdir(path):
            if i.endswith('.whl'):
                sys.path.insert(0, os.path.abspath(os.path.join(path, i)))

        from rpcore import RenderPipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)


Application().run()

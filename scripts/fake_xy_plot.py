from collections import namedtuple
from copy import copy
from itertools import permutations, chain
import random
import csv
from io import StringIO
from PIL import Image
import numpy as np

import modules.scripts as scripts
import gradio as gr

from modules import images, sd_samplers
from modules.hypernetworks import hypernetwork
from modules.processing import process_images, Processed, StableDiffusionProcessingTxt2Img
from modules.shared import opts, cmd_opts, state
import modules.shared as shared
import modules.sd_samplers
import modules.sd_models
import re

class Script(scripts.Script):
    def title(self):
        return "Fake X/Y plot"

    def ui(self, is_img2img):
        with gr.Row():
            path_images = gr.Textbox(label="Images(Path per Line)", lines=10)
        with gr.Row():
            x_values = gr.Textbox(label="X values", lines=1)
        with gr.Row():
            y_values = gr.Textbox(label="Y values", lines=1)
        draw_legend = gr.Checkbox(label='Draw legend', value=True)
        rank = gr.Radio(choices=["Z", "N"], value="Z", label="Rank", interactive=True)

        return [path_images, x_values, y_values, draw_legend, rank]

    def run(self, p, path_images, x_values, y_values, draw_legend, rank):
        pis = path_images.split("\n")
        xs = x_values.split(',')
        ys = y_values.split(',')

        def cell(x, y):
            try:
                if rank == 'Z':
                    i = ys.index(y) * len(xs) + xs.index(x)
                else:
                    i = xs.index(x) * len(ys) + ys.index(y)
                return Image.open(pis[i])
            except:
                raise ValueError("Invalid Params.")

        # draw X/Y Grid
        ver_texts = [[images.GridAnnotation(y)] for y in ys]
        hor_texts = [[images.GridAnnotation(x)] for x in xs]

        image_cache = []
        w, h = Image.open(pis[0]).size

        for iy, y in enumerate(ys):
            for ix, x in enumerate(xs):
                image_cache.append(cell(x, y))

        grid = images.image_grid(image_cache, rows=len(ys))
        if draw_legend:
            grid = images.draw_grid_annotations(grid, w, h, hor_texts, ver_texts)
        #
        
        if opts.grid_save:
            images.save_image(grid, p.outpath_grids, "xy_grid", extension=opts.grid_format, prompt=p.prompt, seed=p.seed, grid=True, p=p)

        return Processed(p, [grid])

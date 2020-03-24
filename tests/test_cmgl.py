#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import numpy as np
import OpenGL.GL as gl

from cmgl.cmgl import drawArrays


class DrawArraysTest(unittest.TestCase):

    def setUp(self):
        # positions
        x_start_pos = 5.1
        x_end_pos = 10.2
        y_start_pos = 1.1
        y_end_pos = 2.2

        # arguments
        self.mode = gl.GL_TRIANGLE_STRIP
        self.vertices = np.array([[x_start_pos, y_start_pos, 0],
                                  [x_end_pos, y_end_pos, 0],
                                  [-x_start_pos, y_start_pos, 0],
                                  [-x_end_pos, y_end_pos, 0]], dtype=np.float32)
        self.colors = np.array([[0, 0, 0, 1],
                                [0, 0, 0, 1],
                                [0, 0, 0, 1],
                                [0, 0, 0, 1]], dtype=np.float32)
        self.texcoords = np.array([[0.0, 0.0],
                                   [1.0, 0.0],
                                   [0.0, 1.0],
                                   [1.0, 1.0]], dtype=np.float32)
        self.normals = np.array([[0, 0, 1],
                                 [0, 0, 1],
                                 [0, 0, 1],
                                 [0, 0, 1]], dtype=np.float32)

    def test_drawArrays_vertices(self):
        drawArrays(self.mode, self.vertices)

    # osx: Segmentation fault
    #def test_drawArrays_colors(self):
    #    drawArrays(self.mode, self.vertices, self.colors)

    # osx: Segmentation fault
    #def test_drawArrays_colors_wrong_length(self):
    #    with self.assertRaises(TypeError) as cm:
    #        drawArrays(self.mode, self.vertices, self.colors[:3])

    #    the_exception = cm.exception
    #    self.assertEqual(the_exception.args[0], "colors and vertices must be the same length")

    def test_drawArrays_texcoords(self):
        drawArrays(self.mode, self.vertices, None, self.texcoords)

    def test_drawArrays_texcoords_wrong_length(self):
        with self.assertRaises(TypeError) as cm:
            drawArrays(self.mode, self.vertices, None, self.texcoords[:3])

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "texcoords and vertices must be the same length")

    # osx: Segmentation fault
    #def test_drawArrays_normals(self):
    #    drawArrays(self.mode, self.vertices, None, self.texcoords, self.normals)

    #def test_drawArrays_normals_wrong_length(self):
    #    with self.assertRaises(TypeError) as cm:
    #        drawArrays(self.mode, self.vertices, None, self.texcoords, self.normals[:3])

    #    the_exception = cm.exception
    #    self.assertEqual(the_exception.args[0], "normals and vertices must be the same length")

    #def test_drawArrays_normals_components(self):
    #    a, b = self.normals.shape
    #    normals2 = np.resize(self.normals, (a, 2))
    #    with self.assertRaises(TypeError) as cm:
    #        drawArrays(self.mode, self.vertices, None, self.texcoords, normals2)

    #    the_exception = cm.exception
    #    self.assertEqual(the_exception.args[0], "normal vectors must have exactly 3 components")

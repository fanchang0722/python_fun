#  Copyright 2014 Google Inc. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import numpy as np
import matplotlib.pyplot as plt


def compute_mandelbrot(N_max, some_threshold, nx, ny):
	x = np.linspace(-2, 1, nx)
	y = np.linspace(-1.5, 1.5, ny)
	c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
	z = c
	print z.shape
	for j in range(N_max):
		z = z ** 2 + c
	mandelbrot_set = (np.abs(z) < some_threshold)
	return mandelbrot_set


mandelbrot_set = compute_mandelbrot(50., 50., 601, 401)

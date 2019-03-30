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


import matplotlib.pylab as plt
from paretochart import pareto

data = [21, 2, 10, 4, 16]
labels = ['tom', 'betty', 'alyson', 'john', 'bob']
fig, axes = plt.subplots(2, 2, figsize=(12,8))

pareto(data, axes=axes[0, 0])
plt.title('Basic chart without labels', fontsize=10)

pareto(data, labels, axes=axes[0, 1], limit=0.75, line_args=('g',))
plt.title('Data with labels, green cum. line, limit=0.75', fontsize=10)

pareto(data, labels, cumplot=False, axes=axes[1, 0], data_kw={'width': 0.5, 'color': 'g'})
plt.title('Data without cum. line, green bar width=0.5', fontsize=10)

pareto(data, labels, limit=0.95, axes=axes[1, 1], limit_kw={'color': 'r'})
plt.title('Data trimmed at 95%, yellow limit line', fontsize=10)

fig.canvas.set_window_title('Pareto Plot Test Figure')
plt.show()
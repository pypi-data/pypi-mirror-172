# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "20/07/2021"


import numpy

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D

from darfix.gui.utils import ChooseDimensionDock


class ZSumWidget(qt.QMainWindow):
    """
    Widget to apply PCA to a set of images and plot the eigenvalues found.
    """

    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self.origin, self.scale = None, None
        self._plot = Plot2D(parent=self)
        self._plot.setDefaultColormap(Colormap(name="viridis", normalization="linear"))
        self._chooseDimensionDock = ChooseDimensionDock(self)
        self._chooseDimensionDock.hide()
        self._chooseDimensionDock.widget.filterChanged.connect(self._filterStack)
        self._chooseDimensionDock.widget.stateDisabled.connect(self._wholeStack)
        layout = qt.QVBoxLayout()
        layout.addWidget(self._plot)
        layout.addWidget(self._chooseDimensionDock)
        widget = qt.QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setDataset(
        self, parent, dataset, indices=None, bg_indices=None, bg_dataset=None
    ):
        # Make sum of dataset data
        self._parent = parent
        self.dataset = dataset
        self.indices = indices
        if len(self.dataset.data.shape) > 3:
            self._chooseDimensionDock.show()
            self._chooseDimensionDock.widget.setDimensions(self.dataset.dims)
        image = self.dataset.zsum(indices=indices)
        self._plot.setGraphTitle(self.dataset.title)
        if self.dataset.transformation:
            transformation = self.dataset.transformation.transformation
            px = transformation[0][0][0]
            py = transformation[1][0][0]
            xscale = (transformation[0][-1][-1] - px) / transformation[0].shape[1]
            yscale = (transformation[1][-1][-1] - py) / transformation[1].shape[0]
            self.origin = (px, py)
            self.scale = (xscale, yscale)
            label = self.dataset.transformation.label
            (
                self._plot.addImage(
                    numpy.rot90(image, 3)
                    if self.dataset.transformation.rotate
                    else image,
                    origin=self.origin,
                    scale=self.scale,
                    xlabel=label,
                    ylabel=label,
                )
            )
        else:
            self._plot.addImage(image, xlabel="pixels", ylabel="pixels")

    def _filterStack(self, dim=0, val=0):
        image = self.dataset.zsum(indices=self.indices, dimension=[dim, val])
        if image.shape[0]:
            if self.origin:
                label = self.dataset.transformation.label
                (
                    self._plot.addImage(
                        numpy.rot90(image, 3)
                        if self.dataset.transformation.rotate
                        else image,
                        origin=self.origin,
                        scale=self.scale,
                        xlabel=label,
                        ylabel=label,
                    )
                )
            else:
                self._plot.addImage(image, xlabel="pixels", ylabel="pixels")
        else:
            self._plot.clear()

    def _wholeStack(self):
        if self.origin:
            label = self.dataset.transformation.label
            (
                self._plot.addImage(
                    numpy.rot90(self.dataset.zsum(), 3)
                    if self.dataset.transformation.rotate
                    else self.dataset.zsum(),
                    origin=self.origin,
                    scale=self.scale,
                    xlabel=label,
                    ylabel=label,
                )
            )
        else:
            self._plot.addImage(self.dataset.zsum(), xlabel="pixels", ylabel="pixels")

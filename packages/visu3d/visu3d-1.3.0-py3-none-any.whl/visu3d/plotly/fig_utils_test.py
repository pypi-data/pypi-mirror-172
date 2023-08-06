# Copyright 2022 The visu3d Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for plotly."""

from __future__ import annotations

import chex
import dataclass_array as dca
from etils import enp
import numpy as np
import pytest
import visu3d as v3d
from visu3d.utils.lazy_imports import plotly_base
from visu3d.utils.lazy_imports import plotly_go as go


@enp.testing.parametrize_xnp()
def test_to_xyz_dict(xnp: enp.NpModule):
  chex.assert_tree_all_close(
      v3d.plotly.to_xyz_dict(
          [
              [0, 1, 2],
              [0, 10, 20],
              [0, 100, 200],
          ]
      ),
      {
          'x': xnp.array([0, 0, 0]),
          'y': xnp.array([1, 10, 100]),
          'z': xnp.array([2, 20, 200]),
      },
  )

  chex.assert_tree_all_close(
      v3d.plotly.to_xyz_dict(
          [
              [0, 1, 2],
              [0, 10, 20],
              [0, 100, 200],
          ],
          pattern='axis_{}',
          names='uvw',
          axis=0,  # pytype: disable=wrong-arg-types
      ),
      {
          'axis_u': xnp.array([0, 1, 2]),
          'axis_v': xnp.array([0, 10, 20]),
          'axis_w': xnp.array([0, 100, 200]),
      },
  )


class VisuObj(v3d.plotly.Visualizable):
  """Test object."""

  def make_traces(self) -> list[plotly_base.BaseTraceType]:
    """Construct the traces of the given object."""
    return [
        go.Scatter3d(
            x=[0, 1, 2],
            y=[0, 1, 2],
            z=[0, 1, 2],
        ),
    ]


class VisuObjImplicit:
  """Test object which do not inherit from `v3d.plotly.Visualizable`."""

  def make_traces(self) -> list[plotly_base.BaseTraceType]:
    """Construct the traces of the given object."""
    return [
        go.Scatter3d(
            x=[0, 1, 2],
            y=[0, 1, 2],
            z=[0, 1, 2],
        ),
    ]


class VisuObjInvalid:
  """Not a visualizable."""


def test_is_visualizable():
  assert v3d.plotly.fig_utils.is_visualizable(VisuObj())
  assert v3d.plotly.fig_utils.is_visualizable(VisuObjImplicit())
  assert not v3d.plotly.fig_utils.is_visualizable(VisuObjInvalid())


def test_make_fig():
  x_trace = go.Scatter3d(
      x=[0, 1, 2],
      y=[0, 1, 2],
      z=[0, 1, 2],
  )
  x_array = np.ones((4, 3))
  fig = v3d.make_fig(
      [
          VisuObj(),
          VisuObjImplicit(),
          x_trace,
          x_array,
      ]
  )
  assert isinstance(fig, go.Figure)

  with pytest.raises(TypeError, match='Unsuported'):
    v3d.make_fig([VisuObjInvalid()])


@pytest.mark.parametrize('shape', [(), (4, 3), (700,), (3, 100, 4)])
def test_subsample(shape: dca.typing.Shape):
  r = v3d.Ray(pos=np.ones(shape + (3,)), dir=np.ones(shape + (3,)))
  _ = r.fig

  r = v3d.Point3d(p=np.ones(shape + (3,)), rgb=np.ones(shape + (3,)))
  _ = r.fig

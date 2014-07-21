from collections import namedtuple
import numpy as np

from .base import State as State_


__all__ = [
  'State',
  'Problem',
  'ADMM',
]


class State(State_):

  def __init__(self, x, z, y):
    self.x = x
    self.z = z
    self.y = y


class Problem(object):

  def __init__(self, f, g, A, B, c, solve_f, solve_g):
    self.f       = f
    self.g       = g
    self.A       = A
    self.B       = B
    self.c       = c
    self.solve_f = solve_f
    self.solve_g = solve_g

  def primal(self, state):
    x, z = state.x, state.z
    if np.allclose(x, z, rtol=1e-10):
      return self.f(x) + self.g(z)
    else:
      return np.inf

  def lagrangian(self, state, rho=0.0):
    x, z, y = state.x, state.z, state.y
    err     = self.constraint_error(state)
    return self.primal(state) + y.dot(err) + (rho / 2.0) * err.dot(err)

  def constraint_error(self, state):
    A, B, c = self.A, self.B, self.c
    x, z    = state.x, state.z
    return A.dot(x) + B.dot(z) - c


class ADMM(object):
  """
  Alternating Direction Method of Multipliers
  """

  def __init__(self, rho):
    self.rho = rho

  def step_y(self, state, problem):
    return state.y + self.rho * problem.constraint_error(state)

  def solve(self, problem, state_0):
    state = state_0
    while True:
      yield state
      x_t1 = problem.solve_f(state                            , self.rho)
      z_t1 = problem.solve_g(state.except_with(x=x_t1)        , self.rho)
      y_t1 = self   .step_y (state.except_with(x=x_t1, z=z_t1), problem )
      state = State(x_t1, z_t1, y_t1)

from numpy.testing import *
import itertools as it
import numpy as np
import unittest

from ..admm import State, Problem, ADMM


def quadratic1():
  f = lambda x: 3 * (x - 2.0) ** 2
  g = lambda z: 1 * (z + 1.0) ** 2
  A =  np.eye(1)
  B = -np.eye(1)
  c =  np.zeros(1)

  def solve_f(state, rho):
    """
    min_{x} f(x) + <y, Ax> + rho/2 ||Ax+Bz-c||_2^2
    """
    x, z, y = state.x, state.z, state.y
    # 0 = 6*(x-2) + A*y + rho*A*(A*x + B*z - c)
    #   = (rho*A*A + 6)*x + (rho*A*(B*z - c) + A*y - 12)
    return - (rho * A * (B*z - c) + A*y - 12) / (rho*A*A + 6)

  def solve_g(state, rho):
    """
    min_{x} g(z) + <y, Bz> + rho/2 ||Ax+Bz-c||_2^2
    """
    x, z, y = state.x, state.z, state.y
    # 0 = 2*(z+1) + B*y + rho*B*(A*x + B*z - c)
    #   = (rho*B*B + 2)*z + (rho*B * (A*x - c) + B*y + 2)
    return - (rho * B * (A*x - c) + B*y +2) / (rho*B*B + 2)

  return Problem(f, g, A, B, c, solve_f, solve_g), State(0, 0, 0)


class ADMMTests(unittest.TestCase):

  def setUp(self):
    self.rho                 = 1.0
    self.admm                = ADMM(self.rho)
    self.problem, self.state = quadratic1()
    self.eps                 = 0.001
    self.iterates            = list(it.islice(self.admm.solve(self.problem, self.state), 0, 100))
    self.solution            = self.iterates[-1]

  def test_constraint_error(self):
    final = self.solution
    assert_allclose(self.problem.constraint_error(final), 0, atol=1e-10)

  def test_optimal(self):
    final = self.solution

    self.assertGreater(
      self.problem.lagrangian(final.except_with(x=final.x+self.eps)),
      self.problem.lagrangian(final),
    )
    self.assertGreater(
      self.problem.lagrangian(final.except_with(x=final.x-self.eps)),
      self.problem.lagrangian(final),
    )
    self.assertGreater(
      self.problem.lagrangian(final.except_with(z=final.z+self.eps)),
      self.problem.lagrangian(final),
    )
    self.assertGreater(
      self.problem.lagrangian(final.except_with(z=final.z-self.eps)),
      self.problem.lagrangian(final),
    )

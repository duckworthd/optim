"""
Example usage of ADMM solver.

A gif is generated showing the iterates as they converge.
"""
from matplotlib import animation
from optim.admm import *
from optim.tests.test_admm import quadratic1
import itertools as it
import numpy     as np
import pylab as pl
import sys


if len(sys.argv) != 2:
  sys.stderr.write("Usage: %s OUTPUT\n" % (sys.argv[1],))
  sys.exit(1)

prob, state = quadratic1()
admm        = ADMM(rho=0.1)
iterates    = list(it.islice(admm.solve(prob, state), 0, 100))

pl.figure()
_   = np.linspace(-2, 5)
xs  = np.asarray([s.x for s in iterates])
zs  = np.asarray([s.z for s in iterates])
xs2 = [prob.primal(State(x=v,z=v,y=0)) for v in xs]
zs2 = [prob.primal(State(x=v,z=v,y=0)) for v in zs]

def animate(i):
  print 'iteration:', i
  pl.cla()
  pl.plot   (_, [prob.f(v) + prob.g(v) for v in _], 'k-' , label='f(x)+g(z)')
  pl.plot   (_, [prob.f(v)             for v in _], 'g--', label='f(x)'     )
  pl.plot   (_, [            prob.g(v) for v in _], 'b--', label=     'g(z)')
  pl.scatter(xs[i], xs2[i], c='g', label='x')
  pl.scatter(zs[i], zs2[i], c='b', label='z')
  pl.xlim(min(_), max(_))
  pl.legend()

anim = animation.FuncAnimation(pl.gcf(), animate, frames=len(iterates))
anim.save(output, writer='imagemagick', fps=4)

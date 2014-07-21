import inspect

__all__ = [
  'State',
]

class State(object):

  def except_with(self, **kwargs):
    kwargs = dict(kwargs)
    for k in self.args:
      kwargs[k] = kwargs.get(k) or getattr(self, k)
    return self.__class__(**kwargs)

  @property
  def args(self):
    args = inspect.getargspec(self.__init__)[0]
    return args[1:]

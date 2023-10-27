from abc import ABC, abstractmethod
from injector import Injector, inject, Binder, Module, singleton

class ProbabilityDistribution(ABC):

  @abstractmethod
  def configure(self, *args, **kargs) -> None:
    pass

  @abstractmethod
  def calculateExpectedValue(self) -> float:
    pass

  @abstractmethod
  def calculateVariance(self) -> float:
    pass

  @abstractmethod
  def calculateProbability(self, x: int) -> float:
    pass

class Binom(ProbabilityDistribution):

  def __init__(self) -> None:
    self.__n = None
    self.__p = None
    self.table = []
  
  @property
  def n(self):
    return self.__n
  
  @n.setter
  def n(self, val: int):
    self.__n = val

  @property
  def p(self):
    return self.__p

  @p.setter
  def p(self, val: float):
    self.__p = val

  def configure(self, n: int, p: float):
    self.__checkIsInvalidForN(n)
    self.__checkIsInvalidForP(p)
    self.n = n
    self.p = p
  
  def calculateExpectedValue(self) -> float:
    assert self.n is not None and self.p is not None
    n = self.n
    p = self.p
    return n * p

  def calculateVariance(self) -> float:
    assert self.n is not None and self.p is not None
    n = self.n
    p = self.p
    return n * p * (1 - p)

  def calculateProbability(self, x: int) -> float:
    assert self.n is not None and self.p is not None
    self.__checkInvalidValue(self.n, x)
    n = self.n
    p = self.p
    self.__createTable(n, p)
    return self.table[n][x]

  def __createTable(self, n: int, p: float, cache=True):
    assert self.n is not None and self.p is not None
    if cache and self.n > n and self.p == p:
      return
    table = [[0.0]*(n+1) for _ in range(n+1)]
    table[0][0] = 1.0
    for i in range(n):
      for j in range(n):
        table[i+1][j] += table[i][j] * (1 - p)
        table[i+1][j+1] += table[i][j] * p
    self.table = table

  def __checkIsInvalidForN(self, n):
    if n < 0:
        raise ValueError("'N' should be non-negative")
  def __checkIsInvalidForP(self, p):
    if p < 0 or p > 1:
        raise ValueError("'P' should be 0 <= p <= 1")
  def __checkInvalidValue(self, n, x):
    if n < x:
        raise ValueError("Invalid value N and X. they should be N > X.")

class BindModule(Module):
  @classmethod
  def configure(cls, binder: Binder):
    binder.bind(ProbabilityDistribution, to=Binom, scope=singleton)

class DIContainer:
  def __init__(self, module: Module) -> None:
    self.injector = Injector(module)
  
  def get(self, cls):
    return self.injector.get(cls)

class Client():
  @inject
  def __init__(self, distribution: ProbabilityDistribution) -> None:
    self.distribution = distribution

  def solve(self, d: int, x: int, *args, **kwargs):
    self.distribution.configure(*args, **kwargs)
    return self.__round(self.distribution.calculateProbability(x), d)

  def __round(self, value: float, digit: int = 4):
    return round(value, digit)

def main(n: int, p: float, x: int, d: int):
  dicontainer = DIContainer(BindModule)
  distribution = dicontainer.get(Binom)
  client = Client(distribution)

  ans = client.solve(n=n, p=p, x=x, d=d)
  print(ans)

if __name__ == "__main__":
  main(n=100, p=0.35, x=35, d=20)
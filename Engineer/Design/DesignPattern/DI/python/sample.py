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
    self.n = n
    self.p = p
  
  def calculateExpectedValue(self) -> float:
    n = self.n
    p = self.p
    if not n or not p:
      return 0
    return n * p

  def calculateVariance(self) -> float:
    n = self.n
    p = self.p
    if not n or not p:
      return 0
    return n * p * (1 - p)

  def calculateProbability(self, x: int) -> float:
    n = self.n
    p = self.p
    if not n or not p:
      return 0
    self.__createTable(n, p)
    return self.table[n][x]

  def __createTable(self, n: int, p: float, cache=True):
    if cache and self.table and self.n and self.p and self.n > n and self.p == p:
      return
    table = [[0.0]*(n+1) for _ in range(n+1)]
    table[0][0] = 1.0
    for i in range(n):
      for j in range(n):
        table[i+1][j] += table[i][j] * (1 - p)
        table[i+1][j+1] += table[i][j] * p
    self.table = table

class AppModule(Module):
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

  def solve(self, round: int, x: int, *args, **kwargs):
    self.distribution.configure(*args, **kwargs)
    return self.__round(self.distribution.calculateProbability(x), round)

  def __round(self, value: float, digit: int = 4):
    return round(value, digit)

def main(n: int, p: float, x: int, round: int):
  dicontainer = DIContainer(AppModule)
  distribution = dicontainer.get(Binom)
  client = Client(distribution)

  ans = client.solve(n=n, p=p, x=x, round=round)
  print(ans)

if __name__ == "__main__":
  main(n=2000, p=0.5, x=1000, round=20)
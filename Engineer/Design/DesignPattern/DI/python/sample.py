from abc import ABC, abstractmethod
from injector import Injector, inject, Binder, Module, singleton

class ProbabilityDistribution(ABC):

  @abstractmethod
  def calculateExpectedValue(parameter) -> float:
    pass

  @abstractmethod
  def calculateVariance(parameter) -> float:
    pass

  @abstractmethod
  def calculateProbability(parameter) -> float:
    pass

class DIContainer(Module):
  def __init__(self) -> None:
    self.injector = Injector(self.__class__.configure)

  @classmethod
  def configure(cls, binder: Binder):
    binder.bind(ProbabilityDistribution, to=Binom, scope=singleton)

  def get(self, cls):
    return self.injector.get(cls)

class Binom(ProbabilityDistribution):

  def __init__(self) -> None:
    self.table = []

  def calculateExpectedValue(self, n: int, p: float) -> float:
    return n * p

  def calculateVariance(self, n: int, p: float) -> float:
    return n * p * (1 - p)

  def calculateProbability(self, n: int, x: int, p: float, cache=True) -> float:
    self.__createTable(n, p, cache=cache)
    return self.table[n][x]

  def __createTable(self, n: int, p: float, cache=True):
    if cache and self.table:
      return
    table = [[0.0]*(n+1) for _ in range(n+1)]
    table[0][0] = 1.0
    for i in range(n):
      for j in range(n):
        table[i+1][j] += table[i][j] * (1 - p)
        table[i+1][j+1] += table[i][j] * p
    self.table = table

class Client():
  @inject
  def __init__(self, distribution: ProbabilityDistribution) -> None:
    self.distribution = distribution

  def solve(self, n: int, x: int, p: float):
    return self.__round(self.distribution.calculateProbability(n, x, p))

  def __round(self, value: float, digit: int = 4):
    return round(value, digit)

dicontainer = DIContainer()
distribution = dicontainer.get(Binom)
client = Client(distribution)

print(client.solve(5, 4, 0.5))
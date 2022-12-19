from logger import Logging
from log_decorator import defaultlog

@defaultlog()
def roop(n = 10000000):
    for i in range(n):
        pass

@defaultlog()
def main():
    instance = Logging()
    logger = instance.create_require()
    roop()
    logger.log(30, "END ---> func: roop")

if __name__ == "__main__":
    main()
from abc import ABC, abstractmethod

class ExtendedFunction(ABC):

    @abstractmethod
    def function(self, x): pass

    def test(self, funcName, argName, fromVal, toVal, step):
        result = ''
        for x in range(fromVal, toVal, step):
            result += 'funcName' + '(' + argName + ') =' +\
                      x + self.function(x)
        return result

from abc import ABC, abstractmethod


class Label(ABC):

    def __init__(self, value : int):
        self.__value = value

    def add_value(self, value_sum : int):
        return self.__value + value_sum

    def get_unicode(self):
        return f'{self._get_unicode_label()}{self._get_index()}'

    def get_latex(self):
        return f'{self._get_latex_label()}{self._get_index()}'

    def get_color(self):
        return self._get_color()

    def get_value(self):
        return self.__value

    @abstractmethod
    def _get_unicode_label(self):
        pass

    @abstractmethod
    def _get_index(self):
        pass

    @abstractmethod
    def _get_latex_label(self):
        pass

    @abstractmethod
    def _get_color(self):
        pass

class Lambda(Label, ABC):
    def _get_unicode_label(self):
        return 'λ'

    def _get_latex_label(self):
        return  r'\lambda_'

class LambdaOne(Lambda):
    def _get_color(self):
        return 'red'

    def _get_index(self):
        return 1

class LambdaTwo(Lambda):
    def _get_color(self):
        return 'yellow'

    def _get_index(self):
        return 2

class Mu(Label, ABC):
    def _get_unicode_label(self):
        return 'μ'

    def _get_latex_label(self):
        return r'\mu_'

class MuOne(Mu):
    def _get_color(self):
        return 'blue'

    def _get_index(self):
        return 1

class MuTwo(Mu):
    def _get_color(self):
        return 'green'

    def _get_index(self):
        return 2
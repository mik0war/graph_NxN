from data_types.labels import LambdaOne, LambdaTwo, MuOne, MuTwo


class Parameters:
    def __init__(self, lam1: int, lam2: int, mu1: int, mu2: int):
        self.lam_one = LambdaOne(lam1)
        self.lam_two = LambdaTwo(lam2)
        self.mu_one = MuOne(mu1)
        self.mu_two = MuTwo(mu2)

    def change_value(self, parameters):
        if self.lam_one != parameters.lam_one:
            self.lam_one.change_value(parameters.lam_one.get_value())

        if self.lam_two != parameters.lam_two:
            self.lam_two.change_value(parameters.lam_two.get_value())

        if self.mu_one != parameters.mu_one:
            self.mu_one.change_value(parameters.mu_one.get_value())

        if self.mu_two != parameters.mu_two:
            self.mu_two.change_value(parameters.mu_two.get_value())


class Interval:
    def __init__(self, time_start: float, time_end: float, parameters: Parameters):
        self.time_start = time_start
        self.time_end = time_end
        self.parameters = parameters

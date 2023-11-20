import flavio
from wilson import Wilson

class Observable:
    #__slots__=("nombre","q2min","q2max","w","_prediction","_uncertainty","_exp","_exp_err_right","_exp_err_left")
    def __init__(self,nombre,q2min=None,q2max=None,w=None):
        self.nombre=nombre
        self.q2min=q2min
        self.q2max=q2max
        self.w=w
        self._prediction=None
        self._uncertainty=None
        self._exp=None
        self._exp_err_right=None
        self._exp_err_left=None

    def __str__(self):
        if self.q2min and self.q2max is not None:
            return f"Valor teórico: {self.nombre} [{self.q2min},{self.q2max}] = {self.prediction:.3f}±{self.uncertainty}\n Valor experimental: {self.nombre} [{self.q2min},{self.q2max}] = {self.exp}+{self.exp_err_right}-{self.exp_err_left}"
        if self.q2min and self.q2max is None:
            return f"Valor teórico: {self.nombre} = {self.prediction}±{self.uncertainty}\n Valor experimental: {self.nombre} = {self.exp}+{self.exp_err_right}-{self.exp_err_left}"

    @property
    def prediction(self):
        print(self._prediction)
        if self._prediction is None:
            print("self._prediction is None")
            if self.q2min is not None and self.q2max is not None:
                if self.w is not None:
                    self._prediction=flavio.np_prediction(self.nombre, self.w, self.q2min, self.q2max)
                    print(self._prediction)
                if self.w is None:
                    self._prediction=flavio.sm_prediction(self.nombre, self.q2min, self.q2max)
            else:
                if self.w is not None:
                    self._prediction=flavio.np_prediction(self.nombre, self.w)
                if self.w is None:
                    self._prediction=flavio.sm_prediction(self.nombre)
        return self._prediction
    
    @property
    def uncertainty(self):
        if self._uncertainty is None:
            if self.q2min is not None and self.q2max is not None:
                if self.w is not None:
                    self._uncertainty=flavio.np_uncertainty(self.nombre, self.w, self.q2min, self.q2max)
                if self.w is None:
                    self._uncertainty=flavio.sm_uncertainty(self.nombre, self.q2min, self.q2max)
            else:
                if self.w is not None:
                    self._uncertainty=flavio.np_uncertainty(self.nombre, self.w)
                if self.w is None:
                    self._uncertainty=flavio.sm_uncertainty(self.nombre)
            return self._uncertainty

    @property
    def exp(self):
        if self._exp is None:
            if self.q2min is not None and self.q2max is not None:
                const=flavio.combine_measurements((self.nombre, self.q2min, self.q2max))
                self._exp=const.central_value
            else:
                const=flavio.combine_measurements(self.nombre)
                self._exp=const.central_value
        return self._exp

    @property
    def exp_err_right(self):
        if self._exp_err_right is None:
            if self.q2min is not None and self.q2max is not None:
                const=flavio.combine_measurements((self.nombre, self.q2min, self.q2max))
                self._exp_err_right=const.error_right
            else:
                const=flavio.combine_measurements(self.nombre)
                self._exp_err_right=const.error_right
        return self._exp_err_right

    @property
    def exp_err_left(self):
        if self._exp_err_left is None:
            if self.q2min is not None and self.q2max is not None:
                const=flavio.combine_measurements((self.nombre, self.q2min, self.q2max))
                self._exp_err_left=const.error_left
            else:
                const=flavio.combine_measurements(self.nombre)
                self._exp_err_left=const.error_left
        return self._exp_err_left

Lambda = 1000
w = Wilson({'lq1_2223': 0.1/Lambda**2, 'lq3_2223': 0.1/Lambda**2}, scale=Lambda, eft='SMEFT', basis='Warsaw')
RK=Observable('<Rmue>(B+->Kll)',1.1, 6.0,w)
print(RK)

x=flavio.np_prediction('<Rmue>(B+->Kll)', w, 1.1, 6.0)
print(x)

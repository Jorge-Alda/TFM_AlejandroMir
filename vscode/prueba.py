import flavio
from time import sleep


def error_RK(w):
    R = flavio.np_prediction('<Rmue>(B+->Kll)', w, 1.1, 6.0)
    sleep(5)
    return 1-R


if __name__ == '__main__':
    R = flavio.sm_prediction('<Rmue>(B+->Kll)', 1.1, 6.0)
    sleep(15)
    print(f"RK = {R:.4f}")

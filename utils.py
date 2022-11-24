"""
Funciones y clases auxiliares
"""

import io
from abc import ABC, abstractmethod
import yaml
import json
import pickle
from contextlib import ContextDecorator
from time import perf_counter


class Serializable(ABC):
    """Clase abstracta para objetos serializables.

    Las clases que lo hereden deben implementar los métodos `a_dict` y `desde_dict`.

    Permite serializar y deserializar a pickle, JSON y YAML.
    """
    @abstractmethod
    def a_dict(self) -> dict:
        """Devuelve un diccionario con la estructura del objeto

        Returns
        -------
        dict
            Diccionario con los miembros y valores de la clase.
        """
        pass

    @staticmethod
    @abstractmethod
    def desde_dict(d: dict) -> "Serializable":
        """Genera un objeto a partir de un diccionario.

        Parameters
        ----------
        d : dict
            Diccionario con los miembros y valores de la clase.

        Returns
        -------
        Serializable
            Objeto reconstruído
        """
        pass

    def a_pickle(self, file: io.BufferedIOBase):
        """Serializa el objeto en formato pickle

        Parameters
        ----------
        file : io.BufferedIOBase
            Archivo binario en el que se serializa el objeto
        """
        pickle.dump(self, file)

    @staticmethod
    def desde_pickle(file: io.BufferedIOBase) -> "Serializable":
        """Deserializa el objeto desde el formato pickle

        Parameters
        ----------
        file : io.BufferedIOBase
            Archivo binario que contiene el objeto en formato pickle

        Returns
        -------
        Serializable
            Objeto deserializado
        """
        return pickle.load(file)

    def a_json(self, file: io.TextIOWrapper | io.StringIO):
        """Serializa el objeto en formato JSON

        Parameters
        ----------
        file : io.TextIOWrapper | io.StringIO
            Archivo de texto en el que se serializa el objeto
        """
        json.dump(self.a_dict(), file, indent=4)

    @classmethod
    def desde_json(cls, file: io.TextIOBase) -> "Serializable":
        """Deserializa el objeto desde el formato JSON

        Parameters
        ----------
        file : io.TextIOBase
            Archivo de texto que contiene el objeto en formato JSON

        Returns
        -------
        Serializable
            Objeto deserializado
        """
        return cls.desde_dict(json.load(file))

    def a_yaml(self, file: io.TextIOBase):
        """Serializa el objeto en formato YAML

        Parameters
        ----------
        file : io.TextIOBase
            Archivo de texto en el que se serializa el objeto
        """
        yaml.dump(self.a_dict(), file)

    @classmethod
    def desde_yaml(cls, file: io.TextIOBase) -> "Serializable":
        """Deserializa el objeto desde el formato YAML

        Parameters
        ----------
        file : io.TextIOBase
            Archivo de texto que contiene el objeto en formato JSON

        Returns
        -------
        Serializable
            Objeto deserializado
        """
        return cls.desde_dict(yaml.safe_load(file))


class Temporizador(ContextDecorator):
    """Temporizadores como gestores de contexto o decoradores"""
    _tiempo = 0

    def __enter__(self):
        self._inicio = perf_counter()
        self._pausado = False
        return self

    def ver_tiempo(self) -> float:
        """Devuelve el tiempo actual, sin detener la ejecución

        Returns
        -------
        float
            Tiempo transcurrido
        """
        if self._pausado:
            return self._tiempo
        else:
            return self._tiempo + perf_counter() - self._inicio

    def pausar(self):
        """Pausa el temporizador
        """
        self._tiempo += perf_counter() - self._inicio
        self._pausado = True

    def reanudar(self):
        """Reanuda el temporizador
        """
        self._inicio = perf_counter()
        self._pausado = False

    def __exit__(self, *args):
        self.pausar()

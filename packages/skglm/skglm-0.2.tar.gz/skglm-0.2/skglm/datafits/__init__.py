from .base import BaseDatafit, BaseMultitaskDatafit
from .single_task import Quadratic, QuadraticSVC, Logistic, Huber, Poisson
from .multi_task import QuadraticMultiTask
from .group import QuadraticGroup


__all__ = [
    BaseDatafit, BaseMultitaskDatafit,
    Quadratic, QuadraticSVC, Logistic, Huber, Poisson,
    QuadraticMultiTask,
    QuadraticGroup
]

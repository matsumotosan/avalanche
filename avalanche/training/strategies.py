from typing import Optional, Sequence, List

from torch.nn import Module
from torch.optim import Optimizer

from avalanche.evaluation import EvalProtocol
from avalanche.training.base_strategy import BaseStrategy
from avalanche.training.plugins import StrategyPlugin, MultiHeadPlugin, \
    CWRStarPlugin


class Naive(BaseStrategy):
    """
    The simplest (and least effective) Continual Learning strategy. Naive just
    incrementally fine tunes a single model without employing any method
    to contrast the catastrophic forgetting of previous knowledge.

    Naive is easy to set up and its results are commonly used to show the worst
    performing baseline.
    """

    def __init__(self, model: Module, optimizer: Optimizer, criterion,
                 evaluation_protocol: Optional[EvalProtocol] = None,
                 train_mb_size: int = 1, train_epochs: int = 1,
                 test_mb_size: int = None, device=None,
                 plugins: Optional[Sequence[StrategyPlugin]] = None):
        """
        Creates an instance of the Naive strategy.

        :param model: The model.
        :param optimizer: The optimizer to use.
        :param criterion: The loss criterion to use.
        :param evaluation_protocol: The evaluation plugin.
        :param train_mb_size: The train minibatch size. Defaults to 1.
        :param train_epochs: The number of training epochs. Defaults to 1.
        :param test_mb_size: The test minibatch size. Defaults to 1.
        :param device: The device to use. Defaults to None (cpu).
        :param plugins: Plugins to be added. Defaults to None.
        """
        super().__init__(
            model, criterion, optimizer, evaluation_protocol,
            train_mb_size=train_mb_size, train_epochs=train_epochs,
            test_mb_size=test_mb_size, device=device, plugins=plugins)


class MTNaive(BaseStrategy):
    """
    A Naive strategy with automatic head expansion.
    """

    def __init__(self, model: Module, optimizer: Optimizer, criterion,
                 evaluation_protocol: Optional[EvalProtocol] = None,
                 train_mb_size: int = 1, train_epochs: int = 1,
                 test_mb_size: int = None, device=None,
                 plugins: Optional[List[StrategyPlugin]] = None,
                 classifier_field: str = 'classifier',
                 keep_initial_layer: bool = False):
        """
        Creates an instance of the Naive strategy.

        :param model: The model.
        :param optimizer: The optimizer to use.
        :param criterion: The loss criterion to use.
        :param evaluation_protocol: The evaluation plugin.
        :param train_mb_size: The train minibatch size. Defaults to 1.
        :param train_epochs: The number of training epochs. Defaults to 1.
        :param test_mb_size: The test minibatch size. Defaults to 1.
        :param device: The device to use. Defaults to None (cpu).
        :param plugins: Plugins to be added. Defaults to None.
        :param classifier_field: name of the output layer.
        :param keep_initial_layer: if True keeps the initial layer for task 0.
        """
        mhp = MultiHeadPlugin(model, classifier_field=classifier_field,
                              keep_initial_layer=keep_initial_layer)
        if plugins is None:
            plugins = [mhp]
        else:
            plugins.append(mhp)
        super().__init__(
            model, criterion, optimizer, evaluation_protocol,
            train_mb_size=train_mb_size, train_epochs=train_epochs,
            test_mb_size=test_mb_size, device=device, plugins=plugins)


class CWRStar(BaseStrategy):
    """
    The simplest (and least effective) Continual Learning strategy. Naive just
    incrementally fine tunes a single model without employing any method
    to contrast the catastrophic forgetting of previous knowledge.

    Naive is easy to set up and its results are commonly used to show the worst
    performing baseline.
    """

    def __init__(self, model: Module, optimizer: Optimizer, criterion,
                 second_last_layer_name, num_classes=50,
                 evaluation_protocol: Optional[EvalProtocol] = None,
                 train_mb_size: int = 1, train_epochs: int = 1,
                 test_mb_size: int = None, device=None,
                 plugins: Optional[List[StrategyPlugin]] = None,
                 ):
        """
        Creates an instance of the Naive strategy.

        :param model: The model.
        :param optimizer: The optimizer to use.
        :param criterion: The loss criterion to use.
        :param second_last_layer_name: name of the second to last layer
                (layer just before the classifier).
        :param num_classes: total number of classes.
        :param evaluation_protocol: The evaluation plugin.
        :param train_mb_size: The train minibatch size. Defaults to 1.
        :param train_epochs: The number of training epochs. Defaults to 1.
        :param test_mb_size: The test minibatch size. Defaults to 1.
        :param device: The device to use. Defaults to None (cpu).
        :param plugins: Plugins to be added. Defaults to None.
        """
        cwsp = CWRStarPlugin(model, second_last_layer_name, num_classes)
        if plugins is None:
            plugins = [cwsp]
        else:
            plugins.append(cwsp)
        super().__init__(
            model, criterion, optimizer, evaluation_protocol,
            train_mb_size=train_mb_size, train_epochs=train_epochs,
            test_mb_size=test_mb_size, device=device, plugins=plugins)

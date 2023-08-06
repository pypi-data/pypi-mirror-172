import unittest

import pytest

from simple_proxy3.observables.observable import Observable


@pytest.mark.asyncio
async def test_observable():
    class TestObserver:
        def __init__(self):
            self._notified = False

        async def notify(self, observable: Observable):
            self._notified = True

    # Arrange
    test_observer = TestObserver()
    test_observable = Observable()

    # Act
    test_observable.register_observer(test_observer)
    await test_observable._notify_observers()

    # Assert
    assert test_observer._notified


@pytest.mark.asyncio
async def test_observable_dup():
    class TestObserver:
        def __init__(self):
            self._notified = False

        async def notify(self, observable: Observable):
            self._notified = True

    # Arrange
    test_observer = TestObserver()
    test_observable = Observable()
    # Act
    test_observable.register_observer(test_observer)

    # Assert
    with pytest.raises(Exception):
        test_observable.register_observer(test_observer)

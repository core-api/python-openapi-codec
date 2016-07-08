from unittest import TestCase as _TestCase


try:
    from unittest import mock  # NOQA
except:
    import mock  # NOQA


class TestCase(_TestCase):
    def assertCountEqual(self, *args, **kwargs):
        if hasattr(self, 'assertItemsEqual'):
            return self.assertItemsEqual(*args, **kwargs)

        return super().assertCountEqual(*args, **kwargs)

from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.units import word_ends


test_data = namedtuple('test_data', 'content args kwargs expected msg')


TESTS = (
    test_data(content='cat dog bee', args=(0,), kwargs={}, expected=3, msg="find current word's end"),
    test_data(content='  cat dog bee', args=(0,), kwargs={}, expected=5, msg="find current word's end from white space"),  # noqa: E501
    test_data(content='a dog bee', args=(0,), kwargs={}, expected=5, msg="find next word's end from 1-char word"),
    test_data(content='a. dog bee', args=(0,), kwargs={}, expected=2, msg="find next word's end in contiguous punctuation"),  # noqa: E501
    test_data(content='cat dog bees', args=(0,), kwargs={'count': 3}, expected=12, msg="find current word's end (count: 3)"),  # noqa: E501
    test_data(content='a dog bees', args=(0,), kwargs={'count': 3}, expected=10, msg="find next word's end from 1-char word (count: 3)"),  # noqa: E501
    test_data(content='a. dog bees', args=(0,), kwargs={'count': 3}, expected=11, msg="find next word's end in contiguous punctuation (count: 3)"),  # noqa: E501
    test_data(content='a.dog bee', args=(0,), kwargs={}, expected=2, msg="find next word's end in interspersed punctuation"),  # noqa: E501
)

TESTS_BIG = (
    test_data(content='cat dog bee', args=(0,), kwargs={'big': True}, expected=3, msg="find current word's end"),
    test_data(content='  cat dog bee', args=(0,), kwargs={}, expected=5, msg="find current word's end from white space"),  # noqa: E501
    test_data(content='a dog bee', args=(0,), kwargs={'big': True}, expected=5, msg="find next word's end from 1-char word"),  # noqa: E501
    test_data(content='a. dog bee', args=(0,), kwargs={'big': True}, expected=2, msg="find next word's end in contiguous punctuation"),  # noqa: E501
    test_data(content='cat dog bees', args=(0,), kwargs={'big': True, 'count': 3}, expected=12, msg="find current word's end (count: 3)"),  # noqa: E501
    test_data(content='a dog bees', args=(0,), kwargs={'big': True, 'count': 3}, expected=10, msg="find next word's end from 1-char word (count: 3)"),  # noqa: E501
    test_data(content='a. dog bee ants', args=(0,), kwargs={'big': True, 'count': 3}, expected=10, msg="find next word's end in contiguous punctuation (count: 3)"),  # noqa: E501
    test_data(content='a. (dog) bee, ants', args=(0,), kwargs={'big': True, 'count': 3}, expected=13, msg="find next word's skipping over many punctuation signs (count: 3)"),  # noqa: E501
)


class Test_WordEnds(ViewTestCase):

    def test_word_ends(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.content)
            actual = word_ends(self.view, *data.args, **data.kwargs)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)

    def test_big_word_ends(self):
        for (i, data) in enumerate(TESTS_BIG):
            self.write(data.content)
            actual = word_ends(self.view, *data.args, **data.kwargs)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)

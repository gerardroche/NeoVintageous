from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase

test_data = namedtuple('test_data', 'text startRegion mode expectedRegion msg')

NORMAL_CASES = (
    test_data('012a4', (3, 3), ViewTestCase.NORMAL_MODE, (0, 0), 'Move to beginning'),
    test_data('  2a4', (3, 3), ViewTestCase.NORMAL_MODE, (2, 2), 'Move to first non-space left'),
    test_data('  234', (1, 1), ViewTestCase.NORMAL_MODE, (2, 2), 'Move to first non-space right'),
)

INTERNAL_NORMAL_CASES = (
    test_data('012a4', (3, 3), ViewTestCase.INTERNAL_NORMAL_MODE, (3, 0), 'Internal move to beginning'),
    test_data('  2a4', (3, 3), ViewTestCase.INTERNAL_NORMAL_MODE, (3, 2), 'Internal move to first non-space left'),
    test_data('  234', (1, 1), ViewTestCase.INTERNAL_NORMAL_MODE, (1, 2), 'Internal move to first non-space right'),
    test_data('  a34', (2, 3), ViewTestCase.INTERNAL_NORMAL_MODE, (2, 2), 'Internal move to first non-space self'),
)

VISUAL_MULTI_CHAR_CASES = (
    test_data('0b2a45', (4, 1), ViewTestCase.VISUAL_MODE, (4, 0), 'Visual no crossover'),
    test_data('0a2b45', (1, 4), ViewTestCase.VISUAL_MODE, (2, 0), 'Visual crossover'),
    test_data('  2ba5', (5, 3), ViewTestCase.VISUAL_MODE, (5, 2), 'Visual first non-space right no crossover'),
    test_data('  2ab5', (3, 5), ViewTestCase.VISUAL_MODE, (4, 2), 'Visual first non-space right crossover'),
    test_data('  2345', (2, 0), ViewTestCase.VISUAL_MODE, (1, 3), 'Visual first non-space left crossover'),
    test_data('  2345', (0, 2), ViewTestCase.VISUAL_MODE, (0, 3), 'Visual first non-space left no crossover'),
    test_data('  23a5', (5, 1), ViewTestCase.VISUAL_MODE, (5, 2), 'Visual first non-space reverse'),
    test_data('  23b5', (1, 5), ViewTestCase.VISUAL_MODE, (1, 3), 'Visual first non-space forward'),
)

VISUAL_ONE_CHAR_CASES = (
    test_data('f', (0, 1), ViewTestCase.VISUAL_MODE, (0, 1), 'Visual single character forward'),
    test_data('r', (1, 0), ViewTestCase.VISUAL_MODE, (1, 0), 'Visual single character reverse'),
)

VISUAL_MULTI_LINE_CASES = (
    test_data(' 123\n 678', (0, 5), ViewTestCase.VISUAL_MODE, (0, 2), 'Visual caret on newline'),
    test_data(' 123\n 678', (8, 4), ViewTestCase.VISUAL_MODE, (8, 1), 'Visual caret on newline reverse'),
    test_data(' 123\n 678', (2, 8), ViewTestCase.VISUAL_MODE, (2, 7), 'Visual forward multiline'),
    test_data(' 123\n 678', (8, 2), ViewTestCase.VISUAL_MODE, (8, 1), 'Visual reverse multiline'),
)


class Test__vi_hat(ViewTestCase):

    def runTests(self, data):
        for (i, data) in enumerate(data):
            self.write(data.text)
            self.select(self._R(*data.startRegion))

            self.view.run_command('_vi_hat', {'mode': data.mode, 'count': 1})

            self._assertRegionsEqual(
                self._R(*data.expectedRegion),
                self.view.sel()[0],
                "Failed on index {} {} : Text:\"{}\" Region:{}".format(i, data.msg, data.text, data.startRegion)
            )

    def test_normal_cases(self):
        self.runTests(NORMAL_CASES)

    def test_internal_normal_cases(self):
        self.runTests(INTERNAL_NORMAL_CASES)

    def test_visual_multiple_character_cases(self):
        self.runTests(VISUAL_MULTI_CHAR_CASES)

    def test_visual_single_character_cases(self):
        self.runTests(VISUAL_ONE_CHAR_CASES)

    def test_visual_multiple_lines_cases(self):
        self.runTests(VISUAL_MULTI_LINE_CASES)

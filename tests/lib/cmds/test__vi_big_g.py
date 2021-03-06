from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_g_InNormalMode(ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.select(0)

        self.view.run_command('_vi_big_g', {'mode': self.NORMAL_MODE, 'count': 1})

        self.assertSelection((6, 6))

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.select(0)

        self.view.run_command('_vi_big_g', {'mode': self.NORMAL_MODE, 'count': 1})

        self.assertSelection((8, 8))


class Test__vi_big_g_InVisualMode(ViewTestCase):

    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.select((0, 1))

        self.view.run_command('_vi_big_g', {'mode': self.VISUAL_MODE, 'count': 1})

        self.assertSelection((0, 8))


class Test__vi_big_g_InInternalNormalMode(ViewTestCase):

    def test_can_move_in_mode_internal_normal(self):
        self.write('abc\nabc\n')
        self.select(1)

        self.view.run_command('_vi_big_g', {'mode': self.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection((0, 8))

    def test_operates_linewise(self):
        self.write('abc\nabc\nabc\n')
        self.select((4, 5))

        self.view.run_command('_vi_big_g', {'mode': self.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection((3, 12))


class Test__vi_big_g_InVisualLineMode(ViewTestCase):

    def test_can_move_in_mode_visual_line(self):
        self.write('abc\nabc\n')
        self.select((0, 4))

        self.view.run_command('_vi_big_g', {'mode': self.VISUAL_LINE_MODE, 'count': 1})

        self.assertSelection((0, 8))

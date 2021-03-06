from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_LET
from .tokens_base import TokenOfCommand
from NeoVintageous.lib import ex
from NeoVintageous.lib import nvim


@ex.command('let', 'let')
class TokenCommandLet(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_LET, 'let', *args, **kwargs)
        self.target_command = 'ex_let'

    @property
    def variable_name(self):
        return self.params['name']

    @property
    def variable_value(self):
        return self.params['value']


def scan_command_let(state):
    params = {
        'name': None,
        'value': None,
    }

    # TODO(guillermooo): :let has many more options.

    m = state.expect_match(
        r'(?P<name>.+?)\s*=\s*(?P<value>.+?)\s*$',
        on_error=lambda: nvim.Error(nvim.E_UNDEFINED_VARIABLE))

    params.update(m.groupdict())

    return None, [TokenCommandLet(params), TokenEof()]

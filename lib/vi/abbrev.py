import os
import json

import sublime


def abbrevs_path():
    return os.path.normpath(
        os.path.join(
            sublime.packages_path(),
            'User/_vintageous_abbrev.sublime-completions'
        )
    )


def load_abbrevs():
    path = abbrevs_path()
    decoded_json = None
    if os.path.exists(path):
        with open(path, 'r') as f:
            decoded_json = json.load(f)

    return decoded_json or {'completions': []}


# TODO: Make entries temporary unless !mksession is used or something like that.
# TODO: Enable contexts for abbrevs?
def save_abbrevs(data):
    path = abbrevs_path()
    with open(path, 'w') as f:
        json.dump(data, f)


class Store(object):
    """Manages storage for abbreviations."""

    def set(self, short, full):
        abbrevs = load_abbrevs()
        idx = self.contains(abbrevs, short)
        if idx is not None:
            abbrevs['completions'][idx] = dict(trigger=short, contents=full)
        else:
            abbrevs['completions'].append(dict(trigger=short, contents=full))

        save_abbrevs(abbrevs)

    def get(self, short):
        raise NotImplementedError()

    def get_all(self):
        abbrevs = load_abbrevs()
        for item in abbrevs['completions']:
            yield item

    def contains(self, data, short):
        # TODO: Inefficient.
        for (i, completion) in enumerate(data['completions']):
            if completion['trigger'] == short:
                return i

        return None

    def erase(self, short):
        data = load_abbrevs()
        idx = self.contains(data, short)
        if idx is not None:
            del data['completions'][idx]
            save_abbrevs(data)

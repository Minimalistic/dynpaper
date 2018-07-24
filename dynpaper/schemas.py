from schema import Schema, Or, Regex, Use
from buzz import Buzz
from prettyprinter import cpprint as cprint
import os


def sch_template(dict):
    base = Schema({
        'path': lambda x: isinstance(x, str) and '{}' in x,
        'range': Regex(r'[0-9]\s*,\s*[0-9]')
    }, ignore_extra_keys=True)
    if not base.is_valid(dict):
        return False
    template = dict['path']
    files = [template.format(i) for i in range(*eval(dict['range']))]
    dict['files'] = Schema(
        [lambda x:os.path.isfile(os.path.expanduser(x))]
    ).validate(files)
    return True


SCH_CONFIG = Schema(
    [
        Schema(
            {
                'time': Or(Regex('[0-1][0-9]:[0-5][0-9]'), Regex('[2][0-3]:[0-5][0-9]')),
                'files': [
                    # Either a file or a dict template3
                    lambda x:os.path.isfile(os.path.expanduser(x)),
                    Schema(
                        {'template': sch_template}
                    )
                ]
            }
        ),
    ]
)

DEFAULT_CONFIG = [
    {
        'time': '06:00',
        'files': [f'~/Pictures/Wallpapers/mojave_dynamic_{i}.jpeg' for i in range(1, 13)]
    },
    {
        'time': '20:00',
        'files': [{'template': {
                'path': '~/Pictures/Wallpapers/mojave_dynamic_{}.jpeg',
                'range': '13, 17'
        }}]
    }
]


def validate_config(config):
    config = SCH_CONFIG.validate(config)
    def unpack(files):
        for f in files:
            if isinstance(f, str):
                yield f
            if isinstance(f, dict):
                for f in f['template']['files']:
                    yield f
    config = map(
        lambda x: {
            'time': x['time'],
            'files': [x for x in unpack(x['files'])]},
        config
    )
    return list(config)

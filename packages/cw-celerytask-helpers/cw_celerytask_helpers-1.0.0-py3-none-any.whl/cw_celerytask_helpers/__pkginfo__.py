"""cw-celerytask-helpers packaging information"""

modname = 'cw_celerytask_helpers'
distname = 'cw-celerytask-helpers'

numversion = (1, 0, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Worker side helpers for cubicweb-celerytask'
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'celery': '~= 5.0',
    'redis': None,
}

classifiers = [
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
]

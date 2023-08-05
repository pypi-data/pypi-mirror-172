# Copyright 2016 Julien Danjou
# Copyright 2016 Joshua Harlow
# Copyright 2013-2014 Ray Holder
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import sys
import time

import six

# sys.maxint / 2, since Python 3.2 doesn't have a sys.maxint...
try:
    MAX_WAIT = sys.maxint / 2
except AttributeError:
    MAX_WAIT = 1073741823


if six.PY2:
    def capture(fut, tb):
        # TODO(harlowja): delete this in future, since its
        # has to repeatedly calculate this crap.
        fut.set_exception_info(tb[1], tb[2])

    def getargspec(func):
        # This was deprecated in Python 3.
        return inspect.getargspec(func)
else:
    def capture(fut, tb):
        fut.set_exception(tb[1])

    def getargspec(func):
        return inspect.getfullargspec(func)


def visible_attrs(obj, attrs=None):
    if attrs is None:
        attrs = {}
    for attr_name, attr in inspect.getmembers(obj):
        if attr_name.startswith("_"):
            continue
        attrs[attr_name] = attr
    return attrs


def find_ordinal(pos_num):
    # See: https://en.wikipedia.org/wiki/English_numerals#Ordinal_numbers
    if pos_num == 0:
        return "th"
    elif pos_num == 1:
        return 'st'
    elif pos_num == 2:
        return 'nd'
    elif pos_num == 3:
        return 'rd'
    elif pos_num >= 4 and pos_num <= 20:
        return 'th'
    else:
        return find_ordinal(pos_num % 10)


def to_ordinal(pos_num):
    return "%i%s" % (pos_num, find_ordinal(pos_num))


def get_callback_name(cb):
    """Get a callback fully-qualified name.

    If no name can be produced ``repr(cb)`` is called and returned.
    """
    segments = []
    try:
        segments.append(cb.__qualname__)
    except AttributeError:
        try:
            segments.append(cb.__name__)
            if inspect.ismethod(cb):
                try:
                    # This attribute doesn't exist on py3.x or newer, so
                    # we optionally ignore it... (on those versions of
                    # python `__qualname__` should have been found anyway).
                    segments.insert(0, cb.im_class.__name__)
                except AttributeError:
                    pass
        except AttributeError:
            pass
    if not segments:
        return repr(cb)
    else:
        try:
            # When running under sphinx it appears this can be none?
            if cb.__module__:
                segments.insert(0, cb.__module__)
        except AttributeError:
            pass
        return ".".join(segments)


try:
    now = time.monotonic  # noqa
except AttributeError:
    from monotonic import monotonic as now  # noqa

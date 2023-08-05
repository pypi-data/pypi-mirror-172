#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022
#             Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

import html
import pickle
import re
from hashlib import sha1

import latex2svg

# Extracted common code used by both doxygen.py and the m.math plugin to
# avoid dependency of doxygen.py on Pelican

# Modified params to use for math rendering
params = latex2svg.default_params.copy()
params.update({
    # Don't use libertine fonts as they mess up things. The latex xcolor
    # package version < 2.12 (the one on Ubuntu 16.04) has a bug that prevents
    # lowercase `f` being used for color names (uppercase works):
    # https://tex.stackexchange.com/a/274531. However, when replacing the
    # colors with CSS classes later (_class_mapping below), the hexadecimal
    # number needs to be lowercase again.
    'preamble': r"""
\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{gensymb}
\usepackage{newtxtext}

\usepackage{xcolor}
\definecolor{m-default}{HTML}{caFe03}
\definecolor{m-primary}{HTML}{caFe04}
\definecolor{m-success}{HTML}{caFe05}
\definecolor{m-warning}{HTML}{caFe06}
\definecolor{m-danger}{HTML}{caFe07}
\definecolor{m-info}{HTML}{caFe08}
\definecolor{m-dim}{HTML}{caFe09}
""",
    # Zoom the letters a bit to match page font size.
    # TODO dvisvgm 2.2.2 was changed to "avoid scientific notation of floating
    # point numbers" (https://github.com/mgieseki/dvisvgm/blob/3facb925bfe3ab47bf40d376d567a114b2bee3a5/NEWS#L90),
    # meaning the default precision (6) is now used for the decimal points, so
    # you'll often get numbers like 194.283203, which is a bit too much
    # precision. Could be enough to have 4 decimal points max, but that would
    # be too little for <2.2.2, where it would mean you get just 194.28. We
    # need to detect the version somehow and then apply reasonable precision
    # based on that.
    'dvisvgm_cmd': 'dvisvgm --no-fonts -Z 1.25',
    })

# Mapping from color codes to CSS classes. Keep in sync with m.plots.
_class_mapping = {
    ('fill=\'#cafe03\'', 'class=\'m-default\''),
    ('fill=\'#cafe04\'', 'class=\'m-primary\''),
    ('fill=\'#cafe05\'', 'class=\'m-success\''),
    ('fill=\'#cafe06\'', 'class=\'m-warning\''),
    ('fill=\'#cafe07\'', 'class=\'m-danger\''),
    ('fill=\'#cafe08\'', 'class=\'m-info\''),
    ('fill=\'#cafe09\'', 'class=\'m-dim\'')
}

# dvisvgm 1.9.2 (on Ubuntu 16.04) doesn't specify the encoding part. However
# that version reports broken "depth", meaning inline equations are not
# vertically aligned properly, so it can't be made to work 100% correct anyway.
_patch_src = re.compile(r"""<\?xml version='1\.0'( encoding='UTF-8')?\?>
<!-- This file was generated by dvisvgm \d+\.\d+\.\d+ -->
<svg height='(?P<height>[^']+)pt' version='1.1' viewBox='(?P<viewBox>[^']+)' width='(?P<width>[^']+)pt' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
""")

# dvisvgm 2.6 has a different order of attributes. According to the changelog,
# the SVGs can be now hashed, which hopefully means that the output won't
# change every second day again. Hopefully.
#
# dvisvgm 2.12 does not necessarily specify the patch version number.
_patch26_src = re.compile(r"""<\?xml version='1\.0' encoding='UTF-8'\?>
<!-- This file was generated by dvisvgm \d+\.\d+(\.\d+)? -->
<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='(?P<width>[^']+)pt' height='(?P<height>[^']+)pt' viewBox='(?P<viewBox>[^']+)'>
""")

# version ignored by all UAs, safe to drop https://stackoverflow.com/a/18468348
_patch_dst = r"""<svg{attribs} style="width: {width:.3f}em; height: {height:.3f}em;{style}" viewBox="{viewBox}">
<title>
{formula}
</title>
"""

# 1 pt is 1.333 px, base font size is 16px. TODO: make this configurable,
# remove the 1.25 scaling
_pt2em = 1.333333/16.0

_unique_src = re.compile(r"""(?P<name> id|xlink:href)='(?P<ref>#?)(?P<id>g\d+-\d+|page\d+)'""")
_unique_dst = r"""\g<name>='\g<ref>eq{counter}-\g<id>'"""

# Counter to ensure unique IDs for multiple SVG elements on the same page.
# Reset back to zero on start of a new page for reproducible behavior.
counter = 0

# Cache for rendered formulas (source formula sha1 -> (depth, svg data)). The
# counter is not included
_cache_version = 0
_cache = None

# Fetch cached formula or render it and add to the cache. The formula has to
# be already wrapped in $, $$ etc. environment.
def fetch_cached_or_render(formula):
    global _cache

    # Cache not used, pass through
    if not _cache:
        out = latex2svg.latex2svg(formula, params=params)
        return out['depth'], out['svg']

    hash = sha1(formula.encode('utf-8')).digest()
    if not hash in _cache[2]:
        out = latex2svg.latex2svg(formula, params=params)
        _cache[2][hash] = (_cache[1], out['depth'], out['svg'])
    else:
        _cache[2][hash] = (_cache[1], _cache[2][hash][1], _cache[2][hash][2])
    return (_cache[2][hash][1], _cache[2][hash][2])

def unpickle_cache(file):
    global _cache

    if file:
        with open(file, 'rb') as f:
            _cache = pickle.load(f)
    else:
        _cache = None

    # Reset the cache if not valid or not expected version
    if not _cache or _cache[0] != _cache_version:
        _cache = (_cache_version, 0, {})

    # Otherwise bump cache age
    else: _cache = (_cache[0], _cache[1] + 1, _cache[2])

def pickle_cache(file):
    global _cache

    # Don't save any file if there is nothing
    if not _cache or not _cache[2]: return

    # Prune entries that were not used
    cache_to_save = (_cache_version, _cache[1], {})
    for hash, entry in _cache[2].items():
        if entry[0] != _cache[1]: continue
        cache_to_save[2][hash] = entry

    with open(file, 'wb') as f:
        pickle.dump(cache_to_save, f)

# Patches the output from dvisvgm
def patch(formula, svg, depth, attribs):
    # patch away XML preamble and needless attributes, convert `pt` to `em`,
    # add vertical align for inline formulas and add additional attribs like
    # CSS classes to the <svg> element
    if depth is None: style = ''
    else: style = ' vertical-align: -{:.3f}em;'.format(depth*1.25)
    def repl(match):
        return _patch_dst.format(
            width=_pt2em*float(match.group('width')),
            height=_pt2em*float(match.group('height')),
            style=style,
            viewBox=match.group('viewBox'),
            attribs=attribs,
            formula=html.escape(formula))

    # There are two incompatible preambles, if the first fails try the second
    svg, found = _patch_src.subn(repl, svg)
    if not found:
        svg, found = _patch26_src.subn(repl, svg)
        assert found, "dvisgm preamble is incompatible with this version of m.css"

    # Make element IDs unique
    global counter
    counter += 1
    svg = _unique_src.sub(_unique_dst.format(counter=counter), svg)

    # Replace color codes with CSS classes
    for src, dst in _class_mapping: svg = svg.replace(src, dst)

    return svg

""" This module is generated by transpiling Haxe into Python and cleaning
the resulting code by hand, e.g. removing unused Haxe classes. To try it
yourself, clone https://github.com/hsluv/hsluv and run:

    haxe -cp haxe/src hsluv.Hsluv -python hsluv.py
"""

from __future__ import division
from functools import wraps as _wraps, partial as _partial  # unexport, see #17
import math as _math  # unexport, see #17


__version__ = '5.0.0'

_m = [[3.240969941904521, -1.537383177570093, -0.498610760293],
      [-0.96924363628087, 1.87596750150772, 0.041555057407175],
      [0.055630079696993, -0.20397695888897, 1.056971514242878]]
_min_v = [[0.41239079926595, 0.35758433938387, 0.18048078840183],
          [0.21263900587151, 0.71516867876775, 0.072192315360733],
          [0.019330818715591, 0.11919477979462, 0.95053215224966]]
_ref_y = 1.0
_ref_u = 0.19783000664283
_ref_v = 0.46831999493879
_kappa = 903.2962962
_epsilon = 0.0088564516
_hex_chars = "0123456789abcdef"


def _normalize_output(conversion):
    # as in snapshot rev 4, the tolerance should be 1e-11
    normalize = _partial(round, ndigits=11-1)

    @_wraps(conversion)
    def normalized(*args, **kwargs):
        color = conversion(*args, **kwargs)
        return tuple(normalize(c) for c in color)
    return normalized


def _distance_line_from_origin(line):
    v = _math.pow(line['slope'], 2) + 1
    return _math.fabs(line['intercept']) / _math.sqrt(v)


def _length_of_ray_until_intersect(theta, line):
    return line['intercept']\
         / (_math.sin(theta) - line['slope'] * _math.cos(theta))


def _get_bounds(l):
    result = []
    sub1 = _math.pow(l + 16, 3) / 1560896
    if sub1 > _epsilon:
        sub2 = sub1
    else:
        sub2 = l / _kappa
    _g = 0
    while _g < 3:
        c = _g
        _g = _g + 1
        m1 = _m[c][0]
        m2 = _m[c][1]
        m3 = _m[c][2]
        _g1 = 0
        while _g1 < 2:
            t = _g1
            _g1 = _g1 + 1
            top1 = (284517 * m1 - 94839 * m3) * sub2
            top2 = (838422 * m3 + 769860 * m2 + 731718 * m1)\
                * l * sub2 - (769860 * t) * l
            bottom = (632260 * m3 - 126452 * m2) * sub2 + 126452 * t
            result.append({'slope': top1 / bottom, 'intercept': top2 / bottom})
    return result


def _max_safe_chroma_for_l(l):
    bounds = _get_bounds(l)
    _hx_min = 1.7976931348623157e+308
    _g = 0
    while _g < 2:
        i = _g
        _g = _g + 1
        length = _distance_line_from_origin(bounds[i])
        if _math.isnan(length):
            _hx_min = length
        else:
            _hx_min = min(_hx_min, length)
    return _hx_min


def _max_chroma_for_lh(l, h):
    hrad = h / 360 * _math.pi * 2
    bounds = _get_bounds(l)
    _hx_min = 1.7976931348623157e+308
    _g = 0
    while _g < len(bounds):
        bound = bounds[_g]
        _g = (_g + 1)
        length = _length_of_ray_until_intersect(hrad, bound)
        if length >= 0:
            if _math.isnan(length):
                _hx_min = length
            else:
                _hx_min = min(_hx_min, length)
    return _hx_min


def _dot_product(a, b):
    _sum = 0
    _g1 = 0
    _g = len(a)
    while _g1 < _g:
        i = _g1
        _g1 = _g1 + 1
        _sum += a[i] * b[i]
    return _sum


def _from_linear(c):
    if c <= 0.0031308:
        return 12.92 * c

    return 1.055 * _math.pow(c, 5 / 12) - 0.055


def _to_linear(c):
    if c > 0.04045:
        return _math.pow((c + 0.055) / 1.055, 2.4)

    return c / 12.92


def _y_to_l(y):
    if y <= _epsilon:
        return y / _ref_y * _kappa

    return 116 * _math.pow(y / _ref_y, 1 / 3) - 16


def _l_to_y(l):
    if l <= 8:
        return _ref_y * l / _kappa

    return _ref_y * _math.pow((l + 16) / 116, 3)


def xyz_to_rgb(_hx_tuple):
    return (
        _from_linear(_dot_product(_m[0], _hx_tuple)),
        _from_linear(_dot_product(_m[1], _hx_tuple)),
        _from_linear(_dot_product(_m[2], _hx_tuple)))


def rgb_to_xyz(_hx_tuple):
    rgbl = (_to_linear(_hx_tuple[0]),
            _to_linear(_hx_tuple[1]),
            _to_linear(_hx_tuple[2]))
    return (_dot_product(_min_v[0], rgbl),
            _dot_product(_min_v[1], rgbl),
            _dot_product(_min_v[2], rgbl))


def xyz_to_luv(_hx_tuple):
    x = float(_hx_tuple[0])
    y = float(_hx_tuple[1])
    z = float(_hx_tuple[2])
    divider = x + 15 * y + 3 * z
    var_u = 4 * x
    var_v = 9 * y
    if divider != 0:
        var_u = var_u / divider
        var_v = var_v / divider
    else:
        var_u = float("nan")
        var_v = float("nan")
    l = _y_to_l(y)
    if l == 0:
        return (0, 0, 0)
    u = 13 * l * (var_u - _ref_u)
    v = 13 * l * (var_v - _ref_v)
    return (l, u, v)


def luv_to_xyz(_hx_tuple):
    l = float(_hx_tuple[0])
    u = float(_hx_tuple[1])
    v = float(_hx_tuple[2])
    if l == 0:
        return (0, 0, 0)
    var_u = u / (13 * l) + _ref_u
    var_v = v / (13 * l) + _ref_v
    y = _l_to_y(l)
    x = 0 - ((9 * y * var_u) / (((var_u - 4) * var_v) - var_u * var_v))
    z = (((9 * y) - (15 * var_v * y)) - (var_v * x)) / (3 * var_v)
    return (x, y, z)


def luv_to_lch(_hx_tuple):
    l = float(_hx_tuple[0])
    u = float(_hx_tuple[1])
    v = float(_hx_tuple[2])
    _v = (u * u) + (v * v)
    if _v < 0:
        c = float("nan")
    else:
        c = _math.sqrt(_v)
    if c < 1e-08:
        h = 0
    else:
        hrad = _math.atan2(v, u)
        h = hrad * 180.0 / _math.pi
        if h < 0:
            h = 360 + h
    return (l, c, h)


def lch_to_luv(_hx_tuple):
    l = float(_hx_tuple[0])
    c = float(_hx_tuple[1])
    h = float(_hx_tuple[2])
    hrad = h / 360.0 * 2 * _math.pi
    u = _math.cos(hrad) * c
    v = _math.sin(hrad) * c
    return (l, u, v)


def hsluv_to_lch(_hx_tuple):
    h = float(_hx_tuple[0])
    s = float(_hx_tuple[1])
    l = float(_hx_tuple[2])
    if l > 100-1e-7:
        return (100, 0, h)
    if l < 1e-08:
        return (0, 0, h)
    _hx_max = _max_chroma_for_lh(l, h)
    c = _hx_max / 100 * s
    return (l, c, h)


def lch_to_hsluv(_hx_tuple):
    l = float(_hx_tuple[0])
    c = float(_hx_tuple[1])
    h = float(_hx_tuple[2])
    if l > 100-1e-7:
        return (h, 0, 100)
    if l < 1e-08:
        return (h, 0, 0)
    _hx_max = _max_chroma_for_lh(l, h)
    s = c / _hx_max * 100
    return (h, s, l)


def hpluv_to_lch(_hx_tuple):
    h = float(_hx_tuple[0])
    s = float(_hx_tuple[1])
    l = float(_hx_tuple[2])
    if l > 100-1e-7:
        return (100, 0, h)
    if l < 1e-08:
        return (0, 0, h)
    _hx_max = _max_safe_chroma_for_l(l)
    c = _hx_max / 100 * s
    return (l, c, h)


def lch_to_hpluv(_hx_tuple):
    l = float(_hx_tuple[0])
    c = float(_hx_tuple[1])
    h = float(_hx_tuple[2])
    if l > 100-1e-7:
        return (h, 0, 100)
    if l < 1e-08:
        return (h, 0, 0)
    _hx_max = _max_safe_chroma_for_l(l)
    s = c / _hx_max * 100
    return (h, s, l)


def rgb_to_hex(_hx_tuple):
    h = "#"
    _g = 0
    while _g < 3:
        i = _g
        _g = _g + 1
        chan = float(_hx_tuple[i])
        c = _math.floor(chan * 255 + 0.5)
        digit2 = int(c % 16)
        digit1 = int((c - digit2) / 16)

        h += _hex_chars[digit1] + _hex_chars[digit2]
    return h


def hex_to_rgb(_hex):
    _hex = _hex.lower()
    ret = []
    _g = 0
    while _g < 3:
        i = _g
        _g = _g + 1
        index = i * 2 + 1
        _hx_str = _hex[index]
        digit1 = _hex_chars.find(_hx_str)
        index1 = i * 2 + 2
        str1 = _hex[index1]
        digit2 = _hex_chars.find(str1)
        n = digit1 * 16 + digit2
        ret.append(n / 255.0)
    return tuple(ret)


def lch_to_rgb(_hx_tuple):
    return xyz_to_rgb(luv_to_xyz(lch_to_luv(_hx_tuple)))


def rgb_to_lch(_hx_tuple):
    return luv_to_lch(xyz_to_luv(rgb_to_xyz(_hx_tuple)))


def _hsluv_to_rgb(_hx_tuple):
    return lch_to_rgb(hsluv_to_lch(_hx_tuple))


hsluv_to_rgb = _normalize_output(_hsluv_to_rgb)


def rgb_to_hsluv(_hx_tuple):
    return lch_to_hsluv(rgb_to_lch(_hx_tuple))


def _hpluv_to_rgb(_hx_tuple):
    return lch_to_rgb(hpluv_to_lch(_hx_tuple))


hpluv_to_rgb = _normalize_output(_hpluv_to_rgb)


def rgb_to_hpluv(_hx_tuple):
    return lch_to_hpluv(rgb_to_lch(_hx_tuple))


def hsluv_to_hex(_hx_tuple):
    return rgb_to_hex(hsluv_to_rgb(_hx_tuple))


def hpluv_to_hex(_hx_tuple):
    return rgb_to_hex(hpluv_to_rgb(_hx_tuple))


def hex_to_hsluv(s):
    return rgb_to_hsluv(hex_to_rgb(s))


def hex_to_hpluv(s):
    return rgb_to_hpluv(hex_to_rgb(s))


del division  # unexport, see #17

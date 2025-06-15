from django import template
import re

register = template.Library()


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value

    swear_patterns = [
        r'(?<!\w)([ХхHh][уyUuЮю][йiIyЙй])\w*',
        r'(?<!\w)([ПпPp][иiIИи][з3Zz][дdDДд])\w*',
        r'(?<!\w)([БбB6][лlLЛл][яяЯя])\w*',
        r'(?<!\w)([ЕеEe][бbB6])\w*',
        r'(?<!\w)([МмMm][уyUu][дdDДд])\w*',
        r'(?<!\w)([ГгGg][оОoO0][ввVvB8][ннNnИи])\w*',
        r'(?<!\w)([ЖжJj][оОoO0][ппPp])\w*',
    ]

    for pattern in swear_patterns:
        value = re.sub(
            pattern,
            lambda m: m.group(1)[0] + '*' * (len(m.group(1)) - 1) + '*' * (len(m.group()) - len(m.group(1))),
            value,
            flags=re.IGNORECASE
        )

    return value
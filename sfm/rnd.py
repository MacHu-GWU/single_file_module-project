# -*- coding: utf-8 -*-

"""
This module provides some easy function to generate random text from built-in 
templates.

- :func:`rand_str`: fixed-length string
- :func:`rand_hexstr`: fixed-length hex string
- :func:`rand_pwd`: random password
- :func:`rand_phone`: random phone number
- :func:`rand_ssn`: random ssn
- :func:`rand_email`: random email
"""

import random
import string

CHARSET_ALPHA_DIGITS = string.ascii_letters + string.digits
CHARSET_PASSWORD = CHARSET_ALPHA_DIGITS + "!@#$%^&*()"
CHARSET_HEXSTR_LOWER = "0123456789abcdef"
CHARSET_HEXSTR_UPPER = CHARSET_HEXSTR_LOWER.upper()
DOMAIN_SURFIX = ["com", "net", "org", "edu"]


def rand_str(length, allowed=CHARSET_ALPHA_DIGITS):
    """Generate fixed-length random string from your allowed character pool.

    :param length: total length of this string.
    :param allowed: allowed charset.

    Example::

        >>> import string
        >>> rand_str(32)
        H6ExQPNLzb4Vp3YZtfpyzLNPFwdfnwz6
    """
    res = list()
    for _ in range(length):
        res.append(random.choice(allowed))
    return "".join(res)


def rand_hexstr(length, lower=True):
    """Gererate fixed-length random hexstring, usually for md5.

    :param length: total length of this string.
    :param lower: use lower case or upper case.
    """
    if lower:
        return rand_str(length, allowed=CHARSET_HEXSTR_LOWER)
    else:
        return rand_str(length, allowed=CHARSET_HEXSTR_UPPER)


def rand_alphastr(length, lower=True, upper=True):
    """Generate fixed-length random alpha only string.
    """
    if lower is True and upper is True:
        return rand_str(length, allowed=string.ascii_letters)
    if lower is True and upper is False:
        return rand_str(length, allowed=string.ascii_lowercase)
    if lower is False and upper is True:
        return rand_str(length, allowed=string.ascii_uppercase)
    else:
        raise Exception


def rand_pwd(length):
    """Random Internet password.

    Example::

        >>> rand_pwd(12)
        TlhM$^jzculH
    """
    return rand_str(length, CHARSET_PASSWORD)


def rand_phone():
    """Random US phone number. (10 digits)

    Example::

        >>> rand_phone()
        (306)-746-6690
    """
    return "(%s)-%s-%s" % (rand_str(3, string.digits),
                           rand_str(3, string.digits),
                           rand_str(3, string.digits))


def rand_ssn():
    """Random SSN. (9 digits)

    Example::

        >>> rand_ssn()
        295-50-0178
    """
    return "%s-%s-%s" % (rand_str(3, string.digits),
                         rand_str(2, string.digits),
                         rand_str(4, string.digits))


def rand_email():
    """Random email.

    Usage Example::

        >>> rand_email()
        Z4Lljcbdw7m@npa.net
    """
    name = rand_str(random.randint(4, 14), string.ascii_lowercase) + \
           rand_str(random.randint(1, 4), string.digits)
    domain = rand_str(random.randint(2, 10), string.ascii_lowercase)
    surfix = random.choice(DOMAIN_SURFIX)
    return "%s@%s.%s" % (name, domain, surfix)


def rand_article(num_p=(4, 10), num_s=(2, 15), num_w=(5, 40)):
    """Random article text.

    Example::

        >>> rand_article()
        ...
    """
    article = list()
    for _ in range(random.randint(*num_p)):
        p = list()
        for _ in range(random.randint(*num_s)):
            s = list()
            for _ in range(random.randint(*num_w)):
                s.append(
                    rand_str(random.randint(1, 15), string.ascii_lowercase))
            p.append(" ".join(s))
        article.append(". ".join(p))
    return "\n\n".join(article)


# --- Just a simple API call for faker ---
try:
    import faker


    class SimpleFaker(object):
        def __init__(self, locale="en_US"):
            self.fake = faker.Factory.create(locale)


    simple_faker = SimpleFaker()
except:  # pragma: no cover
    pass


def set_locale(locale):
    simple_faker.fake = faker.Factory.create(locale=locale)


def first_name():
    return simple_faker.fake.first_name()


def last_name():
    return simple_faker.fake.last_name()


def name():
    return simple_faker.fake.name()


def address():
    return simple_faker.fake.address()


def company():
    return simple_faker.fake.company()

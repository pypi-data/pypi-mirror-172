import secrets
import string
from typing import Set

import deal

deal.activate()
deal.module_load(deal.pure)

from .candidate import Candidate
from .charspace import Charspace
from .constants import PASSWORD_LENGTH_MAX
from .exceptions import DumbValueError


@deal.safe
@deal.has("random")
@deal.pre(
    validator=lambda _: _.length <= PASSWORD_LENGTH_MAX,
    exception=DumbValueError,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: _.min_uppercase + _.min_lowercase + _.min_digits + _.min_specials
    <= _.length,
    exception=DumbValueError,
    message="You cannot request more characters than the password length.",
)
@deal.pre(
    validator=lambda _: _.length <= PASSWORD_LENGTH_MAX,
    exception=DumbValueError,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: _.length > 0,
    message="length must be greater than zero.",
    exception=DumbValueError,
)
@deal.ensure(
    lambda _: _.result.uppers >= _.min_uppercase,
    message="Not enough uppercase characters in result.",
)
@deal.ensure(
    lambda _: _.result.lowers >= _.min_lowercase,
    message="Not enough lowercase characters in result.",
)
@deal.ensure(
    lambda _: _.result.digits >= _.min_digits,
    message="Not enough digit characters in result.",
)
@deal.ensure(
    lambda _: _.result.specials >= _.min_specials,
    message="Not enough special characters in result.",
)
@deal.ensure(
    lambda _: _.allow_repeating or not _.result.has_repeating,
    message="Repeating characters are not allowed.",
)
@deal.ensure(
    lambda _: len(_.result) == _.length,
    message="The returned value len must equal the requested length.",
)
def search(
    *,
    length: int,
    min_uppercase: int,
    min_lowercase: int,
    min_digits: int,
    min_specials: int,
    blocklist: str,
    specials: str,
    allow_repeating: bool,
) -> Candidate:
    charspace_args = {
        "blocklist": blocklist,
    }
    if len(specials):
        charspace_args["extras"] = specials
    else:
        charspace_args["extras"] = string.punctuation

    charspace = Charspace(**charspace_args)
    try_password = Candidate("")

    while not all(
        [
            True
            and try_password.uppers >= min_uppercase
            and try_password.lowers >= min_lowercase
            and try_password.digits >= min_digits
            and try_password.specials >= min_specials
            and (allow_repeating or not try_password.has_repeating)
            and len(try_password) == length
        ]
    ):
        try_password = Candidate(
            generate(charset=charspace.charset, length=length)
        )

    return try_password


@deal.safe
@deal.has("random")
@deal.pre(
    validator=lambda _: _.length <= PASSWORD_LENGTH_MAX,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: _.length > 0,
    message="length must be greater than zero.",
)
@deal.pre(
    lambda _: len("".join(_.charset)) > 0,
    message="charset must have positive len.",
)
@deal.ensure(
    lambda _: len(_.result) == _.length,
    message="The returned value len must equal the requested length.",
)
@deal.ensure(
    lambda _: all(char in "".join(_.charset) for char in _.result),
    message="function return value must be "
    "composed of characters in the charset",
)
def generate(*, charset: Set[str], length: int) -> str:
    """Return a cryptographically secure password of len length using
    characters only from the given charset."""
    return "".join(secrets.choice("".join(charset)) for i in range(length))

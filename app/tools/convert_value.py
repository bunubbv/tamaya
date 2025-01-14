import re
import hashlib
import mimetypes
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

ph = PasswordHasher()
tag_patterns = {
    'details': re.compile(r'\s*feat\.?\s.*'),
    'bracket': re.compile(r'\s*\([^)]*[:;,][^)]*\)'),
    'year_month_day': re.compile(r'^(\d{4})[-., ]?(\d{1,2})[-., ]?(\d{1,2})$'),
    'year_month': re.compile(r'^(\d{4})[-., ]?(\d{1,2})$'),
    'year': re.compile(r'^(\d{4})$'),
}

def password_encode(password: str) -> str:
    return ph.hash(password)


def password_verify(hash_str: str, password: str) -> bool:
    try:
        ph.verify(hash_str, password)
        return True
    
    except InvalidHashError:
        return False
    
    except VerifyMismatchError:
        return False


def get_mime(path: str) -> str:
    """
    Returns the MIME type for a given file path.

    Args:
        path (str): The file path as a string.

    Returns:
        str: The MIME type of the file. Defaults to 'application/octet-stream' 
             if the MIME type cannot be determined.
    """

    mime_type = mimetypes.guess_type(path, strict=True)
    return mime_type[0] if mime_type and mime_type[0] else 'application/octet-stream'


def hash_str(*args) -> str:
    """
    Generate an MD5 hash string from the given arguments.

    Args:
        *args: A variable number of arguments to be included in the hash.
               Each argument will be converted to a string and concatenated.
    """

    try:
        return hashlib.md5(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''


def safe_list(extra, key, default='') -> str:
    """
    Safely retrieves the first value from a list stored in a dictionary by key.

    Args:
        extra (dict): A dictionary-like object to retrieve the value from.
        key (str): The key whose associated value is to be fetched.
        default (str, optional): The default value to return if the key is not 
                                 found or its value is not a non-empty list. Defaults to ''.

    """

    extra = dict(extra)
    value = extra.get(key, [])

    if isinstance(value, list) and value:
        return value[0]

    return default


def convert_date(date: int | str) -> tuple[str, int]:
    """
    Converts a date string or integer into a formatted date string and extracts the year.

    Args:
        date (int | str): The date to be converted.
            It can be an integer (e.g., 20230101) or a string (e.g., '2023-01-01').

    Returns:
        tuple[str, int]:
            str: date (YYYY-MM-DD, YYYY-MM, YYYY).
            int: The year as an integer (YYYY).
    """

    if isinstance(date, int):
        date = str(date)

    try:
        if match := tag_patterns['year_month_day'].match(date):
            year, month, day = match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}", int(year)

        if match := tag_patterns['year_month'].match(date):
            year, month = match.groups()
            return f"{year}-{month.zfill(2)}", int(year)

        if match := tag_patterns['year'].match(date):
            year = match.group(1)
            return year, int(year)
    except:
        return '', 0


def convert_artist(name: str) -> str:
    """
    Remove extra information from artist name to organize.

    Args:
        name (str): the artist name to be converted.

    Examples:
        >>> convert_artist('Artist (feat. Someone)')
        'Artist'

        >>> convert_artist('Band Name (Live; 2023)')
        'Band Name'

        >>> convert_artist('Solo Artist feat. Guest')
        'Solo Artist'
    """

    try:
        cleaned_name = tag_patterns['bracket'].sub('', name)
        cleaned_name = tag_patterns['details'].sub('', cleaned_name)
        return cleaned_name.strip()

    except:
        return ''

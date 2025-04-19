from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    parsed_url = urlparse(value)
    if parsed_url.netloc != "www.youtube.com" and parsed_url.netloc != "youtube.com":
        raise ValidationError("Ссылки разрешены только с домена youtube.com.")

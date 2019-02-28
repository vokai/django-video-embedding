# QUICK START

Django video embedding is a Python-Django library to have custom VideoField in models and custom VideoForm in forms.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install:

```bash
pip install https://github.com/vokai/django-video-embedding/
```

## Usage

```python
[settings.py] 
INSTALLED_APPS = (
    'django_video_embedding',
)


[models.py]
from embed_video.fields import EmbedVideoField

class Item(models.Model):
    video = VideoField()  # same like models.URLField()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

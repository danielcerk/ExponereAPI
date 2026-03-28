from PIL import Image
from io import BytesIO

from celery import shared_task

@shared_task()
def img_compression_task(img_path):

    img = Image.open(img_path)

    img = img.resize(
        (int(img.size[0] * 0.55), int(img.size[1] * 0.55)),
        Image.LANCZOS
    )

    buffer = BytesIO()

    img.save(
        buffer,
        format="PNG",
        optimize=True,
        quality=95
    )

    buffer.seek(0)

    return buffer
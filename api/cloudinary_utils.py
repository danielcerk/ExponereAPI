import uuid
import cloudinary.uploader
import cloudinary.api

from .utils import img_compression

ALLOWED_EXTENSIONS = {"pdf", "xml"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/xml",
    "text/xml"
}


ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif", "svg"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/svg+xml"
}


def upload_to_cloudinary_img(file):

    filename = getattr(file, "name", "")
    content_type = getattr(file, "content_type", "")

    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Arquivo inválido. Apenas imagens são permitidas.")

    if content_type and content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise ValueError("Tipo de arquivo inválido. Apenas imagens são permitidas.")

    img_compressed = img_compression(file)

    short_uuid = str(uuid.uuid4())[:8]

    result = cloudinary.uploader.upload(
        img_compressed,
        public_id=short_uuid,
        folder="exponere/photos",
        resource_type="image",
        overwrite=False
    )

    return result["secure_url"]


def delete_from_cloudinary_img(file_url: str):

    parts = file_url.split("/")
    filename = parts[-1]
    folder = parts[-2]
    public_id = f"{folder}/{filename.split('.')[0]}"

    return cloudinary.uploader.destroy(public_id, resource_type="image")

def upload_to_cloudinary_nf(file):

    filename = getattr(file, "name", "")
    content_type = getattr(file, "content_type", "")

    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:

        raise ValueError("Arquivo inválido. Apenas PDF e XML são permitidos.")

    if content_type and content_type not in ALLOWED_CONTENT_TYPES:

        raise ValueError("Tipo de arquivo inválido. Apenas PDF e XML são permitidos.")

    short_uuid = str(uuid.uuid4())[:8]

    result = cloudinary.uploader.upload(
        file,
        public_id=short_uuid,
        folder="exponere/nfs",
        resource_type="raw",
        overwrite=False
    )

    return result["secure_url"]


def delete_from_cloudinary_nf(file_url: str):

    parts = file_url.split("/")
    filename = parts[-1]
    folder = parts[-2]
    public_id = f"{folder}/{filename.split('.')[0]}"

    return cloudinary.uploader.destroy(public_id, resource_type="raw")
import uuid
import cloudinary.uploader
import cloudinary.api

from .utils import img_compression

def upload_to_cloudinary(file):

    img_compressed = img_compression(file)

    short_uuid = str(uuid.uuid4())[:8]

    result = cloudinary.uploader.upload(
        img_compressed,
        public_id=f"exponere/{short_uuid}",
        folder="exponere",
        resource_type="auto",
        overwrite=False
    )

    return result["secure_url"]

def delete_from_cloudinary(file_url: str):

    parts = file_url.split("/")
    filename = parts[-1]
    folder = parts[-2]
    public_id = f"{folder}/{filename.split('.')[0]}"

    return cloudinary.uploader.destroy(public_id)
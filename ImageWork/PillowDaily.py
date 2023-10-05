from io import BytesIO


def get_image_bytes(image):
    buf = BytesIO()
    image.save(buf, format='PNG')
    image = buf.getvalue()
    buf.close()

    return image
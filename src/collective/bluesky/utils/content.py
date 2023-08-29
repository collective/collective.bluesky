from Acquisition import aq_base
from collective.bluesky.interfaces import BlueskyBlob
from collective.bluesky.settings import IMAGE_WIDTH
from plone.dexterity.content import DexterityContent
from plone.scale.storage import IImageScaleStorage
from typing import Union
from zope.component import getMultiAdapter


__all__ = [
    "media_from_content",
]


IMAGE_ORDER = [
    ("opengraph_image_link", "image_caption", "relation"),
    ("opengraph_image", "image_caption", "field"),
    ("preview_image_link", "preview_caption_link", "relation"),
    ("preview_image", "preview_caption", "field"),
    ("image_link", "image_caption", "relation"),
    ("image", "image_caption", "field"),
]


def media_from_content(content: DexterityContent) -> Union[BlueskyBlob, None]:
    """Parse a content item and return a BlueskyBlob object."""
    content = aq_base(content)
    for field_name, field_caption, field_type in IMAGE_ORDER:
        title = content.title
        description = content.description
        # Image does not have an attribute image_caption
        if content.portal_type == "Image":
            caption = description
        else:
            caption = getattr(content, field_caption, None)
        field = getattr(content, field_name, None)
        if not field:
            continue
        if field_type == "relation":
            content = field.to_object
            caption = caption if caption else (content.description or content.title)
            field_name = "image"
            field = getattr(content, field_name, None)
        storage = getMultiAdapter((content, None), IImageScaleStorage)
        scale = storage.scale(fieldname=field_name, width=IMAGE_WIDTH)
        if scale and "data" in scale:
            data = scale["data"].data
            caption = caption if caption else title
            return BlueskyBlob(
                data=data, mime_type=field.contentType, caption=caption, size=len(data)
            )
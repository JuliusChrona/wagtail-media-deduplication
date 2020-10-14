from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class CustomImage(AbstractImage):
    duplicate = models.ForeignKey(
        'Duplicate',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='images'
    )

    admin_form_fields = Image.admin_form_fields + (
        'duplicate',
    )


class Duplicate(models.Model):
    title = models.CharField(max_length=256, unique=True)
    main_image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('title'),
        ImageChooserPanel('main_image')
    ]

    def __str__(self):
        return self.title


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    class  Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

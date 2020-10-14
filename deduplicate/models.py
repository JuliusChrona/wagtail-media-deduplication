from django.db import models
from django.db.models import Q
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            all_images = CustomImage.objects.filter(~Q(pk=self.pk))
            # a = signature(self.file.url) # пиктча с которой, сравнивают
            for image in all_images:
                print(image.duplicate)
                if image.duplicate:  # Здесь мог быть ваш код (for del)
                    break
            #     # dub_percnt = check_dup(a, image.file.url)
            #     # if dub_percnt <= 0.25:
            #     #     self.duplicate = image.duplicate
            #     #     break
            self.duplicate = image.duplicate
        super().save(force_insert, force_update, using,
                     update_fields)


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

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

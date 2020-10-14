from django.db import models
from django.db.models import Q
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from .hash_opencv import CalcImageHash, CompareHash


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
             update_fields=None, duplicate=None):
        if duplicate:
            self.duplicate = duplicate
        elif self.pk:
            all_images = CustomImage.objects.filter(~Q(pk=self.pk))
            path_to_site = '/home/kiryl/Test/test_site'
            saving_image_hash = CalcImageHash(path_to_site + self.file.url) # пиктча с которой, сравнивают
            for image in all_images:
                compared_image = CalcImageHash(path_to_site + image.file.url)
                print(CompareHash(saving_image_hash, compared_image) <= 15)
                if self.get_file_hash() == image.get_file_hash() or CompareHash(saving_image_hash, compared_image) <= 15:
                    # Если изображения дубликаты и у них нет объекта-списка дубликатов
                    # Создать новый объект-список дубликатов и занести изображения в него
                    if not image.duplicate:
                        duplicates = Duplicate.objects.all()
                        if duplicates:
                            title = duplicates.last().title.replace('Duplicate#', '')
                            title = 'Duplicate#' + str(int(title) + 1)
                        else:
                            title = 'Duplicate#1'
                        new_dupl = Duplicate.objects.create(title=title, main_image=self)
                        self.duplicate = new_dupl
                        image.duplicate = new_dupl
                        image.save(duplicate=new_dupl)  # Внести изображение в дубликаты
                    else:
                        self.duplicate = image.duplicate
                    break

        super().save(force_insert, force_update, using, update_fields)


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

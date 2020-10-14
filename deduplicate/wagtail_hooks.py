from django.db.models import Q
from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Duplicate, CustomImage


class DuplicateAddPermission(PermissionHelper):
    def user_can_create(self, request):
        return False


class DuplicateAdmin(ModelAdmin):
    model = Duplicate
    menu_label = 'Duplicate'
    menu_icon = 'image'
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'get_image', 'get_duplicates')
    permission_helper_class = DuplicateAddPermission

    def get_image(self, obj):
        if obj.main_image:
            return mark_safe(f'<img src={obj.main_image.file.url} width=200px style="height: 200px;">')
        else:
            return '-'

    def get_duplicates(self, obj):
        all_duplicates = obj.images.filter(~Q(id=obj.main_image.id))
        html_images = ''
        for duplicate in all_duplicates[:5]:
            html_images += f'<img src={duplicate.file.url} width=170px \
                            style="height: 150px; margin-top:25px; margin-left:5px;">'
        return mark_safe(html_images)

    get_duplicates.short_description = 'duplicates'
    get_image.short_description = 'image'


class CustomImageAdmin(ModelAdmin):
    model = CustomImage
    menu_label = 'Custom images'
    menu_icon = 'image'
    menu_order = 600
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'get_image', 'created_at', 'get_file_size')
    search_fields = ('title',)
    list_filter = ('duplicate',)

    def get_image(self, obj):
        print(dir(obj))
        return mark_safe(f'<img src={obj.file.url} width=200px style="height: 200px;">')

    get_image.short_description = 'image'


modeladmin_register(CustomImageAdmin)
modeladmin_register(DuplicateAdmin)

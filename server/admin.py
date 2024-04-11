from django.contrib import admin
from .models import ImageUpload, Places, Category, Image

class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview']  # Add fields to display in the list view

    def image_preview(self, obj):
        return obj.image.url if obj.image else None  # Display a preview of the image in the admin list

    image_preview.short_description = 'Image'  # Set the column header text

admin.site.register(ImageUpload, ImageUploadAdmin)

@admin.register(Places)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
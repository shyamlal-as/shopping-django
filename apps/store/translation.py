from modeltranslation.translator import translator, TranslationOptions
from .models import Product,Categories

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)

class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)

translator.register(Product, ProductTranslationOptions)
translator.register(Categories, CategoriesTranslationOptions)
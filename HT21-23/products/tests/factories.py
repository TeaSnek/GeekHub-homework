import factory

from products.models import Product, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('pystr', min_chars=8, max_chars=12)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_name = factory.Sequence(lambda i: f'product {i}')
    price = factory.Faker(
        'pyfloat',
        left_digits=3,
        right_digits=2,
        positive=True,
        min_value=1
    )
    sears_id = factory.Faker(
        'pystr_format',
        letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        string_format='?########'
    )
    short_about = factory.Faker('paragraph')
    brand = factory.Faker('company')
    sears_link = factory.LazyAttribute(lambda obj:
                                       f'https://www.sears.com/{obj.product_name.replace(" ", "-")}'
                                       f'/p-{obj.sears_id.lower()}')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.category.add(*extracted)

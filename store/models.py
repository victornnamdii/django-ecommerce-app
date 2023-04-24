from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(MPTTModel):
    """
    Category table redefined with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        max_length=255,
        help_text=_("Required"),
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"), max_length=255, unique=True
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    """
    Table for different types of Product
    """

    name = models.CharField(
        verbose_name=_("Product Type"),
        max_length=255,
        help_text=_("Required"),
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self) -> str:
        return self.name


class ProductSpecification(models.Model):
    """
    Table for Product specification
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Product Name"),
        max_length=255,
        help_text=_("Required"),
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """
    Table for Product items
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"), max_length=255, help_text=_("Required")
    )
    description = models.TextField(
        verbose_name=_("description"),
        max_length=255,
        help_text=_("Optional"),
        blank=True,
    )
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text=_("Maximum 9999999999.99"),
        verbose_name=_("Regular Price"),
        error_messages={
            "name": {
                "max_length": _(
                    "The price should be between 0 and 9999999999.99"
                ),
            },
        },
    )
    discount_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text=_("Maximum 9999999999.99"),
        verbose_name=_("Discount price"),
        error_messages={
            "name": {
                "max_length": _(
                    "The price should be between 0 and 9999999999.99"
                ),
            },
        },
    )
    use_discount = models.BooleanField(_("Use discount price?"), default=False)
    quantity = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        help_text=_("Change Product Visibility"),
        default=True,
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )
    users_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_wishlist",
        editable=False
    )

    price = models.DecimalField(
        _("Active Price"),
        max_digits=12,
        decimal_places=2,
        editable=False,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.is_active:
            pass
        else:
            self.is_active = self.quantity > 0
        if self.use_discount:
            self.price = self.discount_price
        else:
            self.price = self.regular_price
        super().save()


class ProductSpecificationValue(models.Model):
    """
    Product Specification Table value
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(
        ProductSpecification, on_delete=models.RESTRICT
    )
    value = models.CharField(
        verbose_name=_("value"),
        max_length=255,
        help_text=_("Product Specification value"),
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self) -> str:
        return self.value


class ProductImage(models.Model):
    """
    Table for the product's images
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to="images/",
        default="images/default.png",
        help_text=_("Upload a product image"),
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        max_length=255,
        help_text=_("Please add alternative text"),
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

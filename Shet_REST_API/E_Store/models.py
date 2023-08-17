from django.db import models
from UserProfile .models import UserProfile
from django.utils.timezone import now
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# Create your models here.


class Searche(models.Model):
    search_number = models.AutoField(primary_key=True)
    searches = models.CharField(max_length=1000, blank=False)

    def __int__(self):
        return self.search_number


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("id", )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("id", )

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # DecimalField(max_digits=30, decimal_places=2)
    old_price = models.PositiveIntegerField()
    # DecimalField(max_digits=30, decimal_places=2)
    price = models.PositiveIntegerField()
    discount = models.FloatField(default=0)
    description = models.TextField()
    created = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='shop/images')
    slug = models.CharField(max_length=1000, unique=True, blank=True)
    Ratings = models.CharField(max_length=500, default=0, blank=True)
    Total_Reviews = models.PositiveIntegerField(default=0, blank=True)
    In_Stock = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created", )

    def __str__(self):
        return self.product_name


def calculate_discount(sender, instance, *args, **kwargs):
    discount = ((instance.old_price - instance.price)/instance.old_price)*100
    instance.discount = discount
    print('wprked...')


def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("-product_id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().product_id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_product_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_product_reciever, sender=Product)
pre_save.connect(calculate_discount, sender=Product)


class StarRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    review = models.TextField(blank=True)
    reviewer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    stars = models.IntegerField(null=True, blank=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.reviewer.first_name + "" + self.reviewer.last_name + "" "rated" "" + str(self.stars) + "" "Stars."


def update_ratings(product):
    reviews = StarRating.objects.filter(product=product)
    tnr = reviews.count()
    star1 = reviews.filter(stars=1).count()
    star2 = reviews.filter(stars=2).count()
    star3 = reviews.filter(stars=3).count()
    star4 = reviews.filter(stars=4).count()
    star5 = reviews.filter(stars=5).count()
    UpdatedRatings = (5*(star5) + 4*(star4) + 3 *
                      (star3) + 2*(star2) + 1*(star1))/tnr
    UpdatedRatings = str(UpdatedRatings)
    if float(UpdatedRatings) >= 5:
        UpdatedRatings = 5.0
    Product.objects.filter(product_id=product).update(
        Ratings=UpdatedRatings, Total_Reviews=tnr)


def post_save_ratings_reciever(sender, instance, *args, **kwargs):
    update_ratings(instance.product.product_id)


post_save.connect(post_save_ratings_reciever, sender=StarRating)


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, default="")
    phone = models.CharField(max_length=12, default="")
    message = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

from django.db import models


# Create your models here.
class register(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.TextField(max_length=50)
    otp=models.IntegerField(blank=True,null=True)
    confirm_password=models.TextField(max_length=50)
    s_name=models.CharField(max_length=50,blank=True,null=True)
    education=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    phone=models.IntegerField(blank=True,null=True)
    image=models.ImageField(upload_to="images",blank=True,null=True)

    def __str__(self) -> str:
        return self.username
    

class product(models.Model):
    product_name=models.CharField(max_length=50)
    price=models.IntegerField()
    image=models.ImageField(upload_to='images')


    def __str__(self) -> str:
        return self.product_name


class contect_message(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.IntegerField()
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    
class wishlist_add(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE,blank=True,null=True)
    register=models.ForeignKey(register,on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to='images')
    product_name=models.CharField(max_length=50)
    price=models.IntegerField()

    def __str__(self) -> str:
        return self.product_name
    
class add_to_cart(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE,blank=True,null=True)
    register=models.ForeignKey(register,on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to='images')
    product_name=models.CharField(max_length=50)
    price=models.IntegerField()
    quantity=models.IntegerField()
    total=models.IntegerField()
    order_status=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.product_name
    
class checkout_page(models.Model):
    register=models.ForeignKey(register,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=50)
    phone=models.IntegerField()
    message=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self) -> str:
        return self.email


 
class user_review(models.Model):
    rating=models.IntegerField(choices=[(i,i) for i in range (1,6)])
    comments=models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.rating}"
    
class coupon(models.Model):
    coupon_code=models.CharField(max_length=50)
    discount=models.IntegerField()
    def __str__(self) -> str:
        return self.coupon_code


class user_coupon(models.Model):
    user=models.ForeignKey(register,on_delete=models.CASCADE)
    coupon=models.ForeignKey(coupon,on_delete=models.CASCADE)
    status=models.BooleanField(blank=True,null=True)



class order(models.Model):
    order_id=models.CharField(max_length=20)
    user=models.ForeignKey(register,on_delete=models.CASCADE)
    address=models.ForeignKey(checkout_page,on_delete=models.CASCADE)
    product=models.ManyToManyField(add_to_cart)
    total=models.IntegerField(blank=True,null=True)
    datetime=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    
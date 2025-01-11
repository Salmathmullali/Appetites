from django.db import models

# Create your models here.
class register(models.Model):
    reg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone_no=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    usertype=models.IntegerField(default=2)
    password=models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    id = models.ImageField(upload_to='user_id/', null=True, blank=True)

    def __str__(self):
        return str(self.reg_id)


class delivery_agent(models.Model):
    agent_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to='agent_pic/',null=True,blank=True)
    id_proof=models.ImageField(upload_to='agent_id/', blank=True, null=True)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    usertype=models.IntegerField(default=4)
    available=models.BooleanField(default=True)

    def __str__(self):
        return str(self.agent_id)



class surplus_food_supplier(models.Model):
    supplier_id=models.AutoField(primary_key=True)
    supplier_type=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    address=models.TextField(blank=True)
    phone_no = models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to='supplier_pic/',null=True,blank=True)
    id=models.ImageField(upload_to='supplier_id/',null=True,blank=True)
    usertype=models.IntegerField(default=3)
    status=models.BooleanField(default=False)


    def __str__(self):
        return str(self.supplier_id)

class supplier_surplus_food(models.Model):
    surplus_id=models.AutoField(primary_key=True)
    details = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    uploaded_on=models.DateField(auto_now_add=True)
    uploaded_time = models.CharField(max_length=100)
    time_expire = models.CharField(max_length=100)
    supplier_id=models.ForeignKey('surplus_food_supplier',on_delete=models.CASCADE,to_field='supplier_id')
    status=models.BooleanField(default=True)
    supply_status=models.BooleanField(default=False)


    def __str__(self):
        return str(self.surplus_id)

class surplus_requests(models.Model):
    req_id=models.AutoField(primary_key=True)
    surplus_id = models.ForeignKey('supplier_surplus_food', on_delete=models.CASCADE, to_field='surplus_id')
    user_id=models.ForeignKey('register', on_delete=models.CASCADE, to_field='reg_id')
    accepted_on=models.DateTimeField(auto_now_add=True)
    pickup_at = models.CharField(default='',max_length=100)
    pickup_status = models.BooleanField(default=False)
    delivered_at = models.CharField(default='',max_length=100)
    deliver_status = models.BooleanField(default=False)
    agent_id = models.ForeignKey('delivery_agent', on_delete=models.CASCADE, to_field='agent_id')
    request_status=models.BooleanField(default=True)

    def __str__(self):
        return str(self.req_id)


class complaints(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    complaint=models.TextField(blank=False)
    reply=models.TextField(default="",blank=True)
    reply_status=models.BooleanField(default=True)
    req_id = models.ForeignKey('surplus_requests', on_delete=models.CASCADE, to_field='req_id')

    def __str__(self):
        return str(self.complaint_id)

class feedbacks(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback=models.TextField(blank=False)
    reply=models.TextField(default="",blank=True)
    reply_status=models.BooleanField(default=True)
    req_id = models.ForeignKey('surplus_requests', on_delete=models.CASCADE, to_field='req_id')

    def __str__(self):
        return str(self.feedback_id)


from django.db import models
from django.contrib.auth.models import User


class role_type(models.Model):
    name  = models.CharField(max_length=100)
    code = models.PositiveIntegerField(unique=True)


    def __str__(self):
        return f'{self.name} - {self.code}'
    
class user_role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(role_type, on_delete=models.CASCADE, related_name='user_profiles')


    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'


#image model 
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    
    def __str__(self):
        return f'{self.user} - {self.profile_picture}'    
    


## for making the Dynimic menu 
class BaseContent(models.Model):
    ACTIVE_CHOICES = ((0, 'Inactive'), (2, 'Active'), (1, 'Migrated'), (3, "Archived"))
   
    active = models.PositiveIntegerField(choices=ACTIVE_CHOICES,default=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    class Meta:
        
        # Don't create a table in database, This table is abstract
       
        abstract = True

class Menus(BaseContent):
    #-------------------#
    # Menus module
    # parent is a foriegn key
    # slug field is used
    #--------------------#
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        "SEO friendly url, use only aplhabets and hyphen", max_length=60,unique=True)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING, related_name= 'children',blank=True, null=True)
    front_link = models.CharField(max_length=512, blank=True)
    backend_link = models.CharField(max_length=512, blank=True)
    icon = models.CharField(max_length=512, blank=True)
    order = models.IntegerField(null=True, blank=True)
    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'Menus' 

        
    def __str__(self):
        return self.name     


class RoleMainConfig(models.Model):
    Role =  models.ForeignKey(role_type, on_delete=models.CASCADE, related_name='user_role')
    Menu = models.ForeignKey(Menus, on_delete=models.CASCADE, related_name='menu_role') 

    Add = models.BooleanField(default=False)
    Edit = models.BooleanField(default=False)
    Delete = models.BooleanField(default=False)
    View = models.BooleanField(default=False)



    class Meta:
        unique_together = ('Role', 'Menu')



from django.db import models
from beneficiary.models import School

class UserSchoolMapping(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.school.School_Name}"
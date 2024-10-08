
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import role_type, user_role, profile,Menus ,RoleMainConfig , UserSchoolMapping
from .forms import UserCreationForm, UserUpdateForm

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserUpdateForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'profile_role' )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role', ),
        }),
    )

    def profile_role(self, obj):
        return obj.profile.role

    profile_role.short_description = 'Role'


@admin.register(Menus)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'front_link','active','modified_by')
    search_fields = ('name', 'front_link') 

@admin.register(RoleMainConfig)
class RoleMainConfigAdmin(admin.ModelAdmin):
    list_display = ('Role', 'Menu', 'Add', 'Edit', 'Delete', 'View')
    search_fields = ('Role__name', 'Menu__slug')  
    list_filter = ('Add', 'Edit', 'Delete', 'View')




class UserSchoolMappingAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')
    search_fields = ('user__username', 'school__School_Name')
    list_filter = ('school',)

admin.site.register(UserSchoolMapping, UserSchoolMappingAdmin)

    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(role_type)
admin.site.register(user_role)
admin.site.register(profile)


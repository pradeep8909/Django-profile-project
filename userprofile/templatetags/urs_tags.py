from django import template
from django.contrib.auth.decorators import login_required

from userprofile.models import Menus , RoleMainConfig,role_type, user_role,User
from django.core.cache import cache



register = template.Library()

@register.simple_tag
@login_required
def show_menu(request,user):
    user = request.user

    try:
        user_role_instance = user.profile  
        role = user_role_instance.role
        role_code = role.code

        request.session['role_code'] = role_code

        print(f"Logged-in User: {user.username} | Role: {role.name} | Role Code: {role_code}")

    except user_role.DoesNotExist:
        print("UserRole not found for the user.")
        return []
    if not role_code:
        print("No role_code found.")
        return []
    cache_key = f"menu_{role_code}"
    print(f"Generated Cache Key: {cache_key}")

    menu_items = cache.get(cache_key)
    if menu_items:
        print('Menu items retrieved from cache:', menu_items)
    else:
        print("Menu items not found in cache. Querying the database...")

    if not menu_items:
        role_menus = RoleMainConfig.objects.filter(Role=role, View=True).select_related('Menu')
        print(f"Retrieved RoleMenus: {list(role_menus)}")
        if not role_menus:
            print(f"No menu items found for role: {role.name}")
            return []
        menu_items = [role_menu.Menu for role_menu in role_menus]
        print(f"Menu items fetched from DB: {menu_items}")
        cache.set(cache_key, menu_items, 600)
        print("Menu items cached.")

    return menu_items
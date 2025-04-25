from django import template

register = template.Library()

@register.filter
def has_allowed_area(area_list, allowed_areas):
    """Verifica si el usuario pertenece a una de las áreas permitidas."""
    if not isinstance(area_list, list):
        return False
    allowed = [area.strip().lower() for area in allowed_areas.split(",")]
    user_areas = [area.lower() for area in area_list]
    return any(area in allowed for area in user_areas)

@register.filter
def has_allowed_rol(rol_list, allowed_rols):
    """Verifica si el usuario pertenece a uno de los roles permitidos."""
    if not isinstance(rol_list, list):
        return False
    allowed = [rol.strip().lower() for rol in allowed_rols.split(",")]
    user_rols = [rol.lower() for rol in rol_list]
    return any(rol in allowed for rol in user_rols)

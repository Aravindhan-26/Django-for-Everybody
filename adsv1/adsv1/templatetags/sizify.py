from django import template

register = template.Library()

def sizify(value):
    """
    Simple kb/mb/gb size snippet for templates:
    
    {{ product.file.size|sizify }}
    """
    value = int(value)
    if value < 512000:
        value /= 1024.0
        ext = 'Kb'
    elif value < 4194304000:
        value  /= (1024 ^ 2)
        ext = 'Mb'
    else:
        value /= (1024 ^ 3)
        ext = 'Gb'
    return f"{str(round(value, 2))} {ext}"

register.filter('sizify', sizify)
from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 1000
    if file.size > max_size_kb * 1024 :
        raise ValidationError(f'File cannot be larger than {max_size_kb}KB!') 

# def validate_meal(meal , restaurant):
#     if restaurant.id ==meal.restaurant_id:
#         return True   
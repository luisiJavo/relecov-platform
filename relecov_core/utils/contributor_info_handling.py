# <QueryDict: {'csrfmiddlewaretoken': ['9aFH0i0CpMRqBMO1ARh8AgWXR82w4LipM1XdGUqAPgZy7mRKv3CnXah5GZ4wFFvB'],
# 'hospital_name': ['nombre hospital'], 'admin_email': ['admin mail'],
# 'admin_telephone': ['654123211'], 'admin_position': ['Mega boss']}>


def get_data_from_form(request):
    contributor_info_dict = {}
    contributor_info_dict["hospital_name"] = request.POST["hospital_name"]
    contributor_info_dict["admin_email"] = request.POST["admin_email"]
    contributor_info_dict["admin_telephone"] = request.POST["admin_telephone"]
    contributor_info_dict["admin_position"] = request.POST["admin_position"]
    return contributor_info_dict

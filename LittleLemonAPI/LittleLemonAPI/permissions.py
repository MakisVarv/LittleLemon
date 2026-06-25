def is_manager(user):
    return user.is_authenticated and user.groups.filter(name="Manager").exists()


def is_delivery_crew(user):
    return user.is_authenticated and user.groups.filter(name="Delivery crew").exists()


def is_customer(user):
    return user.is_authenticated and not is_manager(user) and not is_delivery_crew(user)

from blog.forms import RegisterUserForm


def get_context_data(request):
    context = {
        'register': RegisterUserForm()
    }
    return context

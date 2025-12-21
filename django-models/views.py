from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Admin')
def admin_view(request):
    return render(request, 'Admin_view.html')

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Librarian')
def librarian_view(request):
    return render(request, 'Librarian_view.html')


@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Member')
def member_view(request):
    return render(request, 'Member_view.html')


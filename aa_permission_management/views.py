"""
Views for the AA Permission Management app.
"""

# Django
from django.shortcuts import render


def dashboard(request):
    """
    Render the dashboard for AA Permission Management.

    :param request:
    :type request:
    :return:
    :rtype:
    """

    return render(request, "aa_permission_management/views/dashboard.html")

def my_view(request):
    username = "alice"
    password = "p@ssw0rd"
    context = locals()
    return render(request, "my_template.html", context)

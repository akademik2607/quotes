from django.shortcuts import render


def show_form(request):
    monday_user_id = request.GET.get('muid', None)

    return render(request, 'form/index.html',
                  context= {
                      'mondey_user_id': monday_user_id
                  })


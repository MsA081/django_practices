from django.shortcuts import render

# فعلاً از FBV (Function Based View) استفاده می‌کنیم تا جریان را درک کنیم
def home(request):
    # 1. Logic: (مثلاً گرفتن آخرین اخبار)
    context = {
        'title': 'هومینو | خدمات آنلاین منزل',
        'user': request.user
    }
    # 2. Response: تحویل به تمپلیت
    return render(request, 'core/home.html', context)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dang_nhap, name='dang_nhap'),
    path('home/', views.index, name='Home'),
    path('giang_vien/', views.giang_vien, name='giang_vien'),
    path('lop_hoc/', views.lop_hoc, name='lop_hoc'),
    path('sinh_vien/', views.sinh_vien, name='sinh_vien'),
    path('lich_thi/', views.lich_thi, name='lich_thi'),
    path('xem_lich_thi/', views.xem_lich_thi, name='xem_lich_thi'),
    path('DS_giam_thi/', views.giam_thi, name='giam_thi'),
    path('lich_coi_thi/', views.lich_coi_thi, name='lich_coi_thi'),
    path('ds_mon_hoc/', views.ds_mon_hoc, name='ds_mon_hoc'),
    path('thong_tin_ca_nhan/', views.thong_tin_ca_nhan, name='thong_tin_ca_nhan'),
    path('sua_lich_thi/', views.sua_lich_thi, name='sua_lich_thi'),
    path('full_lop_hoc/', views.full_lop_hoc, name='full_lop_hoc'),
    path('thong_ke/', views.thong_ke, name='thong_ke'),
    path('gv_lop_hoc/', views.gv_lop_hoc, name='gv_lop_hoc'),
    path('gv_lich_thi/', views.gv_lich_thi, name='gv_lich_thi'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
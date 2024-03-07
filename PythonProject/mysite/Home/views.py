from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from connect_DB import connectSQL
from . import models, xuLyForm, taiDB
import pandas as pd
from django.shortcuts import redirect
from datetime import datetime, timedelta
import json
# from django.db import connection

# Create your views here.

def index(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    rp = request.POST.get
    if 'user' in request.session:
        if request.method == 'POST':
            # lấy các trường của form được gửi đến
            rp_keys = request.POST.keys()
            if 'ThemSV_Excel' in rp_keys:
                xuLyForm.them_tu_ecxel(request, cursor, 'file_ThemSV')
            elif 'ThemGT_Excel' in rp_keys:
                xuLyForm.them_tu_ecxel(request, cursor, 'file_ThemGT')
            elif 'new_pass' in rp_keys:
                trang_thai = xuLyForm.doi_mat_khau(request, cursor)
                cnxn.commit()
                my_context = {'user': request.session['user'], 'trang_thai': trang_thai}
                cnxn.close()
                return render(request, "pages/home.html", my_context)
                
        cnxn.commit()
        my_context = {'user': request.session['user']}
        cnxn.close()
        return render(request, "pages/home.html", my_context)
    else:
        return redirect('dang_nhap')

def ds_mon_hoc(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.method == "POST":
        if 'form_xoa' in request.POST.keys(): # form xóa môn học
            value = request.POST.get('ma_mon').split()
            xuLyForm.XL_form_xoa(value, cursor)
            cnxn.commit()
            cnxn.close()
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            return redirect('ds_mon_hoc')
        elif 'form1' in request.POST.keys(): # form thêm môn học từ nhập
            xuLyForm.xu_ly_form1(request, cursor)
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            cnxn.commit()
            cnxn.close()
            return redirect('ds_mon_hoc')
        elif 'ThemMH_Excel' in request.POST.keys(): # form thêm môn học từ Excel
            xuLyForm.them_tu_ecxel(request, cursor, 'file')
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            cnxn.commit()
            cnxn.close()
            return redirect('ds_mon_hoc')
        
    list_mon_hoc = taiDB.danh_sach_MH(cursor)
    my_context = {'MonHoc': list_mon_hoc, 'user': request.session['user']}
    if 'trang_thai' in request.session:
        my_context['trang_thai'] = request.session['trang_thai']
        del request.session['trang_thai']
    cnxn.close()
    return render(request, "pages/mon_hoc.html", my_context)

def giang_vien(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.method == "POST":
        if 'XoaGV' in request.POST.keys():
            try:
                value = request.POST.get('XoaGV').split()
                xuLyForm.XL_form_xoa(value, cursor)
                cnxn.commit()
                cnxn.close()
                request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
                return redirect('giang_vien')
            except:
                return ("not oke")
        elif 'form2' in request.POST.keys(): # form thêm giảng viên
            xuLyForm.xu_ly_form2(request, cursor)
            cnxn.commit()
            cnxn.close()
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            return redirect('giang_vien')
        elif 'ThemGV_Excel' in request.POST.keys():
            xuLyForm.them_tu_ecxel(request, cursor, 'file_ThemGV')
            cnxn.commit()
            cnxn.close()
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            return redirect('giang_vien')
    
    list_GV = taiDB.danh_sach_GV(cursor)
    cnxn.close()
    my_context = {'GiangVien': list_GV, 'user': request.session['user']}
    if 'trang_thai' in request.session:
        my_context['trang_thai'] = request.session['trang_thai']
        del request.session['trang_thai']
    return render(request, "pages/giang_vien.html", my_context)

def lop_hoc(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    rp_keys = request.POST.keys()
    rp = request.POST.get
    list_lop_hoc = []
    if request.method == 'POST':
        if 'form_xoa_1' in rp_keys:
            # xóa lớp từ mã lớp
            xuLyForm.XL_form_xoa(request.POST.get('ma_lop').split(), cursor)
            cnxn.commit()

            # lấy ra lớp học theo môn học 
            MaMH = request.POST.get('form_xoa_1')
            list_lop_hoc = taiDB.DS_lop_theo_mon(MaMH, cursor)

            # lấy tên theo mã môn học
            my_context = {'LopHoc': list_lop_hoc, 'TenMon': taiDB.tenMH_theoMaMH(rp('form_xoa_1'), cursor), 'user': request.session['user']}
            cnxn.close()
            return render(request, "pages/lop_hoc.html", my_context)
        value = request.POST.get('form_ds_lop')
        list_lop_hoc = taiDB.DS_lop_theo_mon(value, cursor)

    # lấy tên theo mã môn học, request.POST.get('form_ds_lop') sẽ trả về 1 mã môn học
    TenMon = taiDB.tenMH_theoMaMH((request.POST.get('form_ds_lop')), cursor)
    
    my_context = {'LopHoc': list_lop_hoc, 'TenMon': TenMon, 'user': request.session['user']}
    cnxn.close()
    return render(request, "pages/lop_hoc.html", my_context)

def dang_nhap(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    rp = request.POST.get
    if request.method == 'POST':
        u_name = rp('username')
        pwd = rp('password')
        cursor.execute("select * from taikhoan where taikhoan = '{}'".format(u_name))
        try:
            tk = models.TaiKhoan(*cursor.fetchone())
        except:
            my_context = {'user': 0}
            cnxn.close()
            return render(request, "pages/dang_nhap.html", my_context)
        if tk.matKhau == pwd:
            user = 0
            if tk.isAdmin == 1: user = "Admin"
            elif tk.isUser == 0: user = "SinhVien"
            elif tk.isUser == 1: user = "GiamThi"
            elif tk.isUser == 2: user = "GiangVien"
            cnxn.close()
            request.session['user'] = user
            request.session['username'] = u_name
            
            return redirect('Home')
        else:
            cnxn.close()
            my_context = {'user': "saiMK"}
            return render(request, "pages/dang_nhap.html", my_context)
        
    cnxn.close()
    request.session.pop('user', None)
    return render(request, "pages/dang_nhap.html")
    
def sinh_vien(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.method == "POST":
        if request.POST.get('MaLop'):
            query = "select * from SinhVien, DSLopHoc where SinhVien.MaSV = DSlophoc.MaSV and DSlophoc.MaLH = '{}'"
            query = query.format(request.POST.get('MaLop'))
            cursor.execute(query)
            listSV = []
            stt = 1
            for i in cursor.fetchall():
                sv = models.SinhVien(stt, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                listSV.append(sv)
                stt+=1
            cnxn.close()
            my_context = {'listSV': listSV, 'user': request.session['user']}
            return render(request, "pages/sinh_vien.html", my_context)
        elif 'ThemSV_Excel' in request.POST.keys():
            xuLyForm.them_tu_ecxel(request, cursor, 'file_ThemSV')
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            cnxn.commit()
            cnxn.close()
            return redirect('sinh_vien')

    
    query = "SELECT * FROM SinhVien"
    cursor.execute(query)
    listSV = []
    stt = 1
    for i in cursor.fetchall():
        sv = models.SinhVien(stt, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        listSV.append(sv)
        stt+=1
    my_context = {'listSV': listSV, 'user': request.session['user']}
    cnxn.close()
    if 'trang_thai' in request.session:
        my_context['trang_thai'] = request.session['trang_thai']
        del request.session['trang_thai']
    return render(request, "pages/sinh_vien.html", my_context)

def lich_thi(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    rq = request.POST.get
    if request.method == "POST":
        # lấy thông tin về ngày bắt đầu thi
        Ngay_BD_Thi = rq('ngay_bd_thi')
        # lấy thông tin về học kỳ
        HocKy = rq('HocKy')
        # Tạo danh sách môn thi
        cursor.execute("SELECT COUNT(*) FROM MonHoc")
        n = int(cursor.fetchone()[0])
        list_MonThi = []
        for i in range(1,n+1):
            mt = models.MonThi(1, rq(f'MaMH{i}'), rq(f'TenMH{i}'), rq(f'HinhThuc{i}'), rq(f'SoPhut{i}'))
            list_MonThi.append(mt)

        # lấy danh sách mã giám thị từ DB
        list_MaGiamThi = []
        cursor.execute("SELECT MaGT FROM GiamThi")
        for i in cursor.fetchall():
            list_MaGiamThi.append(i[0])

        # Xếp lịch thi
        list_LichThi = xuLyForm.xep_lich_thi(list_MonThi, list_MaGiamThi, Ngay_BD_Thi, HocKy)

        # thêm lịch thi vào db
        taiDB.add_DB_LichThi(list_LichThi, cursor)
        cnxn.commit()
        cnxn.close()
        my_context = {'list_LichThi': list_LichThi, 'HocKy': HocKy, 'Ngay_BD_Thi': Ngay_BD_Thi, 'user': request.session['user']}
        return render(request, "pages/xem_lich_thi.html", my_context)
    
    list_mon_hoc = taiDB.danh_sach_MH(cursor)
    my_context = {'MonThi': list_mon_hoc, 'user': request.session['user']}
    cnxn.close()
    return render(request, "pages/lich_thi.html", my_context)

def xem_lich_thi(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()

    list_LichThi = []
    user = request.session['user']
    username = request.session['username']
    stt_sv = {}
    dict_ma_lop = {}
    if user == "Admin":
        query = "SELECT * FROM LichThi"
    elif user == "SinhVien":
        query = f"select * from LichThi, DSLopHoc where DSLopHoc.MaSV = '{username}' and DSLopHoc.MaLH = LichThi.MaLH"
        cursor.execute(f"select * from (SELECT malh, masv, ROW_NUMBER() OVER (PARTITION BY malh ORDER BY masv) AS STT FROM dslophoc) as A where A.masv = '{username}'")
        
        for i in cursor.fetchall():
            stt_sv[i[0]] = i[2]
            dict_ma_lop[i[0]] = 0
    cursor.execute(query)
    stt = 1
    
    tmp_list = []
    for i in cursor.fetchall():
        i = i[:11]
        lt = models.LichThi(stt, *i)
        lt.set_NgayThi(Ngay(lt.NgayThi))
        if request.session['user'] == 'SinhVien':
            # tìm thứ tự của sinh viên trong danh sách lớp
            # nếu sĩ số lớp lớn hơn 40 và stt của sinh viên trong lớp lớn hơn int(sĩ số lớp /2) 
            # thì sinh viên thuộc tổ thi 2 của lớp đó
            dict_ma_lop[lt.MaLH] += lt.SoLuong
            if lt.MaLH not in tmp_list:
                if dict_ma_lop[lt.MaLH] >= stt_sv[lt.MaLH]:
                    list_LichThi.append(lt)
                    tmp_list.append(lt.MaLH)
                
            stt+=1
        else:
            list_LichThi.append(lt)
            stt+=1

    HocKy = 'None'
    if len(list_LichThi) != 0:
        HocKy = list_LichThi[0].HocKy
    my_context = {'list_LichThi': list_LichThi, 'HocKy': HocKy, 'user': request.session['user']}
    cnxn.close()
    return render(request, "pages/xem_lich_thi.html", my_context)

def giam_thi(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.method == "POST":
        if 'ThemGT_Excel' in request.POST.keys():
            xuLyForm.them_tu_ecxel(request, cursor, 'file_ThemGT')
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            cnxn.commit()
            cnxn.close()
            return redirect('giam_thi')
    query = "SELECT * FROM GiamThi"
    cursor.execute(query)
    list_tmp = cursor.fetchall()
    listGT = []
    stt = 1
    for i in list_tmp:
        gt = models.GiamThi(stt, *i)
        cursor.execute(f"SELECT COUNT(*) as total FROM LichThi WHERE MaGT1 = '{gt.MaGT}' or MaGT2 = '{gt.MaGT}'")
        gt.set_SoLopCoi(cursor.fetchone()[0])
        listGT.append(gt)
        stt+=1
    my_context = {'listGT': listGT, 'user': request.session['user']}
    cnxn.close()
    if 'trang_thai' in request.session:
        my_context['trang_thai'] = request.session['trang_thai']
        del request.session['trang_thai']
    return render(request, "pages/giam_thi.html", my_context)

def lich_coi_thi(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    values = request.session['username']
    query = f"select * from lichthi where lichthi.magt1 = '{values}' or lichthi.magt2 = '{values}'"
    cursor.execute(query)
    stt = 1
    list_LichThi = []
    for i in cursor.fetchall():
        i = i[:11]
        lt = models.LichThi(stt, *i)
        lt.set_NgayThi(Ngay(lt.NgayThi))
        list_LichThi.append(lt)
        stt+=1
    my_context = {'user': request.session['user'], 'list_LichThi': list_LichThi, 'HocKy': list_LichThi[0].HocKy}
    return render(request, "pages/lich_coi_thi.html", my_context)

def Ngay(input_date):
    year, month, day = map(int, input_date.split('-'))
    date_obj = datetime(year, month, day)
    output_date = date_obj.strftime("%d/%m/%Y") 
    return output_date

def dinh_dang_ngay(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    new_date_str = date_obj.strftime('%Y/%m/%d')
    return new_date_str

def thong_tin_ca_nhan(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.session['user'] == 'SinhVien':
        cursor.execute(f"select * from sinhvien where masv = '{request.session['username']}'")
        tmp = cursor.fetchone()[:8]
        sv  = models.SinhVien(1, *tmp)
        sv.set_NgaySinh(Ngay(sv.NgaySinh))
        my_context = {'user': request.session['user'], 'sinh_vien' : sv}
        return render(request, "pages/thong_tin_ca_nhan.html", my_context)
    elif request.session['user'] == 'GiangVien':
        cursor.execute(f"select * from giangvien where MaGV = '{request.session['username']}'")
        data = cursor.fetchone()
        gv = models.GiangVien('stt', *data)
        my_context = {'user': request.session['user'], 'giang_vien' : gv}
        return render(request, "pages/thong_tin_ca_nhan.html", my_context)
    else:
        pass

def sua_lich_thi(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.method == "POST":
        data = json.loads(request.POST['data'])
        list_LichThi = []
        for i in data:
            i = list(map(str.strip, i))
            print(i)
            try:
                lt = models.LichThi(i[0], 'a', *i[1:])
                print(lt.MaLH, lt.ToThi)
                list_LichThi.append(lt)
                # print(lt.MaLH, lt.PhongThi)
                query = f"UPDATE LichThi SET NgayThi = '{dinh_dang_ngay(lt.NgayThi)}', SoLuong = '{lt.SoLuong}', GioBD = '{lt.GioBD}', SoPhut = '{lt.SoPhut}', PhongThi = '{lt.PhongThi}', GhiChu = N'{lt.GhiChu}', MaGT1 = '{lt.MaGT1}', MaGT2 = '{lt.MaGT2}' WHERE MaLH = '{lt.MaLH}';"
                
                cursor.execute(query)
                cnxn.commit()
                request.session['trang_thai'] = "Cập nhật thông tin thành công!!!"
            except:
                pass
        cnxn.close()
        return redirect('sua_lich_thi')
    
    list_LichThi = []
    user = request.session['user']
    username = request.session['username']
    query = "SELECT * FROM LichThi"
    cursor.execute(query)
    stt = 1
    for i in cursor.fetchall():
        i = i[:11]
        lt = models.LichThi(stt, *i)
        lt.set_NgayThi(Ngay(lt.NgayThi))
        list_LichThi.append(lt)
        stt+=1

    HocKy = 'None'
    if len(list_LichThi) != 0:
        HocKy = list_LichThi[0].HocKy
    my_context = {'list_LichThi': list_LichThi, 'HocKy': HocKy, 'user': request.session['user']}
    if 'trang_thai' in request.session:
        my_context['trang_thai'] = request.session['trang_thai']
        del request.session['trang_thai']
    cnxn.close()
    return render(request, "pages/sua_lich_thi.html", my_context)

def full_lop_hoc(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    if request.method == "POST":
        if 'form3' in request.POST.keys(): # form thêm lớp học
            xuLyForm.xu_ly_form3(request, cursor)
            cnxn.commit()
            cnxn.close()
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            return redirect('full_lop_hoc')
        elif 'LopHoc_Excel' in request.POST.keys():
            xuLyForm.excel_dssv_lop(request, cursor, 'file_LopHoc')
            cnxn.commit()
            cnxn.close()
            request.session['trang_thai'] = "Cập nhật dữ liệu thành công!!!"
            return redirect('full_lop_hoc')
    query = "select * from lophoc"
    cursor.execute(query)
    stt = 1
    list_LH = []
    for i in cursor.fetchall():
        lh = models.LopHoc(stt, *i)
        list_LH.append(lh)
        stt += 1
    my_context = {'LopHoc': list_LH, 'user': request.session['user']}
    cnxn.close()
    if 'trang_thai' in request.session:
        my_context['trang_thai'] = request.session['trang_thai']
        del request.session['trang_thai']
    return render(request, "pages/full_ds_lop.html", my_context)

def thong_ke(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    list_LichThi = []
    if request.method == "POST":
        query = "select lichthi.* from lichthi, lophoc where lichthi.malh = lophoc.malh "
        if request.POST.get('ngay'):
            query += "and ngaythi = '" + dinh_dang_ngay(request.POST.get('ngay')) + "' "
        if request.POST.get('ma_gv'):
            query += "and magv = '" + request.POST.get('ma_gv') + "' "
        if request.POST.get('ten_phong'):
            query += "and PhongThi = '" + request.POST.get('ten_phong') + "' "
        if request.POST.get('ma_mh'):
            query += "and lophoc.MaMH = '" + request.POST.get('ma_mh') + "'"
        cursor.execute(query)
        stt = 1
        for i in cursor.fetchall():
            i = i[:11]
            lt = models.LichThi(stt, *i)
            lt.set_NgayThi(Ngay(lt.NgayThi))
            list_LichThi.append(lt)
            stt+=1

    cnxn.close()
    my_context = {'user': request.session['user'], 'list_LichThi': list_LichThi}
    return render(request, "pages/thong_ke.html", my_context)

def gv_lop_hoc(request):
    cnxn = connectSQL()
    cursor = cnxn.cursor()
    query = f"select * from lophoc where magv = '{request.session['username']}'"
    cursor.execute(query)
    list_LH = []
    stt = 1
    for i in cursor.fetchall():
        lh = models.LopHoc(stt, *i)
        stt+=1
        list_LH.append(lh)
    
    my_context = {'user': request.session['user'], 'LopHoc': list_LH, 'TenMon': taiDB.tenMH_theoMaMH(list_LH[0].MaMH, cursor)}
    cnxn.close()
    return render(request, "pages/gv_lop_hoc.html", my_context)

def gv_lich_thi(request):
    pass
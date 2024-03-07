
import random
from . import models
from connect_DB import connectSQL
from datetime import datetime, timedelta
import pandas as pd
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


def xu_ly_form1(request, cursor):
    lf_1 = ['ma_mon_hoc', 'ten_mon_hoc', 'so_tin_chi']
    rp = request.POST.get
    mh = models.MonHoc(1, rp(lf_1[0]), rp(lf_1[1]), rp(lf_1[2]))
    query = "INSERT INTO MonHoc VALUES (?, ?, ?)"
    values = (mh.MaMH, mh.TenMH, mh.SoTinChi)
    cursor.execute(query, values)


def xu_ly_form2(request, cursor):
    lf_2 = ['ma_giang_vien', 'ten_giang_vien',
            'so_dien_thoai', 'email', 'khoa', '0', 'mat_khau']
    rp = request.POST.get
    gv = models.GiangVien(1, rp(lf_2[0]), rp(lf_2[1]), rp(
        lf_2[2]), rp(lf_2[3]), rp(lf_2[4]), lf_2[5], rp(lf_2[6]))
    query = "INSERT INTO GiangVien VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (gv.MaGV, gv.TenGV, gv.SoDT, gv.Email,
              gv.Khoa, gv.TrangThai, gv.MatKhau)
    cursor.execute(query, values)


def xu_ly_form3(request, cursor):
    rp = request.POST.get
    lf_3 = ['ma_lop', 'ma_mon_hoc', 'nhom_mon_hoc',
            'so_luong', 'phong_hoc', 'ma_giang_vien']
    lh = models.LopHoc(1, rp(lf_3[0]), rp(lf_3[1]), rp(
        lf_3[2]), rp(lf_3[3]), rp(lf_3[4]), rp(lf_3[5]))
    query = "INSERT INTO LopHoc VALUES (?, ?, ?, ?, ?, ?)"
    values = (lh.MaLop, lh.MaMH, lh.NhomMH, lh.SoLuong, lh.PhongHoc, lh.MaGV)
    cursor.execute(query, values)


def XL_form_xoa(value, cursor):
    query = "delete from {} where {} = '{}'"
    query = query.format(*value)
    cursor.execute(query)


def excel_dssv_lop(request, cursor, tenForm):
    file = request.FILES[tenForm]
    excel_file = pd.ExcelFile(file, engine='openpyxl')
    sheet_names = excel_file.sheet_names
    query = ''
    # if tenForm == 'file_LopHoc':
    query = "INSERT INTO DSLopHoc VALUES (?, ?)"

    for sheet_name in sheet_names[1:]:
        df = pd.read_excel(excel_file, sheet_name)
        for index, row in df.iloc[1:].iterrows():
            try:
                listCol = [sheet_name, row[1]]
                cursor.execute(query, *listCol)
            except:
                pass


def them_tu_ecxel(request, cursor, tenForm):
    file = request.FILES[tenForm]
    excel_file = pd.ExcelFile(file, engine='openpyxl')
    sheet_names = excel_file.sheet_names
    query = ''
    if tenForm == 'file':
        query = "insert into MonHoc values (?, ?, ?)"
    elif tenForm == 'file_LopHoc':
        query = "INSERT INTO DSLopHoc VALUES (?, ?)"
        # nếu là file lớp học thì lấy từ sheet thứ 2 trở đi 
        # vì sheet đầu là danh sách lớp có trong file
        # từ sheet thứ 2 sẽ là danh sách sinh viên của từng lớp
        sheet_names = sheet_names[1:]
    elif tenForm == 'file_ThemGV':
        query = "INSERT INTO GiangVien VALUES (?, ?, ?, ?, ?, ?, ?)"
    elif tenForm == 'file_ThemSV':
        query = "INSERT INTO SinhVien VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif tenForm == 'file_ThemGT':
        query = "INSERT INTO GiamThi VALUES (?, ?, ?, ?, ?)"

    for sheet_name in sheet_names:
        df = pd.read_excel(excel_file, sheet_name)
        for index, row in df.iloc[1:].iterrows():
            try:
                listCol = row[df.columns[1:]]
                cursor.execute(query, *listCol)
            except:
                try:
                    query = "INSERT INTO LopHoc VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(query, *row[df.columns[1:]])
                except:
                    pass


def lay_monThi(list_MonThi, ma):
    for i in list_MonThi:
        if i.MaMT == ma:
            return i
    return 0

def tinhNgay(input_date, n):
    day, month, year = map(int, input_date.split('/'))
    date_obj = datetime(year, month, day)
    new_date = date_obj + timedelta(days=n)
    output_date = new_date.strftime("%d/%m/%Y")
    return output_date

def doi_mat_khau(request, cursor):
    taikhoan = request.session['username']
    old_pass = request.POST.get('old_pass')
    query = f"select matkhau from taikhoan where taikhoan = '{taikhoan}'"
    cursor.execute(query)
    matKhau = cursor.fetchone()
    if old_pass == matKhau[0]:
        re_new_pass = request.POST.get('re_new_pass')
        new_pass = request.POST.get('new_pass')
        if new_pass == old_pass:
            return "giong"
        elif new_pass == re_new_pass:
            query = f"UPDATE taikhoan SET matkhau = '{new_pass}' WHERE taikhoan = '{taikhoan}'"
            cursor.execute(query)
            cursor.commit()
            return "thanh_cong"
    return "fail"    

def tinhNgay_sql(input_date, n):
    day, month, year = map(int, input_date.split('/'))
    date_obj = datetime(year, month, day)
    new_date = date_obj + timedelta(days=n)
    output_date = new_date.strftime("%Y-%m-%d")
    return output_date

def xep_lich_thi(list_MonThi, list_MaGT, NgayBD_Thi, HocKy):
    cnxn = connectSQL()
    cursor = cnxn.cursor()

    # lấy danh sách lớp học và tách lớp học thành các tổ thi
    list_LopHoc = []
    cursor.execute("select * from lophoc")
    list_ToThi = []
    stt_to = 1
    for i in cursor.fetchall():
        lh = models.LopHoc(1, i[0], i[1], i[2], i[3], i[4], i[5])
        if len(list_LopHoc) >= 1:
            if lh.MaMH != list_LopHoc[-1].MaMH:
                stt_to = 1
        if lh.SoLuong > 40:
            sl = int(lh.SoLuong / 2)
            to_thi = models.ToThi(1, lh.MaLop, lh.MaMH, stt_to, sl, lh.MaGV)
            list_ToThi.append(to_thi)
            stt_to += 1
            to_thi = models.ToThi(2, lh.MaLop, lh.MaMH, stt_to, lh.SoLuong - sl, lh.MaGV)
            list_ToThi.append(to_thi)
            stt_to += 1
        else:
            to_thi = models.ToThi(1, lh.MaLop, lh.MaMH, stt_to, lh.SoLuong, lh.MaGV)
            list_ToThi.append(to_thi)
            stt_to += 1
        list_LopHoc.append(lh)
    # sắp xếp danh sách tổ thi theo mã môn học tăng dần, nếu mã môn học giống nhau thì xếp tăng dần theo thứ tự tổ thi
    list_ToThi.sort(key=lambda x: (x.MaMH, x.ToThi))
    list_LichThi = []
    # hàm random.shuffle() thực hiện trộn ngẫu nhiên danh sách
    random.shuffle(list_MaGT)
    # danh sách các ca thi trong một ngày
    list_Ca = ['7h', '9h', '14h', '16h']
    # sắp xếp danh sách môn thi theo mã môn thi
    list_MonThi = sorted(list_MonThi, key=lambda x: (x.MaMT))

    toThi_index = 0
    giamThi_index = 0
    ngayThi_index = 0
    monThi_index = 0
    oke = False
    while True:
        for ca in list_Ca:
            oke = False
            # lấy danh sách phòng trống theo từng ca của ngày
            # loại phòng 't' sẽ là phòng thường, 'm' là phòng máy
            loaiphong = 't'
            if list_MonThi[monThi_index].HinhThuc == 'Phòng máy':
                loaiphong = 'm'
            query = f"select * from phonghoc where ngay = '{tinhNgay_sql(NgayBD_Thi, ngayThi_index)}' and ca = '{ca}' and loaiphong = '{loaiphong}' and trangthai = '0'"
            cursor.execute(query)
            list_PhongThi = cursor.fetchall()
            for phong in list_PhongThi:
                phong_thi = models.Phong(*phong)
                lt = models.LichThi(toThi_index + 1, 
                                    HocKy, 
                                    list_ToThi[toThi_index].MaLop, 
                                    list_ToThi[toThi_index].ToThi, 
                                    list_ToThi[toThi_index].SoLuong, 
                                    tinhNgay(NgayBD_Thi, ngayThi_index), 
                                    ca, list_MonThi[monThi_index].SoPhut, phong_thi.tenPhong, list_MonThi[monThi_index].HinhThuc, 
                                    list_MaGT[giamThi_index],
                                    list_MaGT[giamThi_index+1])
                list_LichThi.append(lt)
                # mỗi tổ thi sẽ có 2 giám thị coi thi nên sau mỗi lần xếp index sẽ + 2
                giamThi_index += 2
                # nếu đã xếp đến 2 người cuối cùng trong danh sách giám thị thì thực hiện trộn ngẫu nhiên lại danh sách giám thị
                if giamThi_index > len(list_MaGT)-1:
                    giamThi_index = 0
                    random.shuffle(list_MaGT)
                
                toThi_index += 1
                # duyệt hết danh sách tổ thi thì trả về dạnh sách lịch thi
                if toThi_index >= len(list_ToThi):
                    return list_LichThi
                
                if toThi_index > 0:
                    # nếu xếp lịch thi cho một môn xong thì môn tiếp theo sẽ xếp vào ngày tiếp theo
                    # nghĩa là nếu xếp xong lịch thi cho tổ thi cuối cùng của một môn 
                    # nếu ngày đó vẫn còn ca trống thì cũng không thi môn tiếp theo
                    # mà môn tiếp theo sẽ được xếp vào ngày hôm sau
                    # việc xếp lịch thi bằng cách này sẽ đảm bảo mỗi sinh viên chỉ thi 1 ca 1 ngày
                    if list_ToThi[toThi_index].MaMH != list_ToThi[toThi_index-1].MaMH:
                        monThi_index += 1
                        oke = True
                        break
            if oke == True:
                break
        ngayThi_index += 1
        

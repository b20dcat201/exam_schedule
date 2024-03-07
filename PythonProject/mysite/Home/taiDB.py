
from . import models
from datetime import datetime

def danh_sach_MH(cursor):
    cursor.execute("SELECT * FROM MonHoc")
    list_mon_hoc = []
    stt = 1
    for i in cursor.fetchall():
        mh = models.MonHoc(stt, i[0], i[1], i[2])
        list_mon_hoc.append(mh)
        stt += 1
    return list_mon_hoc

def danh_sach_GV(cursor):
    query = "SELECT * FROM GiangVien"
    cursor.execute(query)
    list_GV = []
    stt = 1
    for i in cursor.fetchall():
        gv = models.GiangVien(stt, i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        list_GV.append(gv)
        stt += 1
    return list_GV

def DS_lop_theo_mon(value, cursor):
    list_lop_hoc = []
    query = "SELECT * FROM LopHoc WHERE MaMH = (?)"
    cursor.execute(query, (value))
    stt = 1
    for i in cursor.fetchall():
        lh = models.LopHoc(stt, i[0], i[1], i[2], i[3], i[4], i[5])
        list_lop_hoc.append(lh)
        stt += 1
    return list_lop_hoc

def tenMH_theoMaMH(value, cursor):
    cursor.execute("SELECT TenMH FROM MonHoc WHERE MaMH = (?)", value)
    TenMon = cursor.fetchone()
    return TenMon[0]

def dinh_dang_ngay(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    new_date_str = date_obj.strftime('%Y/%m/%d')
    return new_date_str

def add_DB_LichThi(list_LichThi, cursor):
    query = "INSERT INTO LichThi VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    for i in list_LichThi:
        values = [i.HocKy, i.MaLH, i.ToThi, i.SoLuong, dinh_dang_ngay(i.NgayThi), i.GioBD, i.SoPhut, i.PhongThi, i.GhiChu, i.MaGT1, i.MaGT2]
        cursor.execute(query, values)
        cursor.commit()
        # try:
        #     cursor.execute(query, *i)
        #     cursor.commit()
        # except:
        #     pass

def up_LichThi(cursor):
    list_tmp = []
    query = "SELECT * FROM LichThi"
    cursor.execute(query)
    for i in cursor.fetchall():
        lt = models.LichThi(1, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])
        list_tmp.append(lt)
    return list_tmp
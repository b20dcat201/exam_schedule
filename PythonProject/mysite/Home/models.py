from django.db import models

# Create your models here.
class MonHoc:
    def __init__(self, SoTT, MaMH, TenMH, SoTinChi) -> None:
        self.SoTT = SoTT
        self.MaMH = MaMH
        self.TenMH = TenMH
        self.SoTinChi = SoTinChi

    def __str__(self) -> str:
        return self.MaMH + " " + self.TenMH + " " + self.SoTinChi
    
class GiangVien:
    def __init__(self, SoTT, MaGV, TenGV, SoDT, Email, Khoa, TrangThai, MatKhau) -> None:
        self.SoTT = SoTT
        self.MaGV = MaGV
        self.TenGV = TenGV
        self.SoDT = SoDT
        self.Email = Email
        self.Khoa = Khoa
        self.TrangThai = TrangThai
        self.MatKhau = MatKhau

class LopHoc:
    def __init__(self, SoTT, MaLop, MaMH, NhomMH, SoLuong, PhongHoc, MaGV) -> None:
        self.SoTT = SoTT
        self.MaLop = MaLop 
        self.MaMH = MaMH
        self.NhomMH = NhomMH 
        self.SoLuong = SoLuong 
        self.PhongHoc = PhongHoc  
        self.MaGV = MaGV

    def __str__(self) -> str:
        return self.MaLop + " " + self.MaMH + " " + str(self.SoLuong) + " " + self.PhongHoc + " " + self.MaGV

class ToThi:
    def __init__(self, SoTT, MaLop, MaMH, ToThi, SoLuong, MaGV) -> None:
        self.SoTT = SoTT
        self.MaLop = MaLop 
        self.MaMH = MaMH
        self.ToThi = ToThi
        self.SoLuong = SoLuong
        self.MaGV = MaGV

    def __str__(self) -> str:
        return self.MaLop + " " + self.MaMH + " " + str(self.ToThi) + " " + str(self.SoLuong) + " " + self.MaGV

class SinhVien:
    def __init__(self, SoTT, MaSV, TenSV, NgaySinh, GioiTinh, SoDT, Nganh, Khoa, Email) -> None:
        self.SoTT = SoTT
        self.MaSV = MaSV
        self.TenSV = TenSV
        self.NgaySinh = NgaySinh
        self.GioiTinh = GioiTinh
        self.SoDT = SoDT
        self.Email = Email
        self.Nganh = Nganh
        self.Khoa = Khoa
    
    def set_NgaySinh(self, NgaySinh):
        self.NgaySinh = NgaySinh

class LichThi:
    def __init__(self, STT, HocKy, MaLH, ToThi, SoLuong, NgayThi, GioBD, SoPhut, PhongThi, GhiChu, MaGT1, MaGT2) -> None:
        self.STT = STT
        self.HocKy = HocKy
        self.MaLH = MaLH
        self.ToThi = ToThi
        self.SoLuong = SoLuong
        self.NgayThi = NgayThi
        self.GioBD = GioBD
        self.SoPhut = SoPhut
        self.PhongThi = PhongThi
        self.GhiChu = GhiChu
        self.MaGT1 = MaGT1
        self.MaGT2 = MaGT2
        
        
    def set_MaLH(self, MaLH):
        self.MaLH = MaLH

    def set_NgayThi(self, NgayThi):
        self.NgayThi = NgayThi
        
class MonThi:
    def __init__(self, SoTT, MaMT, TenMT, HinhThuc, SoPhut) -> None:
        self.HinhThuc = HinhThuc
        self.SoPhut = SoPhut
        self.MaMT = MaMT
        self.TenMT = TenMT
        self.SoTT = SoTT

class GiamThi:
    def __init__(self, SoTT, MaGT, TenGT, SoLopCoi, SDT, Email) -> None:
        self.MaGT = MaGT
        self.TenGT = TenGT
        self.SoLopCoi = SoLopCoi
        self.SDT = SDT
        self.Email = Email
        self.SoTT =SoTT

    def set_SoLopCoi(self, SoLopCoi):
        self.SoLopCoi = SoLopCoi

class TaiKhoan:
    def __init__(self, taiKhoan, matKhau, isAdmin, isUser) -> None:
        self.taiKhoan = taiKhoan
        self.matKhau = matKhau
        self.isAdmin = isAdmin
        self.isUser = isUser

class Phong:
    def __init__(self, tenPhong, sucChua, ngay, ca, loaiphong, trangThai) -> None:
        self.tenPhong = tenPhong
        self.sucChua = sucChua
        self.ngay = ngay
        self.ca = ca
        self.loaiPhong = loaiphong
        self.trangThai = trangThai
    
    def __str__(self) -> str:
        return self.tenPhong + " " + str(self.sucChua) + " " + self.ngay + " " + self.ca + " " + self.loaiPhong + " " + str(self.trangThai)


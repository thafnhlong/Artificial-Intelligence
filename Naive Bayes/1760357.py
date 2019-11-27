global DanhSachTruongHop
DanhSachTruongHop = {}

global TapDuLieu
TapDuLieu = {}
TapDuLieu['danhSachNam'] = []
TapDuLieu['soLuongCoDoc'] = 0
TapDuLieu['soLuongAnDuoc'] = 0

global NaiveBayes
NaiveBayes = {}
NaiveBayes['xacSuatKhongDoc'] = 0
NaiveBayes['xacSuatCoDoc'] = 0
NaiveBayes['lopKhongDoc'] = {}
NaiveBayes['lopCoDoc'] = {}

def xuLyNamTheoLop(Nam,refdata,refdataother):
    
    Nam = Nam.copy()
    Nam.pop('loaiNam')
    for thuoctinh,giatri in Nam.items():
        if thuoctinh not in refdata:
            refdata[thuoctinh] = {}
        if giatri not in refdata[thuoctinh]:
            refdata[thuoctinh][giatri] = 0
            
        if thuoctinh not in refdataother:
            refdataother[thuoctinh] = {}
        if giatri not in refdataother[thuoctinh]:
            refdataother[thuoctinh][giatri] = 0
        
        refdata[thuoctinh][giatri] += 1

def phanTachNam(Nam):
    
    for thuoctinh,giatri in Nam.items():
    
        if thuoctinh == 'loaiNam':
            if giatri == 'e' :
                TapDuLieu['soLuongAnDuoc'] += 1
                xuLyNamTheoLop(Nam,NaiveBayes['lopKhongDoc'],NaiveBayes['lopCoDoc'])
            else :
                TapDuLieu['soLuongCoDoc'] += 1   
                xuLyNamTheoLop(Nam,NaiveBayes['lopCoDoc'],NaiveBayes['lopKhongDoc'])
            TapDuLieu['danhSachNam'].append(Nam)
            continue
        
        if thuoctinh not in DanhSachTruongHop:
            DanhSachTruongHop[thuoctinh] = []
        if giatri not in DanhSachTruongHop[thuoctinh]:
            DanhSachTruongHop[thuoctinh].append(giatri)
        
def tinhToanXacSuat():
    NaiveBayes['xacSuatKhongDoc'] = 1.0 * (TapDuLieu['soLuongAnDuoc'] + 1) / (TapDuLieu['soLuongCoDoc'] + TapDuLieu['soLuongAnDuoc'])
    NaiveBayes['xacSuatCoDoc'] = 1.0 * (TapDuLieu['soLuongCoDoc'] + 1) / (TapDuLieu['soLuongCoDoc'] + TapDuLieu['soLuongAnDuoc'])
    
    for thuoctinh,giatri in NaiveBayes['lopKhongDoc'].items():
        for tengiatri,soluong in giatri.items():
            m = NaiveBayes['lopKhongDoc'][thuoctinh][tengiatri]
            k = len(DanhSachTruongHop[thuoctinh])
            NaiveBayes['lopKhongDoc'][thuoctinh][tengiatri] = 1.0 * (m+1) / (TapDuLieu['soLuongAnDuoc'] + k)
    
    for thuoctinh,giatri in NaiveBayes['lopCoDoc'].items():
        for tengiatri,soluong in giatri.items():
            m = NaiveBayes['lopCoDoc'][thuoctinh][tengiatri]
            k = len(DanhSachTruongHop[thuoctinh])
            NaiveBayes['lopCoDoc'][thuoctinh][tengiatri] = 1.0 * (m+1) / (TapDuLieu['soLuongCoDoc'] + k)

def layDuLieu(str):
    arr = str.replace('\n','').split(',')
    Nam = {}
    Nam['loaiNam'] = arr[0]
    Nam['hinhDang'] = arr[1]
    Nam['beMat'] = arr[2]
    Nam['mauSac'] = arr[3]
    Nam['vetTham'] = arr[4]
    Nam['muiHuong'] = arr[5]
    Nam['mauBaoTu'] = arr[6]
    Nam['phanBo'] = arr[7]
    Nam['moiTruong'] = arr[8]
    return Nam


def layXacSuatTheoLop(Nam,refdata):
    p = 1.0
    Nam = Nam.copy()
    Nam.pop('loaiNam')
    for thuoctinh,giatri in Nam.items():
        p *= refdata[thuoctinh][giatri]
    return p
def kiemTraMauNam(Nam):
    pce = layXacSuatTheoLop(Nam,NaiveBayes['lopKhongDoc']) * NaiveBayes['xacSuatKhongDoc']
    pcp = layXacSuatTheoLop(Nam,NaiveBayes['lopCoDoc']) * NaiveBayes['xacSuatCoDoc']
    return (pce,pcp)

def huanLuyen(path):
    f = open(path,'r')
    dulieu = f.readlines()
    f.close()
    for line in dulieu:
        if line.isspace(): 
            continue 
        Nam = layDuLieu(line)
        phanTachNam(Nam)
        
    tinhToanXacSuat()





huanLuyen('mush_room_dataset/mushroom_test_short.csv')

NamMoi = layDuLieu('~,x,f,n,t,n,n,v,d')
pce,pcp = kiemTraMauNam(NamMoi)
print('pce: ',pce,'pcp: ', pcp)
if pce>pcp:
    print('Nam an duoc')
else:
    print('Nam doc')

#print(TapDuLieu)
#print(DanhSachTruongHop)
#print(NaiveBayes)

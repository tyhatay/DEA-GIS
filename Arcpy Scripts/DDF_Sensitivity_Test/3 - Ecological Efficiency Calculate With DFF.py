#-*coding:mbcs*-#
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Orman Yollarinin Fonksiyonel Duruma Bagli Etkinlik Skorlarinin Belirlenmesi (Tubitak 1002 - Proje No. 122O785)
#  @author: Ars. Gor. Taha Yasin HATAY (ArresT)
#  DDF Testi eklendi: Fare & Grosskopf (2000) - Reviewer 1 yaniti icin
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import arcpy
import os
import sys
import numpy as np
from scipy.optimize import fmin_slsqp, linprog
import pandas as pd

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

##########################################################################################################
#Girisler
##########################################################################################################
Workspace = arcpy.GetParameterAsText(0)
Ekolojik_Etkinlik_Tablosu = arcpy.GetParameterAsText(1)
yol_name = arcpy.GetParameterAsText(2)
input_name = arcpy.GetParameterAsText(3)
if input_name == '#' or not input_name:
    input_name = "baki_puani, Yamac_Egimi, Yol_Genisligi, Kazi_Yukseklik, Kayip_Orman, Sev_Heyelan"
output_name = arcpy.GetParameterAsText(4)
if output_name == '#' or not output_name:
    output_name = "Akarsu, Sanat_Yapisi, Baglanti_Alan"

##########################################################################################################
#Cikislar
##########################################################################################################
ALL_Layer = arcpy.GetParameterAsText(5)
etkinlik_matrisi_Layer = arcpy.GetParameterAsText(6)
normalize_tablo_Layer = arcpy.GetParameterAsText(7)
korelasyon_table_Layer = arcpy.GetParameterAsText(8)
Ekolojik_Etkinlik_Analiz_Layer = arcpy.GetParameterAsText(9)
Ekolojik_Etkinlik_Target_Etkin_Layer = arcpy.GetParameterAsText(10)
Ekolojik_Etkinlik_Target_Etkin_Olmayan_Layer = arcpy.GetParameterAsText(11)

##########################################################################################################
# Analize girecek veriler icin normalize veri tablosunun acilmasi
##########################################################################################################
arcpy.TableToTable_conversion(Ekolojik_Etkinlik_Tablosu, Workspace, "Normalize_Veri_Tablosu", "", "", "")
normalize_tablo = Workspace + r"\\Normalize_Veri_Tablosu"
arcpy.TableToTable_conversion(Ekolojik_Etkinlik_Tablosu, Workspace, "girdi_cikti_verileri", "", "", "")
girdi_cikti_verileri = Workspace + r"\\girdi_cikti_verileri"

##########################################################################################################
# 1 km orman yollarina gore ayarlanacak verilerin yol uzunluguna bolunmesi
##########################################################################################################
carpim_listesi = ["Kayip_Orman", "Sev_Heyelan", "Sanat_Yapisi", "Baglanti_Alan"]
existing_fields = [field.name for field in arcpy.ListFields(normalize_tablo)]
fields_to_process = [field for field in carpim_listesi if field in existing_fields]
if not fields_to_process:
    arcpy.AddError("Belirtilen sutunlar tabloda bulunamadi.")
    sys.exit(1)
    
with arcpy.da.UpdateCursor(normalize_tablo, fields_to_process + ["VZA_uzunluk"]) as cursor:
    for row in cursor:
        for i in range(len(fields_to_process)):
            row[i] = row[i] * 1000 / row[-1] if row[-1] != 0 else 0
        cursor.updateRow(row)
        
##########################################################################################################
# Normalize min max degerleri
##########################################################################################################
alanlar_min_max = {
    "baki_puani": {"min": 0, "max": 1},
    "Yamac_Egimi": {"min": 0, "max": 100},
    "Yol_Genisligi": {"min": 3, "max": 10},
    "Kazi_Yukseklik": {"min": 0, "max": 20},
    "Kayip_Orman": {"min": 0, "max": 10},
    "Sev_Heyelan": {"min": 0, "max": 10},
    "Akarsu": {"min": 0, "max": 800},
    "Sanat_Yapisi": {"min": 0, "max": 20},
    "Baglanti_Alan": {"min": 1, "max": 10}
}

##########################################################################################################
# Normalizasyon
##########################################################################################################
with arcpy.da.UpdateCursor(normalize_tablo, list(alanlar_min_max.keys())) as cursor:
    for row in cursor:
        for i, alan in enumerate(list(alanlar_min_max.keys())):
            min_value = alanlar_min_max[alan]["min"]
            max_value = alanlar_min_max[alan]["max"]
            normalized_value = 0.00001 + (row[i] - min_value) / (max_value - min_value)
            row[i] = normalized_value
        cursor.updateRow(list(row))

##########################################################################################################
# Korelasyon
##########################################################################################################
alan_isimleri = [field.name for field in arcpy.ListFields(normalize_tablo)]
korelasyondata = [row for row in arcpy.da.SearchCursor(normalize_tablo, alan_isimleri)]
korelasyon_verileri = pd.DataFrame(korelasyondata, columns=alan_isimleri)
del korelasyon_verileri['OBJECTID']
del korelasyon_verileri['Shape_Length']
del korelasyon_verileri['VZA_uzunluk']
korelasyon_matrisi = korelasyon_verileri.corr()

csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
korelasyon_matrisi.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "Korelasyon_Matrisi")
arcpy.Delete_management(csv_path1)
korelasyon_table_path = Workspace + r"\\Korelasyon_Matrisi"
arcpy.management.AlterField(korelasyon_table_path, "Field1", "Degiskenler", "Degiskenler")

##########################################################################################################
# Girdi ve cikti sutunlarinin ayarlanmasi
##########################################################################################################
input_fields = input_name.split(', ')
output_fields = output_name.split(', ')
names_field = yol_name

input_count = len(input_fields)
output_count = len(output_fields)

fields = arcpy.ListFields(normalize_tablo)
field_names = [field.name for field in fields]

for field in input_fields + output_fields:
    if field not in field_names:
        arcpy.AddError("Minimize Target Field ve Maximize Target Field ile Feature Tablosu uyum saglamiyor")
        sys.exit()

X = np.empty((0, len(input_fields)), float)
y = np.empty((0, len(output_fields)), float)
names = []

with arcpy.da.SearchCursor(normalize_tablo, input_fields + output_fields + [names_field]) as cursor:
    for row in cursor:
        X = np.append(X, [np.array([row[i] for i in range(len(input_fields))])], axis=0)
        y = np.append(y, [np.array([row[i] for i in range(len(input_fields), len(input_fields) + len(output_fields))])], axis=0)
        names.append(row[-1])

xy = np.hstack((X, y))
data = pd.DataFrame(xy, index=names, columns=input_fields + output_fields)

if (data == 0).any().any() or data.isnull().any().any():
    arcpy.AddError("Hata: Verilerinizde 0 degeri bulunmaktadir!")
    sys.exit(1)

##########################################################################################################
# VZA (DEA) CLASS - ORIJINAL CCR MODELI (degismedi)
##########################################################################################################
class DEA(object):
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.n = inputs.shape[0]
        self.m = inputs.shape[1]
        self.r = outputs.shape[1]
        self.unit_ = range(self.n)
        self.input_ = range(self.m)
        self.output_ = range(self.r)
        self.output_w = np.zeros((self.r, 1), dtype=np.float)
        self.input_w = np.zeros((self.m, 1), dtype=np.float)
        self.lambdas = np.zeros((self.n, 1), dtype=np.float)
        self.efficiency = np.zeros_like(self.lambdas)
        self.names = []

    def __efficiency(self, unit):
        denominator = np.dot(self.inputs, self.input_w)
        numerator = np.dot(self.outputs, self.output_w)
        return (numerator / denominator)[unit]

    def __target(self, x, unit):
        in_w, out_w, lambdas = x[:self.m], x[self.m:(self.m + self.r)], x[(self.m + self.r):]
        denominator = np.dot(self.inputs[unit], in_w)
        numerator = np.dot(self.outputs[unit], out_w)
        return numerator / denominator

    def __constraints(self, x, unit):
        in_w, out_w, lambdas = x[:self.m], x[self.m:(self.m + self.r)], x[(self.m + self.r):]
        constr = []
        for input in self.input_:
            t = self.__target(x, unit)
            lhs = np.dot(self.inputs[:, input], lambdas)
            cons = t * self.inputs[unit, input] - lhs
            constr.append(cons)
        for output in self.output_:
            lhs = np.dot(self.outputs[:, output], lambdas)
            cons = lhs - self.outputs[unit, output]
            constr.append(cons)
        for u in self.unit_:
            constr.append(lambdas[u])
        return np.array(constr)

    def __optimize(self):
        d0 = self.m + self.r + self.n
        self.caniniyedigim = []
        for unit in self.unit_:
            x0 = np.random.rand(d0) - 0.5
            x0 = fmin_slsqp(self.__target, x0, f_ieqcons=self.__constraints, args=(unit,))
            self.input_w, self.output_w, self.lambdas = x0[:self.m], x0[self.m:(self.m + self.r)], x0[(self.m + self.r):]
            self.efficiency[unit] = self.__efficiency(unit)
            self.lambdas[np.where(self.lambdas <= 0.001)[0]] = 0
            self.caniniyedigim.append(self.lambdas)
        self.caniniyedigim = np.array(self.caniniyedigim)
        self.caniniyedigim = pd.DataFrame(self.caniniyedigim, columns=names, index=names)

    def name_units(self, names):
        assert(self.n == len(names))
        self.names = names

    def fit(self):
        self.__optimize()
        arcpy.AddWarning("Her Yol Biriminde Ekolojik Etkinlik Skorlari:\n")
        arcpy.AddWarning("------------------------------------------------------------------------")
        for n, eff in enumerate(self.efficiency):
            if len(self.names) > 0:
                name = "Birim kod: %s" % self.names[n]
            else:
                name = "Birim kod: %d" % (n + 1)
            arcpy.AddMessage("%s Ekolojik Etkinlik Skoru: %.4f" % (name, eff))
        arcpy.AddWarning("------------------------------------------------------------------------")


##########################################################################################################
# DDF TEST FONKSIYONU
# Fare & Grosskopf (2000) - LP tabanli Directional Distance Function
# Amac: Non-discretionary DEA uygulayinca discrimination loss olusup olusmadigini kanitlamak
# Bu fonksiyon ANA ANALIZ ICIN KULLANILMAZ - sadece reviewer yaniti icin test amaclidir
##########################################################################################################
def run_ddf_test(X_matrix, y_matrix, isim_listesi, non_disc_indices, senaryo_adi):

    n_units = X_matrix.shape[0]
    m_inputs = X_matrix.shape[1]
    n_outputs = y_matrix.shape[1]

    beta_skorlar = []

    for unit in range(n_units):
        x0 = X_matrix[unit]
        y0 = y_matrix[unit]

        gx = np.array([0.0 if i in non_disc_indices
                       else float(x0[i]) for i in range(m_inputs)])

        if np.all(gx == 0):
            beta_skorlar.append(0.0)
            continue

        # LP: [beta, lambda_1, ..., lambda_n]
        # Hedef: maximize beta → minimize -beta
        c = np.zeros(1 + n_units)
        c[0] = -1.0

        A_ub_listesi = []
        b_ub_listesi = []

        # Girdi kisiti: x0_i - beta*gx_i >= X_i @ lambda
        # LP formu:    X_i @ lambda + beta*gx_i <= x0_i
        for i in range(m_inputs):
            satir = np.zeros(1 + n_units)
            satir[0] = gx[i]          # ← DUZELTME: +gx (onceden -gx idi)
            satir[1:] = X_matrix[:, i]
            A_ub_listesi.append(satir)
            b_ub_listesi.append(float(x0[i]))

        # Cikti kisiti: Y @ lambda >= y0
        # LP formu:    -Y @ lambda <= -y0
        for r in range(n_outputs):
            satir = np.zeros(1 + n_units)
            satir[1:] = -y_matrix[:, r]
            A_ub_listesi.append(satir)
            b_ub_listesi.append(-float(y0[r]))

        A_ub_array = np.array(A_ub_listesi)
        b_ub_array = np.array(b_ub_listesi)

        sinirlar = [(0, None)] * (1 + n_units)

        try:
            sonuc = linprog(c,
                            A_ub=A_ub_array,
                            b_ub=b_ub_array,
                            bounds=sinirlar,
                            method='simplex')

            if sonuc.success:
                beta = max(0.0, float(sonuc.x[0]))
                beta_skorlar.append(round(beta, 6))
            else:
                beta_skorlar.append(None)
                arcpy.AddWarning("DDF uyari: %s birimi icin LP cozum bulunamadi (status: %d)" % (
                    isim_listesi[unit], sonuc.status))
        except Exception as e:
            beta_skorlar.append(None)
            arcpy.AddWarning("DDF hata: %s - %s" % (isim_listesi[unit], str(e)))

    # Sonuclari raporla
    arcpy.AddWarning("=" * 70)
    arcpy.AddWarning("DDF TEST SONUCLARI: %s" % senaryo_adi)
    arcpy.AddWarning("Non-discretionary indisler: %s" % str(non_disc_indices))
    arcpy.AddWarning("Fare & Grosskopf (2000) LP tabanli DDF")
    arcpy.AddWarning("-" * 70)

    etkin_sayisi = 0
    verimsiz_sayisi = 0
    hata_sayisi = 0

    for i, (ad, beta) in enumerate(zip(isim_listesi, beta_skorlar)):
        if beta is None:
            arcpy.AddWarning("  %s: HATA - LP cozulemedi" % ad)
            hata_sayisi += 1
        elif beta < 0.0001:
            arcpy.AddMessage("  %s: beta = %.6f --> ETKIN" % (ad, beta))
            etkin_sayisi += 1
        else:
            arcpy.AddMessage("  %s: beta = %.6f --> VERIMSIZ" % (ad, beta))
            verimsiz_sayisi += 1

    arcpy.AddWarning("-" * 70)
    arcpy.AddWarning("OZET: Etkin=%d | Verimsiz=%d | Hata=%d | Toplam=%d" % (
        etkin_sayisi, verimsiz_sayisi, hata_sayisi, n_units))

    if etkin_sayisi == n_units:
        arcpy.AddWarning(">>> DISCRIMINATION LOSS TESPIT EDILDI!")
        arcpy.AddWarning(">>> Tum DMUlar etkin: Non-disc DEA bu veri seti icin uygulanamaz.")
        arcpy.AddWarning(">>> Orijinal CCR modeli korunmalidir.")
    elif hata_sayisi == n_units:
        arcpy.AddWarning(">>> TUM BIRIMLER HATA: LP formülasyon sorunu.")
    else:
        arcpy.AddWarning(">>> Discrimination loss tespit edilmedi.")

    arcpy.AddWarning("=" * 70)

    return beta_skorlar


##########################################################################################################
# ANA ANALIZ - ORIJINAL CCR DEA (degismedi)
##########################################################################################################
if __name__ == "__main__":
    hedef_eff_siniri = 1.2

    while True:
        dea = DEA(X, y)   # Orijinal CCR - non_disc_indices YOK
        dea.name_units(names)
        dea.fit()
        if all((dea.efficiency >= 0) & (dea.efficiency <= hedef_eff_siniri)):
            break

    caniniyedigim = dea.caniniyedigim
    etkinlik_matrisi = caniniyedigim.copy()
    etkinlik_matrisi['Score'] = dea.efficiency

    ##########################################################################################################
    # DDF TESTLERI - REVIEWER 1 YANITI ICIN
    # Ekolojik senaryo girdi sirasi:
    #   0: baki_puani  (Baki puani - aspect score)
    #   1: Yamac_Egimi (Yamac egimi - slope)
    #   2: Yol_Genisligi
    #   3: Kazi_Yukseklik
    #   4: Kayip_Orman
    #   5: Sev_Heyelan (Heyelan sikligi - landslide frequency)
    ##########################################################################################################
    arcpy.AddWarning("")
    arcpy.AddWarning("*" * 70)
    arcpy.AddWarning("DDF TESTLERI BASLIYOR - REVIEWER 1 YANITI ICIN")
    arcpy.AddWarning("Referans: Fare & Grosskopf (2000), Ruggiero (1998)")
    arcpy.AddWarning("*" * 70)

    # KONFIGURASYON 1: Tum terrain degiskenleri non-discretionary
    run_ddf_test(
        X_matrix=X,
        y_matrix=y,
        isim_listesi=names,
        non_disc_indices=[0, 1, 5],
        senaryo_adi="Konfigurasyon 1: Baki + Egim + Heyelan (3 non-disc)"
    )

    # KONFIGURASYON 2: Sadece egim non-discretionary
    run_ddf_test(
        X_matrix=X,
        y_matrix=y,
        isim_listesi=names,
        non_disc_indices=[1],
        senaryo_adi="Konfigurasyon 2: Sadece Yamac Egimi (1 non-disc)"
    )

    # KONFIGURASYON 3: Sadece baki non-discretionary
    run_ddf_test(
        X_matrix=X,
        y_matrix=y,
        isim_listesi=names,
        non_disc_indices=[0],
        senaryo_adi="Konfigurasyon 3: Sadece Baki Puani (1 non-disc)"
    )

    arcpy.AddWarning("*" * 70)
    arcpy.AddWarning("DDF TESTLERI TAMAMLANDI")
    arcpy.AddWarning("Ana analiz sonuclari orijinal CCR modelinden gelmektedir.")
    arcpy.AddWarning("*" * 70)
    arcpy.AddWarning("")

##########################################################################################################
# Etkinlik matrisi olusturma
##########################################################################################################
csv_path = arcpy.env.scratchGDB + "\\buff.csv"
etkinlik_matrisi.to_csv(csv_path, index=True)
arcpy.TableToTable_conversion(csv_path, Workspace, "Etkinlik_Matrisi")
arcpy.Delete_management(csv_path)
old_field = "Field1"
etkinlik_table_path = Workspace + r"\\Etkinlik_Matrisi"
arcpy.AlterField_management(etkinlik_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Etkinlik matrisinin girdi verileri ile carpilmasi islemi
##########################################################################################################
birlestirme_df = pd.DataFrame()
for i in range(len(caniniyedigim)):
    mask = (caniniyedigim.iloc[[i]] > 0) & (caniniyedigim.iloc[[i]] < 5)
    col_indices = caniniyedigim.columns[mask.iloc[0]]
    result_df = data.loc[col_indices, :]
    mask_df = caniniyedigim.iloc[[i], :].loc[:, mask.iloc[0]]
    mask_df = mask_df.T
    maskindex = mask_df.columns[0]
    result_df.index = result_df.index.astype(str)
    mask_df.index = mask_df.index.astype(str)
    merged_df = pd.concat([result_df, mask_df], axis=1)
    merged_df.iloc[:, :-1] = merged_df.iloc[:, :-1].multiply(merged_df.iloc[:, -1], axis=0)
    merged_df_sum = pd.DataFrame(merged_df.iloc[:, :-1].sum(axis=0)).T
    merged_df_sum.index = [maskindex]
    birlestirme_df = pd.concat([birlestirme_df, merged_df_sum], axis=0)

##########################################################################################################
# Data Denormalize
##########################################################################################################
data_denormalize = data.copy()
for col in data.columns:
    original_col = col
    if original_col in alanlar_min_max:
        min_value = alanlar_min_max[original_col]['min']
        max_value = alanlar_min_max[original_col]['max']
        data_denormalize[col] = data[col] * (max_value - min_value) + min_value - 0.00001

field = ['VZA_uzunluk']
uzunluk = [row[0] for row in arcpy.da.SearchCursor(Ekolojik_Etkinlik_Tablosu, field)]
uzunluk_frame = pd.DataFrame(uzunluk, columns=field)
data_denormalize['VZA_uzunluk'] = uzunluk_frame['VZA_uzunluk'].values

for col in carpim_listesi:
    data_denormalize[col] = data_denormalize[col] * data_denormalize["VZA_uzunluk"] / 1000

##########################################################################################################
# Hedef verilerinin olusturulmasi
##########################################################################################################
hedef_denormalize = birlestirme_df.copy()
for col in birlestirme_df.columns:
    original_col = col
    if original_col in alanlar_min_max:
        min_value = alanlar_min_max[original_col]['min']
        max_value = alanlar_min_max[original_col]['max']
        hedef_denormalize[col] = birlestirme_df[col] * (max_value - min_value) + min_value - 0.00001

arcpy.AddWarning("baki_puani normalizasyon degeri     - Min= 0 - Max= 1   - birimsiz")
arcpy.AddWarning("Yamac_Egimi normalizasyon degeri    - Min= 0 - Max= 100 - birim= (%)")
arcpy.AddWarning("Yol_Genisligi normalizasyon degeri  - Min= 3 - Max= 10  - birim= (m) ")
arcpy.AddWarning("Kazi_Yukseklik normalizasyon degeri - Min= 0 - Max= 20  - birim= (m)")
arcpy.AddWarning("Kayip_Orman normalizasyon degeri    - Min= 0 - Max= 10  - birim= (ha/km)")
arcpy.AddWarning("Sev_Heyelan normalizasyon degeri    - Min= 0 - Max= 10  - birim= (adet/km)")
arcpy.AddWarning("Akarsu normalizasyon degeri         - Min= 0 - Max= 800 - birim= (m)")
arcpy.AddWarning("Sanat_Yapisi normalizasyon degeri   - Min= 0 - Max= 20  - birim= (adet/km)")
arcpy.AddWarning("Baglanti_Alan normalizasyon degeri  - Min= 1 - Max= 10  - birim= (adet/km)")
arcpy.AddWarning("------------------------------------------------------------------------")

field = ['VZA_uzunluk']
uzunluk = [row[0] for row in arcpy.da.SearchCursor(Ekolojik_Etkinlik_Tablosu, field)]
uzunluk_frame = pd.DataFrame(uzunluk, columns=field)
hedef_denormalize['VZA_uzunluk'] = uzunluk_frame['VZA_uzunluk'].values

for col in carpim_listesi:
    hedef_denormalize[col] = hedef_denormalize[col] * hedef_denormalize["VZA_uzunluk"] / 1000

hedef_denormalize['Score'] = etkinlik_matrisi['Score'].values
hedef_denormalize['Score'] = hedef_denormalize['Score'].round(3)

degisim = hedef_denormalize.copy()
col1 = degisim.columns.copy()
degisim.columns = ['HEDEF_' + str(col) for col in degisim.columns]
degisim.rename(columns={'HEDEF_Score': 'Score'}, inplace=True)

if "VZA_uzunluk" in hedef_denormalize.columns:
    del hedef_denormalize["VZA_uzunluk"]
if "VZA_uzunluk" in data_denormalize.columns:
    del data_denormalize["VZA_uzunluk"]

csv_path2 = arcpy.env.scratchGDB + "\\buff2.csv"
degisim.to_csv(csv_path2, index=True)
arcpy.TableToTable_conversion(csv_path2, Workspace, "hedefler")
arcpy.Delete_management(csv_path2)
old_field = "Field1"
target_table_path = Workspace + r"\\hedefler"
arcpy.AlterField_management(target_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Degisim oranlarinin hesaplanmasi
##########################################################################################################
degisim_oranlari = pd.DataFrame()
for col in data_denormalize.columns:
    for row in data_denormalize.index:
        oran = round((((hedef_denormalize.loc[row, col] - data_denormalize.loc[row, col]) / data_denormalize.loc[row, col]) * 100), 2)
        degisim_oranlari.loc[row, col] = oran

degisim_oranlari.columns = ['PROJEKSIYON_' + str(col1[i]) for i in range(degisim_oranlari.shape[1])]
degisim_oranlari[degisim_oranlari.abs() < 0.001] = 0

csv_path3 = arcpy.env.scratchGDB + "\\buff3.csv"
degisim_oranlari.to_csv(csv_path3, index=True)
arcpy.TableToTable_conversion(csv_path3, Workspace, "projection")
arcpy.Delete_management(csv_path2)
old_field = "Field1"
projection_table_path = Workspace + r"\\projection"
arcpy.AlterField_management(projection_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Etkinlik Analizi tablosu (ALL)
##########################################################################################################
ALL = pd.concat([data_denormalize, degisim, degisim_oranlari], axis=1)
new_order = []

for i in range(len(data_denormalize.columns)):
    new_order.append(data_denormalize.columns[i])
    new_order.append(degisim.columns[i])
    new_order.append(degisim_oranlari.columns[i])

ALL = ALL.reindex(columns=new_order)
ALL['Score'] = etkinlik_matrisi['Score'].values
ALL['Score'] = ALL['Score'].round(3)

csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
ALL.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "ALL")
arcpy.Delete_management(csv_path1)
old_field = "Field1"
ALL_table_path = Workspace + r"\\ALL"
arcpy.AlterField_management(ALL_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Referans kumeleri
##########################################################################################################
matris_coz = pd.DataFrame(np.copy(caniniyedigim))
matris_coz.columns = caniniyedigim.columns
matris_coz.index = caniniyedigim.index

referans_df = pd.DataFrame(columns=[yol_name, 'Referanslar'])

for index, row in matris_coz.iterrows():
    yol_kodu = index
    satir_sonuclar = []
    for sutun_adi, deger in row.iteritems():
        if sutun_adi != index and 0 < deger < 1:
            satir_sonuclar.append("{0} ({1:.5f})".format(sutun_adi, deger))
    if satir_sonuclar:
        referans_df = pd.concat([referans_df, pd.DataFrame({yol_name: [yol_kodu], 'Referanslar': [", ".join(satir_sonuclar)]})], ignore_index=True)

csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
referans_df.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "Referans")
arcpy.Delete_management(csv_path1)
Referans_table_path = Workspace + r"\\Referans"

arcpy.JoinField_management(ALL_table_path, yol_name, Referans_table_path, yol_name)
arcpy.DeleteField_management(ALL_table_path, [yol_name + "_1"])
arcpy.management.DeleteField(ALL_table_path, "Field1")
with arcpy.da.UpdateCursor(ALL_table_path, "Referanslar") as cursor:
    for row in cursor:
        if row[0] is None:
            row[0] = 'Etkin'
            cursor.updateRow(row)

##########################################################################################################
# ArcGIS Gorsellestirme
##########################################################################################################
if "\\" in Ekolojik_Etkinlik_Tablosu:
    arcpy.management.Copy(str(Ekolojik_Etkinlik_Tablosu), str(Workspace) + r"\\Ekolojik_Etkinlik_Analizi")
else:
    arcpy.management.Copy(str(Workspace) + "\\" + str(Ekolojik_Etkinlik_Tablosu), str(Workspace) + r"\\Ekolojik_Etkinlik_Analizi")

Ekolojik_Etkinlik_Analiz = str(Workspace) + r"\\Ekolojik_Etkinlik_Analizi"
fields = [f.name for f in arcpy.ListFields(str(Ekolojik_Etkinlik_Analiz))]
fields.remove('Shape')
fields.remove('OBJECTID')
fields.remove(yol_name)
fields.remove('Shape_Length')
arcpy.DeleteField_management(str(Ekolojik_Etkinlik_Analiz), fields)

arcpy.JoinField_management(Ekolojik_Etkinlik_Analiz, yol_name, ALL_table_path, yol_name)
arcpy.DeleteField_management(Ekolojik_Etkinlik_Analiz, [yol_name + "_1"])

query_1 = "Score >= 0.9999"
Ekolojik_Etkinlik_Target_Etkin = str(Workspace) + r"\\Ekolojik_Etkin_Olan"
arcpy.Select_analysis(Ekolojik_Etkinlik_Analiz, Ekolojik_Etkinlik_Target_Etkin, query_1)

query_2 = "Score < 1"
Ekolojik_Etkinlik_Target_Etkin_Olmayan = str(Workspace) + r"\\Ekolojik_Etkin_Olmayan"
arcpy.Select_analysis(Ekolojik_Etkinlik_Analiz, Ekolojik_Etkinlik_Target_Etkin_Olmayan, query_2)

arcpy.Delete_management(projection_table_path)
arcpy.Delete_management(target_table_path)
arcpy.Delete_management(girdi_cikti_verileri)
arcpy.Delete_management(Referans_table_path)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

ALL_Layer = arcpy.mapping.TableView(ALL_table_path)
arcpy.mapping.AddTableView(df, ALL_Layer)

etkinlik_matrisi_Layer = arcpy.mapping.TableView(etkinlik_table_path)
arcpy.mapping.AddTableView(df, etkinlik_matrisi_Layer)

normalize_tablo_Layer = arcpy.mapping.TableView(normalize_tablo)
arcpy.mapping.AddTableView(df, normalize_tablo_Layer)

korelasyon_table_Layer = arcpy.mapping.TableView(korelasyon_table_path)
arcpy.mapping.AddTableView(df, korelasyon_table_Layer)

Ekolojik_Etkinlik_Target_Etkin_Olmayan_Layer = arcpy.mapping.Layer(Ekolojik_Etkinlik_Target_Etkin_Olmayan)
arcpy.mapping.AddLayer(df, Ekolojik_Etkinlik_Target_Etkin_Olmayan_Layer)

Ekolojik_Etkinlik_Target_Etkin_Layer = arcpy.mapping.Layer(Ekolojik_Etkinlik_Target_Etkin)
arcpy.mapping.AddLayer(df, Ekolojik_Etkinlik_Target_Etkin_Layer)

Ekolojik_Etkinlik_Analiz_Layer = arcpy.mapping.Layer(Ekolojik_Etkinlik_Analiz)
arcpy.mapping.AddLayer(df, Ekolojik_Etkinlik_Analiz_Layer)

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
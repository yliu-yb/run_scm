import os

para1 = "2016053102"
para2 = "2016060400"
para3 = str(24 * 4 - 2)
para4 = str(1)  # physics
para5 = str(0)  # temp_diff
para6 = str(3)  # bk grid res
para7 = str(3)  # tau
for tau in [6,12]:
    for bg in [3, 9, 27]:
        para6 = str(bg)  # bk grid res
        para7 = str(tau)  # tau
        print(para1, para2, para3, para4, para5, para6, para7)
        os.system(
            "python main_2.py " + para1 + " " + para2 + " " + para3 + " " + para4 + " " + para5 + " " + para6 + " " + para7)
        pass
exit()
print(para1, para2, para3, para4, para5, para6, para7)
os.system("python main_2.py " + para1 + " " + para2 + " " + para3 + " " + para4 + " " + para5 + " " + para6 + " " + para7)

#
# float QVAPOR(Time, force_layers);
#         QVAPOR:FieldType = 104 ;
#         QVAPOR:MemoryOrder = "Z  " ;
# 		QVAPOR:description = "Water vapor mixing ratio" ;
# 		QVAPOR:units = "kg kg-1" ;
# 		QVAPOR:stagger = "" ;
# 		QVAPOR:_FillValue = -999.f ;
#     float QCLOUD(Time, force_layers);
#         QCLOUD:FieldType = 104 ;
#         QCLOUD:MemoryOrder = "Z  " ;
# 		QCLOUD:description = "Cloud water mixing ratio" ;
# 		QCLOUD:units = "kg kg-1" ;
# 		QCLOUD:stagger = "" ;
# 		QCLOUD:_FillValue = -999.f ;
#     float QRAIN(Time, force_layers);
#         QRAIN:FieldType = 104 ;
#         QRAIN:MemoryOrder = "Z  " ;
# 		QRAIN:description = "Rain water mixing ratio" ;
# 		QRAIN:units = "kg kg-1" ;
# 		QRAIN:stagger = "" ;
# 		QRAIN:_FillValue = -999.f ;
#     float T(Time, force_layers);
#         T:FieldType = 104 ;
#         T:MemoryOrder = "Z  " ;
# 		T:description = "perturbation potential temperature theta-t0" ;
# 		T:units = "K" ;
# 		T:stagger = "" ;
# 		T:_FillValue = -999.f ;
#     float U(Time, force_layers);
#         U:FieldType = 104 ;
# 		U:MemoryOrder = "Z  " ;
# 		U:description = "x-wind component" ;
# 		U:units = "m s-1" ;
# 		U:stagger = "" ;
# 		U:_FillValue = -999.f ;
#     float V(Time, force_layers);
#         V:FieldType = 104 ;
# 		V:MemoryOrder = "Z  " ;
# 		V:description = "y-wind component" ;
# 		V:units = "m s-1" ;
# 		V:stagger = "" ;
# 		V:_FillValue = -999.f ;
#     float W(Time, force_layers);
#         W:FieldType = 104 ;
# 		W:MemoryOrder = "Z  " ;
# 		W:description = "z-wind component" ;
# 		W:units = "m s-1" ;
# 		W:stagger = "" ;
# 		W:_FillValue = -999.f ;
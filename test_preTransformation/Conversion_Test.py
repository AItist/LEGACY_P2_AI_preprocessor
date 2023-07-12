import numpy as np

c1 = '924,42,-1457,1003,126,-1457,1051,120,-1457,1095,116,-1457,896,147,-1384,867,153,-1383,838,159,-1383,1202,88,-1096,832,143,-728,992,-65,-1301,870,-42,-1196,1419,-320,-868,696,-258,-298,1558,-815,-1005,619,-756,-180,1468,-1057,-1316,622,-1046,-1021,1477,-1157,-1457,576,-1145,-1178,1411,-1130,-1466,632,-1096,-1270,1390,-1090,-1339,667,-1077,-1097,1271,-1224,-228,798,-1199,236,1249,-1943,-60,822,-1923,935,1242,-2562,1052,814,-2535,2016,1264,-2685,1119,812,-2656,2102,1111,-2788,303,850,-2768,1278,'
c2 = '924,402,-1457,1003,486,-1457,1051,480,-1457,1095,476,-1457,896,507,-1384,867,513,-1383,838,519,-1383,1202,448,-1096,832,503,-728,992,295,-1301,870,318,-1196,1419,40,-868,696,102,-298,1558,-455,-1005,619,-396,-180,1468,-697,-1316,622,-686,-1021,1477,-797,-1457,576,-785,-1178,1411,-770,-1466,632,-736,-1270,1390,-730,-1339,667,-717,-1097,1271,-864,-228,798,-839,236,1249,-1583,-60,822,-1563,935,1242,-2202,1052,814,-2175,2016,1264,-2325,1119,812,-2296,2102,1111,-2428,303,850,-2408,1278,'

print(len(c1.split(',')[:-1]))
# print(len(c2.split(',')[:-1]))

split_c1 = c1.split(',')[:-1]
split_c2 = c2.split(',')[:-1]

# print(split_c1)
# print(split_c2)
# print(type(split_c1))

numpy_c1 = np.array([int(i) for i in split_c1])
numpy_c2 = np.array([int(i) for i in split_c2])

numpy_c1 = numpy_c1.reshape(-1, 3)
numpy_c2 = numpy_c2.reshape(33, 3)

print(numpy_c1[0])
# print(numpy_c2[0]) 
# print(numpy_c1)

def convert_string_to_numpy_array(string):
    split_string = string.split(',')[:-1]
    numpy_array = np.array([int(i) for i in split_string])
    return numpy_array.reshape(-1, 3)

numpy_result1 = convert_string_to_numpy_array(c1)
numpy_result2 = convert_string_to_numpy_array(c2)

print(numpy_result1[0])
print(numpy_result2[0])
import math

def to_xy (lon, lat):
    """经纬度转换成xy坐标"""
    xy_coordinate = []
    # 地球周长
    L = 6381372*math.pi*2 
    # 平面展开，将周长视为X轴
    W = L 
    # Y轴约等于周长一般
    H = L/2 
    # 米勒投影中的一个常数，范围大约在正负2.3之间
    mill = 2.3 
    # 将经度从度数转换为弧度
    x = lon*math.pi/180 
    # 将纬度从度数转换为弧度
    y = lat*math.pi/180 
    # 这里是米勒投影的转换
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y)) 
    # 这里将弧度转为实际距离 ，转换结果的单位是公里
    x = (W/2)+(W/(2*math.pi))*x
    y = (H/2)-(H/(2*mill))*y
    xy_coordinate.append((int(round(x)),int(round(y))))
    return xy_coordinate[0]
 
 
def from_xy(x, y):
    """xy坐标转换成经纬度"""
    lonlat_coordinate = []
    L = 6381372 * math.pi*2
    W = L
    H = L/2
    mill = 2.3
    lat = ((H/2-y)*2*mill)/(1.25*H)
    lat = ((math.atan(math.exp(lat))-0.25*math.pi)*180)/(0.4*math.pi)
    lon = (x-W/2)*360/W
    # TODO 最终需要确认经纬度保留小数点后几位
    lonlat_coordinate.append((round(lon,15),round(lat,15)))
    return lonlat_coordinate[0]


# 示例使用
# lat = 28.89796
# lon = 118.561932

# x, y = to_xy(lon, lat)
# print(f'x: {x}  y: {y}')

# lat, lon = from_xy(x, y)
# print(f'lat: {lat}  lon: {lon}')

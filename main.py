from utils.get_pixels import select_points_on_pic_handly
from utils.get_pictures import get_omni_pics
pics = get_omni_pics()

print(len(pics))
select_points_on_pic_handly(pics[1])
import sys
sys.path.append('d:/dev/stock')

from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우의 경우
# font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 리눅스의 경우
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
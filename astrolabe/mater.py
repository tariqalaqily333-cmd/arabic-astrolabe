# -*- coding: utf-8 -*-
from.utils import ar, polar_to_xy, stereographic_r, CARDINAL
from PIL import ImageDraw

class Mater:
    """الوجه - الأم: الصفيحة الثابتة بالإسطرلاب"""

    def __init__(self, draw, center, radius, lat, fonts):
        self.draw = draw
        self.cx = center
        self.cy = center
        self.r_max = radius
        self.lat = lat
        self.font_t = fonts['title']
        self.font_l = fonts['large']
        self.font_s = fonts['small']

    def draw_mater(self):
        """رسم الأم كاملة"""
        # 1. الدائرة الخارجية
        self.draw.ellipse([self.cx-self.r_max, self.cy-self.r_max,
                          self.cx+self.r_max, self.cy+self.r_max],
                         outline='black', width=5)

        # 2. المقنطرات - دوائر الارتفاع
        for alt in range(5, 91, 5):
            r = stereographic_r(alt, self.r_max)
            width = 2 if alt % 10 == 0 else 1
            color = '#000000' if alt % 10 == 0 else '#BBBBBB'
            self.draw.ellipse([self.cx-r, self.cy-r, self.cx+r, self.cy+r],
                             outline=color, width=width)
            if alt % 10 == 0 and alt < 90:
                self.draw.text((self.cx, self.cy-r-25), ar(f"{alt}°"),
                             **الرسالة 4: ملف `astrolabe/mater.py` - الوجه / الأم**

جوه فولدر `astrolabe` اعمل ملف اسمه `mater.py` وحط فيه ده:

```python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
from.utils import ar, load_font, polar_to_xy, stereographic_r, CARDINAL
import math

class Mater:
    """الوجه - الأم: الصفيحة الثابتة بالشبكات"""

    def __init__(self, latitude, size=2480, radius=1000):
        self.lat = math.radians(latitude)
        self.size = size
        self.center = size // 2
        self.radius = radius
        self.img = Image.new('RGB', (size, size), 'white')
        self.draw = ImageDraw.Draw(self.img)
        self.font_t = load_font(40)
        self.font_l = load_font(22)
        self.font_s = load_font(18)

    def circle(self, r, color='black', width=2):
        self.draw.ellipse([self.center-r, self.center-r, self.center+r],
                         outline=color, width=width)

    def line(self, x1, y1, x2, y2, color='black', width=1):
        self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2],
                      fill=color, width=width)

    def text(self, txt, x, y, font, color='black', anchor='mm'):
        self.draw.text((self.center+x, self.center+y), ar(txt), font=font, fill=color, anchor=anchor)

    def draw_limb(self):
        """الإطار الخارجي - الحجرة"""
        self.circle(self.radius, width=6)
        # تدريج 360 درجة
        for deg in range(360):
            r1 = self.radius - 8 if deg % 10 == 0 else self.radius - 4
            r2 = self.radius
            w = 2 if deg % 10 == 0 else 1
            x1, y1 = polar_to_xy(r1, deg, 0, 0)
            x2, y2 = polar_to_xy(r2, deg, 0, 0)
            self.line(x1, y1, x2, y2, width=w)
            if deg % 30 == 0:
                x, y = polar_to_xy(self.radius - 30, deg, 0, 0)
                self.text(f"{deg}°", x, y, self.font_s)

    def draw_almucantars(self):
        """المقنطرات - دوائر الارتفاع"""
        for alt in range(0, 91, 5):
            r = stereographic_r(alt, self.radius)
            if r > self.radius: continue
            w = 3 if alt % 10 == 0 else 1
            c = '#000' if alt % 10 == 0 else '#BBB'
            self.circle(r, c, w)
            if alt % 10 == 0 and alt!= 90:
                self.text(f"{alt}°", 0, -r-25, self.font_s, '#666')

    def draw_azimuths(self):
        """السموت - خطوط السمت"""
        for az in range(0, 360, 10):
            x2, y2 = polar_to_xy(self.radius, az, 0, 0)
            w = 2 if az % 30 == 0 else 1
            c = '#000' if az % 30 == 0 else '#DDD'
            self.line(0, 0, x2, y2, c, w)

    def draw_horizon(self):
        """خط الأفق"""
        self.draw.line([self.center-self.radius, self.center, self.center+self.radius, self.center],
                      fill='#8B0000', width=4)
        self.text("الأفق", 0, 30, self.font_l, '#8B0000')

    def draw_cardinal_points(self):
        """الجهات الأصلية"""
        dirs = [(0, 0), (90, 1), (180, 2), (270, 3)]
        for angle, i in dirs:
            x, y = polar_to_xy(self.radius + 60, angle, 0, 0)
            self.text(CARDINAL[i], x, y, self.font_t, '#8B0000')

    def draw_twilight_lines(self):
        """خطوط الشفق"""
        for twilight in [6, 12, 18]: # مدني، بحري، فلكي
            r = stereographic_r(-twilight, self.radius)
            if r <= self.radius:
                self.circle(r, '#0066CC', 1)
                self.text(f"شفق {twilight}°", 0, r+20, self.font_s, '#0066CC')

    def render(self):
        """رسم الوجه كامل"""
        self.draw_limb()
        self.draw_almucantars()
        self.draw_azimuths()
        self.draw_horizon()
        self.draw_twilight_lines()
        self.draw_cardinal_points()
        return self.img
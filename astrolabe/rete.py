# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
from.utils import ar, load_font, polar_to_xy, ZODIAC_AR, ZODIAC_SYMBOLS
from.stars import get_bright_stars
import math

class Rete:
    """العنكبوت - دائرة البروج والنجوم الثابتة"""

    def __init__(self, size=2480, radius=920):
        self.size = size
        self.center = size // 2
        self.radius = radius
        self.img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.font_l = load_font(24)
        self.font_s = load_font(16)
        self.obliquity = math.radians(23.44) # ميل دائرة البروج

    def ecliptic_to_xy(self, lon_deg, r):
        """تحويل طول برجي إلى x,y على دائرة البروج"""
        # نحول للسمت مباشرة على دائرة البروج
        x, y = polar_to_xy(r, lon_deg, 0, 0)
        return x, y

    def star_to_xy(self, ra, dec, r_ecliptic):
        """تحويل مطلع مستقيم وميل النجم لإحداثيات على العنكبوت"""
        # إسقاط ستيريوجرافيك تقريبي للنجوم
        ra_rad = math.radians(ra)
        dec_rad = math.radians(dec)
        # نصف قطر يعتمد على الميل
        r_star = r_ecliptic * math.tan(math.pi/4 - dec_rad/2)
        x = r_star * math.cos(ra_rad)
        y = r_star * math.sin(ra_rad)
        return x, y

    def draw_ecliptic_circle(self):
        """دائرة فلك البروج"""
        self.draw.ellipse([self.center-self.radius, self.center-self.radius,
                          self.center+self.radius, self.center+self.radius],
                         outline='#8B4513', width=5)

    def draw_zodiac(self):
        """تقسيم البروج الـ12 مع الرموز"""
        for i in range(12):
            angle = i * 30
            # خط فاصل بين البروج
            x1, y1 = polar_to_xy(self.radius * 0.94, angle, 0, 0)
            x2, y2 = polar_to_xy(self.radius * 1.06, angle, 0, 0)
            self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2],
                          fill='#8B4513', width=4)

            # اسم البرج والرمز في المنتصف
            mid_angle = angle + 15
            xm, ym = polar_to_xy(self.radius * 0.85, mid_angle, 0, 0)
            self.draw.text((self.center+xm, self.center+ym), ar(ZODIAC_SYMBOLS[i]),
                         **الرسالة 5: ملف `astrolabe/rete.py` - العنكبوت**

جوه فولدر `astrolabe` اعمل ملف اسمه `rete.py` وحط فيه ده:

```python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
from.utils import ar, load_font, polar_to_xy, ZODIAC_AR, ZODIAC_SYMBOLS
from.stars import get_bright_stars
import math

class Rete:
    """العنكبوت: دائرة البروج والنجوم الثابتة"""

    def __init__(self, latitude, size=2480, radius=1000):
        self.lat = math.radians(latitude)
        self.obliquity = math.radians(23.44)
        self.size = size
        self.center = size // 2
        self.radius = radius * 0.92 # العنكبوت أصغر من الأم
        self.img = Image.new('RGBA', (size, size), (0,0,0,0))
        self.draw = ImageDraw.Draw(self.img)
        self.font_t = load_font(36)
        self.font_l = load_font(24)
        self.font_s = load_font(18)
        self.stars = get_bright_stars(2.0)

    def circle(self, r, color='#8B4513', width=3):
        self.draw.ellipse([self.center-r, self.center-r, self.center+r],
                         outline=color, width=width)

    def line(self, x1, y1, x2, y2, color='#8B4513', width=2):
        self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2],
                      fill=color, width=width)

    def text(self, txt, x, y, font, color='#8B4513', anchor='mm'):
        self.draw.text((self.center+x, self.center+y), ar(txt), font=font, fill=color, anchor=anchor)

    def ecliptic_coords(self, lon_deg):
        """تحويل طول برجي إلى إحداثيات على العنكبوت"""
        # دائرة فلك البروج مائلة 23.44° عن خط الاستواء
        lon = math.radians(lon_deg)
        dec = math.asin(math.sin(lon) * math.sin(self.obliquity))
        ra = math.atan2(math.sin(lon) * math.cos(self.obliquity), math.cos(lon))

        # إسقاط ستيريوجرافيك
        r_star = self.radius * math.tan(math.pi/4 - dec/2)
        x = r_star * math.cos(ra)
        y = r_star * math.sin(ra)
        return x, y

    def draw_ecliptic(self):
        """دائرة فلك البروج"""
        self.circle(self.radius, width=5)

        # تقسيم 12 برج
        for i in range(12):
            angle = i * 30
            x1, y1 = polar_to_xy(self.radius * 0.95, angle, 0, 0)
            x2, y2 = polar_to_xy(self.radius * 1.05, angle, 0, 0)
            self.line(x1, y1, x2, y2, width=4)

            # اسم البرج والرمز
            angle_mid = angle + 15
            x_t, y_t = polar_to_xy(self.radius * 0.85, angle_mid, 0, 0)
            self.text(ZODIAC_SYMBOLS[i], x_t, y_t, self.font_l)
            x_t2, y_t2 = polar_to_xy(self.radius * 0.75, angle_mid, 0, 0)
            self.text(ZODIAC_AR[i], x_t2, y_t2, self.font_s)

    def draw_tropics(self):
        """مدار السرطان والجدي"""
        tropic_can_r = self.radius * math.tan(math.radians((90 - 23.44)/2))
        tropic_cap_r = self.radius * math.tan(math.radians((90 + 23.44)/2))

        self.draw.ellipse([self.center-tropic_can_r, self.center-tropic_can_r,
                          self.center+tropic_can_r, self.center+tropic_can_r],
                         outline='#2E8B57', width=2)
        self.text("مدار السرطان", 0, -tropic_can_r-30, self.font_s, '#2E8B57')

        self.draw.ellipse([self.center-tropic_cap_r, self.center-tropic_cap_r,
                          self.center+tropic_cap_r, self.center+tropic_cap_r],
                         outline='#2E8B57', width=2)
        self.text("مدار الجدي", 0, -tropic_cap_r-30, self.font_s, '#2E8B57')

    def draw_stars(self):
        """رسم النجوم على العنكبوت"""
        for star in self.stars:
            ra_rad = math.radians(star['ra'])
            dec_rad = math.radians(star['dec'])

            # إسقاط ستيريوجرافيك للنجم
            r_star = self.radius * math.tan(math.pi/4 - dec_rad/2)
            if r_star > self.radius * 1.1: continue

            x = r_star * math.cos(ra_rad)
            y = r_star * math.sin(ra_rad)

            # حجم النجمة حسب القدر
            size = max(3, 8 - star['mag'] * 2)

            # رسم النجمة
            self.draw.ellipse([self.center+x-size, self.center+y-size,
                              self.center+x+size, self.center+y+size],
                             fill='#FFD700', outline='#FFA500', width=2)
            # اسم النجمة
            self.text(star['name'], x+15, y, self.font_s, '#333', anchor='lm')

    def draw_equator(self):
        """خط الاستواء السماوي"""
        eq_r = self.radius
        self.circle(eq_r, '#4169E1', 2)
        self.text("خط الاستواء", eq_r+40, 0, self.font_s, '#4169E1', anchor='lm')

    def render(self):
        """رسم العنكبوت كامل"""
        self.draw_ecliptic()
        self.draw_tropics()
        self.draw_equator()
        self.draw_stars()
        return self.img
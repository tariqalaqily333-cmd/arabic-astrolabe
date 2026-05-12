#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, math, os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(str(text)))

def load_font(size):
    try: return ImageFont.truetype("fonts/Cairo-Regular.ttf", size)
    except: return ImageFont.load_default()

class AstrolabeMath:
    def __init__(self, lat):
        self.lat = math.radians(lat)
        self.obliquity = math.radians(23.44)

    def stereographic(self, alt, az, r_max):
        """إسقاط ستيريوجرافيك للإرتفاع والسمت"""
        alt_rad = math.radians(alt)
        az_rad = math.radians(az - 90)
        r = r_max * math.tan(math.pi/4 - alt_rad/2)
        x = r * math.cos(az_rad)
        y = r * math.sin(az_rad)
        return x, y

    def ecliptic_to_ra_dec(self, lon):
        """تحويل طول برجي إلى مطلع مستقيم وميل"""
        lon_rad = math.radians(lon)
        dec = math.asin(math.sin(lon_rad) * math.sin(self.obliquity))
        ra = math.atan2(math.sin(lon_rad) * math.cos(self.obliquity), math.cos(lon_rad))
        return math.degrees(ra) % 360, math.degrees(dec)

class AstrolabeFull:
    def __init__(self, settings_file):
        with open(settings_file, 'r', encoding='utf-8') as f:
            s = json.load(f)
        self.lat = s['latitude']
        self.title = s['title']
        self.author = s.get('author', 'الأستاذ طارق')
        self.months = s['month_names']
        self.zodiac = s['zodiac_names']
        self.symbols = s['zodiac_symbols']
        self.cardinal = s['cardinal_points']
        self.math = AstrolabeMath(self.lat)

        # حجم الصفحة A4 300dpi
        self.size = 2480
        self.center = self.size // 2
        self.radius = 1000
        self.img = Image.new('RGB', (self.size, self.size), 'white')
        self.draw = ImageDraw.Draw(self.img)
        self.font_t = load_font(36)
        self.font_l = load_font(18)
        self.font_s = load_font(14)

        # نجوم العنكبوت - 20 نجم لامع
        self.stars = [
            {"name": "الدبران", "ra": 68.98, "dec": 16.51},
            {"name": "العيوق", "ra": 78.63, "dec": 45.99},
            {"name": "رجل الجبار", "ra": 78.63, "dec": -8.20},
            {"name": "الشعرى اليمانية", "ra": 101.28, "dec": -16.72},
            {"name": "الشعرى الشامية", "ra": 114.82, "dec": 5.22},
            {"name": "قلب الأسد", "ra": 152.09, "dec": 11.97},
            {"name": "السماك الأعزل", "ra": 201.30, "dec": -11.16},
            {"name": "السماك الرامح", "ra": 213.92, "dec": 19.18},
            {"name": "قلب العقرب", "ra": 247.35, "dec": -26.43},
            {"name": "النسر الواقع", "ra": 279.23, "dec": 38.78},
            {"name": "النسر الطائر", "ra": 297.70, "dec": 8.87},
            {"name": "فم الحوت", "ra": 344.41, "dec": -29.62}
        ]

    def circle(self, r, color='black', width=2):
        self.draw.ellipse([self.center-r, self.center+r, self.center+r], outline=color, width=width)

    def text(self, txt, x, y, font, color='black', anchor='mm'):
        self.draw.text((self.center+x, self.center+y), ar(txt), font=font, fill=color, anchor=anchor)

    def draw_mater(self):
        """1. رسم الأم - الصفيحة الثابتة"""
        # الدائرة الخارجية
        self.circle(self.radius, width=5)

        # دوائر المقنطرات - الارتفاع
        for alt in range(5, 91, 5):
            r = self.radius * math.tan(math.radians((90 - alt)/2))
            w = 2 if alt % 10 == 0 else 1
            c = '#000000' if alt % 10 == 0 else '#CCCCCC'
            self.circle(r, c, w)
            if alt % 10 == 0:
                self.text(f"{alt}°", 0, -r-30, self.font_s, '#666')

        # خطوط السمت
        for az in range(0, 360, 10):
            angle = math.radians(az - 90)
            x2 = self.radius * math.cos(angle)
            y2 = self.radius * math.sin(angle)
            w = 2 if az % 30 == 0 else 1
            c = '#000000' if az % 30 == 0 else '#CCCCCC'
            self.draw.line([self.center, self.center, self.center+x2, self.center+y2], fill=c, width=w)

        # الاتجاهات
        dirs = [(0, 0), (90, 1), (180, 2), (270, 3)]
        for angle, i in dirs:
            r = self.radius + 80
            rad = math.radians(angle - 90)
            self.text(self.cardinal[i], r*math.cos(rad), r*math.sin(rad), self.font_t, '#8B0000')

        # خط الأفق
        self.draw.line([self.center-self.radius, self.center, self.center+self.radius, self.center], fill='#8B0000', width=4)
        self.text("الأفق", 0, 20, self.font_l, '#8B0000')

    def draw_rete(self):
        """2. رسم العنكبوت - دائرة البروج والنجوم"""
        rete_r = self.radius * 0.92

        # دائرة فلك البروج
        self.circle(rete_r, '#8B4513', 4)

        # تقسيم البروج
        for i in range(12):
            angle = i * 30 - 90
            rad = math.radians(angle)
            x1 = rete_r * 0.96 * math.cos(rad)
            y1 = rete_r * 0.96 * math.sin(rad)
            x2 = rete_r * 1.04 * math.cos(rad)
            y2 = rete_r * 1.04 * math.sin(rad)
            self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2], fill='#8B4513', width=3)

            # اسم البرج والرمز
            angle_mid = angle + 15
            rad_mid = math.radians(angle_mid)
            self.text(f"{self.symbols[i]}", rete_r*0.88*math.cos(rad_mid), rete_r*0.88*math.sin(rad_mid), self.font_l, '#8B4513')
            self.text(self.zodiac[i], rete_r*0.80*math.cos(rad_mid), rete_r*0.80*math.sin(rad_mid), self.font_s, '#8B4513')

        # مدار الجدي والسرطان
        tropic_cap = self.radius * 0.6
        tropic_can = self.radius * 0.3
        self.circle(tropic_cap, '#2E8B57', 2)
        self.circle(tropic_can, '#2E8B57', 2)
        self.text("مدار الجدي", 0, -tropic_cap-25, self.font_s, '#2E8B57')
        self.text("مدار السرطان", 0, -tropic_can-25, self.font_s, '#2E8B57')

        # رسم النجوم
        for star in self.stars:
            # تحويل مطلع مستقيم وميل إلى إحداثيات
            ra_rad = math.radians(star['ra'])
            dec_rad = math.radians(star['dec'])
            r_star = rete_r * math.tan(math.pi/4 - dec_rad/2)
            x = r_star * math.cos(ra_rad)
            y = r_star * math.sin(ra_rad)

            # رسم النجمة
            self.draw.ellipse([self.center+x-6, self.center+y-6, self.center+x+6, self.center+y+6],
                             fill='#FFD700', outline='#FFA500', width=2)
            self.text(star['name'], x+15, y, self.font_s, '#333', anchor='lm')

    def draw_title(self):
        """3. العنوان والبيانات"""
        self.text(self.title, 0, -self.radius-150, self.font_t)
        self.text(f"خط العرض: {self.lat}° شمالاً", 0, -self.radius-100, self.font_l)
        self.text(f"صناعة {self.author} - 2026م", 0, -self.radius-70, self.font_l)
        self.text("الإسطرلاب العربي الكامل", 0, self.radius+100, self.font_l, '#666')

    def save(self):
        os.makedirs('output', exist_ok=True)
        path = f"output/astrolabe_full_{self.lat}N_{datetime.now().strftime('%Y%m%d')}.png"
        self.img.save(path, dpi=(300,300))
        print(f"✅ تم توليد الإسطرلاب الكامل: {path}")
        return path

if __name__ == "__main__":
    print("🌟 جاري توليد الإسطرلاب العربي الكامل...")
    a = AstrolabeFull('settings/cairo.json')
    a.draw_mater() # الأم
    a.draw_rete() # العنكبوت
    a.draw_title() # العنوان
    a.save()
    print("🎉 تم! زي موقع in-the-sky بس عربي 100%")
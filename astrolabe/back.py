# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
from.utils import ar, load_font, polar_to_xy, MONTHS_AR, ZODIAC_AR
import math

class Back:
    """الظهر: التقاويم + مربع الظل + الجيب"""

    def __init__(self, size=2480, radius=1000):
        self.size = size
        self.center = size // 2
        self.radius = radius
        self.img = Image.new('RGB', (size, size), 'white')
        self.draw = ImageDraw.Draw(self.img)
        self.font_t = load_font(40)
        self.font_l = load_font(24)
        self.font_s = load_font(18)

    def circle(self, r, color='black', width=2):
        self.draw.ellipse([self.center-r, self.center-r, self.center+r],
                         outline=color, width=width)

    def text(self, txt, x, y, font, color='black', anchor='mm'):
        self.draw.text((self.center+x, self.center+y), ar(txt), font=font, fill=color, anchor=anchor)

    def draw_calendar_circles(self):
        """دوائر التقويم: ميلادي + بروج"""
        # 1. دائرة الأشهر الميلادية - 365 يوم
        r_month = self.radius * 0.95
        self.circle(r_month, width=4)
        for i in range(12):
            angle = i * 30 - 90
            x1, y1 = polar_to_xy(r_month * 0.92, angle, 0, 0)
            x2, y2 = polar_to_xy(r_month * 1.08, angle, 0, 0)
            self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2],
                          fill='black', width=3)
            x_t, y_t = polar_to_xy(r_month * 0.82, angle+15, 0, 0)
            self.text(MONTHS_AR[i], x_t, y_t, self.font_s)

        # 2. دائرة البروج - 360 درجة
        r_zodiac = self.radius * 0.75
        self.circle(r_zodiac, '#8B4513', 4)
        for i in range(12):
            angle = i * 30 - 90
            x1, y1 = polar_to_xy(r_zodiac * 0.9, angle, 0, 0)
            x2, y2 = polar_to_xy(r_zodiac * 1.1, angle, 0, 0)
            self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2],
                          fill='#8B4513', width=3)
            x_t, y_t = polar_to_xy(r_zodiac * 0.8, angle+15, 0, 0)
            self.text(ZODIAC_AR[i], x_t, y_t, self.font_s, '#8B4513')

    def draw_shadow_square(self):
        """مربع الظل - لحساب الارتفاع"""
        sq = self.radius * 0.5
        left = self.center - sq
        top = self.center - sq
        right = self.center + sq
        bottom = self.center + sq

        # المربع الخارجي
        self.draw.rectangle([left, top, right, bottom], outline='black', width=4)
        self.text("مربع الظل", 0, -sq-40, self.font_l)

        # تدريج 12 قسم
        for i in range(13):
            # أفقي
            y = top + i * (2*sq) / 12
            self.draw.line([left, y, left+20, y], fill='black', width=2)
            self.draw.line([right-20, y, right, y], fill='black', width=2)
            if i % 3 == 0:
                self.text(str(i), -sq-30, y-self.center, self.font_s)
                self.text(str(i), sq+30, y-self.center, self.font_s)

            # عمودي
            x = left + i * (2*sq) / 12
            self.draw.line([x, top, x, top+20], fill='black', width=2)
            self.draw.line([x, bottom-20, x, bottom], fill='black', width=2)
            if i % 3 == 0:
                self.text(str(i), x-self.center, -sq-30, self.font_s)
                self.text(str(i), x-self.center, sq+30, self.font_s)

        # القطر
        self.draw.line([left, bottom, right, top], fill='red', width=3)

    def draw_sine_quadrant(self):
        """ربع الجيب - أعلى يمين"""
        r = self.radius * 0.4
        cx = self.center + self.radius * 0.5
        cy = self.center - self.radius * 0.5

        # ربع الدائرة
        self.draw.arc([cx-r, cy-r, cx+r, cy+r], 270, 360, fill='blue', width=3)
        self.draw.line([cx, cy, cx+r, cy], fill='blue', width=2)
        self.draw.line([cx, cy, cx, cy-r], fill='blue', width=2)
        self.text("ربع الجيب", 0, -r-30, self.font_s, 'blue')

        # تدريج 90 درجة
        for deg in range(0, 91, 5):
            angle = 270 + deg
            x1, y1 = polar_to_xy(r*0.9, angle, cx-self.center, cy-self.center)
            x2, y2 = polar_to_xy(r, angle, cx-self.center, cy-self.center)
            self.draw.line([self.center+x1, self.center+y1, self.center+x2, self.center+y2],
                          fill='blue', width=1)

    def draw_title(self):
        self.text("ظهر الإسطرلاب", 0, -self.radius-80, self.font_t)
        self.text("التقويم الميلادي + البروج + مربع الظل", 0, self.radius+80, self.font_l)

    def render(self):
        self.draw_calendar_circles()
        self.draw_shadow_square()
        self.draw_sine_quadrant()
        self.draw_title()
        return self.img
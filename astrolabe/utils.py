# -*- coding: utf-8 -*-
import math
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont

def ar(text):
    """تحويل النص العربي للعرض الصحيح"""
    if not text: return ""
    return get_display(arabic_reshaper.reshape(str(text)))

def load_font(size):
    """تحميل خط القاهرة"""
    try: 
        return ImageFont.truetype("../fonts/Cairo-Regular.ttf", size)
    except: 
        try:
            return ImageFont.truetype("fonts/Cairo-Regular.ttf", size)
        except:
            return ImageFont.load_default()

def deg_to_rad(deg):
    return math.radians(deg)

def rad_to_deg(rad):
    return math.degrees(rad)

def stereographic_r(alt, r_max):
    """نصف قطر الإسقاط الستيريوجرافيك"""
    return r_max * math.tan(deg_to_rad((90 - alt) / 2))

def polar_to_xy(r, angle_deg, cx, cy):
    """تحويل من إحداثيات قطبية لكارتيزية"""
    angle = deg_to_rad(angle_deg - 90)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    return x, y

ZODIAC_AR = ["الحمل","الثور","الجوزاء","السرطان","الأسد","السنبلة","الميزان","العقرب","القوس","الجدي","الدلو","الحوت"]
ZODIAC_SYMBOLS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
CARDINAL = ["ش","ق","ج","غ"]
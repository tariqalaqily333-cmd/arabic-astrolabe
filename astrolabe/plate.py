# -*- coding: utf-8 -*-
"""
قاعدة بيانات النجوم الثابتة للإسطرلاب
المطلع المستقيم RA بالدرجات، الميل Dec بالدرجات لعام 2026
"""
STARS_2026 = [
    {"name": "الدبران", "arabic": "Aldebaran", "ra": 68.98, "dec": 16.51, "mag": 0.87},
    {"name": "العيوق", "arabic": "Capella", "ra": 79.17, "dec": 45.99, "mag": 0.08},
    {"name": "رجل الجبار", "arabic": "Rigel", "ra": 78.63, "dec": -8.20, "mag": 0.12},
    {"name": "منكب الجوزاء", "arabic": "Betelgeuse", "ra": 88.79, "dec": 7.41, "mag": 0.42},
    {"name": "الشعرى اليمانية", "arabic": "Sirius", "ra": 101.28, "dec": -16.72, "mag": -1.46},
    {"name": "الشعرى الشامية", "arabic": "Procyon", "ra": 114.82, "dec": 5.22, "mag": 0.34},
    {"name": "قلب الأسد", "arabic": "Regulus", "ra": 152.09, "dec": 11.97, "mag": 1.35},
    {"name": "السماك الأعزل", "arabic": "Spica", "ra": 201.30, "dec": -11.16, "mag": 0.98},
    {"name": "السماك الرامح", "arabic": "Arcturus", "ra": 213.92, "dec": 19.18, "mag": -0.05},
    {"name": "قلب العقرب", "arabic": "Antares", "ra": 247.35, "dec": -26.43, "mag": 1.06},
    {"name": "النسر الواقع", "arabic": "Vega", "ra": 279.23, "dec": 38.78, "mag": 0.03},
    {"name": "النسر الطائر", "arabic": "Altair", "ra": 297.70, "dec": 8.87, "mag": 0.77},
    {"name": "ذنب الدجاجة", "arabic": "Deneb", "ra": 310.36, "dec": 45.28, "mag": 1.25},
    {"name": "فم الحوت", "arabic": "Fomalhaut", "ra": 344.41, "dec": -29.62, "mag": 1.16},
    {"name": "سهيل", "arabic": "Canopus", "ra": 95.98, "dec": -52.70, "mag": -0.72},
    {"name": "الظليم", "arabic": "Achernar", "ra": 24.43, "dec": -57.24, "mag": 0.46},
    {"name": "حضار", "arabic": "Hadar", "ra": 210.96, "dec": -60.37, "mag": 0.61},
    {"name": "الرجل", "arabic": "Rigil Kentaurus", "ra": 219.92, "dec": -60.83, "mag": -0.01},
]

def get_stars():
    return STARS_2026

def get_bright_stars(mag_limit=2.0):
    """نجوم ألمع من القدر المحدد"""
    return [s for s in STARS_2026 if s['mag'] <= mag_limit]
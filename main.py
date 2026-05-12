from astrolabe import Astrolabe

def main():
    # إنشاء أسطرلاب للرياض
    ast = Astrolabe(latitude=24.7136, longitude=46.6753, name="Riyadh")
    
    # إضافة نجوم مشهورة
    stars = [
        ("Sirius", 101.287, -16.716),      # الشعرى اليمانية
        ("Betelgeuse", 88.793, 7.407),     # يد الجوزاء
        ("Vega", 279.235, 38.784),         # النسر الواقع
        ("Arcturus", 213.915, 19.182),     # السماك الرامح
    ]
    
    for name, ra, dec in stars:
        ast.add_star(name, ra, dec)
    
    # رسم كل الوجوه
    ast.render_mater("mater.png")
    ast.render_plate("plate.png") 
    ast.render_rete("rete.png")
    ast.render_back("back.png")
    
    print("خلصنا! الملفات اتحفظت: mater.png, plate.png, rete.png, back.png")

if __name__ == "__main__":
    main()
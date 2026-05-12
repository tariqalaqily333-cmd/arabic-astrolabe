import argparse
import json
from .core import Astrolabe

def main():
    parser = argparse.ArgumentParser(
        description='Astrolabe Generator - مولد الأسطرلاب العربي',
        epilog='مثال: astrolabe create --lat 24.7 --lon 46.7 --name Riyadh'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='الأوامر المتاحة')
    
    # 1. أمر create
    create_parser = subparsers.add_parser('create', help='إنشاء أسطرلاب جديد')
    create_parser.add_argument('--lat', type=float, required=True, help='خط العرض')
    create_parser.add_argument('--lon', type=float, required=True, help='خط الطول') 
    create_parser.add_argument('--name', type=str, default='MyCity', help='اسم الموقع')
    create_parser.add_argument('--output', type=str, default='astrolabe.json', help='ملف الحفظ')
    
    # 2. أمر add-star
    star_parser = subparsers.add_parser('add-star', help='إضافة نجم')
    star_parser.add_argument('--file', type=str, default='astrolabe.json', help='ملف الأسطرلاب')
    star_parser.add_argument('--name', type=str, required=True, help='اسم النجم')
    star_parser.add_argument('--ra', type=float, required=True, help='المطلع المستقيم بالدرجات')
    star_parser.add_argument('--dec', type=float, required=True, help='الميل بالدرجات')
    
    # 3. أمر render
    render_parser = subparsers.add_parser('render', help='رسم أجزاء الأسطرلاب')
    render_parser.add_argument('--file', type=str, default='astrolabe.json', help='ملف الأسطرلاب')
    render_parser.add_argument('--part', choices=['mater', 'plate', 'rete', 'back', 'all'], 
                              default='all', help='الجزء المراد رسمه')
    render_parser.add_argument('--outdir', type=str, default='.', help='مجلد الإخراج')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        ast = Astrolabe(args.lat, args.lon, args.name)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(ast.to_dict(), f, ensure_ascii=False, indent=2)
        print(f'تم إنشاء الأسطرلاب: {args.output}')
        
    elif args.command == 'add-star':
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ast = Astrolabe.from_dict(data)
        ast.add_star(args.name, args.ra, args.dec)
        with open(args.file, 'w', encoding='utf-8') as f:
            json.dump(ast.to_dict(), f, ensure_ascii=False, indent=2)
        print(f'تم إضافة النجم {args.name}')
        
    elif args.command == 'render':
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ast = Astrolabe.from_dict(data)
        
        if args.part in ['mater', 'all']:
            ast.render_mater(f'{args.outdir}/mater.png')
            print('تم رسم الأم: mater.png')
        if args.part in ['plate', 'all']:
            ast.render_plate(f'{args.outdir}/plate.png')
            print('تم رسم الصفيحة: plate.png')
        if args.part in ['rete', 'all']:
            ast.render_rete(f'{args.outdir}/rete.png')
            print('تم رسم العنكبوت: rete.png')
        if args.part in ['back', 'all']:
            ast.render_back(f'{args.outdir}/back.png')
            print('تم رسم الظهر: back.png')
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
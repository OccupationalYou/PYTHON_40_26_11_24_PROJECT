import json
from base import SessionLocal, create_db, Base, engine
from sqlalchemy import create_engine
from models.user import User
from models.product import Product
from models.associations import user_products

catalogData = {
    '1': {
        'name': 'Готові збірки',
        'items': [
            {"title": "Козак", "price": "9 200 грн", "images": ["/static/images/Kozak.jpg", "/static/images/Kozak_2.jpg", "/static/images/Kozak_3.jpg", "/static/images/Kozak_4.jpg", "/static/images/Kozak_5.jpg"], "description": "Ryzen 5 5500, 16GB DDR4, GTX 1660 Super, SSD 512GB"},
            {"title": "Отаман", "price": "15 600 грн", "images": ["/static/images/Otaman.jpg", "/static/images/Otaman_2.jpg", "/static/images/Otaman_3.jpg", "/static/images/Otaman_4.jpg", "static/images/Otaman_5.jpg"], "description": "i5-12400F, 32GB DDR4, RTX 3060, SSD 1TB"},
            {"title": "Король", "price": "34 900 грн", "images": ["/static/images/Korol.jpg", "/static/images/Korol_2.jpg", "/static/images/Korol_3.jpg", "/static/images/Korol_4.jpg", "/static/images/Korol_5.jpg"], "description": "i9-13900K, 64GB DDR5, RTX 4090, SSD 2TB"},
            {"title": "Гетьман", "price": "18 700 грн", "images": ["/static/images/Getman.jpg", "static/images/Getman_2.jpg", "/static/images/Getman_3.jpg", "static/images/Getman_4.jpg", "static/images/Getman_5.jpg"], "description": "Ryzen 7 7800X3D, 32GB DDR5, RTX 4070, SSD 1TB"},
            {"title": "Монстр", "price": "79 999 грн", "images": ["/static/images/Monstr.jpg", "/static/images/Monstr_2.jpg", "/static/images/Monstr_3.jpg", "/static/images/Monstr_4.jpg", "/static/images/Monstr_5.jpg"], "description": "i9-14900K, 128GB DDR5, RTX 4090, SSD 4TB"},
            {"title": "Легенда", "price": "22 100 грн", "images": ["/static/images/Legenda.jpg", "/static/images/Legenda_2.jpg", "/static/images/Legenda_3.jpg", "/static/images/Legenda_4.jpg", "/static/images/Legenda_5.jpg"], "description": "i7-14700K, 32GB DDR5, RTX 4070, SSD 1TB"},
            {"title": "Гарнір", "price": "12 000 грн", "images": ["/static/images/Garnir.jpg", "/static/images/Garnir_2.jpg", "/static/images/Garnir_3.jpg", "/static/images/Garnir_4.jpg", "/static/images/Garnir_5.jpg"], "description": "i5-10400F, 16GB DDR4, GTX 1650, SSD 512GB"},
        ]
    },
    '2': {
        'name': 'Материнські плати',
        'items': [
            {"title": "ASUS PRIME B450M-K II", "price": "2 500 грн", "images": ["/static/images/ASUS_PRIME_B450M-K_II.jpg", "/static/images/ASUS_PRIME_B450M-K_II_2.jpg"], "description": "Материнська плата ASUS PRIME B450M-K II - це надійне рішення для складання комп'ютера на базі процесорів AMD Ryzen. Вона підтримує DDR4 пам'ять і має всі необхідні роз'єми для підключення компонентів."},
            {"title": "ASUS Prime H510M A", "price": "3 100 грн", "images": ["/static/images/ASUS_Prime_H510M_A.jpg"], "description": "Материнська плата ASUS Prime H510M A - це компактна і функціональна материнська плата для процесорів Intel."},
            {"title": "Asus TUF GAMING B760-PLUS WIFI", "price": "7 600 грн", "images": ["/static/images/Asus_TUF_GAMING_B760-PLUS_WIFI.jpg"], "description": "Ігрова материнська плата Asus TUF GAMING B760-PLUS WIFI - це високопродуктивна плата з підтримкою Wi-Fi та RGB підсвічуванням."},
            {"title": "Gigabyte B550M Aorus Elite", "price": "4 000 грн", "images": ["/static/images/Gigabyte_B550M_Aorus_Elite.jpg"], "description": "Материнська плата Gigabyte B550M Aorus Elite - це відмінний вибір для ігрової системи з підтримкою процесорів AMD Ryzen."},
            {"title": "ASROCK B660M PG SONIC WIFI", "price": "5 000 грн", "images": ["/static/images/ASROCK_B660M_PG_SONIC_WIFI.jpg"], "description": "Материнська плата ASROCK B660M PG SONIC WIFI - це плата з унікальним дизайном Sonic та підтримкою Wi-Fi."},
            {"title": "MSI PRO B760M-P", "price": "5 500 грн", "images": ["/static/images/MSI_PRO_B760M-P.jpg"], "description": "Материнська плата MSI PRO B760M-P - це надійна і продуктивна плата для бізнес-завдань."},
            {"title": "GIGABYTE H410M H v2", "price": "2 000 грн", "images": ["/static/images/GIGABYTE_H410M_H_v2.jpg"], "description": "Материнська плата GIGABYTE H410M H v2 - це бюджетне рішення для офісних комп'ютерів."},
            {"title": "MSI MPG Z490 GAMING PLUS", "price": "6 000 грн", "images": ["/static/images/MSI_MPG_Z490_GAMING_PLUS.jpg"], "description": "Ігрова материнська плата MSI MPG Z490 GAMING PLUS - це потужна плата з підтримкою розгону процесорів Intel."},
        ]
    },
    '3': {
        'name': 'Процесори',
        'items': [
            {"title": "i5-10400f", "price": "3 500 грн", "images": ["/static/images/i5-10400f.jpg"], "description": "Процесор i5-10400f - це шестиядерний процесор з підтримкою багатопоточності."},
            {"title": "Ryzen 5 5600", "price": "4 000 грн", "images": ["/static/images/Ryzen_5_5600.jpg"], "description": "Процесор Ryzen 5 5600 - це шестиядерний процесор для ігрових і робочих завдань."},
            {"title": "i7 12700F", "price": "9 500 грн", "images": ["/static/images/i7_12700F.jpg"], "description": "Процесор i7 12700F - це потужний процесор для ігор і професійних програм."},
            {"title": "i3 13100", "price": "4 200 грн", "images": ["/static/images/i3_13100.jpg"], "description": "Процесор i3 13100 - це чотириядерний процесор для офісних і домашніх комп'ютерів."},
            {"title": "i7 14700KF", "price": "14 000 грн", "images": ["/static/images/i7_14700KF.jpg"], "description": "Процесор i7 14700KF - це високопродуктивний процесор для геймерів і розробників."},
            {"title": "i3 10105", "price": "2 500 грн", "images": ["/static/images/i3_10105.jpg"], "description": "Процесор i3 10105 - це бюджетний процесор для офісних завдань."},
            {"title": "i9 11900k", "price": "15 000 грн", "images": ["/static/images/i9_11900k.jpg"], "description": "Процесор i9 11900k - це потужний процесор для ігрових систем."},
            {"title": "Ryzen7 5700g", "price": "7 000 грн", "images": ["/static/images/Ryzen7_5700g.jpg"], "description": "Процесор Ryzen7 5700g - це процесор з вбудованим графічним ядром."},
        ]
    },
    '4': {
        'name': 'Кулери',
        'items': [
            {"title": "Cooler Master Hyper 212", "price": "1 200 грн", "images": ["/static/images/Cooler_Master_Hyper_212.jpg"], "description": "Cooler Master Hyper 212 - це популярний кулер з великим радіатором і тихим вентилятором."},
            {"title": "ID-Cooling SE-214-XT ARGB", "price": "900 грн", "images": ["/static/images/ID-Cooling_SE-214-XT_ARGB.jpg"], "description": "ID-Cooling SE-214-XT ARGB - це кулер з ARGB підсвічуванням і ефективним охолодженням."},
            {"title": "Jonsbo CR-1200 Black", "price": "700 грн", "images": ["/static/images/Jonsbo_CR-1200_Black.jpg"], "description": "Jonsbo CR-1200 Black - це компактний кулер з RGB підсвічуванням."},
            {"title": "Б/У Кулер INTEL", "price": "150 грн", "images": ["/static/images/BU_Kuler_INTEL.jpg"], "description": "Б/У Кулер INTEL - це стандартний кулер для процесорів Intel."},
            {"title": "ID-Cooling", "price": "300 грн", "images": ["/static/images/ID-Cooling.jpg"], "description": "ID-Cooling - це універсальний кулер для процесорів AMD і Intel."},
            {"title": "Deepcool Iceedge mini fs 2.0", "price": "600 грн", "images": ["/static/images/Deepcool_Iceedge_mini_fs_2.0.jpg"], "description": "Deepcool Iceedge mini fs 2.0 - це мініатюрний кулер для невеликих корпусів."},
            {"title": "AIGO ICE200PRO", "price": "800 грн", "images": ["/static/images/AIGO_ICE200PRO.jpg"], "description": "AIGO ICE200PRO - це кулер з RGB підсвічуванням."},
            {"title": "Cooler Master Hyper 717", "price": "1 500 грн", "images": ["/static/images/Cooler_Master_Hyper_717.jpg"], "description": "Cooler Master Hyper 717 - це потужний кулер для високоефективних процесорів."},
        ]
    },
    '5': {
        'name': 'Оперативна пам\'ять',
        'items': [
            {"title": "Kingston DDR4 16GB", "price": "1 500 грн", "images": ["/static/images/Kingston_DDR4_16GB.jpg"], "description": "Оперативна пам'ять Kingston DDR4 16GB - це стандартний модуль пам'яті для сучасних комп'ютерів."},
            {"title": "HyperX DDR4 16GB", "price": "1 800 грн", "images": ["/static/images/HyperX_DDR4_16GB.jpg"], "description": "Оперативна пам'ять HyperX DDR4 16GB - це високопродуктивний модуль для ігрових систем."},
            {"title": "G.Skill DDR4 32 GB", "price": "2 500 грн", "images": ["/static/images/G.Skill_DDR4_32_GB.jpg"], "description": "Оперативна пам'ять G.Skill DDR4 32 GB - це великий об'єм пам'яті для професійних завдань."},
            {"title": "Patriot DDR5 32GB", "price": "3 500 грн", "images": ["/static/images/Patriot_DDR5_32GB.jpg"], "description": "Оперативна пам'ять Patriot DDR5 32GB - це новий стандарт пам'яті з високою швидкістю."},
            {"title": " G.Skill DDR4 16GB", "price": "1 700 грн", "images": ["/static/images/G.Skill_DDR4_16GB.jpg"], "description": "Оперативна пам'ять G.Skill DDR4 16GB - це надійний модуль пам'яті."},
            {"title": "Kingston Fury DDR5 32GB", "price": "4 000 грн", "images": ["/static/images/Kingston_Fury_DDR5_32GB.jpg"], "description": "Оперативна пам'ять Kingston Fury DDR5 32GB - це високошвидкісний модуль для ігрових систем."},
            {"title": "Exceleram DDR5 64 GB", "price": "7 000 грн", "images": ["/static/images/Exceleram_DDR5_64_GB.jpg"], "description": "Оперативна пам'ять Exceleram DDR5 64 GB - це великий об'єм пам'яті для професійних завдань."},
            {"title": "Trazident DDR4 32GB", "price": "2 800 грн", "images": ["/static/images/Trazident_DDR4_32GB.jpg"], "description": "Оперативна пам'ять Trazident DDR4 32GB - це надійний модуль пам'яті."},
        ]
    },
    '6': {
        'name': 'Відеокарти',
        'items': [
            {"title": "RX5700XT", "price": "5 500 грн", "images": ["/static/images/RX5700XT.jpg"], "description": "Відеокарта RX5700XT - це потужна відеокарта для ігрових систем."},
            {"title": "RX580", "price": "3 500 грн", "images": ["/static/images/RX580.jpg"], "description": "Відеокарта RX580 - це надійна відеокарта для ігор і робочих завдань."},
            {"title": "RX6800XT", "price": "11 000 грн", "images": ["/static/images/RX6800XT.jpg"], "description": "Відеокарта RX6800XT - це високопродуктивна відеокарта для геймерів."},
            {"title": "RTX5070TI", "price": "25 000 грн", "images": ["/static/images/RTX5070TI.jpg"], "description": "Відеокарта RTX5070TI - це потужна відеокарта для ігор і професійних програм."},
            {"title": "RTX3060TI", "price": "10 500 грн", "images": ["/static/images/RTX3060TI.jpg"], "description": "Відеокарта RTX3060TI - це оптимальний вибір для ігрових систем."},
            {"title": "RTX4070TI", "price": "20 000 грн", "images": ["/static/images/RTX4070TI.jpg"], "description": "Відеокарта RTX4070TI - це високопродуктивна відеокарта."},
            {"title": "RX7900XTX", "price": "20 000 грн", "images": ["/static/images/RX7900XTX.jpg"], "description": "Відеокарта RX7900XTX - це топова відеокарта для геймерів."},
            {"title": "RTX2060super", "price": "8 000 грн", "images": ["/static/images/RTX2060super.jpg"], "description": "Відеокарта RTX2060super - це потужна відеокарта."},
        ]
    },
    '7': {
        'name': 'Накопичувачі',
        'items': [
            {"title": "SSD Samsung 1TB", "price": "2 000 грн", "images": ["/static/images/SSD_Samsung_1TB.jpg"], "description": "Накопичувач SSD Samsung 1TB - це швидкий і надійний SSD накопичувач."},
            {"title": "SSD Kingston 480GB", "price": "1 000 грн", "images": ["/static/images/SSD_Kingston_480GB.jpg"], "description": "Накопичувач SSD Kingston 480GB - це надійний і швидкий накопичувач."},
            {"title": "SSD Patriot 128GB", "price": "500 грн", "images": ["/static/images/SSD_Patriot_128GB.jpg"], "description": "Накопичувач SSD Patriot 128GB - це бюджетний накопичувач."},
            {"title": "SSD Patriot 256GB", "price": "700 грн", "images": ["/static/images/SSD_Patriot_256GB.jpg"], "description": "Накопичувач SSD Patriot 256GB - це надійний накопичувач."},
            {"title": "SSD Apacer 240GB", "price": "600 грн", "images": ["/static/images/SSD_Apacer_240GB.jpg"], "description": "Накопичувач SSD Apacer 240GB - це бюджетний накопичувач."},
            {"title": "SSD Prologix 1 TB", "price": "1 900 грн", "images": ["/static/images/SSD_Prologix_1_TB.jpg"], "description": "Накопичувач SSD Prologix 1 TB - це великий об'єм пам'яті для зберігання даних."},
            {"title": "SSD Samsung 512 GB", "price": "1 200 грн", "images": ["/static/images/SSD_Samsung_512_GB.jpg"], "description": "Накопичувач SSD Samsung 512 GB - це швидкий і надійний накопичувач."},
            {"title": "SSD Patriot 480gb", "price": "1 100 грн", "images": ["/static/images/SSD_Patriot_480gb.jpg"], "description": "Накопичувач SSD Patriot 480gb - це надійний накопичувач."},
        ]
    },
    '8': {
        'name': 'Блоки живлення',
        'items': [
            {"title": "Chieftec 600W", "price": "1 600 грн", "images": ["/static/images/Chieftec_600W.jpg"], "description": "Блок живлення Chieftec 600W - це надійний блок живлення для ігрових систем."},
            {"title": "GameMax 600W", "price": "1 500 грн", "images": ["/static/images/GameMax_600W.jpg"], "description": "Блок живлення GameMax 600W - це блок живлення для ігрових систем."},
            {"title": "AeroCool VX Plus 500", "price": "1 000 грн", "images": ["/static/images/AeroCool_VX_Plus_500.jpg"], "description": "Блок живлення AeroCool VX Plus 500 - це бюджетний блок живлення."},
            {"title": "Chieftec 750w", "price": "2 000 грн", "images": ["/static/images/Chieftec_750w.jpg"], "description": "Блок живлення Chieftec 750w - це потужний блок живлення для високопродуктивних систем."},
            {"title": "MSI MPG 850W", "price": "3 000 грн", "images": ["/static/images/MSI_MPG_850W.jpg"], "description": "Блок живлення MSI MPG 850W - це потужний блок живлення з RGB підсвічуванням."},
            {"title": "Chieftec 850w", "price": "2 800 грн", "images": ["/static/images/Chieftec_850w.jpg"], "description": "Блок живлення Chieftec 850w - це потужний блок живлення."},
            {"title": "Gigabyte 650w", "price": "1 800 грн", "images": ["/static/images/Gigabyte_650w.jpg"], "description": "Блок живлення Gigabyte 650w - це надійний блок живлення."},
            {"title": "Gamemax 500W", "price": "1 200 грн", "images": ["/static/images/Gamemax_500W.jpg"], "description": "Блок живлення Gamemax 500W - це бюджетний блок живлення."},
        ]
    },
    '9': {
        'name': 'Корпуси',
        'items': [
            {"title": "GameMax Storm Black", "price": "2 000 грн", "images": ["/static/images/GameMax_Storm_Black.jpg"], "description": "Корпус GameMax Storm Black - це стильний корпус з RGB підсвічуванням."},
            {"title": "GameMax MT525", "price": "1 800 грн", "images": ["/static/images/GameMax_MT525.jpg"], "description": "Корпус GameMax MT525 - це компактний корпус для невеликих збірок."},
            {"title": "Gamdias Aura", "price": "2 500 грн", "images": ["/static/images/Gamdias_Aura.jpg"], "description": "Корпус Gamdias Aura - це корпус з унікальним дизайном."},
            {"title": "GTL", "price": "1 000 грн", "images": ["/static/images/GTL.jpg"], "description": "Корпус GTL - це бюджетний корпус для офісних комп'ютерів."},
            {"title": "Vinga Ghost", "price": "1 500 грн", "images": ["/static/images/Vinga_Ghost.jpg"], "description": "Корпус Vinga Ghost - це стильний корпус з прозорою бічною панеллю."},
        ]
    }
}


def drop_all_tables():
    """Drops all tables from the database."""
    print("Удаление существующих таблиц...")
    Base.metadata.drop_all(bind=engine)
    print("Все таблицы удалены.")


def load_products_to_db():
    """Loads product data from JSON to the database."""
    create_db()

    with SessionLocal() as session:
        all_products = []
        for category_id, category_data in catalogData.items():
            category_name = category_data['name']
            for item in category_data['items']:
                try:
                    images_json = json.dumps(item['images'])

                    price_str = item['price'].lower().replace("грн", "").replace(" ", "").strip()
                    price = float(price_str)

                    product = Product(
                        name=item['title'],
                        price=price,
                        description=item['description'],
                        image_url=images_json,
                        user_id=1
                    )
                    all_products.append(product)
                except Exception as e:
                    print(f"Ошибка при обработке элемента: {item['title']}. Ошибка: {e}")
                    continue

        session.bulk_save_objects(all_products)
        session.commit()
    print("Данные успешно занесены в базу данных!")
    print(f"Всего добавлено элементов: {len(all_products)}")


if __name__ == "__main__":
    drop_all_tables()
    load_products_to_db()

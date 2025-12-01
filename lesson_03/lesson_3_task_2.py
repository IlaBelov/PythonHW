from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 17", "+79111234567"),
    Smartphone("Samsung", "Galaxy S25", "+79222345678"),
    Smartphone("Xiaomi", "Redmi Note 14 Pro", "+79333456789"),
    Smartphone("Huawei", "Pura 80", "+79444567890"),
    Smartphone("Vivo", "X200", "+79555678901")
]
for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")

from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Catalog  # Cambia "catalog" por el nombre de tu app

PRODUCTS = [
    {
        "name": "Mesa Redonda Blanca",
        "description": "Mesa redonda para eventos con capacidad para 8 personas.",
        "price": Decimal("95.00"),
        "stock": 20,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387151/images_3_jjedmv.jpg",
        "categories": "mobiliario",
    },
    {
        "name": "Silla Tiffany Blanca",
        "description": "Silla elegante para bodas y eventos.",
        "price": Decimal("12.50"),
        "stock": 300,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387086/alquiler-muebles-eventos_silla-tiffany-blanca_sttnqz.jpg",
        "categories": "mobiliario",
    },
    {
        "name": "Mantel Blanco",
        "description": "Mantel de tela premium para mesas redondas.",
        "price": Decimal("18.00"),
        "stock": 100,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387086/imageUrl_1_th0b9i.webp",
        "categories": "mobiliario",
    },
    {
        "name": "Plato Base Dorado",
        "description": "Plato decorativo para montaje de mesa.",
        "price": Decimal("4.50"),
        "stock": 200,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387086/Image-1_rxfb2x.webp",
        "categories": "vajilla",
    },
    {
        "name": "Juego de Cubiertos",
        "description": "Cubiertos de acero inoxidable.",
        "price": Decimal("3.00"),
        "stock": 400,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1748126917/couvert-dore-cuillere-couteau-fourchette_tanns1.jpg",
        "categories": "vajilla",
    },
    {
        "name": "Copa de Vino",
        "description": "Copa de cristal elegante.",
        "price": Decimal("2.80"),
        "stock": 500,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387934/copa-vino-50-cl-vinetis_ckk4ho.jpg",
        "categories": "vajilla",
    },
    {
        "name": "Centro de Mesa Floral",
        "description": "Arreglo floral decorativo.",
        "price": Decimal("45.00"),
        "stock": 40,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387935/images_4_bavymc.jpg",
        "categories": "decoracion",
    },
    {
        "name": "Arco de Globos",
        "description": "Arco decorativo para fiestas.",
        "price": Decimal("120.00"),
        "stock": 15,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387934/imagen2-1_jnrabh.webp",
        "categories": "decoracion",
    },
    {
        "name": "Guirnalda LED",
        "description": "Luces LED cálidas decorativas.",
        "price": Decimal("35.00"),
        "stock": 60,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387934/images_5_bcyjf3.jpg",
        "categories": "iluminacion",
    },
    {
        "name": "Reflector RGB",
        "description": "Reflector LED para ambientación.",
        "price": Decimal("80.00"),
        "stock": 25,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1748126928/productos31_17983_hwyoxy.jpg",
        "categories": "iluminacion",
    },
    {
        "name": "Parlante Profesional",
        "description": "Equipo de sonido para eventos.",
        "price": Decimal("350.00"),
        "stock": 10,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1748126916/productos31_122850_ub6oii.jpg",
        "categories": "iluminacion",
    },
    {
        "name": "Castillo Inflable",
        "description": "Juego inflable para niños.",
        "price": Decimal("650.00"),
        "stock": 5,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387934/image-95ed8e9b85024f4b9cafec913f4c3f1e_xo5ukw.png",
        "categories": "entretenimiento",
    },
    {
        "name": "Máquina de Algodón",
        "description": "Máquina para preparar algodón de azúcar.",
        "price": Decimal("180.00"),
        "stock": 8,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/w_1500_h_1500_fit_cover_iq1cmj.webp",
        "categories": "entretenimiento",
    },
    {
        "name": "Fuente de Chocolate",
        "description": "Fuente para eventos.",
        "price": Decimal("240.00"),
        "stock": 6,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/Fuente-de-Chocolate-en-Cascada-de-Acero-Inoxidable-Nostalgia_g47fmu.webp",
        "categories": "comida_bebidas",
    },
    {
        "name": "Dispensador de Bebidas",
        "description": "Dispensador de jugos o cócteles.",
        "price": Decimal("65.00"),
        "stock": 20,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/w_1500_h_1500_fit_cover_1_g24tjp.webp",
        "categories": "comida_bebidas",
    },
    {
        "name": "Carpa 6x6",
        "description": "Carpa impermeable para eventos.",
        "price": Decimal("950.00"),
        "stock": 8,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/images_6_swhhsg.jpg",
        "categories": "infraestructura",
    },
    {
        "name": "Pista de Baile",
        "description": "Piso modular para baile.",
        "price": Decimal("1200.00"),
        "stock": 4,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/877A-Frosted-and-Morror-Dance-Floor_zwlzww.jpg",
        "categories": "infraestructura",
    },
    {
        "name": "Decoración Temática Frozen",
        "description": "Kit decorativo inspirado en Frozen.",
        "price": Decimal("180.00"),
        "stock": 10,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/1b51cf1ae1bc578cb9fea3a7eaa601c2_iusucv.jpg",
        "categories": "tematica",
    },
    {
        "name": "Kit de Cumpleaños Unicornio",
        "description": "Decoración temática completa.",
        "price": Decimal("150.00"),
        "stock": 12,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387933/81Pl8TX86_L._AC_UF894_1000_QL80__pcn21k.jpg",
        "categories": "tematica",
    },
    {
        "name": "Basurero para Eventos",
        "description": "Basurero plástico resistente.",
        "price": Decimal("25.00"),
        "stock": 30,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387932/images_7_spnzfr.jpg",
        "categories": "limpieza",
    },
    {
        "name": "Paquete de Bolsas de Basura",
        "description": "Bolsas resistentes de alta capacidad.",
        "price": Decimal("8.00"),
        "stock": 100,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387932/23834_ubmnrt.webp",
        "categories": "limpieza",
    },
    {
        "name": "Servicio de DJ",
        "description": "DJ profesional para fiestas.",
        "price": Decimal("900.00"),
        "stock": 10,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387934/images_8_dmquli.jpg",
        "categories": "servicios",
    },
    {
        "name": "Servicio de Fotografía",
        "description": "Cobertura fotográfica del evento.",
        "price": Decimal("1200.00"),
        "stock": 5,
        "image_url": "https://res.cloudinary.com/db4psl26k/image/upload/v1784387932/fotografia-profesional-1200px_eyyoww.webp",
        "categories": "servicios",
    },
]


class Command(BaseCommand):
    help = "Carga productos de ejemplo en el catálogo."

    def handle(self, *args, **kwargs):
        created = 0

        for product in PRODUCTS:
            _, was_created = Catalog.objects.get_or_create(
                name=product["name"], defaults=product
            )

            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Se crearon {created} productos."))

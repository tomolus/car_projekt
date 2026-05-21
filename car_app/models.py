from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, help_text="Produktionsland")

    def __str__(self):
        return self.name

class Car(models.Model):
    # Relationen
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='cars')
    
    # Basisdaten
    model_name = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Kategorien (Choices)
    CAR_TYPES = [('Limousine', 'Limousine'), ('SUV', 'SUV'), ('Kombi', 'Kombi'), ('Coupé', 'Coupé'), ('Cabrio', 'Cabrio'), ('Hatchback', 'Hatchback'), ('Pickup', 'Pickup'), ('Sportwagen', 'Supersportwagen'), ('Van', 'Van')]
    car_type = models.CharField(max_length=50, choices=CAR_TYPES)
    
    ENGINE_TYPES = [('Benzin', 'Benzin'), ('Diesel', 'Diesel'), ('Hybrid', 'Hybrid'), ('Elektro', 'Elektro'), ('Wasserstoff', 'Wasserstoff')]
    engine_type = models.CharField(max_length=50, choices=ENGINE_TYPES)
    
    TRANSMISSION_TYPES = [('Manuell', 'Manuell'), ('Automatik', 'Automatik'), ('Doppelkupplung', 'Doppelkupplung'), ('CVT', 'CVT')]
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_TYPES)
    
    DRIVE_TYPES = [('Front', 'Frontantrieb'), ('Heck', 'Heckantrieb'), ('Allrad', 'Allrad')]
    drive_type = models.CharField(max_length=50, choices=DRIVE_TYPES)

    # Leistungsdaten
    hp = models.IntegerField(help_text="PS")
    kw = models.IntegerField(help_text="kW", blank=True, null=True)
    torque = models.IntegerField(help_text="Drehmoment in Nm")
    top_speed = models.IntegerField(help_text="km/h")
    acceleration = models.FloatField(help_text="0-100 km/h in Sekunden")
    
    # Effizienz
    consumption = models.FloatField(help_text="l/100 km oder kWh/100 km")
    range = models.IntegerField(help_text="Reichweite in km", blank=True, null=True)
    capacity = models.FloatField(help_text="Tank (Liter) oder Batterie (kWh)")

    # Maße & Gewicht
    length = models.IntegerField(help_text="Länge in mm")
    width = models.IntegerField(help_text="Breite in mm")
    height = models.IntegerField(help_text="Höhe in mm")
    trunk_volume = models.IntegerField(help_text="Kofferraum in Liter")
    weight = models.IntegerField(help_text="Leergewicht in kg")
    seats = models.IntegerField()

    # Ausstattung
    safety_features = models.TextField(help_text="z.B. ABS, 6 Airbags, ESP")
    assistance_systems = models.TextField(help_text="z.B. Abstandstempomat, Spurhalteassistent")

    def save(self, *args, **kwargs):
        # Automatische Umrechnung von PS in kW, falls nicht angegeben (1 PS ≈ 0.735 kW)
        if self.hp and not self.kw:
            self.kw = int(self.hp * 0.735499)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.manufacturer.name} {self.model_name} ({self.year})"
        

# Create your models here.

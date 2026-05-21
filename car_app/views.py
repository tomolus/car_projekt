from django.shortcuts import render, get_object_or_404
from .models import Manufacturer, Car
import math

def manufacturer_select(request):
    """Schritt 1: Hersteller auswählen"""
    manufacturers = Manufacturer.objects.all()
    return render(request, 'car_app/manufacturer_select.html', {'manufacturers': manufacturers})

def car_search(request, manufacturer_id=None):
    """Schritt 2: Suchen, Filtern und Ähnlichkeitssuche"""
    
    # Zwang: Wenn kein Hersteller gewählt wurde, leite um (deaktivierbar, siehe Tipps)
    cars = Car.objects.all()
    if manufacturer_id:
        cars = cars.filter(manufacturer_id=manufacturer_id)

    # 1. Genaue Namenssuche
    query = request.GET.get('q')
    if query:
        cars = cars.filter(model_name__icontains=query)

    # 2. Harte Filter (Fahrzeugtyp, max. Preis, min. Sitze)
    car_type = request.GET.get('car_type')
    if car_type:
        cars = cars.filter(car_type=car_type)
        
    max_price = request.GET.get('max_price')
    if max_price:
        cars = cars.filter(price__lte=max_price)

    # 3. ÄHNLICHKEITS-ALGORITHMUS (Match-Score)
    # Finde das Auto, das den gewünschten Werten am nächsten kommt
    target_hp = request.GET.get('target_hp')
    target_consumption = request.GET.get('target_consumption')
    
    scored_cars = []
    if target_hp or target_consumption:
        for car in cars:
            score = 0
            # Je geringer die Abweichung, desto besser (niedriger Score = besser)
            if target_hp:
                # Straf-Punkte für PS-Abweichung (z.B. 1 Punkt pro fehlendem/überschüssigem PS)
                score += abs(car.hp - int(target_hp))
            if target_consumption:
                # Straf-Punkte für Verbrauch (z.B. 10 Punkte pro Liter Abweichung, um es zu gewichten)
                score += abs(car.consumption - float(target_consumption)) * 10
            
            scored_cars.append((score, car))
        
        # Sortiere nach bestem Score (niedrigster Wert zuerst)
        scored_cars.sort(key=lambda x: x[0])
        # Extrahiere nur die Autos aus der sortierten Liste
        cars = [item[1] for item in scored_cars]

    context = {
        'cars': cars,
        'car_types': Car.CAR_TYPES,
        'selected_manufacturer_id': manufacturer_id
    }
    return render(request, 'car_app/search.html', context)
    def car_compare(request, car1_id, car2_id):
    car1 = get_object_or_404(Car, id=car1_id)
    car2 = get_object_or_404(Car, id=car2_id)
    
    # Optional: Differenzen berechnen, um sie im Template farblich zu markieren
    diff_price = car1.price - car2.price
    diff_hp = car1.hp - car2.hp
    
    context = {
        'car1': car1,
        'car2': car2,
        'diff_price': diff_price,
        'diff_hp': diff_hp
    }
    return render(request, 'car_app/compare.html', context)

# Create your views here.

from PIL import Image, ExifTags
from fractions import Fraction
from datetime import datetime
from django.utils import timezone
from math import radians, cos, sin, asin, sqrt
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def extract_metadata(file_obj):
    try:
        image = Image.open(file_obj)
        exif_data = image._getexif()
        if not exif_data:
            return None

        exif = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}

        gps_info = exif.get("GPSInfo")
        if not gps_info:
            return None

        gps_data = {ExifTags.GPSTAGS.get(k, k): gps_info[k] for k in gps_info.keys()}

        lat = convert_to_degrees(gps_data["GPSLatitude"])
        if gps_data["GPSLatitudeRef"] != "N":
            lat = -lat

        lon = convert_to_degrees(gps_data["GPSLongitude"])
        if gps_data["GPSLongitudeRef"] != "E":
            lon = -lon

        alt = gps_data.get("GPSAltitude")
        alt = float(Fraction(alt)) if alt else None

        raw_date = clean_exif_string(exif.get("DateTimeOriginal", ""))
        date_taken = None
        if raw_date:
            date_taken = timezone.make_aware(
                datetime.strptime(raw_date, "%Y:%m:%d %H:%M:%S")
            )

        return {
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "date_taken": date_taken,
            "marca": clean_exif_string(exif.get("Make", "No disponible")),
            "model": clean_exif_string(exif.get("Model", "No disponible")),
            "software": clean_exif_string(exif.get("Software", "No disponible")),
            "orientation": exif.get("Orientation", 1),
            "direction": clean_exif_string(exif.get("GPSImgDirection", 0)),
        }
    except Exception as e:
        print(f"Error extrayendo metadatos: {e}")
        return None


def convert_to_degrees(value):
    d = float(Fraction(value[0]))
    m = float(Fraction(value[1]))
    s = float(Fraction(value[2]))
    return d + (m / 60.0) + (s / 3600.0)


# Limpia los caracteres nulos de la cadena EXIF
def clean_exif_string(value):
    if isinstance(value, str):
        return value.replace("\x00", "").strip()
    return value


def calculate_distance_meters(lat1, lon1, alt1, lat2, lon2, alt2):
    # Radio de la tierra en metros
    R = 6371000

    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dalt = alt2 - alt1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    distancia_horizontal = R * c

    # Distancia real incluyendo altitud
    distancia_total = sqrt(distancia_horizontal**2 + dalt**2)
    return distancia_total


def send_upload_and_not_upload_panoramas(not_upload_panoramas, upload_panoramas, first_name, last_name, email):
    full_name = f"{first_name} {last_name}"

    subject = "Resumen de carga de panoramas"

    html_content = render_to_string(
        "emails/upload_and_not_upload_panoramas.html",  # Asegúrate que este template existe
        {
            "full_name": full_name,
            "email": email,
            "upload_panoramas": upload_panoramas,
            "not_upload_panoramas": not_upload_panoramas,
            "login_url": "https://beautiful-einstein.51-79-98-210.plesk.page/stratiview/auth/sign_in/",
        },
    )

    email_msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send(fail_silently=False)


def calculate_decimal_range(value_str):
    if "." in value_str:
        decimals = len(value_str.split(".")[1])
        return 10 ** (-decimals)
    return 0.0001  # default fallback
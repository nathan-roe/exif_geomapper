import os
import re
import ffmpeg
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener


asset_dir = "assets"
directory = os.fsencode(asset_dir)

for file in os.listdir(directory):
    try:

        filename = os.fsdecode(file)
        img_path = os.path.join(asset_dir, filename)

        if(filename.endswith('.heic')):
            register_heif_opener()

        if(filename.lower().endswith(('mov','mp4','m4a','3gp','3g2','mj2'))):
            video = ffmpeg.probe(img_path)
            for key,value in video['format']['tags'].items():
                # convert decimal degrees to DMS
                if(key.endswith('location.ISO6709')):
                    decimals = re.split(r'[+-]', value)
                    coordinates = []
                    for position in (
                            {'degree': float(decimals[1]), 'cardinal': 'N' if float(decimals[1]) > 0 else 'S'},
                            {'degree': float(decimals[2]), 'cardinal': 'W' if float(decimals[2]) > 0 else 'E'}):
                        d = int(position['degree'])
                        m = (position['degree'] - d) * 60;
                        s = round((m - int(m)) * 60, 3)
                        m = int(m)
                        coordinates.append(f'{d}°{m}\'{s}"{position["cardinal"]}')
                    print(f'GPS info found - {img_path}:\n\t- formatted location: {" ".join(coordinates)}\n')
                                
        else:
            GPS_TAG_ID = next(tag for tag,name in ExifTags.TAGS.items() if name == "GPSInfo")
    
            img = Image.open(img_path)
            exif_data = img.getexif()
    
            gps_data = exif_data.get_ifd(GPS_TAG_ID)
    
            if(len(gps_data.keys()) == 0):
                print(f'No GPS tag - img: {img_path}\n')
                print(f'exif data: {exif_data}')
                continue

            formatted_location = f'{int(gps_data[2][0])}°{int(gps_data[2][1])}\'{float(round(gps_data[2][2], 1))}"{gps_data[1]} {int(gps_data[4][0])}°{int(gps_data[4][1])}\'{gps_data[4][2]}"{gps_data[3]}'
            formatted_gps_data = "\n\t\t- ".join([f'{k}: {v}' for k,v in gps_data.items()])

            print(f'GPS info found - {img_path}:\n\t- formatted location: {formatted_location}\n\t- GPS data: \n\t\t- {formatted_gps_data}\n')
    except Exception as e:
        print(f'There was an error parsing the image data: {e}')

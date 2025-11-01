import xml.etree.ElementTree as ET
import glob
import os
import json

def xml_to_yolo_bbox(bbox, w, h):
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


input_dir = "../datasets/ACID_7000/Annotations"
output_dir = "../datasets/ACID_7000/labels" 
image_dir = "../datasets/ACID_7000/JPEG/images"

classes = []
os.makedirs(output_dir, exist_ok=True)

archivos_xml = glob.glob(os.path.join(input_dir, '*.xml'))

print(f"Procesando {len(archivos_xml)} archivos XML...")

for archivo_xml in archivos_xml:
    nombre = os.path.basename(archivo_xml)
    nombre_archivo = os.path.splitext(nombre)[0]
    
    imagen_path = os.path.join(image_dir, f"{nombre_archivo}.jpg")
    
    if os.path.exists(imagen_path):
        resultado = []
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        width = int(root.find("size").find("width").text)
        height = int(root.find("size").find("height").text)

        for obj in root.findall('object'):
            etiqueta = obj.find("name").text

            if etiqueta not in classes:
                classes.append(etiqueta)
            index = classes.index(etiqueta)
            
            bndbox = obj.find("bndbox")
            pil_bbox = [
                int(bndbox.find("xmin").text),
                int(bndbox.find("ymin").text),
                int(bndbox.find("xmax").text), 
                int(bndbox.find("ymax").text)
            ]
            
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            resultado.append(f"{index} {bbox_string}")

        if resultado:
            with open(os.path.join(output_dir, f"{nombre_archivo}.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(resultado))

with open('../datasets/classes.txt', 'w', encoding='utf-8') as f:
    json.dump(classes, f, indent=2)


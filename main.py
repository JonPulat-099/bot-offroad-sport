# Install: pip install img2table pytesseract pillow
from img2table.ocr import TesseractOCR
from img2table.document import Image
import pandas as pd
import argparse
import xml.etree.ElementTree as ET


def extract_table_img2table(image_path):
    # Initialize OCR
    ocr = TesseractOCR(n_threads=1, lang="eng")

    # Load image
    doc = Image(image_path, detect_rotation=True)

    # Extract tables
    extracted_tables = doc.extract_tables(
        ocr=ocr, implicit_rows=True, borderless_tables=True
    )

    # Convert to DataFrame
    if extracted_tables:
        table_data = extracted_tables[0].df  # First table
        return table_data
    return None


def generate_kml(df, output_file):
    # Create KML structure
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")

    # Add document name
    name = ET.SubElement(document, "n")
    name.text = "OFF ROAD POINTS"

    for index, row in df.iterrows():
        # Create placemark for each point
        placemark = ET.SubElement(document, "Placemark")

        # Name (column 0)
        name_elem = ET.SubElement(placemark, "name")
        name_elem.text = str(f"Point {index + 1}: F{row.iloc[0]}")

        # Description (column 3)
        if len(row) > 3:
            desc_elem = ET.SubElement(placemark, "description")
            desc_elem.text = str(f"Ball: {row.iloc[3]}")

        # Coordinates (columns 1,2 = lat,lon)
        point = ET.SubElement(placemark, "Point")
        coordinates = ET.SubElement(point, "coordinates")
        # KML format: lon,lat,altitude
        coordinates.text = f"{row.iloc[2]},{row.iloc[1]},0"

    # Write to file
    tree = ET.ElementTree(kml)
    ET.indent(tree, space="  ", level=0)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract table from image and generate KML"
    )
    parser.add_argument("image", help="Path to image file")
    parser.add_argument("-startrow", type=int, default=1, help="Start row index")
    parser.add_argument("-endrow", type=int, default=None, help="End row index")
    parser.add_argument(
        "-cols",
        nargs="+",
        type=int,
        default=[1, 2, 3, 4],
        help="Column indices (name,lat,lon,desc)",
    )
    parser.add_argument("-o", "--output", default="points.kml", help="Output KML file")

    args = parser.parse_args()

    df = extract_table_img2table(args.image)
    if df is not None:
        end_row = args.endrow if args.endrow else len(df)

        selected_df = df.iloc[args.startrow : end_row, args.cols]
        print("Extracted data:")
        print(selected_df)

        # Generate KML file
        generate_kml(selected_df, args.output)
        print(f"KML file saved as: {args.output}")
    else:
        print("No table found in image")

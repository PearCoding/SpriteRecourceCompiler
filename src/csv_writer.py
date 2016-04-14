import csv


class CSVWriter:
    @staticmethod
    def write(path, tiles):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            for tile in tiles:
                writer.writerow([tile.x, tile.y, tile.width, tile.height])

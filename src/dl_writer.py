
class DLWriter:
    @staticmethod
    def write(path, tiles):
        with open(path, 'w') as f:
            for tile in tiles:
                f.write("(sprite\n")
                f.write("  :name    '%s'\n" % tile.name)
                f.write("  :left    %i\n" % tile.x)
                f.write("  :top     %i\n" % tile.y)
                f.write("  :width   %i\n" % tile.width)
                f.write("  :height  %i\n" % tile.height)
                f.write(")\n")

from .filter import Filter

""" Just some common image file extensions which are compatible with PILLOW """
StandardFilterCases = ['*.png', '*.PNG',
                       '*.jpg', '*.JPG', '*.jpeg', '*.JPEG',
                       '*.tif', '*.TIF', '*.tiff', '*.TIFF',
                       '*.bmp', '*.BMP',
                       '*.gif', '*.GIF',
                       '*.pcx', '*.PCX',  # Picture Exchange file
                       '*.ppm', '*.PPM', '*.pbm', '*.PBM', '*.pgm', '*.PGM', '*.pam', '*.PAM',  # Portable Anymap
                       # READ ONLY
                       '*.dds', '*.DDS',
                       '*.ico', '*.ICO',
                       '*.psd', '*.PSD',
                       '*.tga', '*.TGA',
                       ]


def get_standard_filter():
    f = Filter()
    for case in StandardFilterCases:
        f.add(case)
    return f

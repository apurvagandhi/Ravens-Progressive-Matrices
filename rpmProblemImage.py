from PIL import Image
import numpy


class rpmProblemImage:
    def __init__(self, name, figure):
        print ("In rpmProblemImage class init :  ", name, "----- ", figure.visualFilename)
        self.name = name
        self.image_filename = figure.visualFilename
        #opens up original image
        self.image = Image.open(figure.visualFilename) 
        # summarize some details about the image
        print(self.image.format)
        print(self.image.size)
        print(self.image.mode)
        # asarray() class is used to convert
        # PIL images into NumPy arrays
        self.numpy_image = numpy.array(self.image)
        #self.image_numpy_array = ImageUtil.binarize(self.image)
        #print(self.numpy_image)
        #self.object_count = len(figure.objects)
        

#******************************************************
# Name: Apurva Gandhi
# Last Updated Date: 01.21.2023
# Last completed assignment: Milestone 1
# Agent for solving Raven's Progressive Matrices. 
#******************************************************

from PIL import Image
import numpy
import ImageUtil

UNKNOWN = -1
DEBUG = 0
DIFF_THRESH = 2
MIN_OPTION_DIFF_THRESH = 5


class rpmFrame:
    def __init__(self,name,figure):
        #print "In rpmFrame init :  ", name, figure.visualFilename
        self.name = name
        self.image_filename = figure.visualFilename
        self.image = Image.open(figure.visualFilename)  # original image
        self.im_np = ImageUtil.binarize(self.image)     # Image bitmap in np array
        
class Agent:
    
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    
    # Learning: This is the constructor method for a class in Python. The __init__ method is 
    # automatically called when an object of the class is created.
    def __init__(self):
        
        # Learning: The code initializes two instance variables, 
        # input_frames and option_frames, and assigns empty dictionary objects to them.
        # The self keyword is used to refer to the instance of the class, 
        # and the dot notation is used to access the instance variables.
        self.input_frames={}
        self.option_frames={}
        
        # Learning: The pass statement is used as a placeholder, and does nothing. 
        # It is used when a statement is required syntactically but you do not want any command or code to execute.
        pass
    
    
    # ******************************************************************************************
    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    # ******************************************************************************************
    def Solve(self, problem):
        answer = -1
        self.loadData(problem)

        if problem.problemType == '2X2':
            answer = self.solve2x2(problem)
        return answer
    
    # ******************************************************************************************
    # created new instances of a class "rpmFrame" for each of the keys 
    # in the figures dictionary of the problem object, and stored them in either the 
    # "input_frames" or "option_frames" dictionary, depending on whether the key is a letter or a number
    # ******************************************************************************************
    def loadData(self, problem):
        if problem.problemType == '2x2':            
                self.input_frames['A'] = rpmFrame('A', problem.figures['A'])
                self.input_frames['B'] = rpmFrame('B', problem.figures['B'])
                self.input_frames['C'] = rpmFrame('C', problem.figures['C'])
                self.option_frames['1'] = rpmFrame('1', problem.figures['1'])
                self.option_frames['2'] = rpmFrame('2', problem.figures['2'])
                self.option_frames['3'] = rpmFrame('3', problem.figures['3'])
                self.option_frames['4'] = rpmFrame('4', problem.figures['4'])
                self.option_frames['5'] = rpmFrame('5', problem.figures['5'])
                self.option_frames['6'] = rpmFrame('6', problem.figures['6'])    
                
    def solve2x2(self,problem):
        answer = self.isIdentical('A','B','C')
        if answer != -1: 
            return answer
        
    def isIdentical(self, f1,f2,f3):
        image_a = self.getImage(f1)
        image_b = self.getImage(f2)
        image_c = self.getImage(f3)
        
        diff_ab = ImageUtil.find_image_diff(image_a, image_b)
        
        if diff_ab < DIFF_THRESH :
                option_diff_list=[]
                for i in range(1,7):
                    option_image = self.getImage(str(i))
                    option_diff = ImageUtil.find_image_diff(image_c, option_image )
                    option_diff_list.append(option_diff)
                min_diff = min(option_diff_list)
                min_index = option_diff_list.index(min_diff)
                print ("isIdentical : diff_ab=",diff_ab , " min_value= " , min_diff , " min_index =", min_index+1)
                
                if(min_diff < MIN_OPTION_DIFF_THRESH):
                    return min_index+1
        return -1
    
    # ******************************************************************************************
    # This defines a method called "getImage" that takes a single argument, "frame_key",
    # which is used to determine which image to return.
    # The method first checks if "frame_key" is alphabetic (i.e. a string containing only letters) by calling the built-in "isalpha()" 
    # method on the "frame_key" variable. If "frame_key" is alphabetic, the method returns the "image" attribute of an 
    # object stored in the "input_frames" dictionary, using the "frame_key" as the key to look up the appropriate object.
    # If "frame_key" is not alphabetic, the method returns the "image" attribute of an object stored 
    # in the "option_frames" dictionary, again using the "frame_key" as the key to look up the appropriate object.
    # ******************************************************************************************
    def getImage(self,frame_key):
        if frame_key.isalpha():
            return self.input_frames[frame_key].image
        else:
            return self.option_frames[frame_key].image
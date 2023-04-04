from PIL import Image
import numpy
import ImageUtil
import cv2 

#******************************************************
# Name: Apurva Gandhi
# Last Updated Date: 03.16.2023
# Last completed assignment: Milest one 3
# Agent for solving Raven's Progressive Matrices. 
#******************************************************
DIFFERENCE_TOLERENCE = 0.01
IDENTICAL_TOLERENCE = 0.022

class rpmFrame:
    def __init__(self,name,figure):
        self.image = Image.open(figure.visualFilename)  # original image
        self.im_np_binary = ImageUtil.binarize(self.image)     # Image bitmap in np array
                
class Agent:
    def __init__(self):
        self.input_frames={}
        self.option_frames={}
        pass
    
    def Solve(self, problem):
        answer = -1
        self.loadData(problem)
        if problem.problemType == '2x2':
            print(problem.name)
            answer = self.solve2x2(problem)
        elif problem.problemType == '3x3':
            print(problem.name)
            answer = self.solve3x3(problem)
        return answer
    
    def loadData(self, problem):
        fig_keys = problem.figures.keys()
        for i in fig_keys:
            if i.isalpha():
                i=i.upper()
                self.input_frames[i] = rpmFrame(i,problem.figures[i])
            else :
                self.option_frames[i] = rpmFrame(i,problem.figures[i]) 

    def solve2x2(self,problem):
        image_A = self.get_Image_As_Array('A')
        image_B = self.get_Image_As_Array('B')
        image_C = self.get_Image_As_Array('C')

        if self.isIdentical(image_A,image_B):
            print("Image A and B are Identical, searching for answer similar to C")
            possible_options = self.search_answer_in_options(image_C)
            if(len(possible_options) == 0):
                return -10           
            print("Possible options are", possible_options)
            return self.another_method(image_C, possible_options)
        elif self.isIdentical(image_A,image_C):
            print("Image A and C are Identical, searching for answer similar to B")
            possible_options = self.search_answer_in_options(image_B)
            if(len(possible_options) == 0):
                return -10           
            print("Possible options are", possible_options)
            return self.another_method(image_B, possible_options) 
        elif self.isHorizontalFlip(image_A, image_B):
            print("Image A and B are horizontally flipped, searching for answer similar to flipped horizontal C")
            possible_options = self.search_answer_in_options(numpy.fliplr(image_C))
            if(len(possible_options) == 0):
                return -10           
            print("Possible options are", possible_options)
            return self.another_method(image_C, possible_options)
        elif self.isVerticalFlip(image_A, image_C):
            print("Image A and C are vertically flipped, searching for answer similar to flipped vertically B")
            possible_options = self.search_answer_in_options(numpy.flipud(image_B))    
            if(len(possible_options) == 0):
                return -10           
            print("Possible options are", possible_options)
            return self.another_method(image_B, possible_options)
        else:
            return -10

    def largest_value_index(self, arr, n):
    
        max = arr[0]
        largest_index = 0
    
        for i in range(1, n):
            if arr[i] > max:
                max = arr[i]
                largest_index = i
        return largest_index

    def solve3x3(self,problem):
        image_A = self.get_Image_As_Array('A')
        image_B = self.get_Image_As_Array('B')
        image_C = self.get_Image_As_Array('C')
        image_D = self.get_Image_As_Array('D')
        image_E = self.get_Image_As_Array('E')
        image_F = self.get_Image_As_Array('F')
        image_G = self.get_Image_As_Array('G')
        image_H = self.get_Image_As_Array('H')
        if self.isIdenticalRow(image_A,image_B, image_C) and self.isIdenticalRow(image_D,image_E, image_F) and self.isIdentical(image_G, image_H):
            possible_options = self.search_answer_in_options(image_H)
            if(len(possible_options) == 0):
                return -10           
            return self.another_method(image_H, possible_options)
        else:
            possible_answers = []
            possible_answers.append(self.calculate_horizontal_relationship_1(image_A, image_C, image_D, image_F, image_G))
            possible_answers.append(self.calculate_horizontal_relationship_2(image_B, image_C, image_E, image_F, image_H))
            possible_answers.append(self.calculate_vertical_relationship_1(image_A, image_G, image_B, image_H, image_C))
            possible_answers.append(self.calculate_vertical_relationship_2(image_D, image_G, image_E, image_H, image_F))
            count = [0] * 8
            for relationship in possible_answers:
                for method in relationship:
                    count[0] += method.count(1)
                    count[1] += method.count(2)
                    count[2] += method.count(3)
                    count[3] += method.count(4)
                    count[4] += method.count(5)
                    count[5] += method.count(6)
                    count[6] += method.count(7)
                    count[7] += method.count(8)

            print(self.largest_value_index(count, len(count))+1)
            return self.largest_value_index(count, len(count))+1
    def isIdenticalRow(self, f1, f2, f3):
        if self.isIdentical(f1,f3):
            if self.isIdentical(f2,f3):
                return True
        return False
    
    def isIdentical(self, f1,f2):
        if self.calculate_mse(f1, f2) < IDENTICAL_TOLERENCE:
            return True
        else:
            return False
            
    def isHorizontalFlip(self, f1, f2):
        print("HERE",self.calculate_mse(numpy.fliplr(f1),f2))
        if self.calculate_mse(numpy.fliplr(f1), f2) < IDENTICAL_TOLERENCE:
            return True
        else: 
            return False

    def isVerticalFlip(self, f1, f2):
        print("HERE2",self.calculate_mse(numpy.flipud(f1),f2))
        if self.calculate_mse(numpy.flipud(f1), f2) < IDENTICAL_TOLERENCE:
            return True
        else:
            return False
    def calculate_mse(self, f1, f2):
        return numpy.square(numpy.subtract(f1,f2)).mean()
    
    def search_answer_in_options(self, search_frame):
        possible_answers = []
        for i in range(1,7):
            if self.calculate_mse(search_frame, self.get_Image_As_Array(str(i))) < IDENTICAL_TOLERENCE:
                print(i)
                possible_answers.append(i)
        return possible_answers
    
    def another_method(self, main_frame, possible_option_index):
        answers = {}
        for i in possible_option_index:
            mse = self.calculate_mse(main_frame, self.get_Image_As_Array(str(i)))
            answers[i] = mse
        for key, value in answers.items():
            print(key, value)
        lowest_value = min(answers.values())
        for key, value in answers.items():
            if value == lowest_value:
                answer_index = key
        return answer_index

    def calculate_horizontal_relationship_1(self,a,c,d,f,g):
        DPR_AC = self.dark_pixel_ratio(a, c)
        DPR_DF = self.dark_pixel_ratio(d, f)
        IPR_AC = self.intersection_pixel_ratio(a, c)
        IPR_DF = self.intersection_pixel_ratio(d, f)
        option_based_on_dpr = self.closet_dpr_ratio_from_option(DPR_AC + DPR_DF / 2, g)
        option_based_on_ipr = self.closet_ipr_ratio_from_option(IPR_AC + IPR_DF / 2, g)
        return option_based_on_dpr, option_based_on_ipr
    
    def calculate_horizontal_relationship_2(self,b,c,e,f,h):
        DPR_BC = self.dark_pixel_ratio(b, c)
        DPR_CF = self.dark_pixel_ratio(c, f)
        IPR_BC = self.intersection_pixel_ratio(b, c)
        IPR_CF = self.intersection_pixel_ratio(c, f)
        option_based_on_dpr = self.closet_dpr_ratio_from_option(DPR_BC + DPR_CF / 2, h)
        option_based_on_ipr = self.closet_ipr_ratio_from_option(IPR_BC + IPR_CF / 2, h)
        return option_based_on_dpr, option_based_on_ipr
        
    def calculate_vertical_relationship_1(self,a,g,b,h,c):
        DPR_AG = self.dark_pixel_ratio(a, g)
        DPR_BH = self.dark_pixel_ratio(b, h)
        IPR_AG = self.intersection_pixel_ratio(a, g)
        IPR_BH = self.intersection_pixel_ratio(b, h)
        option_based_on_dpr = self.closet_dpr_ratio_from_option(DPR_AG + DPR_BH / 2, c)
        option_based_on_ipr = self.closet_ipr_ratio_from_option(IPR_AG + IPR_BH / 2, c)
        return option_based_on_dpr, option_based_on_ipr

    def calculate_vertical_relationship_2(self,d,g,e,h,f):
        DPR_DG = self.dark_pixel_ratio(d, g)
        DPR_EH = self.dark_pixel_ratio(e, h)
        IPR_DG = self.intersection_pixel_ratio(d, g)
        IPR_EH = self.intersection_pixel_ratio(e, h)
        option_based_on_dpr = self.closet_dpr_ratio_from_option(DPR_DG + DPR_EH / 2, f)
        option_based_on_ipr = self.closet_ipr_ratio_from_option(IPR_DG + IPR_EH / 2, f)
        return option_based_on_dpr, option_based_on_ipr
    
    def closet_dpr_ratio_from_option(self, relationship_dpr, image):
        possible_choice = []
        for i in range(1,9):
            option_dpr = self.dark_pixel_ratio(image, self.get_Image_As_Array(str(i)))
            if abs(relationship_dpr - option_dpr) < 0.015:
                possible_choice.append(i)
        return possible_choice
    
    def closet_ipr_ratio_from_option(self, relationship_dpr, image):
        possible_choice = []
        for i in range(1,9):
            option_dpr = self.intersection_pixel_ratio(image, self.get_Image_As_Array(str(i)))
            if abs(relationship_dpr - option_dpr) < 0.4:
                possible_choice.append(i)
        return possible_choice

    def dark_pixel_ratio(self, a, b):
        dark_pixels_a = a.size - numpy.count_nonzero(a)
        dark_pixels_b = b.size - numpy.count_nonzero(b)
        dark_pixels_a_ratio = dark_pixels_a/a.size
        dark_pixels_b_ratio = dark_pixels_b/b.size
        return abs(dark_pixels_a_ratio - dark_pixels_b_ratio)

    def intersection_pixel_ratio(self, a, b):
        intersection = cv2.bitwise_and(a, b)
        intersecting_dark_pixel = intersection.size - numpy.count_nonzero(intersection)    
        return intersecting_dark_pixel / (a.size - numpy.count_nonzero(a) + a.size - numpy.count_nonzero(b))

    def get_Image_As_Array(self,frame_key):
        if frame_key.isalpha():
            return self.input_frames[frame_key].im_np_binary
        else:
            return self.option_frames[frame_key].im_np_binary


"""
THE PURPOSE OF OUR CODE IS TO COUNT THE NUMBER OF ROIs (regions of interest) IN AN INPUT IMAGE. THE CODE WAS DESIGNED SPECIFICALLY FOR CELLS (bacteria, yeast, human cells, etc.) (Synthetic cell images were used in the planning and testing of the code) BUT CAN BE USED FOR OTHER ROIs IF DESIRED. The code also creates a csv file of images and cell counts if the user wants.
Our code does this through image thresholding, binary masking and using some loops, functions and dictionaries
To be able to run this code on your computer, please make sure that you have downloaded "Imageio", "Matplotlib", "Numpy", "Scikit-image", and "Microsoft Excel" (to be able to open the csv file)

The dataset used to test our project is "Synthetic Cell Images and Masks" (only images were used, masks were not used), which was generated using the SIMCEP simulation tool (dataset is available in Kaggle). However, the images in the dataset are in .tif format. Unfortunately, .tif and .tiff formats are not supported by our code.
Hence, the test images were converted to .png or .jpg files (using a web converter) before using. 
If you are willing to use images from the same dataset or any images with .tif or .tiff format, please ensure to convert these files into any supported formats (which are .png, .jpeg, .jpg)
Lastly, please ensure that the input images are in the same directory as Wing 101.
 """
#this code is from an outside source (Data Carpentry - Image Processing with Python) and was modified and commented by us (until line 157)

#We want a python library that can play with images instead of txt files or csv files.
#import imageio for reading/analysing and showing images
import imageio.v3 as iio
#import matplotlib to create histograms and plots to help analyze our images
import matplotlib.pyplot as plt
#import numpy for mathematical operations and analysing our images
import numpy as np
#We want a module that can do image processing and output a modified version of the image when we want the colorful image to become black, white and gray (grayscale), so import scikit image (skimage). 
import skimage as ski
#want to generate a csv file of cell counts
#code below is ours
import csv


#To initiate the while loop to show a menu
#code below is ours
menu_option = 'X'

#create an empty list of images (will be used to create a dictionary for option O (creating a csv file for outputs))
#code below is ours
list_of_images = []

#create an empty list of cell counts (will be used to create a dictionary for option O (creating a csv file for outputs))
#code below is ours
list_of_counts = []


#loop until the user inputs E
#code below is ours
while(menu_option != 'E'):
    menu_string = """
    A = Add images to get cell counts
    O = Output cell counts as a csv file (The file will be created in the same directory as Wing) WARNING: If an image is added twice, only the cell count of the second attempt will be recorded
    You can first add all the images and then click O to output all of the image to counts in csv
    E = End program
    Choose an option:
    """
    #get user input
    #code below is ours
    menu_option = input(menu_string)
    if(menu_option == 'A'):
        """INPUT: can only be .png or .jpg or .jpeg images. The cells should not be overlapping, in the case of overlapping cells the program will count them as 1 cell
        The program works best in grayscale images and cells which have distinct boundaries and contrast with background. Colourful images can be tried, however, the cell count can be far from the actual cell count.
        """
        
        #ask the user to give the name of the image to be analysed and mention all the requirements and warnings
        input_image = input(""" Welcome to the Cell Counter by Hilal and Qiting! 
        It is required for you to upload an input image in order to run the program. 
        Please ensure that you have all the system requirements ("Imageio", "Matplotlib", "Numpy", and "Scikit-image" before starting.)
        
        INPUT IMAGE: can only be .png or .jpg or .jpeg images. The cells should not be overlapping; in the case of overlapping cells, the program will count them as 1 cell so please take this into account when using the cell count in your analysis.
        
        The program works best in grayscale images and cells which have distinct boundaries and contrast with the background. Colourful (RGB) microscopy images can be tried, however, the cell count can be far from the actual cell count due to the nature of RGB images.
        
        Finally, please ensure that the input image is in the same directory as Wing 101.
        
        After entering the name of the input image the code will also ask you to enter a threshold value.
        Then the code will firstly show the original (input) image in an x-y axis plot. 
        Then if the image is RGB in its nature, it will show the grayscale image. 
        Then, a histogram of the distribution of the pixels (in grayscale) will be shown for the user to understand the heterogeneity of their picture. 
        Please note that if an image has many peaks, especially between 0 and 1; the image is heterogenous. And the code will not be highly reliable as heterogeneity increases (which is mostly the case in colourful images).
        Then, it will show the binary mask of the image depending on the threshold value.
        After observing/analysing the output images, please close all output images to see the cell count in the python shell.
        
        Please enter the name of the input image: 
        """)
       
        #to store the name of the input image in the list
        list_of_images.append(str(input_image))
        
        #code below is from Data Carpentry - Image Processing with Python
        #read the image using the imageio module
        image_of_interest = iio.imread(uri=input_image) 
        
        #showing the original images with x and y axis using matplotlib (next 3 lines of code)
        fig, ax = plt.subplots() 
        
        #writing title on top of the picture
        ax.set_title("Original Picture") #this code is written by us
        ax.imshow(image_of_interest)
        
        
        #binary image values are 0(black) and 1(white), but in reality, the cells can be colourful, or grayscale which means they can have gray and other colours, hence every pixel has a value between 0 and 1
        
        #we need to convert the image to grayscale for better image processing due to the limitations of processing colorful images (low contrast between background etc.). Even if the image seems grayscale, it can be an RGB image and only the computer can understand this. So, we need some code to see if the image is grayscale (has 2 channels), RGB (has 3 channels), or a different type which can have more than 3 channels. We will convert to grayscale if the image given is RGB in its nature.
        
        #if the image is RGB (has 3 channels), we need to turn it into grayscale image to continue (using skimage)
        if (len(image_of_interest.shape) == 3):
            gray_shapes = ski.color.rgb2gray(image_of_interest)
        #if the image is already grayscale, make it equal to the gray_shapes variable and skip changing it into grayscale
        #code below is ours
        elif (len(image_of_interest.shape) == 2): 
            gray_shapes = image_of_interest
        else:
            print("The image is not suitable for analysing in this program because it has more than 3 channels or less than 2 channels, please upload a new one.")
        
        #code below is from Data Carpentry - Image Processing with Python
        #We need to blur the image to denoise and to increase the SNR (signal to noise ratio) (refining the image) (using skimage)
        blurred_shapes = ski.filters.gaussian(gray_shapes, sigma=1.0)
        
        #create the grayscale and blurred version of the image
        fig, ax = plt.subplots()
        
        #writing title on top of the picture
        ax.set_title("Grayscale Picture") #this code is written by us
        #show the output grayscale image
        ax.imshow(blurred_shapes, cmap="gray") #cmap is for putting image to gray tones 
        
        
        #create a histogram of the distribution of the pixels of the refined grayscale image
        #Historam will help the user to understand how heterogenous their image is, so they can understand if the code will work good on their image or not.
        #a peak near 0 means the image has many black pixels and a peak near 1 means many white pixels in the picture
        #If an image has many peaks, especially between 0 and 1; the image is heterogenous and the code will not be highly reliable as heterogeneity increases (which is mostly the case in colourful images)
        histogram, bin_edges = np.histogram(blurred_shapes, bins=256, range=(0.0, 1.0))
        
        #creating the histogram
        fig, ax = plt.subplots()
        ax.plot(bin_edges[0:-1], histogram) 
        #title of the histogram
        ax.set_title("Grayscale Histogram")  #this code is written by us
        #title of x axis
        ax.set_xlabel("Grayscale value")  #this code is written by us
        #title of y axis
        ax.set_ylabel("Pixels")  #this code is written by us
        #scale of x axis
        ax.set_xlim(0, 1.0) 
        
        #this code is written by us
        #creating a mask based on the threshold
        #We are going to ask the user to give us a threshold value between 0 and 1 which will be used to identify the ROIs (it is like the resolution of identifying cells)
        threshold = float(input("""Now it is required for the user to input a threshold value (t) for identifying ROIs.
        In the original image, if your regions of interest (ROIs)(cells that you are looking for) have a clear contrast between their background, then use higher threshold values (example: t=0.9). 
        But if your ROIs do not have a big contrast between their background then use a lower threshold value (example: t = 0.1) (to decide this, you can enter a random threshold value at first and then use the grayscale version of the image and the histogram generated to further decide on the threshold value you will use. If your cells are mostly white, then use higher values; if they are less white and closer to black/gray, use lower t value) 
        The recommended t value for the dataset used for this program is 0.1.
        Please enter the threshold value: 
        """))
        
        t = threshold 
        
        #code below is from Data Carpentry - Image Processing with Python
        #creating a binary mask of the cells (ROIs)
        binary_mask = blurred_shapes < t
        fig, ax = plt.subplots()
        
        #showing the binary mask (output) to the user
        ax.set_title("Masked Picture")
        ax.imshow(binary_mask, cmap="gray")
        plt.show()  #this code was written by us
        
        
        #This part is generated by AI (ChatGPT), modified and commented by us (until line 212)
        #the function to count the cells
        def count_cells(binary_mask_given):
            """This function loops over every pixel of the binary mask and counts the number of ROIs (cells) present in the image.
                INPUT: The binary mask created by the previous code that generated a black and white picture of the original image
                OUTPUT: the number of the cell present in the binary mask
                REQUIREMENT AND LIMITATION: The user should create binary mask before using this function. And in case of overlapping cells, this function will count them as 1 cell.
            """
            #set the number of cells to 0
            num_cells = 0
            
            #Get the dimensions of the binary mask
            rows, cols = binary_mask_given.shape
                
            #"Visited" variable to keep track of the pixels that were already looped over and identified.
            visited = np.zeros_like(binary_mask_given, dtype=bool) #.zeros_like is a function in numpy used to return an array of 0s with the same shape and data type as the input array (the binary mask).
                
            #Directions for visiting the 8 neighbouring pixels of a pixel (up, down, left, right, and 4 diagonals)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            
            #this is a function required to have a correct cell count. It uses DPS (depth-first search). This allows the computer to not visit a visited pixel again and reduced the amount of resources required to run the code (and count the cells).
            def flood_fill(r, c):
                """
                Marks all connected black pixels together so that it does not loop over the visited cells gain
                INPUT: the position of the pixel (row, column)
                """
                #Depth-first search (DFS) algorithm to know visited pixels
                stack = [(r, c)] 
                visited[r, c] = True
                
                while stack:
                    current_r, current_c = stack.pop()
                    
                    #Loop over all 8 neighbouring cells to see if they were visited
                    for dr, dc in directions:
                        nr, nc = current_r + dr, current_c + dc
                        
                        #If the neighbouring pixel is a black pixel and is not visited before
                        if (0 <= nr < rows) and (0 <= nc < cols) and not (visited[nr, nc]) and (binary_mask_given[nr, nc] == 0):
                            visited[nr, nc] = True
                            #add the pixel to a new cell (the pixel is not part of the current cell, it is a part of the new cell)
                            stack.append((nr, nc))    
               
            #Loop over each pixel in the binary mask (First; loop over every column in the first row, then second row, and goes like that)
            for r in range(rows):
                for c in range(cols):
                    #If there is a black pixel (0) that has not been visited before, it's a part of a new cell
                    if (binary_mask_given[r, c] == 0) and not (visited[r, c]):
                        #this is a new cell, so increase the count by 1
                        num_cells = num_cells + 1 
                        #Marking all connected black pixels as 1 cell
                        flood_fill(r, c) 
            return num_cells   #this code was written by us
        
        #code below is written by us            
        #calling and using the function with the binary mask created
        final_count = count_cells(binary_mask)
        #to store the cell count of the input image in the list
        list_of_counts.append(final_count)
        #printing the final cell count in the Python shell
        print("There are", final_count, "cell(s) in your image.")
        
    elif(menu_option == 'O'):
        #want to create a dictionary: key is the image, value is the cell count of the image
        #create an empty dictionary
        images_to_counts = {}
        
        #loop over each list at the same time using zip function learned from ChatGPT to create key value pairs
        for image, count in zip(list_of_images, list_of_counts):
            #create key value pairs and add it to the dictionary
            #we assume that the key is unique in the list_of_images
            images_to_counts[image] = count
            
        #code below is written by us    
        #output the image and the matched cell count as csv file
        output_csvfile = open("output_file.csv", "w", newline="")
        writer = csv.writer(output_csvfile) #we got help() from python
        #create a header for each coloums
        writer.writerow(["Images", "Counts"]) #we got help() from python
        for image, count in images_to_counts.items():
            writer.writerow([image, count])
        #close the file when finished
        output_csvfile.close()
        print("""Check the directory that Wing is saved in. 
        The output csv file is located in the same directory as Wing. 
        The file's name is output_file.csv""")
        
    
    elif(menu_option == 'E'):
        print("The cell count program ends!!!")
        #end the program and exit the while loop
        break 
    else:
        #If the user gives an input that is not in the menu options, it will be an invalid input. Let the user know and show the menu option again.
        print("Invalid menu option. Please try again")


#TESTING OUR CODE
#to test our code, please try different cell images and see if the cell count matches with the actual cell count.
#Testing images:
#test_1cell.jpg has only 1 cell
#many_cells.jpg has 40 cells (counted by humans) but the code counts as 34 due to a few overlapping cells
#so_many_cells.jpg has so many cells (over 50)
#few_cells.jpg has 16 cells but the result will be less due to a few overlapping cells
#overlapping_cells.jpg has so many overlapping cells, the cell count is far from the actual value
#neuron1.jpg is a colourful neuron cell image and there is 1 cell in the image. Use a little higher threshold value (ex: 0.5) and the code will give 1 as count, however it will give more if smaller thresholds are used (ex: 0.1). But don't use a too high threshold value because it would give 0 as count. (ex: 0.9) (This image is taken from Fluorescent Neuronal Cells dataset on Kaggle)

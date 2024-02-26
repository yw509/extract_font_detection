
## Synopsis 

This project aims to detect the fonts of letters in a paper. The results are binary png images of detected letters. 

When users upload an image with their desired font, the project will first detect corners of the target paper in this image by using Morphological operations. Then, the paper will be re-projected where its corners will be matched to the image's corners. Upper and lower cases of 26 letters will be recognized by functions in the pytesseract module. The final step is to crop these letters out from the original image, resize them into the same size and convert the image to binary image by thresholding method.


## Installation 

Step 1: installation
Use the terminal and go to the directory you want to install the program. Type the following in the command line: 
git clone git@github.com:oberlin-csci353/semester-project-lcwj.git


Step 2: installing dependencies
To make the program run, you need to install following libraries in your device. 
1. tesseract-ocr
Follow the instructions in this link to install tesseract-ocr properly. https://github.com/tesseract-ocr/tesseract#installing-tesseract
2. pytesseract
Follow the instructions in this link to install pytesseract properly. https://pypi.org/project/pytesseract/
3. opencv-python
Follow the instructions in this link to install opencv-python properly. https://github.com/opencv/opencv-python
4. numpy
Follow the instructions in this link to install numpy properly. https://numpy.org/install/
5. scikit-image
Follow the instructions in this link to install scikit-image properly. https://scikit-image.org/docs/stable/install.html
6.scipy
Follow the instructions in this link to install scipy properly. https://scipy.org/install/


Step 3: Adjusting the code for your operating system.
For MacOS users:
If you're using MacOS operating system, you need to open the file named FontDetection.py using an editor (Text Editor, Sublime, Emacs...) and delete the line under the comment "for Windows users" (pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'). We suggest that you use Homebrew to install tesseract-ocr, which would automatically set the path to tesseract-ocr. Here is the link to install tesseract-ocr by Homebrew: https://formulae.brew.sh/formula/tesseract Here is the link to install Homebrew: https://docs.brew.sh/Installation 

For Windows users:
If you're using Windows operating system, you need to open the file named FontDetection.py using an editor (Text Editor, Sublime, Emacs...). You need change the line under the comment "for Windows users" (pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe') to the path to your tesseract file. 


## Usage 
1. save the image you want to apply the font detection to the program directory. In the image, be sure there is a paper with text that you want to detect its font. The image should contain the four corners of the paper, and the paper should be the largest shape in the whole image.What's more, We assume the aspect ratio of the paper is the same as the image. If the ratio of paper is significant different with the images's, the final results would be affected. 
2. Use your terminal and go to the program directory.
3. Run the program by typing this in your terminal: python3 FontDetection.py
<img width="536" alt="Screen Shot 2022-05-26 at 20 10 20" src="https://user-images.githubusercontent.com/65196927/170603569-745d958c-d15b-42fb-a954-a0a3866008c7.png">

4. It would ask you "Which picture do you want to detect? " You should input the name of the image. Make sure that you include the file extensions and be aware that case matters (".png" is different with ".PNG"). 
5. If the program successfully reads the image, it would show you an image and ask you to rotate it. Enter the degree that you want to rotate the image counterclockwise to adjust the image. Since we used cv2.waitKey() after cv2.imshow, in order to tell program continue working, users should randomly press a key after viewing an image.
<img width="442" alt="Screen Shot 2022-05-26 at 20 13 01" src="https://user-images.githubusercontent.com/65196927/170603808-49652979-4b0e-4a22-bc57-11f0237c4657.png">

6. Wait until the program finishes running. You can find the result in the directory called "print_result" 


## Known Issues 

There is no knwon issues/bugs for the project. 


## Authors 

1. Ran Liu - Threshold the image, crop letters and draw the rectangles around them
2. Nolan Chen - Detect Corners of the target paper, recognize letters from the paper 
3. Yuchen Wang - Project Transformation, Calculate the mean height of detected rectangles for letters

We basically brainstormed and implemented together for most of the project. We usually met twice a week to discuss and work on this project, where one person was responsible for typing the codes, and the other two gave the ideas and checked at the last. In the last one and a half week, we started test and improve our project together. 


## References 
1. https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
2. https://pypi.org/project/pytesseract/ 
3. https://scikit-image.org/docs/stable/user_guide.html 
4. https://numpy.org/doc/stable/reference/index.html
5. and lectures


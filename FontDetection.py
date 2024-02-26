import pytesseract
import numpy as np
import cv2
from scipy.signal import convolve2d
import skimage
from skimage import transform
from skimage.filters import threshold_otsu

# for Windows users
#pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#detect corners of the target paper
def cornerDetection(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur image
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    # do otsu threshold on gray image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # apply morphology
    kernel = np.ones((7,7), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    cv2.imwrite("morph.png", morph)

    # get largest contour
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    area_thresh = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            area_thresh = area
            big_contour = c

    # draw white filled largest contour on black just as a check to see it got the correct region
    page = np.zeros_like(img)
    cv2.drawContours(page, [big_contour], 0, (255,255,255), -1)

    # get perimeter and approximate a polygon
    peri = cv2.arcLength(big_contour, True)
    corners = cv2.approxPolyDP(big_contour, 0.04 * peri, True)
    rectangle = True
    if len(corners) > 4:
        rect = cv2.minAreaRect(big_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print(box)
        polygon2 = img.copy()
        cv2.drawContours(polygon2, [box], 0, (0, 0, 255), 2)
        cv2.imwrite('contours.png', polygon2)
        box = np.expand_dims(box, axis = 1)
        print(box)
        corners = box
        rectangle = False
    else:
        # draw polygon on input image from detected corners
        polygon = img.copy()
        print(corners)
        cv2.polylines(polygon, [corners], True, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imwrite('detected.png', polygon)

    return corners, rectangle


#return the index of a letter in the list
def letterNum(str):
    if str.isalpha() and str.isupper():
        return ord(str)-65
    elif str.isalpha() and str.islower():
        return ord(str)-71
    else:
        return 0


#project the paper into image size with corner matched
def project_transform(image, src, dst):
    x_dst = [val[0] for val in dst] + [dst[0][0]]
    y_dst = [val[1] for val in dst] + [dst[0][1]]

    tform = transform.estimate_transform('projective',
                                         np.array(src),
                                         np.array(dst))
    transformed = transform.warp(image, tform.inverse)

    cv2.imshow('detected', cv2.resize(transformed,(540,700)))
    cv2.waitKey()

    #rotate based on the detected result
    rotate_num = input("How many degree do you want to rotate in counterclockwise? ")
    if (int(rotate_num) != 0):
        transformed = transform.rotate(transformed, int(rotate_num), resize = True)
    cv2.imshow('detected', cv2.resize(transformed,(540,700)))
    cv2.waitKey()

    return transformed


#get the mean height of detected corners for letters
def mean_height(letters):
    totalh = 0
    count = 0
    h_list = []
    w_list = []
    for i in range (0, len(letters)):
        if len(letters[i])!=0:
            count += 1
            currenth = letters[i][4] - letters[i][2]
            currentw = letters[i][3] - letters[i][1]
            h_list.append(currenth)
            w_list.append(currentw)
            totalh += currenth
    meanh = totalh / count

    return meanh, h_list, w_list


#threshold the image into black&white
def processImage(img):
    k=np.ones((5,5))/25
    img2=convolve2d(img,k,boundary="symm")
    t=threshold_otsu(img2)
    for i in range(len(img2)):
        for j in range(len(img2[i])):
            if img2[i][j]>t:
                img2[i][j]=255
            else:
                img2[i][j]=0

    return img2


#crop letters and draw rectangles around them
def crop_letters(img2, letters,meanh):
    final_array = []

    c = 0
    for i in range(0, len(letters)):
        if len(letters[i])!=0:
            c += 1
            crop_img_now = img2[(hImg - letters[i][4]):(hImg - letters[i][2]), letters[i][1]:letters[i][3]]
            print(crop_img_now)
            #resize rectangles based on meanheight in order to make them as same size
            try:
                #crop_img_now= processImage(cv2.resize(crop_img_now,(int(img2.shape[1]*meanh/img.shape[0]),int(meanh))))
                crop_img_now = cv2.resize(crop_img_now, (int(img2.shape[1] * meanh / img.shape[0]), int(meanh)))
                final_array.append(crop_img_now)

            #save cropped letters images into a certain repository
                cv2.imwrite("print_result/"+letters[i][0]+str(c) + ".png", crop_img_now)
            except:
                print("An exception occurred")
    return final_array

if __name__ == '__main__' :
    #read in the target image
    img_name = input("Which picture do you want to detect? ")
    img = cv2.imread(str(img_name))
    img_shape = img.shape

    #detect corners of the paper in the image
    corner, rec =cornerDetection(img)

    if rec:
        area_of_interest = [(corner[0][0][0], corner[0][0][1]), (corner[1][0][0], corner[1][0][1]),
                            (corner[2][0][0], corner[2][0][1]), (corner[3][0][0], corner[3][0][1])]
    else:
        area_of_interest = [(corner[0][0][0], corner[0][0][1]), (corner[3][0][0], corner[3][0][1]),
                            (corner[2][0][0], corner[2][0][1]), (corner[1][0][0], corner[1][0][1])]

    area_of_projection = [(0, 0),
                        (0, img_shape[0]),
                        (img_shape[1], img_shape[0]),
                        (img_shape[1], 0)]

    #re-project this paper
    transformed_result = project_transform(img, area_of_interest, area_of_projection)

    #gray the image
    img2 = cv2.normalize(transformed_result, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img2 = cv2.filter2D(img2, -1, kernel)

    cv2.imwrite('detected2.png',img2)
    custom_config = r'-l eng --oem 3 --psm 1'
    boxes = pytesseract.image_to_boxes(img2)

    text=pytesseract.image_to_string(img2,config=custom_config)
    hImg, wImg = img2.shape
    letters=[]
    for i in range(52):
        letters.append([])

    #add detected letters to a list
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        if b[0].isalpha() and len(b[0])==1:
            int_num = letterNum(b[0])
            if int_num > 0 and int_num < 52:
                coord=[b[0],x,y,w,h]
                if letters[int_num]==[]:
                    letters[int_num]=coord

    height, hlist, wlist = mean_height(letters)
    crop_array = crop_letters(img2, letters,height)

    #print out detected letters and their rectangles' coordinates
    for i in letters:
        if len(i)!=0:
            cv2.rectangle(img2, (i[1], hImg - i[2]), (i[3], hImg - i[4]), (0, 0, 255), 1)
            cv2.putText(img2, i[0], (i[1], hImg - i[2] + 13), cv2.FONT_HERSHEY_SIMPLEX, 4, (50, 205, 50), 5)
            print(i)

    #save the image with letters and squres into the current repository
    cv2.imwrite('detected2.png',img2)
    print(text)

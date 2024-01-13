import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class MonitorOSD:
    """Class to generate objects for cross-platform OSD analysis"""
    class OSDTreeNode:
        """Internal Class to contain osd menu structure"""
        str = ""
        def __init__(self, str):
            self.str = str
            pass
        def __str__(self):
            pass

    osd_tree = OSDTreeNode()
    def __init__(self, monitortype="BVM-D9", dir="monitor_osd_data"):

def getText(img, verbose=False, safeAreaPercentage=0.40):
    """ Function to retrieve the text from a predefined center of the image

    Args:
        img (image): opencv frame object
    """
    # Preprocessing the image starts
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if verbose:
        cv2.imshow("test", gray)
        cv2.waitKey(0)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Inverse Image
    thresh1 = ~thresh1

    if verbose:
        cv2.imshow("test", thresh1)
        cv2.waitKey(0)

    # Specify structure shape and kernel size. 
    # Kernel size increases or decreases the area 
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect 
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    #dilation = cv2.erode(thresh1, rect_kernel,  iterations = 1)

    if verbose:
        cv2.imshow("test", dilation)
        cv2.waitKey(0)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                    cv2.CHAIN_APPROX_NONE)
 
    # Creating a copy of image
    im2 = img.copy()
    
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file

    master_string = ""

    # Calculate safe area:
    safeAreaPercentage = 0.40
    height, width, _ = im2.shape
    safex = int(width * safeAreaPercentage // 2)
    safey = int(height * safeAreaPercentage // 2)
    # Draw Safe Area:
    cv2.rectangle(im2, (safex, safey), (width - safex, height - safey), (0, 0, 255), 2)

    padding = 7
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if x < safex or x > width - safex or y < safey or y > height - safey:
            pass
        else:
            if verbose:
                # Drawing a rectangle on copied image
                rect = cv2.rectangle(im2, (x-padding, y-padding), (x + w + padding, y + h + padding), (0, 255, 0), 2)
                cv2.imshow("test", im2)
                cv2.waitKey(0)

            # Cropping the text block for giving input to OCR
            cropped = im2[y-padding:(y + h+padding), x-padding:(x + w+padding)]
            
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            
            # Append to master string
            master_string += "\n" + text
            
    return master_string


if __name__ == "__main__":
    # Read image from which text needs to be extracted
    #img = cv2.imread("lights_off_better.jpg")
    #img = cv2.imread("notilt.jpg")
    img = cv2.imread(r"data\deflection_3.jpg")
    #img = cv2.imread("lights_on.jpg")

    screenoutput = getText(img)

    print(screenoutput)







import argparse
import numpy as np
import cv2
import os

# Watermark Configuration
font = cv2.FONT_HERSHEY_COMPLEX
color = (255, 255, 255)
thickness = 4

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=False,
                help='Path to target file')
ap.add_argument('-w', '--watermark', required=True,
                help='Text you would like to watermark image with | (Enclose in quotes if there are spaces)')
ap.add_argument('-d', '--directory', required=False,
                help='Processes every image in the CWD')
ap.add_argument('-p', '--pos', required=True,
                help='Options are "ul"(upper left) "ur"(upper right) "ll"(lower left) "lr"(lower right)')
ap.add_argument('-ntsc', '--NTSCgrayscale',action = 'store_true',required = False,
                help = 'Change image to National Television System Committee standard for grayscale')
ap.add_argument('-EQG','--EqualizeGrayHistogram',action = 'store_true',required = False,
                help = 'Take gray image and equalize the intensities in the image')
ap.add_argument('-EQC','--EqualizeColorHistogram',action = 'store_true',required = False,
                help = 'Take colored image and equalize the intensities in the image')
ap.add_argument('-MF','--MedianFilter',action = 'store_true',required = False,
                help = 'Take gray image and apply a median smoothing filter to reduce noise')
args = ap.parse_args()


def process_image(working_image, watermark, pos):
    text_length = len(watermark)
    width = len(working_image) #im.size[1]
    height = len(working_image[1])
    print("width: "+ str(width))
    print("shape[0]: "+ str(working_image.shape[0]))
    print("height: "+ str(height))
    print("shape[1]: "+ str(working_image.shape[1]))
    if working_image.shape[0] >= 4000:
        avg_char = 120
        text_width = text_length * avg_char
        fontScale = 6
        image_ul = (0, 150)
        image_ur = (working_image.shape[1] - text_width, 150)
        image_ll = (0, working_image.shape[0] - 50)
        image_lr = (working_image.shape[1] - text_width, working_image.shape[0] - 50)
    else:
        avg_char = 80
        text_width = text_length * avg_char
        fontScale = 4
        image_ul = (0, 100)
        image_ur = (working_image.shape[1] - text_width, 100)
        image_ll = (0, working_image.shape[0] - 50)
        image_lr = (working_image.shape[1] - text_width, working_image.shape[0] - 50)

    if pos == 'ul':
        new_image = cv2.putText(working_image, args.watermark, image_ul, font, fontScale, color, thickness, cv2.LINE_AA)

    if pos == 'ur':
        new_image = cv2.putText(working_image, args.watermark, image_ur, font, fontScale, color, thickness, cv2.LINE_AA)

    if pos == 'll':
        new_image = cv2.putText(working_image, args.watermark, image_ll, font, fontScale, color, thickness, cv2.LINE_AA)

    if pos == 'lr':
        new_image = cv2.putText(working_image, args.watermark, image_lr, font, fontScale, color, thickness, cv2.LINE_AA)

    if not os.path.exists(os.getcwd() + '\\Watermarked'):
        os.mkdir(os.getcwd() + '\\Watermarked')

    path = os.getcwd() + '\\' + 'Watermarked' + '\\' + file
    cv2.imwrite(path, new_image)

def medianFilter(matrix):
    outputMatrix = matrix.copy()
    matrix = np.pad(matrix, ((1, 1), (1, 1)), 'constant') #pad matrix with 0's
    matrixRows = len(matrix)
    matrixColumns = len(matrix[0])
    for i in range(1, matrixRows - 1):
        for j in range(1, matrixColumns - 1):

            MiddleInt = matrix[i][j]
            TopRightInt = matrix[i - 1][j + 1]
            MiddleRightInt = matrix[i][j + 1]
            BottomRightInt = matrix[i + 1][j + 1]
            TopLeftInt = matrix[i - 1][j-1]
            MiddleLeftInt = matrix[i][j - 1]
            BottomLeftInt = matrix[i - 1][j + 1]
            TopInt = matrix[i+1][j]
            BottomInt = matrix[i-1][j]
            matrixOfInts = [MiddleRightInt,TopRightInt,TopInt,TopLeftInt,MiddleInt,MiddleLeftInt,BottomLeftInt,BottomInt,BottomRightInt]
            matrixOfInts.sort() # sort array
            outputMatrix[i-1][j-1] = matrixOfInts[5]  # there will always be 9 elements so index 5 will be median 100% of the time
    return outputMatrix


def ntsc_grayscale(img):
    b, g, r = cv2.split(img)
    rows = len(r)  # grab rows and cols of any single channel matrix
    cols = len(r[0])
    unnormalized = b.copy()  # need a one channel matrix to copy, we will overwrite all the values
    normalized = b.copy()
    for i in range(rows):
        for j in range(cols):
            unnormalized[i][j] = ((76.245 * r[i][j] + 149.685 * g[i][j] + 29.071 * b[i][j]) / 255)  # NTSC method
            normalized[i][j] = unnormalized[i][j] / 255  # incase we need a lil normalized one
    return unnormalized

def getHistogramAndEqualize(img):
    newimg = img.copy()
    array = [None]*256            # Two empty arrays with 256 spots 0-255
    probability = [None]*256      # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    rows = len(img)               # Use len instead of img.shape() because of pixel size
    cols = len(img[0])            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    pixels = rows*cols
    for i in range(rows):
        for j in range(cols):
            if array[img[i][j]] is None:  # if this is the first time we have see this intensity value, set it to one
                array[img[i][j]] = 1
            else:                          # else increment it by one (cant increment a none value)
                array[img[i][j]] += 1
    count = 0
    for k in array:
        if k is None:  # if we did not find any intensity for that value, set it to equal instead of none
            probability[count] = 0
            array[count] = 0
        else:           # else find the probability of that intensity
            probability[count] = k/pixels
        count += 1
    # ship the array off to the distribution function but let the function know the level
    equalizedarray = cumulativeDistribution(256,probability)

    for i in range(rows):
        for j in range(cols):
            # iterate through the array and give our equalized image the new value
            newimg[i][j] = equalizedarray[img[i][j]]
    return newimg
    # plt.hist(array,bins='auto')    # for testing
    # plt.show()


def cumulativeDistribution(Level,probability):
    newarray = [None]*Level           # similar to above we make two empty arrays with the level
    probabilityadd = [None]*Level
    count = 0
    for i in probability:
        if count == 0: # if this is the first probability, just take the level-1 and times it by the probability
            newarray[count] = round((Level - 1) * i)
            probabilityadd[count] = i # start a tally of the probability so we dont need to do recursive functions
        else:
            # add the last probability to the current to keep the running tally
            probabilityadd[count] = probabilityadd[count-1] + i
            # take the probability total and multiply by the level - 1 and set it to that count.
            newarray[count] = round((Level-1) * (probabilityadd[count]))
        count += 1
    return newarray # send the equalized array back

def equalizecolor(img):
    ycrcb = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB) # convert to a nice color scheme
    channels = cv2.split(ycrcb) # use split to give us the nice color channels
    cv2.equalizeHist(channels[0],channels[0]) # use a nice function to nicely equalize the channels
    cv2.merge(channels,ycrcb) # nicely merge the channels back
    cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
    return img


###############################################################################


if __name__ == "__main__":
    for file in os.listdir(os.getcwd()):
        if file.endswith('.jpg') or file.endswith('.png'):
            working_image = cv2.imread(os.getcwd() + '\\' + file)
            if args.NTSCgrayscale:
                working_image = ntsc_grayscale(working_image)
                # cv2.imshow('grayscale',working_image)  # testing
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            if args.EqualizeGrayHistogram:
                if args.NTSCgrayscale:  # if its already gray ya cant gray it again
                    working_image = getHistogramAndEqualize(working_image)
                else:  # gray it before equalizing
                    working_image = ntsc_grayscale(working_image)
                    working_image = getHistogramAndEqualize(working_image)
            if args.EqualizeColorHistogram:
                working_image = equalizecolor(working_image)
            if args.MedianFilter:
                if args.NTSCgrayscale:  # if its already gray ya cant gray it again
                    working_image = medianFilter(working_image)
                else:  # gray it before filtering
                    working_image = ntsc_grayscale(working_image)
                    working_image = medianFilter(working_image)
            process_image(working_image, args.watermark, args.pos)

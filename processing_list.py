
from PIL import Image, ImageOps
import math
import statistics

def imageResize(width, height, img):
    widthRatio = width/img.size[0]
    heightRatio = height/img.size[1]
    
    newWidth = int(widthRatio*img.size[0])
    newHeight = int(heightRatio*img.size[1])
    
    newImage = img.resize((newWidth, newHeight))
    return newImage

def ImgNegative(img_input,coldepth):
    #solusi 1
    #img_output=ImageOps.invert(img_input)
    
    #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i,j] = (255-r, 255-g, 255-b)
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output

def ImgRotate(img_input,coldepth,deg):
    #solusi 1
    # img_output=img_input.rotate(deg)
    
    # #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if deg == 90 or deg == -270:
                r, g, b = img_input.getpixel((j,img_input.size[0]-i-1))
            elif deg == 180:
                r, g, b = img_input.getpixel((i, img_input.size[1]-1-j))
            elif deg == -90 or deg == 270:
                r, g, b = img_input.getpixel((img_input.size[1]-j-1,i))
            elif deg == -180:
                r, g, b = img_input.getpixel((img_input.size[1]-1-i, img_input.size[1]-1-j))
            elif deg == 0:
                r, g, b = img_input.getpixel((i,j))
            pixels[i,j] = (r, g, b)
                
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output

def ImgTranslation(img_input, coldepth, direction, n):

    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if direction == "x":
                if j <= n:
                    r, g, b = (0, 0, 0)
                else:
                    r, g, b = img_input.getpixel((i, j - n))
            elif direction == "y":
                if i <= n:
                    r, g, b = (0, 0, 0)
                else:
                    r, g, b = img_input.getpixel((i - n, j))
            elif direction == "xy":
                if j <= n or i <= n:
                    r, g, b = (0, 0, 0)
                else:
                    r, g, b = img_input.getpixel((i - n, j - n))
            pixels[i,j] = (r, g, b)   
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output

def ImgThreshold(img_input,coldepth,thrVal):
    t = thrVal
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    
    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    oldPixels = img_input.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if oldPixels[i,j] < (t, t, t):
                pixels[i,j] = (0, 0, 0)
            elif oldPixels[i,j] >= (t, t, t):
                pixels[i,j] = (255, 255, 255)
            
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output

def ImgBrightness(img_input,coldepth,brightVal):
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i,j] = (brightVal+r, brightVal+g, brightVal+b)
            if (r,g,b) > (255,255,255):
                pixels[i,j] = (255,255,255)
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output


def ImgLogTransform(img_input,coldepth,constVal):
    # img_input = imageResize(300, 300, img_input)
    
    if coldepth!=24:
        img_input = img_input.convert('RGB')
     
    # solusi 2    
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            
            r = constVal * int(math.log(r + 1))
            g = constVal * int(math.log(g + 1))
            b = constVal * int(math.log(b + 1))
            pixels[i,j] = (r, g, b)
            
            if r > 255:
                r = 255
            elif g > 255:
                g = 255
            elif b > 255:
                b = 255
    
                
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output


def ImgBlend(img_input, coldepth, img_input2, coldepth2, alpha1, alpha2):
    
    img_input = imageResize(300, 300, img_input)
    img_input2 = imageResize(300, 300, img_input2)
    
    # Zasya Copyright  
    
    # img_output = Image.blend(img_input, img_input2, alpha=0.2)
    
    # img_input2.show()
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    elif coldepth2!=24:
        img_input2 = img_input2.convert('RGB')
      
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    print(alpha1)
    print(alpha2)
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            color1 = img_input.getpixel((i, j))
            color2 = img_input2.getpixel((i, j))
            r = int(color1[0]*alpha1) + int(color2[0]*alpha2)
            g = int(color1[1]*alpha1) + int(color2[1]*alpha2)
            b = int(color1[2]*alpha1) + int(color2[2]*alpha2)
            pixels[i,j] =  (r, g, b)
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output

def ImgFlip(img_input,coldepth,flipVal):
    #solusi 1
    # img_output=img_input.flip()
    
    #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if flipVal == "vertical": 
                r, g, b = img_input.getpixel((i, img_input.size[1]-1-j))
            elif flipVal == "vertical-horizontal":
                r, g, b = img_input.getpixel((img_input.size[1]-1-i, img_input.size[1]-1-j))
            elif flipVal == "horizontal": 
                r, g, b = img_input.getpixel((img_input.size[1]-1-i, j))
            pixels[i,j] = (r, g, b)
                
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output

def ZoomIn(img_input, coldepth, scaleVal):
    if coldepth != 24:
        img_input.convert('RGB')
    
    row = img_input.size[0] * scaleVal
    col = img_input.size[1] * scaleVal
    img_output = Image.new('RGB', (row, col))
    pixel = img_output.load()

    for i in range(row-1):
        for j in range(col-1):
            r, g, b = img_input.getpixel((int(i/scaleVal), int(j/scaleVal)))  
            pixel[i, j] = (r, g, b)                                                                        
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output      
    
def ZoomOut(img_input, coldepth, scaleVal):
    if coldepth != 24:
        img_input.convert('RGB')
    print(scaleVal)
    row = int(img_input.size[0]/scaleVal)
    col = int(img_input.size[1]/scaleVal)
    img_output = Image.new('RGB', (row, col))
    pixel = img_output.load()
    print(row)
    print(col)
   
    for i in range(row-1):
        for j in range(col-1):
            r, g, b = img_input.getpixel((int(i * scaleVal), int(j * scaleVal)))  
            pixel[i, j] = (r, g, b)                                                      
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output  

def Median(img_input, coldepth):
    if coldepth != 24:
        img_input.convert('RGB')

    row = int(img_input.size[0])
    col = int(img_input.size[1])
    img_output = Image.new('RGB', (row, col))
    print(row)
    print(col)
    mask = [(0,0)] * 9
    for i in range(row-1):
        for j in range(col-1):
            mask[0] = img_input.getpixel((i-1, j-1))
            mask[1] = img_input.getpixel((i-1, j))
            mask[2] = img_input.getpixel((i-1, j+1))
            mask[3] = img_input.getpixel((i, j-1))
            mask[4] = img_input.getpixel((i, j))
            mask[5] = img_input.getpixel((i, j+1))
            mask[6] = img_input.getpixel((i+1, j-1))
            mask[7] = img_input.getpixel((i+1, j))
            mask[8] = img_input.getpixel((i+1, j+1)) 
            
            mask.sort()
            img_output.putpixel((i, j),(mask[4]))
                                                            
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output  


def Mean(img_input, coldepth):

    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    
    mask = [(0,0)] * 9

    for i in range(1, img_input.size[0] - 1):
        for j in range(1, img_input.size[1] - 1):
            red = 0
            green = 0
            blue = 0
            mask[0] = img_input.getpixel((i-1,j-1))
            mask[1] = img_input.getpixel((i-1,j))
            mask[2] = img_input.getpixel((i-1,j+1))
            mask[3] = img_input.getpixel((i,j-1))
            mask[4] = img_input.getpixel((i,j))
            mask[5] = img_input.getpixel((i,j+1))
            mask[6] = img_input.getpixel((i+1,j-1))
            mask[7] = img_input.getpixel((i+1,j))
            mask[8] = img_input.getpixel((i+1,j+1))
            
            for k in range(8):
                r, g, b = mask[k]
                red = red + r
                green = green + g
                blue = blue + b
                
            red = int(red * 1/9)
            green = int(green * 1/9)
            blue = int(blue * 1/9)
            
            pixels[i,j] = (red, green, blue)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output
              
                    
def Edge(img_input, coldepth, type):
    img_input = img_input.convert('L')

    img_output = Image.new('L', (img_input.size[0], img_input.size[1]))
    pixel = img_output.load()
    mask = [(0,0)] * 9
    mask2 = [(0,0)] * 9

    if type == "robert":
        gX = [[1, 0], [0, -1]]
        gY = [[0, 1], [-1, 0]]
        mask = [(0,0)] * 4
        mask2 = [(0,0)] * 4
        for i in range(img_input.size[0] - 1):
            for j in range(img_input.size[1] - 1):
                valueX = 0
                valueY = 0
                finalValue = 0
                mask[0] = (img_input.getpixel((i-1, j-1)) * gX[0][0])
                mask[1] = (img_input.getpixel((i-1, j)) * gX[0][1])
                mask[2] = (img_input.getpixel((i-1, j+1)) * gX[1][0])
                mask[3] = (img_input.getpixel((i, j-1)) * gX[1][1])
                
                mask2[0] = (img_input.getpixel((i-1, j-1)) * gY[0][0])
                mask2[1] = (img_input.getpixel((i-1, j)) * gY[0][1])
                mask2[2] = (img_input.getpixel((i-1, j+1)) * gY[1][0])
                mask2[3] = (img_input.getpixel((i, j-1)) * gY[1][1])
                
                for x in range(4):
                    rgb = mask[x]
                    valueX = valueX + rgb
                for y in range(4):
                    rgb2 = mask2[y]
                    valueY = valueY + rgb2
                finalValue = valueX + valueY
                # print(finalValue)
                if finalValue < 0: 
                    finalValue = 0
                elif finalValue > 255:
                    finalValue = 255
                pixel[i,j] = (finalValue) 
    else:
        if type == "sobel":
            gX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
            gY = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        elif type == "prewitt":
            gX = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
            gY = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
        elif type == "laplacian":
            gX = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
            gY = [[-1, 2, -1], [2, -4, 2], [-1, 2, -1]]
        elif type == "scharr": 
            gX = [[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]]
            gY = [[3, 10, 3], [0, 0, 0], [-3, -10, -3]]
            

        for i in range(img_input.size[0] - 1):
            for j in range(img_input.size[1] - 1):
                valueX = 0
                valueY = 0
                finalValue = 0
                
                #for gradient X
                mask[0] = (img_input.getpixel((i-1, j-1)) * gX[0][0])
                mask[1] = (img_input.getpixel((i-1, j)) * gX[0][1])
                mask[2] = (img_input.getpixel((i-1, j+1)) * gX[0][2])
                mask[3] = (img_input.getpixel((i, j-1)) * gX[1][0])
                mask[4] = (img_input.getpixel((i, j)) * gX[1][1])
                mask[5] = (img_input.getpixel((i, j+1)) * gX[1][2])
                mask[6] = (img_input.getpixel((i+1, j-1)) * gX[2][0])
                mask[7] = (img_input.getpixel((i+1, j)) * gX[2][1])
                mask[8] = (img_input.getpixel((i+1, j+1)) * gX[2][2])
                
                #for gradient Y
                mask2[0] = (img_input.getpixel((i-1, j-1)) * gY[0][0])
                mask2[1] = (img_input.getpixel((i-1, j)) * gY[0][1])
                mask2[2] = (img_input.getpixel((i-1, j+1)) * gY[0][2])
                mask2[3] = (img_input.getpixel((i, j-1)) * gY[1][0])
                mask2[4] = (img_input.getpixel((i, j)) * gY[1][1])
                mask2[5] = (img_input.getpixel((i, j+1)) * gY[1][2])
                mask2[6] = (img_input.getpixel((i+1, j-1)) * gY[2][0])
                mask2[7] = (img_input.getpixel((i+1, j)) * gY[2][1])
                mask2[8] = (img_input.getpixel((i+1, j+1)) * gY[2][2])
                
                for x in range(8):
                    rgb = mask[x]
                    valueX = valueX + rgb
                
                for y in range(8):
                    rgb2 = mask2[y]
                    valueY = valueY + rgb2
                finalValue = valueX + valueY
                
                if finalValue < 0: 
                    finalValue = 0
                elif finalValue > 255:
                    finalValue = 255
                pixel[i,j] = (finalValue)  
                

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output

def Morphology(img_input, coldepth, mode):
    # if coldepth != 24:
    img_input.convert('L')

    row = int(img_input.size[0])
    col = int(img_input.size[1])
    img_output = Image.new('L', (row, col))
    print(row)
    print(col)
    mask = [(0,0)] * 9
    singlePixel = [(0,0)] * 9
    for i in range(row-1):
        for j in range(col-1):
            mask[0] = img_input.getpixel((i-1, j-1))
            mask[1] = img_input.getpixel((i-1, j))
            mask[2] = img_input.getpixel((i-1, j+1))
            mask[3] = img_input.getpixel((i, j-1))
            mask[4] = img_input.getpixel((i, j))
            mask[5] = img_input.getpixel((i, j+1))
            mask[6] = img_input.getpixel((i+1, j-1))
            mask[7] = img_input.getpixel((i+1, j))
            mask[8] = img_input.getpixel((i+1, j+1)) 
            # print(mask[0][0])
            
            for k in range(9):
                singlePixel[k] = mask[k][0]
                # print(singlePixel[k])
            
            if mode == "erosion":
                img_output.putpixel((i, j),(min(singlePixel)))
            elif mode == "dilation":
                img_output.putpixel((i, j),(max(singlePixel)))
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output  

def Morphology2(img_input, coldepth, mode):
    img_input.convert('L')

    if mode == "opening": 
        img_morphology1 = Morphology(img_input, coldepth, "erosion")
        # img_morphology1.show()
    elif "bottom_hat": 
        img_morphology1 = Morphology(img_input, coldepth, "dilation")
        # img_morphology1.show()
    
    row = int(img_input.size[0])
    col = int(img_input.size[1])
    img_output = Image.new('L', (row, col))
    print(row)
    print(col)
    mask = [(0,0)] * 9
    mask_pure = [(0,0)] * 9
    singlePixel = [(0,0)] * 9
    for i in range(row-1):
        for j in range(col-1):
                        
            mask[0] = img_morphology1.getpixel((i-1, j-1))
            mask[1] = img_morphology1.getpixel((i-1, j))
            mask[2] = img_morphology1.getpixel((i-1, j+1))
            mask[3] = img_morphology1.getpixel((i, j-1))
            mask[4] = img_morphology1.getpixel((i, j))
            mask[5] = img_morphology1.getpixel((i, j+1))
            mask[6] = img_morphology1.getpixel((i+1, j-1))
            mask[7] = img_morphology1.getpixel((i+1, j))
            mask[8] = img_morphology1.getpixel((i+1, j+1)) 

            for k in range(9):
                singlePixel[k] = mask[k][0]
                # print(singlePixel[k])
            if mode == "opening":
                img_output.putpixel((i, j),(max(singlePixel)))
            elif mode == "closing":
                img_output.putpixel((i, j),(min(singlePixel)))
            
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output          

def Morphology3(img_input, coldepth, mode):
    img_input.convert('L')

    if mode == "top_hat": 
        img_morphology1 = Morphology2(img_input, coldepth, "opening")
        # img_morphology1.show()
    elif mode == "bottom_hat": 
        img_morphology1 = Morphology2(img_input, coldepth, "closing")
        # img_morphology1.show()
    
    row = int(img_input.size[0])
    col = int(img_input.size[1])
    img_output = Image.new('L', (row, col))
    print(row)
    print(col)
    mask = [(0,0)] * 9
    mask_pure = [(0,0)] * 9
    singlePixel = [(0,0)] * 9
    for i in range(row-1):
        for j in range(col-1):
            
            mask_pure[0] = img_input.getpixel((i-1, j-1))
            mask_pure[1] = img_input.getpixel((i-1, j))
            mask_pure[2] = img_input.getpixel((i-1, j+1))
            mask_pure[3] = img_input.getpixel((i, j-1))
            mask_pure[4] = img_input.getpixel((i, j))
            mask_pure[5] = img_input.getpixel((i, j+1))
            mask_pure[6] = img_input.getpixel((i+1, j-1))
            mask_pure[7] = img_input.getpixel((i+1, j))
            mask_pure[8] = img_input.getpixel((i+1, j+1)) 
            
            
            mask[0] = img_morphology1.getpixel((i-1, j-1))
            mask[1] = img_morphology1.getpixel((i-1, j))
            mask[2] = img_morphology1.getpixel((i-1, j+1))
            mask[3] = img_morphology1.getpixel((i, j-1))
            mask[4] = img_morphology1.getpixel((i, j))
            mask[5] = img_morphology1.getpixel((i, j+1))
            mask[6] = img_morphology1.getpixel((i+1, j-1))
            mask[7] = img_morphology1.getpixel((i+1, j))
            mask[8] = img_morphology1.getpixel((i+1, j+1)) 

            for k in range(9):
                singlePixel[k] = mask[k][0]
                # print(singlePixel[k])
                
            if mode == "top_hat":
                for t in range(8):
                    img_output.putpixel((i, j),(mask_pure[t][0] - singlePixel[t]))
            elif mode == "bottom_hat":
                for t in range(8):
                    img_output.putpixel((i, j),(singlePixel[t] - mask_pure[t][0]))
            
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
                
    return img_output  
       
def Gaussian(img_input, coldepth):
    img_input = img_input.convert('L')

    img_output = Image.new('L', (img_input.size[0], img_input.size[1]))
    pixel = img_output.load()
    mask = [(0,0)] * 9

    kernel = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    for i in range(img_input.size[0] - 1):
        for j in range(img_input.size[1] - 1):
            value = 0
            finalValue = 0
            #for gradient X
            mask[0] = (img_input.getpixel((i-1, j-1)) * kernel[0][0])
            mask[1] = (img_input.getpixel((i-1, j)) * kernel[0][1])
            mask[2] = (img_input.getpixel((i-1, j+1)) * kernel[0][2])
            mask[3] = (img_input.getpixel((i, j-1)) * kernel[1][0])
            mask[4] = (img_input.getpixel((i, j)) * kernel[1][1])
            mask[5] = (img_input.getpixel((i, j+1)) * kernel[1][2])
            mask[6] = (img_input.getpixel((i+1, j-1)) * kernel[2][0])
            mask[7] = (img_input.getpixel((i+1, j)) * kernel[2][1])
            mask[8] = (img_input.getpixel((i+1, j+1)) * kernel[2][2])

            for k in range(8):
                tempValue = mask[k]
                value = value + tempValue
                
            finalValue = int(value / 16)
            pixel[i,j] = (finalValue)  
               

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
        
    return img_output


def Grayscale(img_input,coldepth):
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('L',(img_input.size[0],img_input.size[1]))
    pixel = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            value = int((r + g + b) / 3)
            # value = int((r * 0.299) + (g * 0.587) + (b * 0.114))
            pixel[i, j] = value
    return img_output

def hsv(img_input,coldepth):
    # return img_input.convert("HSL")
    if coldepth!=24:
        img_input = img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixel = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            r, g, b = r / 255.0, g / 255.0, b / 255.0
            
            cmax = max(r, g, b)
            cmin = min(r, g, b)
            diff = cmax-cmin
            
            if cmax == cmin:
                h = 0
            elif cmax == r:
                h = (60 * ((g - b) / diff) + 360) % 360
            elif cmax == g:
                h = (60 * ((b - r) / diff) + 120) % 360
            elif cmax == b:
                h = (60 * ((r - g) / diff) + 240) % 360
            if cmax == 0:
                s = 0
            else:
                s = (diff / cmax) * 100
            v = cmax * 100

            pixel[i,j] = (int(h),int(s),int(v))
        
    return img_output


#Dibuat secara sadar untuk kebutuhan diri sendiri. (1915051024/Putu Zasya Eka Satya Nugraha)
        
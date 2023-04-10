import PySimpleGUI as sg 
import os.path 
from PIL import Image, ImageOps
from processing_list import *
import io

# Kolom Area No 1: Area open folder and select image 
for_image = 1
file_list_column = [ 
    [ 
        sg.In(size = (20, 1), enable_events = True, key = "ImgFolder"), 
        sg.FolderBrowse(size = (8, 1))  
    ],
    [ 
        sg.Frame("Choose image " + str(for_image), [
            [ 
                sg.Button("Change", size=(25, 1), key="SelectFor"), 
            ],

            [ 
                sg.Listbox( 
                values=[], enable_events=True, size=(27, 10), key="ImgList" 
                ), 
            ]
        ],key="ImgSelectFor"), 
    ],
    [
        sg.Frame('Image Information', [
            [ 
                sg.Text("Image Size : "),
                sg.Text(size = (14, 1), key="ImgSize")
            ], 
            [ 
                sg.Text("Color Depth : "),
                sg.Text(size=(14, 1), key="ImgColorDepth")
            ], 
        ], font = ("Helvetica", 10)) #, size = (16, 1)
    ],
    [
        sg.Frame('Processing 1', [
             [ 
                sg.Button("Negative", size=(11, 1), key="ImgNegative"), 
                sg.Button("Brightness", size=(11, 1), key="ImgBrightness")
            ],
            [
                sg.Button("Threshold", size=(11, 1), key="ImgThreshold"),
                sg.Button("Logarithmic", size=(11, 1), key="ImgLogTransform"),
            ],
            [
                sg.Slider(orientation ='horizontal', key='SliderTarget', range=(0,255), size=(23, 15))
            ],
        ]) #, size = (10, 1)
    ]
    
] 
# Kolom Area No 2: Area viewer image input 
image_viewer_column = [ 
    [sg.Text("Image Input :")], 
    [sg.Text(size=(40, 1), key="FilepathImgInput")], 
    [sg.Image(key="ImgInputViewer")], 
    [sg.Text(key = "SeparatorImage")]
]


# Kolom Area No 3: Area Image info dan Tombol list of processing 
list_processing = [ 
    [
        sg.Frame('Processing 2', [
            [
                sg.Button("Rotate", size=(12, 1), key="ImgRotate"), 
                sg.Button("Blend", size=(12, 1), key="ImgBlend")
            ],
            [
                sg.Button("Image Flip", size=(26, 1), key="ImgFlip")
            ],
            [
                sg.Button("Zoom In", size=(12, 1), key="Plus"),
                sg.Button("Zoom Out", size=(12, 1), key="Minus")
            ],
            [
                sg.Button("Trans X", size=(7, 1), key = "TranslationX"),
                sg.Button("Trans Y", size=(8, 1), key = "TranslationY"),
                sg.Button("Trans XY", size=(7, 1), key = "TranslationXY") 
            ],
            [
                sg.Text(size=(27, 1), key="rule", visible=False)
            ],
            [
                sg.InputText(key='inputType', size=(30, 1), visible=False)
            ],
            [
                sg.Text(size=(27, 1), key="rule2", visible=False)
            ],
            [
                sg.InputText(key='inputType2', size=(30, 1), visible=False)
            ]
        ])
    ], 
    [
        sg.Frame('Processing 3', [
            [
                sg.Button("Median", size=(12, 1), key="Median"),
                sg.Button("Mean", size=(12, 1), key = "Mean")
            ],
            [
                sg.Button("Sobel", size=(12, 1), key = "Sobel"),  
                sg.Button("Prewitt", size=(12, 1), key = "Prewitt")  
            ],
            [
                sg.Button("Scharr", size=(12, 1), key = "Scharr"),
                sg.Button("Robert", size=(12, 1), key = "Robert")
            ],
            [
                sg.Button("Laplacian", size=(12, 1), key = "Laplacian"),
                sg.Button("Gaussian", size=(12, 1), key = "Gaussian")    
            ],
            [
                sg.Button("Grayscale", size=(12, 1), key = "Grayscale"),
                sg.Button("HSV/HSL", size=(12, 1), key = "HSV")
            ],
            [
                sg.Button("Erosion", size=(12, 1), key = "Erosion"),
                sg.Button("Dilation", size=(12, 1), key = "Dilation")
            ],
            [
                sg.Button("Opening", size=(12, 1), key = "Opening"),
                sg.Button("Closing", size=(12, 1), key = "Closing")
            ],
            [
                sg.Button("TWH", size=(12, 1), key = "Top_hat"),
                sg.Button("TBH", size=(12, 1), key = "Bottom_hat")
            ]
        ])
    ]   
] 
# Kolom Area No 4: Area viewer image output 
image_viewer_column2 = [ 
    [sg.Text("Image Processing Output:")], 
    [sg.Text(size=(40, 1), key="ImgProcessingType")], 
    [sg.Image(key="ImgOutputViewer")], 
    [sg.Text(" ")]
] 
# Gabung Full layout 
layout = [ 
    [ 
        sg.Column(file_list_column), 
        sg.VSeperator(), 
        sg.Column(image_viewer_column), 
        sg.VSeperator(), 
        sg.Column(image_viewer_column2), 
        sg.VSeperator(), 
        sg.Column(list_processing)         
    ] 
] 
window = sg.Window("Mini Image Editor by Zasya", layout, modal = False) 

# Windows Image 2
def Window2(fileName, img):
    layout2 = [
        [sg.Text("Image Input 2: ")], 
        [sg.Image(fileName)], 
    ]
    window2 = sg.Window("Image 2", layout2, modal = True)  
    while True: 
        event, values = window2.read()
        if event == sg.WIN_CLOSED: 
            break
#nama image file temporary setiap processing output
filename_out = "out.png"

# Run the Event Loop 
win2_active = False

while True:
    event, values = window.read() 
    if event == "Exit" or event == sg.WIN_CLOSED: 
        break 
    if not win2_active or for_image == 2:
        win2_active = True
        layout2 = [
            [sg.Text("Image Input 2: ")], 
            # [sg.Image(key="ImgInputViewer2")], 
        ]
        window2 = sg.Window("Image 2", layout2, modal = True) 
        while True:
            event2, values2 = window2.read()
            if event2 is None:
                win2_active = False

                break
# Folder name was filled in, make a list of files in the folder 
    if event == "ImgFolder": 
        folder = values["ImgFolder"] 
        
        try: 
        # Get list of files in folder 
            file_list = os.listdir(folder) 
        except: 
            file_list = [] 
            
        fnames = [ 
            f 
            for f in file_list 
                if os.path.isfile(os.path.join(folder, f)) 
                and f.lower().endswith((".png", ".gif", ".bmp", ".jpg")) 
        ] 
        window["ImgList"].update(fnames)
    elif event == "SelectFor":
        for_image = for_image == 2 and 1 or 2
        window["ImgSelectFor"].update("Choose image " + str(for_image))
    elif event == "ImgList": # A file was chosen from the listbox 
        try: 
            filename = os.path.join( 
            values["ImgFolder"], values["ImgList"][0] 
            )
            if for_image == 1: 
                image_input = Image.open(filename)
                image_input.thumbnail((300,300))
                temp_image = io.BytesIO()
                image_input.save(temp_image, format="PNG")
                window["FilepathImgInput"].update(filename)
                # window["ImgInputViewer"].update(filename=filename, size=(200,200))
                window["ImgInputViewer"].update(data=temp_image.getvalue())

                window["ImgProcessingType"].update(filename) 
                window["ImgOutputViewer"].update(data=temp_image.getvalue()) 
                img_input = Image.open(filename) 
                #img_input.show() 
                img_input = img_input.resize((300,300))
                
                #Size 
                img_width, img_height = img_input.size 
                window["ImgSize"].update(str(img_width)+" x "+str(img_height)) 
                
                #Color depth 
                mode_to_coldepth = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 
                24, "HSV": 24, "I": 32, "F": 32, "W":24 } 
                coldepth = mode_to_coldepth[img_input.mode] 
                window["ImgColorDepth"].update(str(coldepth))
                            
            else: 
                # window["SeparatorImage"].update('_' * 45)
                # window["FilepathImgInput2"].update(filename)
                # window["ImgInputViewer2"].update(filename=filename)
                img_input2 = Image.open(filename)  
                img_input2 = img_input2.resize((300,300))
                image_input2.thumbnail((300,300))
                temp_image2 = io.BytesIO()
                image_input2.save(temp_image2, format="PNG")
                window["inputType2"].update(data=temp_image2.getvalue())
                # Window2(filename, img_input2)
                # img_input2.show()
                # sg.popup_no_buttons(title='image2', text_color=('#F7F6F2'), image=filename, modal = False)
                # print('done')
        except: 
            pass
    
    elif event == "ImgNegative":
        try:
            #element management
            window["inputType2"].update(visible=False)
            window["rule2"].update(visible=False)
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["ImgProcessingType"].update("Image Negative")
            
            #calling function
            img_output=ImgNegative(img_input, coldepth)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgRotate":
        try:
            #element management
            window["inputType2"].update(visible=False)
            window["rule2"].update(visible=False)
            window["rule"].update("90/ 180/ 270/ 0/ -90/ -180/ -270")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["ImgProcessingType"].update("Image Rotate")
            
            #get value
            degVal = int(values["inputType"])
            
            #calling function
            img_output=ImgRotate(img_input,coldepth,degVal)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "TranslationX":
        try:
            #element management
            window["inputType2"].update(visible=False)
            window["rule2"].update(visible=False)
            window["rule"].update("input n value")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["ImgProcessingType"].update("Image Translation X")
            
            #get value
            n = int(values["inputType"])
            
            img_output=ImgTranslation(img_input,coldepth, "x", n)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "TranslationY":
        try:
            #element management
            window["inputType2"].update(visible=False)
            window["rule2"].update(visible=False)
            window["rule"].update("input n value")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["ImgProcessingType"].update("Image Translation Y")
            
            #get value
            n = int(values["inputType"])
            
            img_output=ImgTranslation(img_input,coldepth, "y", n)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "TranslationXY":
        try:
            #element management
            window["inputType2"].update(visible=False)
            window["rule2"].update(visible=False)
            window["rule"].update("input n value")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["ImgProcessingType"].update("Image Translation X and Y")
            
            #get value
            n = int(values["inputType"])
            
            img_output=ImgTranslation(img_input,coldepth, "xy", n)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
          
    elif event == "ImgThreshold":
        try:
            #element management
            window["inputType2"].update(visible=False)
            window["rule2"].update(visible=False)
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["SliderTarget"].update(visible=True)
            window["ImgProcessingType"].update("Image Threshold")
            
            #get value
            thrVal = int(values["SliderTarget"])
            
            #calling function
            img_output=ImgThreshold(img_input,coldepth, thrVal)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgBrightness":
        try:
            #element management
            window["rule2"].update(visible=False)
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["SliderTarget"].update(visible=True)
            window["ImgProcessingType"].update("Image Brightness")
            
            #get value
            brightVal = int(values["SliderTarget"])
            
            #calling function
            img_output=ImgBrightness(img_input,coldepth,brightVal)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "ImgLogTransform":
        try:
            #element management
            window["rule2"].update(visible=False)
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["SliderTarget"].update(visible=True)
            window["ImgProcessingType"].update("Image Log Transform")
            
            #get value
            constVal = int(values["SliderTarget"])
            
            #calling function
            img_output=ImgLogTransform(img_input,coldepth,constVal)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "ImgBlend":
        try:
            #element management
            window["rule"].update("alpha image1: 0.0 - 1.0")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["inputType2"].update(visible=True)
            window["rule2"].update("alpha image2: 0.0 - 1.0")
            window["rule2"].update(visible=True)
            window["ImgProcessingType"].update("Image Blend")
                       
            #get alpha value of textbox
            alpha1 = float(values["inputType"])
            alpha2 = float(values["inputType2"])
            
            #get coldepth from image2
            coldepth2 = mode_to_coldepth[img_input2.mode]
           
            #calling function
            img_output=ImgBlend(img_input, coldepth, img_input2, coldepth2, alpha1, alpha2)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event =="ImgFlip":
        try:
            #element management
            window["rule2"].update(visible=False)
            window["rule"].update("horizontal/ vertical/ vertical-horizontal")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Image Flip")
            
            #get value
            flipVal = str(values["inputType"])

            #calling function
            img_output=ImgFlip(img_input,coldepth,flipVal)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Plus":
        try:
            #element management
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Image Zoom In")
            
            #get value
            scaleVal = int(values["inputType"])
            
            #calling function
            img_output=ZoomIn(img_input,coldepth,scaleVal)
            
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Minus":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=True)
            window["inputType"].update(visible=True)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Image Zoom Out")
            scaleVal = int(values["inputType"])
            img_output=ZoomOut(img_input,coldepth,scaleVal)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "Median":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Median Noise Reduction")
            img_output=Median(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "Mean":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Mean Noise Reduction")
            img_output=Mean(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "Sobel":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Sobel Detection")
            img_output=Edge(img_input,coldepth, "sobel")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "Prewitt":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Prewitt Detection")
            img_output=Edge(img_input,coldepth, "prewitt")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Laplacian":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Laplacian Detection")
            img_output=Edge(img_input,coldepth, "laplacian")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "Scharr":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Scharr Detection")
            img_output=Edge(img_input,coldepth, "scharr")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Robert":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Robert Detection")
            img_output=Edge(img_input,coldepth, "robert")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Erosion":
        try:
            print('erosion')
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Erosion")
            img_output=Morphology(img_input,coldepth, "erosion")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Dilation":
        try:
            print('dilation')
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Dilation")
            img_output=Morphology(img_input,coldepth, "dilation")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Gaussian":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Gaussian Filter")
            img_output=Gaussian(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Grayscale":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Grayscale")
            img_output=Grayscale(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Opening":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Opening")
            img_output=Morphology2(img_input,coldepth, "opening")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "Closing":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Closing")
            img_output=Morphology2(img_input,coldepth, "closing")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Top_hat":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Top White Hat")
            img_output=Morphology3(img_input,coldepth, "top_hat")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
    elif event == "Bottom_hat":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("Top Black Hat")
            img_output=Morphology3(img_input,coldepth, "bottom_hat")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
    
    elif event == "HSV":
        try:
            window["rule2"].update(visible=False)
            window["rule"].update("2/ 4/ 6")
            window["rule"].update(visible=False)
            window["inputType"].update(visible=False)
            window["inputType2"].update(visible=False)
            window["ImgProcessingType"].update("HSV/HSL")
            img_output=hsv(img_input,coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass
        
        
#Modified by Zasya
            
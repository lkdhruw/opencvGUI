from tkinter import *
from PIL import Image
from PIL import ImageFilter
import io
import cv2

vc = cv2.VideoCapture(0)


class Window:
    def __init__(self, master):
        master.title("Digital Image Processing")
        master.minsize(800, 400)

        toolbar = Frame(root)
        toolbar.grid(row=1, column=1)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        canvas = Canvas(root, width=1300, height=640)
        canvas.grid(row=2, column=1)

        scrollbar = Scrollbar(root, command=canvas.yview)
        scrollbar.grid(row=2, column=2, sticky=W + E + N + S)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.bind('<Configure>', on_configure)

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        self.filename = ""
        self.imageLabel = Label(toolbar, text="Image").grid(row=1, column=1)
        self.imageInput = Entry(toolbar)
        self.imageInput.grid(row=1, column=2)
        self.imageInput.insert(0, "Select an image")

        self.button = Button(toolbar, text="Browse", command=self.browseimg)
        self.button.grid(row=1, column=3)

        self.getCambutton = Button(toolbar, text="Capture", command=self.capture)
        self.getCambutton.grid(row=1, column=4)

        # im = Image.open("lena.png")
        im = Image.open("Default.png")
        self.originalImage = im
        self.originalImage240x240 = self.originalImage
        self.originalImage240x240.thumbnail((240, 240))
        self.originalImage360x360 = self.originalImage
        self.originalImage360x360.thumbnail((360, 360))
        self.originalImage480x480 = self.originalImage
        self.originalImage480x480.thumbnail((480, 480))

        image = self.originalImage240x240
        photo = self.imageToBytes(image)
        self.originalImageView = Label(frame, width=240, height=240)
        self.originalImageView.grid(row=2, column=1)
        self.originalImageView["image"] = photo
        self.originalPhoto = photo
        Label(frame, text="Original image").grid(row=3, column=1)

        # pixels = list(im.getdata())

        image = self.originalImage240x240
        image = image.convert("L")
        photo = self.imageToBytes(image)
        self.grayscaleImageView = Label(frame, width=240, height=240)
        self.grayscaleImageView.grid(row=2, column=2)
        self.grayscaleImageView["image"] = photo
        self.grayscalePhoto = photo
        Label(frame, text="Grayscale image").grid(row=3, column=2)

        image = self.originalImage240x240
        image = image.quantize(7)
        photo = self.imageToBytes(image)
        self.quantizeImageView = Label(frame, width=240, height=240)
        self.quantizeImageView.grid(row=2, column=3)
        self.quantizeImageView["image"] = photo
        self.quantizePhoto = photo
        self.quantizeScale = Scale(frame, label="Quantize", from_=2, to=8, length=240, orient=HORIZONTAL)
        self.quantizeScale.grid(row=3, column=3)
        self.quantizeScale.set(5)
        self.quantizeScale.bind("<B1-Motion>", self.quantize)

        image = self.originalImage240x240
        image = image.convert("L")
        photo = self.imageToBytes(image)
        self.binaryImageView = Label(frame, width=240, height=240)
        self.binaryImageView.grid(row=2, column=4)
        self.binaryImageView["image"] = photo
        self.binaryPhoto = photo
        self.binaryScale = Scale(frame, label="Binary", from_=0, to=255, length=240, orient=HORIZONTAL)
        self.binaryScale.grid(row=3, column=4)
        self.binaryScale.set(128)
        self.binaryScale.bind("<B1-Motion>", self.binary)

        image = self.originalImage240x240.copy()
        if image.mode == "RGB":
            R, G, B = image.split()
            width, _ = image.size
            listR = list(R.getdata())
            listG = list(G.getdata())
            listB = list(B.getdata())

            for i, px in enumerate(R.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (px, 0, 0))
            photo = self.imageToBytes(image)
            self.RImageView = Label(frame, width=240, height=240)
            self.RImageView.grid(row=2, column=5)
            self.RImageView["image"] = photo
            self.RPhoto = photo
            Label(frame, text="R component").grid(row=3, column=5)

            for i, px in enumerate(G.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (0, px, 0))
            photo = self.imageToBytes(image)
            self.GImageView = Label(frame, width=240, height=240)
            self.GImageView.grid(row=4, column=1)
            self.GImageView["image"] = photo
            self.GPhoto = photo
            Label(frame, text="G component").grid(row=5, column=1)

            for i, px in enumerate(B.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (0, 0, px))
            photo = self.imageToBytes(image)
            self.BImageView = Label(frame, width=240, height=240)
            self.BImageView.grid(row=4, column=2)
            self.BImageView["image"] = photo
            self.BPhoto = photo
            Label(frame, text="B component").grid(row=5, column=2)

            for i, px in enumerate(G.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (0, px, listB[i]))
            photo = self.imageToBytes(image)
            self.GBImageView = Label(frame, width=240, height=240)
            self.GBImageView.grid(row=4, column=3)
            self.GBImageView["image"] = photo
            self.GBPhoto = photo
            Label(frame, text="RGB-R component").grid(row=5, column=3)

            for i, px in enumerate(B.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (listR[i], 0, px))
            photo = self.imageToBytes(image)
            self.RBImageView = Label(frame, width=240, height=240)
            self.RBImageView.grid(row=4, column=4)
            self.RBImageView["image"] = photo
            self.RBPhoto = photo
            Label(frame, text="RGB-G component").grid(row=5, column=4)

            for i, px in enumerate(R.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (px, listG[i], 0))
            photo = self.imageToBytes(image)
            self.RGImageView = Label(frame, width=240, height=240)
            self.RGImageView.grid(row=4, column=5)
            self.RGImageView["image"] = photo
            self.RGPhoto = photo
            Label(frame, text="RGB-B component").grid(row=5, column=5)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.BLUR)
        photo = self.imageToBytes(image)
        self.filterBlurImageView = Label(frame, width=240, height=240)
        self.filterBlurImageView.grid(row=6, column=1)
        self.filterBlurImageView["image"] = photo
        self.filterBlurPhoto = photo
        Label(frame, text="Blur").grid(row=7, column=1)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.CONTOUR)
        photo = self.imageToBytes(image)
        self.filterContourImageView = Label(frame, width=240, height=240)
        self.filterContourImageView.grid(row=6, column=2)
        self.filterContourImageView["image"] = photo
        self.filterContourPhoto = photo
        Label(frame, text="Contour").grid(row=7, column=2)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.DETAIL)
        photo = self.imageToBytes(image)
        self.filterDetailImageView = Label(frame, width=240, height=240)
        self.filterDetailImageView.grid(row=6, column=3)
        self.filterDetailImageView["image"] = photo
        self.filterDetailPhoto = photo
        Label(frame, text="Detail").grid(row=7, column=3)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        photo = self.imageToBytes(image)
        self.filterEdge_enhanceImageView = Label(frame, width=240, height=240)
        self.filterEdge_enhanceImageView.grid(row=6, column=4)
        self.filterEdge_enhanceImageView["image"] = photo
        self.filterEedge_enhancePhoto = photo
        Label(frame, text="Eedge Enhance").grid(row=7, column=4)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        photo = self.imageToBytes(image)
        self.filterEdge_enhance_moreImageView = Label(frame, width=240, height=240)
        self.filterEdge_enhance_moreImageView.grid(row=6, column=5)
        self.filterEdge_enhance_moreImageView["image"] = photo
        self.filterEdge_enhance_morePhoto = photo
        Label(frame, text="Edge Enhance More").grid(row=7, column=5)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.EMBOSS)
        photo = self.imageToBytes(image)
        self.filterEmbossImageView = Label(frame, width=240, height=240)
        self.filterEmbossImageView.grid(row=8, column=1)
        self.filterEmbossImageView["image"] = photo
        self.filterEmbossPhoto = photo
        Label(frame, text="Emboss").grid(row=9, column=1)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.FIND_EDGES)
        photo = self.imageToBytes(image)
        self.filterFind_edgesImageView = Label(frame, width=240, height=240)
        self.filterFind_edgesImageView.grid(row=8, column=2)
        self.filterFind_edgesImageView["image"] = photo
        self.filterFind_edgesPhoto = photo
        Label(frame, text="Find Edges").grid(row=9, column=2)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.SMOOTH)
        photo = self.imageToBytes(image)
        self.filterSmoothImageView = Label(frame, width=240, height=240)
        self.filterSmoothImageView.grid(row=8, column=3)
        self.filterSmoothImageView["image"] = photo
        self.filterSmoothPhoto = photo
        Label(frame, text="Smooth").grid(row=9, column=3)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.SMOOTH_MORE)
        photo = self.imageToBytes(image)
        self.filterSmooth_moreImageView = Label(frame, width=240, height=240)
        self.filterSmooth_moreImageView.grid(row=8, column=4)
        self.filterSmooth_moreImageView["image"] = photo
        self.filterSmooth_morePhoto = photo
        Label(frame, text="Smooth More").grid(row=9, column=4)

        image = self.originalImage240x240
        image = image.filter(ImageFilter.SHARPEN)
        photo = self.imageToBytes(image)
        self.filterSharpenImageView = Label(frame, width=240, height=240)
        self.filterSharpenImageView.grid(row=8, column=5)
        self.filterSharpenImageView["image"] = photo
        self.filterSharpenPhoto = photo
        Label(frame, text="Sharpen").grid(row=9, column=5)

    def imageToBytes(self, image):
        b = io.BytesIO()
        image.save(b, 'gif')
        p = b.getvalue()
        photo = PhotoImage(data=p)
        return photo

    def loadOriginal(self):
        image = self.originalImage240x240
        photo = self.imageToBytes(image)
        self.originalImageView["image"] = photo
        self.originalPhoto = photo

    def loadGrayscale(self):
        image = self.originalImage240x240
        image = image.convert("L")
        photo = self.imageToBytes(image)
        self.grayscaleImageView["image"] = photo
        self.grayscalePhoto = photo

    def quantize(self, event):
        quantizeValue = self.quantizeScale.get()
        if quantizeValue == self.quantizeScale["to"] and self.quantizeScale["to"] < 256:
            self.quantizeScale["to"] = self.quantizeScale["to"] * 2

        if quantizeValue < self.quantizeScale["to"] / 2 and self.quantizeScale["to"] > 8:
            self.quantizeScale["to"] = self.quantizeScale["to"] / 2
        self.quantizeScale["label"] = "Quantize (2-" + str(self.quantizeScale["to"]) + ")"

        self.loadQuantize(quantizeValue)

    def loadQuantize(self, quantizeValue):
        # quantizeValue = self.quantizeScale.get()
        image = self.originalImage240x240
        image = image.quantize(quantizeValue)
        photo = self.imageToBytes(image)
        self.quantizeImageView["image"] = photo
        self.quantizePhoto = photo

    def binary(self, event=None):
        threshold = self.binaryScale.get()
        image = self.originalImage240x240
        image = image.convert("L")
        width, _ = image.size
        black = 1
        white = 1
        for i, px in enumerate(image.getdata()):
            y = int(i / width)
            x = int(i % width)
            if px > threshold:
                image.putpixel((x, y), 255)
                white += 1
            else:
                image.putpixel((x, y), 0)
                black += 1

        photo = self.imageToBytes(image)
        self.binaryImageView["image"] = photo
        self.binaryScale["label"] = "Binary- B: " + str(black * 100 / (black + white)) + " % W:" + str(
            white * 100 / (black + white)) + " %"
        self.binaryPhoto = photo

    def RGB(self):
        image = self.originalImage240x240.copy()
        if image.mode == "RGB":
            R, G, B = image.split()
            width, _ = image.size
            listR = list(R.getdata())
            listG = list(G.getdata())
            listB = list(B.getdata())

            for i, px in enumerate(R.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (px, 0, 0))
            photo = self.imageToBytes(image)
            self.RImageView["image"] = photo
            self.RPhoto = photo

            for i, px in enumerate(G.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (0, px, 0))
            photo = self.imageToBytes(image)
            self.GImageView["image"] = photo
            self.GPhoto = photo

            for i, px in enumerate(B.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (0, 0, px))
            photo = self.imageToBytes(image)
            self.BImageView["image"] = photo
            self.BPhoto = photo

            for i, px in enumerate(G.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (0, px, listB[i]))
            photo = self.imageToBytes(image)
            self.GBImageView["image"] = photo
            self.GBPhoto = photo

            for i, px in enumerate(B.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (listR[i], 0, px))
            photo = self.imageToBytes(image)
            self.RBImageView["image"] = photo
            self.RBPhoto = photo

            for i, px in enumerate(R.getdata()):
                y = int(i / width)
                x = int(i % width)
                image.putpixel((x, y), (px, listG[i], 0))
            photo = self.imageToBytes(image)
            self.RGImageView["image"] = photo
            self.RGPhoto = photo

    def blur(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.BLUR)
        photo = self.imageToBytes(image)
        self.filterBlurImageView["image"] = photo
        self.filterBlurPhoto = photo

    def contour(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.CONTOUR)
        photo = self.imageToBytes(image)
        self.filterContourImageView["image"] = photo
        self.filterContourPhoto = photo

    def detail(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.DETAIL)
        photo = self.imageToBytes(image)
        self.filterDetailImageView["image"] = photo
        self.filterDetailPhoto = photo

    def edge_enhance(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        photo = self.imageToBytes(image)
        self.filterEdge_enhanceImageView["image"] = photo
        self.filterEedge_enhancePhoto = photo

    def edge_enhance_more(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        photo = self.imageToBytes(image)
        self.filterEdge_enhance_moreImageView["image"] = photo
        self.filterEdge_enhance_morePhoto = photo

    def emboss(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.EMBOSS)
        photo = self.imageToBytes(image)
        self.filterEmbossImageView["image"] = photo
        self.filterEmbossPhoto = photo

    def find_edges(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.FIND_EDGES)
        photo = self.imageToBytes(image)
        self.filterFind_edgesImageView["image"] = photo
        self.filterFind_edgesPhoto = photo

    def smooth(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.SMOOTH)
        photo = self.imageToBytes(image)
        self.filterSmoothImageView["image"] = photo
        self.filterSmoothPhoto = photo

    def smooth_more(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.SMOOTH_MORE)
        photo = self.imageToBytes(image)
        self.filterSmooth_moreImageView["image"] = photo
        self.filterSmooth_morePhoto = photo

    def sharpen(self):
        image = self.originalImage240x240
        image = image.filter(ImageFilter.SHARPEN)
        photo = self.imageToBytes(image)
        self.filterSharpenImageView["image"] = photo
        self.filterSharpenPhoto = photo

    def browseimg(self):
        from tkinter.filedialog import askopenfilename
        # from tkFileDialog import askopenfilename
        Tk().withdraw()
        self.filename = askopenfilename()
        self.imageInput.delete(0, END)
        self.imageInput.insert(0, self.filename)
        self.originalImage = Image.open(self.filename)
        self.originalImage240x240 = self.originalImage
        self.originalImage240x240.thumbnail((240, 240))
        self.originalImage360x360 = self.originalImage
        self.originalImage360x360.thumbnail((360, 360))
        self.originalImage480x480 = self.originalImage
        self.originalImage480x480.thumbnail((480, 480))

        self.loadOriginal()
        self.loadGrayscale()
        self.loadQuantize(5)
        self.binary()
        self.RGB()
        self.blur()
        self.contour()
        self.detail()
        self.edge_enhance()
        self.edge_enhance_more()
        self.emboss()
        self.find_edges()
        self.smooth()
        self.smooth_more()
        self.sharpen()

    def capture(self):
        if vc.isOpened():
            rval, frame = vc.read()

            self.originalImage = Image.fromarray(frame, mode='RGB')
            self.originalImage240x240 = self.originalImage
            self.originalImage240x240.thumbnail((240, 240))
            self.originalImage360x360 = self.originalImage
            self.originalImage360x360.thumbnail((360, 360))
            self.originalImage480x480 = self.originalImage
            self.originalImage480x480.thumbnail((480, 480))

            self.loadOriginal()
            self.loadGrayscale()
            self.loadQuantize(5)
            self.binary()
            self.RGB()
            self.blur()
            self.contour()
            self.detail()
            self.edge_enhance()
            self.edge_enhance_more()
            self.emboss()
            self.find_edges()
            self.smooth()
            self.smooth_more()
            self.sharpen()


root = Tk()

window = Window(root)

root.mainloop()
# root.destroy()

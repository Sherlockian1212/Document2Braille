# Document2Braille
## Final project in Digital Image Processing and Machine Learning.
A project to convert images containing text into Braille. 

## Authors

1. **Thai Thi Kim Yen** - *Student ID: 47.01.104.250*
2. **Hoang Thuy Quynh Huong** - *Student ID: 47.01.104.096*

### Lecturer: Dr. NGO QUOC VIET (Thầy Việt dễ thương)

## Installation
```
git clone <https://github.com/Sherlockian1212/Document2Braille.git>
```

## Usage

### Install Tesseract-OCR

#### Ubuntu
```commandline
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
#### macOS
To install Tesseract run this command:
```commandline
sudo port install tesseract
```
To install Vietnamese language data, run:
```commandline
sudo port install tesseract-vie
```

#### Windows
Installer for Windows for Tesseract 3.05, Tesseract 4 and Tesseract 5 are available from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). These include the training tools. Both 32-bit and 64-bit installers are available.

An installer for the OLD version 3.02 is available for Windows from our [download](https://tesseract-ocr.github.io/tessdoc/Downloads.html) page. This includes the English training data. If you want to use another language, [download the appropriate training data](https://tesseract-ocr.github.io/tessdoc/Data-Files.html), unpack it using [7-zip](http://www.7-zip.org/), and copy the .traineddata file into the ‘tessdata’ directory, probably `C:\Program Files\Tesseract-OCR\tessdata`.

To access tesseract-OCR from any location you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, probably `C:\Program Files\Tesseract-OCR`.

Experts can also get binaries build with Visual Studio from the build artifacts of the [Appveyor Continuous Integration](https://ci.appveyor.com/project/zdenop/tesseract/history).

### Install the necessary packages

```
pip install -r requiments.txt
```

## Methods
### 1. Image Pre-Processing

![Edge Detection](resources/EdgeDetection/EdgeDetection.png)

![K-means](resources/K-means/K-means.png)

### 2. Text Extraction

![Tesseract-OCR](resources/Tesseract/Tesseract_OCR.png)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## References
[1] Ngo Quoc Viet (2017). Xử lý ảnh số. NXB ĐHSP Tp.HCM.

[2] Ngo Quoc Viet. Digital Image Processing lecture slides. (Bài giảng của thầy Việt dễ thương)

## License

[MIT](https://choosealicense.com/licenses/mit/)
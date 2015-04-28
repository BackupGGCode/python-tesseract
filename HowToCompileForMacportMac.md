obsolete now !! use homebrew version pls
[Compile for HomeBrew](https://code.google.com/p/python-tesseract/wiki/HowToCompilePythonTesseractForHomebrewMacMountainLion)

# How to compile python-tesseract (for Mac Mountain Lion ) #
```
launch xCode, then go to Preferences -> Downloads and install "Command Line Tools". 
Restart Terminal and you will be able to use Make.

1. Install MacPorts
wget https://distfiles.macports.org/MacPorts/MacPorts-2.1.2-10.8-MountainLion.pkg
sudo port install subversion wget axel cmake automake autoconf libtool swig swig-python

2. Install Leptonica
wget http://www.leptonica.com/source/leptonica-1.69.tar.gz
tar zxvf leptonica-1.69.tar.gz
cd leptonica-1.69
./configure --prefix=/opt/local
make
sudo make install


3. Install opencv
sudo port install opencv +python27

4. Install tesseract-ocr
svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/ tesseract-ocr
sudo port install gcc gcc-c++ make python27
cd tesseract-ocr/
sed -i '.bak'  's/^libtoolize/glibtoolize/g' autogen.sh
sed -i '.bak'  's|usr/local|opt/local|g' configure.ac
./autogen.sh
./configure --prefix=/opt/local
make
sudo make install

5.
wget http://python-tesseract.googlecode.com/files/python-tesseract.macosx-10.8-intel.tar.gz
sudo tar zxvf python-tesseract.macosx-10.8-intel.tar.gz -C /opt/local

or 
svn checkout http://python-tesseract.googlecode.com/svn/trunk/ python-tesseract
cd python-tesseract
sudo port install py27-coverage
python setup.py clean
python setup.py build
python setup.py install


```
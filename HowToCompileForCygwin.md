# How to compile python-tesseract from svn version of tesseract-ocr #
## For cygwin Only ##
### 1. Install cygwin by starting [setup.exe](http://cygwin.com/setup.exe) ###
### 2. then install subversion and wget ###
### 3. start cygwin-bash-shell ###
```
svn --force export http://apt-cyg.googlecode.com/svn/trunk/ /bin/
chmod +x /bin/apt-cyg
apt-cyg install nano make autobuild libtool libiconv gcc4 libtiff-devel libpng14-devel libgif-devel libSM-devel libjbig-devel
apt-cyg -m http://fd0.x0.to/cygwin install liblept-devel
apt-cyg -m ftp://ftp.cygwinports.org/pub/cygwinports/ install libwebp-devel libopencv-devel python-cv
apt-cyg -m ftp://ftp.jaist.ac.jp/pub/cygwin/ install patch libjasper-devel zlib-devel libbz2-devel 

*Optional*
wget http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.2/OpenCV-2.4.2.tar.bz2/download
tar jxvf OpenCV-2.4.2
cd OpenCV-2.4.2
wget http://python-tesseract.googlecode.com/files/opencv-2.4.2-cygwin-patch-20120807.txt
patch -p1 < opencv-2.4.2-cygwin-patch-20120807.txt
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_LEGACY_CYGWIN_WIN32=0 -D CMAKE_INSTALL_PREFIX=/usr -D BUILD_SHARED_LIBS=ON -D BUILD_PYTHON_SUPPORT=ON ..
make && make install 
```
### 4. Compile Tesseract ###
```
svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/ tesseract-ocr
cd tesseract-ocr
./autogen.sh --prefix=/usr
./configure --prefix=/usr
make clean && make -j 10 && make install 
```


### 5. Make python-tesseract ###
```
svn checkout http://python-tesseract.googlecode.com/svn/trunk python-tesseract
cd python-tesseract
apt-cyg install swig python libcurl-devel cmake
python setup.py build
python setup.py install
cd test-slim
export TESSDATA_PREFIX="./"
python test.py

```
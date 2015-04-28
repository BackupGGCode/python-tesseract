# How to compile python-tesseract (for Centos 6.3 ) #
```
yum groupinstall "Development Tools" -y
yum -y install wget cmake 
yum -y install libjpeg-devel libpng-devel libtiff-devel zlib-devel
yum -y install gcc gcc-c++ make numpy
wget http://www.leptonica.com/source/leptonica-1.71.tar.gz
tar zxvf leptonica-1.70.tar.gz
cd leptonica-1.70
./configure --prefix=/usr
make
make install

cd ..
wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.3/OpenCV-2.4.3.tar.bz2
tar jxvf OpenCV-2.4.3.tar.bz2
cd OpenCV-2.4.3
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr -D BUILD_PYTHON_SUPPORT=ON .
make
make install

cd ..
#svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/ tesseract-ocr
#wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz
#tar zxvf tesseract-ocr-3.02.02.tar.gzcd tesseract-ocr/
wget https://tesseract-ocr.googlecode.com/archive/3.03-rc1.tar.gz
tar zxvf tesseract-ocr-3.03-rc1.tar.gz
cd tesseract-ocr
/autogen.sh
./configure --prefix=/usr
make
make install
cp tessdata/eng* /usr/share/tessdata

cd ..
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py 
easy_install pip
yum install python-devel -y
svn checkout http://python-tesseract.googlecode.com/svn/trunk/ python-tesseract
cd python-tesseract
python setup.py build
python setup.py install
cd test-slim
rm *.pyc
rm *.pyd
python test.py
```


# How to compile python-tesseract (for Centos 6 ) #
```
cd ~
mkdir temp
cd temp
yum groupinstall "Development Tools" -y
yum install axel wget cmake -y 
yum -y install libjpeg-devel libpng-devel libtiff-devel zlib-devel
yum -y install gcc gcc-c++ make
wget http://www.leptonica.com/source/leptonica-1.69.tar.gz
tar zxvf leptonica-1.69.tar.gz
cd leptonica-1.69
./configure --prefix=/usr --libdir=lib64
make
sudo make install

cd ..
wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.2/OpenCV-2.4.2.tar.bz2
tar jxvf OpenCV-2.4.2.tar.bz2
wget http://python-tesseract.googlecode.com/files/opencv-2.4.0-fix-pkgconfig.patch
patch -p1 < opencv-2.4.0-fix-pkgconfig.patch
mkdir release
cd release
sed -i.bak 's|libdir=|libdir=/usr/lib64|g' unix-install/opencv.pc
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr  -D CMAKE_LIBRARY_PATH=/usr/lib64 -D BUILD_PYTHON_SUPPORT=ON ..
make
make install

cd ..
svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/ tesseract-ocr

cd tesseract-ocr/
./autogen.sh
./configure --prefix=/usr --with-libdir=lib64
make
make install

cd /usr/lib
cp -Rf *opencv* /usr/lib64
cp -Rf *tess* /usr/lib64
cp -Rf *lept* /usr/lib64

cd ~/temp
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py 
easy_install pip
yum install python-devel -y
svn checkout http://python-tesseract.googlecode.com/svn/trunk/ python-tesseract
cd python-tesseract
python setup.py build
python setup.py install
cd test-slim
rm *.pyc
rm *.pyd
python test.py


```
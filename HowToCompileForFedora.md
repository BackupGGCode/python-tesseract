# How to compile python-tesseract for Fedora #
## Install Basics ##
```
yum groupinstall "Development Tools" -y
yum install swig gcc-c++ leptonica rpm-build numpy opencv* -y
yum install python-devel tesseract-devel opencv-devel -y 

```

## Compile Python-Tesseract ##
```
cd ..
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py 
easy_install pip
yum install python-devel -y
svn checkout http://python-tesseract.googlecode.com/svn/trunk/ python-tesseract
cd python-tesseract
python setup.py clean
python setup.py build
python setup.py install --user
python setup.py bdist_rpm
cd test-slim
rm *.pyc
rm *.pyd
python test.py
```
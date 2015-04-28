[![](http://python-tesseract.googlecode.com/files/sf_coffee_small.jpg)](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)     [If you find python-tesseract useful, please consider ](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USKD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)**_[buying me a coffee.](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USKD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)_**
# How to compile python-tesseract (for Mac Mountain Lion/Maverick ) #
## 1. Install Command Line Tools ##
launch xCode, then go to Preferences -> Downloads and install "Command Line Tools".
Restart Terminal and you will be able to use Make.

## 2. Install misc ##
```
brew -v update && brew -v upgrade
brew rm opencv python    #optional
brew install python libpng freetype pkgconfig
brew install wget axel swig subversion
brew install leptonica tesseract  
brew install opencv
#brew tap homebrew/science                       #needed for the time being only (30 June 2013)
#brew install -vd --tbb opencv
#brew install homebrew/science/opencv    # enable above if this command line don't install opencv

```
## 3. install python libs ##
```
echo 'export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH' >> ~/.bash_profile
echo 'export PATH=/usr/local/share/python:/usr/local/bin:$PATH' >> ~/.bash_profile
export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH'
export PATH=/usr/local/share/python:/usr/local/bin:$PATH
easy_install pip
pip install numpy --upgrade
pip install scipy pandas cython patsy matplotlib #optional

```
### testing ###
```
>export PYTHONPATH="/usr/local/lib/python2.7/site-packages:$PYTHONPATH"
>which python
/usr/local/bin/python
>python
Python 2.7.3 (default, Mar  5 2013, 00:02:42) 
[GCC 4.2.1 Compatible Apple LLVM 4.2 (clang-425.0.24)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> quit()
```

4.
## uninstall python-tesseract ##
```
sudo rm -Rf /usr/local/lib/python2.7/site-packages/*tess* 
```
## Install python-tesseract ##
Either
```
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
#sudo easy_install https://bitbucket.org/3togo/python-tesseract/downloads/python-tesseract_0.8-3.0-py2.7_macosx-10.9-intel.egg
easy_install https://bitbucket.org/3togo/python-tesseract/downloads/python_tesseract-0.9.1-py2.7-macosx-10.10-x86_64.egg
#### for homebrew<--- no need to use "sudo"
```
or
```
svn checkout http://python-tesseract.googlecode.com/svn/trunk/src python-tesseract
cd python-tesseract
python setup.py clean
python setup.py build
python setup.py install
export PYTHONPATH="/usr/local/lib/python2.7/site-packages:$PYTHONPATH"
cd test-slim
python test.py
```


# How to compile python-tesseract (for Ubuntu Raring & Saucy & Trusty ) #
```
sudo apt-get install python-distutils-extra tesseract-ocr tesseract-ocr-eng libopencv-dev libtesseract-dev libleptonica-dev python-all-dev swig libcv-dev python-opencv python-numpy python-setuptools python3-all-dev  build-essential subversion python3-setuptools
svn checkout http://python-tesseract.googlecode.com/svn/trunk/src python-tesseract
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
python setup.py install --user
cd test-slim
export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
python test.py
==to make deb==
sudo apt-get install cdbs dh-buildinfo devscripts python-stdeb
dch -i
debuild binary
debuild -i -us -uc -b
debuild -ai386 -us -uc -b

==cross-compile i386==
sudo apt-get install pbuilder
sudo pbuilder --create --architecture i386
sudo pbuilder --login --save-after-login
sudo pbuilder --build python-tesseract_0.9-0.5ubuntu2.dsc
```

# How to compile python-tesseract (for Ubuntu Oneiric) #
```
sudo apt-get install tesseract-ocr-eng tesseract-ocr-dev libleptonica-dev python-all-dev swig libcv-dev
tar zxvf python-tesseract-xxxx.tar.gz
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
sudo python setup.py install

==to make deb==
sudo apt-get install cdbs dh-buildinfo
./buildDeb

```


# How to compile python-tesseract (for Ubuntu Natty) #
```
sudo add-apt-repository ppa:nutznboltz/tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr-dev leptonica python-all-dev swig
tar zxvf python-tesseract-xxxx.tar.gz
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
sudo python setup.py install

==to make deb==
sudo python setup.py --command-packages=stdeb.command sdist_dsc debianize bdist_deb 

```


# How to compile python-tesseract (for Mac OS X Lion) #

First, install tesseract svn as suggested by mcradle<br>
<a href='http://mousecradle.wordpress.com/2011/05/17/compiling-svn-tesseract-on-osx/'>http://mousecradle.wordpress.com/2011/05/17/compiling-svn-tesseract-on-osx/</a><br>
Then,<br>
<pre><code>sudo port select python python27<br>
sudo port uninstall opencv<br>
sudo port install py27-numpy<br>
sudo port install opencv +python27<br>
sudo port install leptonica swig swig-python <br>
export LDFLAGS="-L/opt/local/lib"<br>
tar zxvf python-tesseract-xxxx.tar.gz<br>
cd python-tesseract<br>
python config.py<br>
python setup.py clean<br>
python setup.py build<br>
sudo python setup.py install<br>
</code></pre>
<i>If you  ran into "Segmentation fault 11" then following the steps suggested by Solem</i><br>
<a href='http://www.janeriksolem.net/2011/12/installing-opencv-python-interface-on.html'>http://www.janeriksolem.net/2011/12/installing-opencv-python-interface-on.html</a>

<h1>How to compile python-tesseract from svn version of tesseract-ocr</h1>
<h2>For cygwin Only</h2>
<h3>1. Install cygwin by starting <a href='http://cygwin.com/setup.exe'>setup.exe</a></h3>
<h3>2. then install subversion and wget</h3>
<h3>3. start cygwin-bash-shell</h3>
<pre><code>svn --force export http://apt-cyg.googlecode.com/svn/trunk/src /bin/<br>
chmod +x /bin/apt-cyg<br>
apt-cyg install nano make autobuild libtool libiconv gcc4 libtiff-devel libpng14-devel libgif-devel libSM-devel libjbig-devel<br>
</code></pre>
<h2>For Natty</h2>
<pre><code>apt-get build-dep tesseract-ocr leptonica<br>
</code></pre>
<h2>For both  Natty and Cygwin</h2>
<h3>1. compile and link webp and leptonica</h3>
<pre><code>wget http://webp.googlecode.com/files/libwebp-0.1.3.tar.gz<br>
tar zxvf libwebp-0.1.3.tar.gz<br>
cd libwebp-0.1.3<br>
./autogen.sh<br>
./configure LDFLAGS="-no-undefined  -Wl,--as-needed" --prefix=/usr<br>
make clean &amp;&amp; make -j 4 &amp;&amp; make install<br>
cd ..<br>
<br>
wget http://leptonica.googlecode.com/files/leptonica-1.68.tar.gz<br>
tar zxvf leptonica-1.68.tar.gz<br>
cd leptonica-1.68<br>
./autobuild<br>
./configure LDFLAGS="-no-undefined  -Wl,--as-needed" --prefix=/usr<br>
make clean &amp;&amp; make -j 4 &amp;&amp; make install<br>
cd ..<br>
<br>
</code></pre>
<h3>2. compile and link tesseract-ocr</h3>
<pre><code>sudo apt-get install libtiff-dev libjpeg-dev libpng-dev subversion devscripts build-essential debhelper autoconf automake libtool libleptonica-dev<br>
</code></pre>
<b>Static Build(easy)<br>
<pre><code>svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/src tesseract-ocr-read-only<br>
cd tesseract-ocr-read-only<br>
./autogen.sh --prefix=/usr<br>
./configure --prefix=/usr --disable-shared<br>
make clean &amp;&amp; make -j 4 &amp;&amp; make install<br>
cd ..<br>
</code></pre></b>

<b>Shared Build(difficult)</b><br>
<i>Cygwin is buggy on producing shared library.</i>
<pre><code>svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/src tesseract-ocr-read-only<br>
cd tesseract-ocr-read-only<br>
#wget http://python-tesseract.googlecode.com/files/fix_ugly_cygwin_bug.diff<br>
#patch -p0 -i fix_ugly_cygwin_bug.diff<br>
./autogen.sh --prefix=/usr<br>
./configure LDFLAGS="-no-undefined  -Wl,--as-needed" --prefix=/usr<br>
make clean &amp;&amp; make "USING_MULTIPLELIBS=1" &amp;&amp; make install <br>
</code></pre>

<h3>3. Make python-tesseract</h3>
<pre><code>svn checkout http://python-tesseract.googlecode.com/svn/trunk/src python-tesseract<br>
cd python-tesseract<br>
#apt-cyg install swig python #for cygwin only<br>
#apt-get install swig python # for natty only<br>
python setup.py build<br>
python setup.py install<br>
</code></pre>
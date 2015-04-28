# How to install compiled python-tesseract (for Cygwin Windows 7) #
## 1. Install cygwin by starting [setup.exe](http://cygwin.com/setup.exe) ##
## 2. then install subversion and wget ##
## 3. start cygwin-bash-shell ##
## 4. copy and paste the following lines onto the cygwin shell ##
```
svn --force export http://apt-cyg.googlecode.com/svn/trunk/ /bin
chmod +x /bin/apt-cyg
apt-cyg install unzip python libgcc1 libtiff-devel libpng14-devel libgif-devel libSM-devel libjbig-devel
wget http://python-tesseract.googlecode.com/files/python-tesseract-0.6.cygwin-1.7.9-i686.zip
unzip python-tesseract-0.6.cygwin-1.7.9-i686.zip -d/
```
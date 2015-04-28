# How to install deb version of Python-tesseract in Ubuntu(Precise) #
```
wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.4_amd64.deb
wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.4_i386.deb
sudo apt-get install tesseract-ocr
sudo dpkg -i python-tesseract*.deb
sudo apt-get -f install
```



# How to install deb version of Python-tesseract in Ubuntu(Oneiric) #
```
wget http://python-tesseract.googlecode.com/files/tesseract-ocr_3.01-2ubuntu1_amd64.deb
wget http://python-tesseract.googlecode.com/files/tesseract-ocr-eng_3.01-1ubuntu1_all.deb
wget http://python-tesseract.googlecode.com/files/tesseract-ocr-osd_3.01-2ubuntu1_all.deb
sudo dpkg -i tesseract-ocr*.deb
wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.1_amd64.deb
sudo dpkg -i python-tesseract*.deb

```

# Manually uninstall non-deb version of python-tesseract #
Deb version install python-tesseract in pyshared rather than
dist-packages!!!
```
sudo rm /usr/local/lib/python2.7/dist-packages/python_tesseract* 
sudo rm /usr/local/lib/python2.7/dist-packages/tesseract* 
```

# How to install deb version of Python-tesseract in Ubuntu(Natty) #
```
sudo add-apt-repository ppa:nutznboltz/tesseract
sudo apt-get update
sudo apt-get install leptonica
wget http://python-tesseract.googlecode.com/files/tesseract-ocr_3.0.1%2Bsvn625-1~ppa2~natty1_amd64.deb
sudo dpkg -i tesseract-ocr*.deb
wget http://python-tesseract.googlecode.com/files/tesseract-ocr-eng_3.0.1%2Bsvn625-1~ppa2~natty1_all.deb
sudo dpkg -i tesseract-ocr-eng*.deb
sudo apt-get install tesseract-ocr-dev
wget http://python-tesseract.googlecode.com/files/python-tesseract_0.6-1.1_amd64.deb
sudo dpkg -i python-tesseract*.deb

```
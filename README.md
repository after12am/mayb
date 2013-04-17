Mayb
====

Mayb is image recommendation system of [pinterest](http://pinterest.com/). This recommendation system consists of two main core of
scraping and clustering. The first part is to extract feature of words and images from web page. The second part
has responsibility for classification of images by scoring their features using pearson's correlation. 
Classification is implemented by calculating the similarity of words related to image, not implemented by analysing 
image itself. Because of this, this algorism of classification realizes a good performance while being low cost. 
  
<img src="https://raw.github.com/after12am/Mayb/master/doc/Mayb.png"/>

## Requires

Maby is depend on these libraries. You have to install those with easy_install.

* lxml 2.3.5
* chardet

```
sudo easy_install "lxml==2.3.5"
sudo easy_install chardet
```

## Usage

In the beginning of recommending images, we have to setup database.

```
cd /path/to/src
python mayb.py setup
```

option to crawle pinterest is:

```
cd /path/to/src
python mayb.py crawle
```

option to cluster pins we got is:

```
cd /path/to/src
python mayb.py train
```

In the end, run the following command in your new terminal and visit at `http://localhost:8000/`. 
The images which is displayed on are ones that Mayb could recommend to you. If you click any image, 
Mayb would shows you similar images which has strong relationship with that you select.

```
cd /path/to/www;
python -m CGIHTTPServer
```

## Notes

* run `python mayb.py crawle` before run `python mayb.py train`.

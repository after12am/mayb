Mayb
====

Mayb is context-aware image recommendation system specified on the [pinterest](http://pinterest.com/). This recommendation system proposes related images in addition to similar images on the basis of repins of pinterest users and is implemented by using context of image, not by analysing image itself.


**Crawler is not working correctly now, because the specification of pinterest has changed. Fortunately, I seem to be able to support it by improving crawler. Thanks. See you later.**


<img src="https://raw.github.com/after12am/Mayb/master/doc/Mayb.png"/>


## strategy

There is variation in the way of users's classification of images. It is pinned to the different board even in the same image. This feature can be used to find related images using pearson's correlation. 


## Require

Maby is depend on these libraries. You have to install those with easy_install.

* lxml 2.3.5
* chardet

```
$ sudo easy_install "lxml==2.3.5"
$ sudo easy_install chardet
```

## Usage

In the beginning of recommending images, we have to setup database.

```
$ cd /path/to/src
$ python mayb.py setup
```

option to crawle pinterest is:

```
$ cd /path/to/src
$ python mayb.py crawle
```

option to cluster pins we got is:

```
$ cd /path/to/src
$ python mayb.py train
```

In the end, run the following command in your new terminal and visit at `http://localhost:8000/`. 
The images which is displayed on are ones that Mayb could recommend to you. If you click any image, 
Mayb would shows you similar images which has strong relationship with that you select.

```
$ cd /path/to/www;
$ python -m CGIHTTPServer
```

## Notes

* run `python mayb.py crawle` before run `python mayb.py train`.

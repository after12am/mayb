Mayb
====

Mayb is image recommendation system. This recommendation system consists of two main core of scraping and clustering. 
Scraping part is to extract appropriate content, such as words and images, as fetures from html. 
This part is important, because similarity of each pins dependents on their fetures. We have to find what characterize it. 
Clustering part has responsibility for classification of images by scoring their features. 
I think you would get expected results. Have a good time!

## In the beginning

Since I prepared the test data, Let's play with it. Run the following command in your new terminal and visit at `http://localhost:8000/`. 
The images which is displayed on are ones that Mayb could recommend to you. If you click any image, 
Mayb would shows you similar images which has strong relationship with that you select.

```
cd /path/to/www;
python -m CGIHTTPServer
```
　
　
<img src="https://raw.github.com/after12am/Mayb/master/doc/Mayb.png"/>

## Usage

As a starting place of recommending images, we have to setup database.

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

## Notes

* run `python mayb.py crawle` before run `python mayb.py train`.
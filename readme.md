# Selenium proxy server changer

## Description

Selenium proxy server changer is a python project that can find proxy servers from the website [https://hidemy.name/en/proxy-list/](https://hidemy.name/en/proxy-list/) and then use them. This project came to life from an idea of browsing the web more anonymously whilst paying no money to do so. 

The program itself is split into two main parts. One of them being getting new proxies to use and saving them to a file. The second part being choosing a random proxy from the file and seeing if it connects and works well. Proxies are chosen from the website based on the HTTPS type and speed limit of 1000ms. The proxies that do not work will be removed from the file upon encountering one.

Due to the online proxy-list being free you can expect that not all proxies are fit to use and sometimes you might encounter a scenario where there aren't any suitable proxies. Although that has seemed to be a very rare case because of the speed limit that has been set high enough.

The chromedriver with the new proxy server will be redirected to the website [https://whatismyipaddress.com/](https://whatismyipaddress.com/) to confirm the IP change and the driver will run until the input is given to the command line.

**This project is not in active development and was made for personal use rather than public, so it may get outdated.**

## How to run

To run the program you need to have python 3 and the dependencies mentioned below.

Python 3 can be installed from [here](https://www.python.org/downloads/).

The program can be run by using the command
```
python proxy.py
```

## Dependencies

This project relies on two modules - selenium and undetected_chromedriver.
This might raise the question why use another chromedriver if selenium has one already, but undetected_chromedriver helps to bypass the cloudfare check when loading the [https://hidemy.name/](https://hidemy.name/) website. The basic selenium chromedriver got stuck on the cloudfare loading screen.

Commands to install the dependencies
```
pip install undetected-chromedriver
pip install selenium
```

## Author

Andreas Randmäe
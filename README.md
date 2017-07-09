Task
====

In this assignment you are asked to create a simple API Proxy in Python that combines and caches multiple calls to the C42 API into one single call with a lightweight response. These kind of API Proxies are useful when creating a mobile application (in order to send as little data as possible over the wire) or when combining multiple different API's into one.

In this assignment you're asked to create a GET endpoint /events-with-subscriptions/ that combines two separate calls towards the C42 API into one response that contains the event title and the first names of its attendees.


Solution
========

Let's use python3, aiohttp, asyncio to fire requests to API in async mode
 and utilize modern technologies. We also could use Django Channels or just Django.

Things to keep in mind:
- end API can be down or could return data with non-expected structure
- we should cache only successful responses
- let's use redis or memcache for caching

P.S. In Django view caching is ready out of the box, with aiohttp
we need to use something like aiohttp-cache.


Live demo
=========

https://still-coast-28329.herokuapp.com/event-with-subscriptions/9d3b488d6d8dfef63f0c5d986bf86429_14901767281894


Installation
============

prerequisites
-------------
- python 3.6

Installation process
--------------------
```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
Run dev server
--------------
```
export CALENDAR42_TOKEN=<value>
python app.py
# Go to http://127.0.0.1:8080/event-with-subscriptions/9d3b488d6d8dfef63f0c5d986bf86429_14901767281894
```

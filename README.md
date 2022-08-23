# URLShortener
This project will create a short url to use for the given original URL.

## How to Run: 
Option 1: Site is hosted on python anywhere:
	- http://keerthana25.pythonanywhere.com/

Option 2: Download and Run Code

  - python3 init_db
  - flask run //this common will provide a url to access
  

#### Credentials
- username: user
- password: userPassword


## The future work for this project would be: 
- Improve Security - temporarily I have login/password but that needs to be improved. AllUrls page should only be seen with special permission
- Way to create users and roles
- More error handling (database issues etc) and more logs
- Mechanism for the short urls to expire and/or user have ability to remove urls they created 
- Add more analytics/metrics as needed
- Upload log files to Splunk (or other similar areas) so when an issue arises it can be easily debugged. 
- Change hosting of the site to internal company server


## Additional Maintenance: 
- Some sort of caching mechanism to prevent load on database if it gets too big
- Depending on load, shard database.
- Change technique on getting random short URLs ( maybe some sort of encoding/decoding). Right now it’s a 4 word random generator which creates ~450k words. But if we need more that we need a different mechanism
- Add load balancers as currently there is a single point of failure
- Testing - Currently I have functional test cases but more are needed. 
    - Create regression testing
    - Load Testing -  (First get information on how many users will be using it and how many links they will be creating)
- Clean up UI code

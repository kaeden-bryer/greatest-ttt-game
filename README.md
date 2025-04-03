# Tic Tac Terminator🤖
CSI2470 Networks Project

By Devin, Peter and Kaeden
Group 3 -- Game Server

### Description
A real-time 2 player tic tac toe game that runs in the terminal. The two players are connected over a TCP connection to an AWS EC2 instance through socket programming. In addition, users are able to track their wins/losses and view a leaderboard through a SQL database in the server. 

### How to Compile and Run the Application 
If you have GitHub CLI and Git, clone this repo by running "gh repo clone kaeden-bryer/greatest-ttt-game". If you don't want to clone the entire repo, download the below required files: 

**testuser.py** -- Execute this file by running "python3 testuser.py" in the terminal in a directory with this file to run the game. This file contains all the code necessary to run the program and send game information over sockets.

**serverFile.py** -- This is the file run by the Ubuntu server. Handles client requests and processes information.

**peterr.py** -- This file (courtesy of Peter) contains all the logic behind the user sign-in and database operations.

With these files downloaded, open your terminal and switch into the directory containing these files. Run the command "python3 testuser.py".

Enjoy the game!🎉


#### Troubeshooting
If this program isn't running, try the following:

1. Make sure the "ip" variable in "testuser.py" is set to IP address of the server. Unfortunately, a static IP address in AWS costs money, so this could change. However, currently it should be "44.201.187.226"
2. Make sure the "port" variable in "testuser.py" is set to "2470". This is the port the server instance is listening on.

If the above aren't working, the AWS server might be down and not listening. Please contact kaedenbryer@oakland.edu if a connection cannot be established after trying the above.

### Technical Requirements

**1. Programming Language:** 
Python and SQLite. Server runs on Ubuntu Server

**2.Networking Protocol:**
TCP

**3. Features:**
Client Process:
1. Connect to the server using IP address "44.201.187.226" and port 2470
2. Send user and game data to the server
3. Receive updated game status and leaderboard from server

Server Process:
1. Listen on port 2470
2. Accept multiple client connections (for TCP).
3. Process the client's request and respond.

**4. Concurrency (TCP):**
The server is able to handle two clients at once, allowing them to play each other.

*Devon can you talk more about this here, and whether it's possible to have more than 2 users?*

**5. Error Handling:**
Implement basic error handling for situations like lost connections,
invalid inputs, or server overloads.

*Devon can you talk about error handling here*

**6. Security:**
Implement at least one security feature. Examples include:
o Input validation.
o Basic authentication.

Both of these features are implemented in some regard. *Input validation* is incorporated when the user inputs a square they would like to populate. If the number is less than 1 or greater than 9, the user is prompted again in a while loop. *Basic authentication* is incorporated when the user first enters the game. In order to play, the user must first login or register. New users are added to a SQL database in the server, and logins are checked relationally. In addition, passwords are *hashed* using SHA-256 to protect users in the event of a data breach.

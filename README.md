# CS341 Scraping
put the cs341 assignments and lectures into google calendar (Why does every course use a diff site?????)

Authorize google calendar api:
- Go to https://developers.google.com/calendar/quickstart/python, follow their Step 1 and 2
- When you run the python file it might say "Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={???}&redirect_uri={???}&scope={???}&state={???}&access_type=offline", open a browser window with an error message like "The redirect uri, localhost + some long number, is not authorized"
- Go to https://console.developers.google.com/apis/credentials, select the project you created in the top left drop down, edit the Oauth 2.0 client id to add that localhost url, like http://localhost:12345/, into "Authorized redirect URIs"
- Paste the link from the terminal in browser and accept the permissions
- CtrlC the terminal and run python file again it should scrape https://student.cs.uwaterloo.ca/~cs341/ 

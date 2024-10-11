Hola Visitors,
=


Hope you are all doing well. Wishing you a good health!

Let me walk you through the assignment!!

## _**Brief :**_

- I have created a main "**app.py**" file which fetches the manhwa contents from the Azure SQL Database and displays in the website.
- Flask is utilized to host the web application.
- Requirements.txt file contains the packages required to run the app.py.
- The Images of the Manhwas are fetched from the Azure Blob Storage.
- The Insert-Data-To-DB.py file is used to insert the JSON content to the Database.
- The Fetch-Data-From-DB is used to fetch the data from the DB using a SELECT statement.
- The Upload-Images-To-Blob.py is used to upload the static assets [Images] to the Blob Storage.
- Index.html is the website.
- The .env will not be in this repo because it contains the important credentials.
- The Procfile is used to define the startup commands for custom applications. It tells Azure which process to run to start the app, such as launching a web server.
- GitHub Actions has been creates by the Azure Web Apps for CI and CD.

## **Note:**

- I've only created the Architecture for the thing I've done in this time duration.
- I'll write down the things that must be added to make it Scalable and Highly Available.

## Architecture:

![Manhwa (2)](https://github.com/user-attachments/assets/91b9efe8-5374-406d-866b-849a0fee37b3)

## Scaling:

- As of now to get a less amount of cost, I've used B1 basic in App Service Plan.
- We can auto-scale by two types: Rules-Based, Automatic.
- We can auto scale based on CPU Percentage, Memory Percentage and HTTP Queue Length.
- We can set the scale of CPU Percentage to 70-80% and Memory Percentage to 75-85%. We need to analyse the number of requests to our website and then decide the HTTP Queue Length.
- Scale out if the metrics is above the percentage and scale in if the metrics are below 45%.
- Also setup Cooldown periods to avoid scaling too often in a less period of time.

## Availability:

- Have two regions, one is the Active one which contains the App Service and Database. This is the main region.
- Next is the Standby region, also known as secondary region. Here you will have the same application and the Database is Geo-Replicated.
- If the First region shuts down, the workloads goes to the second region by using Azure FrontDoor.
- Also Azure FrontDoor offers CDN so the contents of the Web App will be cached to the edge location nearby to the user. This reduces the latency.
- Can use a Cache layer for the DB to reduce the Load of retrieving data from the DB.

## Security:

- Firstly Security must be implemented as soon as we start building an application and it must not be a second thought.
- The DB can be accessed only by the Azure Services and through your IP. [You have to upload your IP each and every time to test the App Locally]
- The Storage Account is in Private and doesn't allow anonymous access.
- The Azure FrontDoor has WAF which prevents the web app from DDOS.
- The Web App has a separate domain with HTTPS enabled by default so it ensures secure communication over the internet. No need to add SSL Certificates.
- The credentials are in a .env file which is gitignored by GitHub. Hardcoding credentials is a bad practice.

Result:

https://manhwa-world.azurewebsites.net

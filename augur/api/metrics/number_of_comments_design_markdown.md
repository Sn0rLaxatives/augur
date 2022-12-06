The API endpoint number of comment-lines will use the Augur database to provide the number of lines that are comments in a project in a json format.
Steps for the development of this endpoint:
1. Study the existing endpoint structure in Augur.
2. Create a template for the new endpoint in a new file
3. Write SQL query that extracts the number of lines that are comments in a given repository from the augur database
4. Combine the SQL query with the Python API code
5. Test the new endpoint with a fake database and see if the returned data is correct
6. Push the endpoint to the new main Augur branch

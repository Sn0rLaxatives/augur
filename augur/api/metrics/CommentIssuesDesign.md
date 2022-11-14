The comment issues endpoint is used to pull data from the Augur Database surrounding issues with comments and present it in json format to be eventually turned into a displayable metric for users to analyze.
The development for this endpoint is as follows:
  1. Study the existing endpoint structure in Augur
  2. Create a template for the new endpoint in a new file
  3. Write code to extract comments with issues from the database
  4. Test the newly written code with a fake database to see if the extracted data is equal to the data in the database
  5. Push the new endpoint to the main Augur branch

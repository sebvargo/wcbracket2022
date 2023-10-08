Heroku Dyno Command:  
web flask db upgrade; gunicorn quiniela:app --preload --workers=3 --threads=8 --worker-class=gthread 

# Known Errors
## 1st Round Errors

### Error 1
- Description: In cases were teams in a group tie in Points, Goal difference and goals scored, the tie breaker is alphabetical. 
- Solution: Long term solution is to program other tie breaker criteria. Short term solution was to adjust ties directly in the database to match what users saw in the prediction Excel file. 

## 2nd Round Errors

There were two types of errors when saving the user's 2nd round picks. These picks were submitted via the 'round2' route and the UI was controlled by round2.js.
There is no clear pattern for when the errors occur, but I suspect it is related to inconsistent JavaScript behaviour.
Javascript for this view is controlled by *round2.js*.


### Error 1
 - Description: Prediction.winner not recorded property in cases were Prediction.goals1 > Prediction.goals2, or viceversa
 - Solution: Loop through all prediction check that winner matches team with most goals.
 - Notes: Instances of these error are captured on *'2nd round error.csv'*
### Error 2
- Description: Prediction.winner not in Prediction.team1/2 of a child game. For example: 
  - Quarterfinals NED 1-1 ARG | **Prediction.winner = ARG**, leads to  Semifinal **Prediction.team1 = NED** - BRA
  - Solution: Get each Prediction where Prediction.goals1 == Prediction.goals2, and its corresponding child game. If Prediction.winner not in [ChildPrediction.team1, ChildPrediction.team2] then you switch the Prediction winner to the other team.  

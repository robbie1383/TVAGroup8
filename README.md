# Welcome to the TVA software of Group 8! 
The application is made to be as user friendly as possible, but it still requires a specific type of input. \
In this case, we decided to work with .csv files in order to use the pandas DataFrame class. We have already added some example elections that you can use to test the software,
but in case you would like to use your own, please follow the following template for the files:
```
Voter 1,Voter 2,Voter 3,Voter 4
A,B,C,D
B,A,D,C
D,C,A,B
C,D,B,A
```
This will result in the following pandas DataFrame:
```
  Voter 1  Voter 2  Voter 3  Voter 4
0       A        B        C        D
1       B        A        D        C
2       D        C        A        B
3       C        D        B        A
```
Please make sure that:
- there is no space between the ```,``` and the values;
- the columns are specified as ```Voter n```;
- the candidates are capital letters, alphabetically starting from A.
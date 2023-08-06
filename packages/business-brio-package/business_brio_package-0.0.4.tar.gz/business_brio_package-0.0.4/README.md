# business_brio
**business_brio** (pronounced “Business Brio”) is an open-source python package which contains sub-module named 'performance_rank_discrete'
This submodule has one class named 'test' and this has one method named 'result'.

This sub-module of the package(business_brio) will help you to get interpretation of several associates' performance (good or bad) 
on basis of two groups.

## How the dataset should be?

It is applicable for many uscases.
Lets say a dataset has three columns:

 1.Salesman id (having more than one level e.g. 36, PQ23, N2Z4, etc.).
 
 2.Saleflag i.e. 0 and 1 where 0 refers unsold and 1 refers sold (this may be 0 for unfulfiled cases and 1 for fulfiled cases).
 
 3.Type of market (only two levels i.e. two types of market e.g. urban, rural ).


## How to install our package?

```
pip install business_brio
```

## how to import and see the desired output?
```
from business_brio import performance_rank_discrete
obj=performance_rank_discrete.test(arg1, arg2, arg3, arg4)
table,intpret=obj.result(n=20)
print(intpret)
print(table)
```
## Arguments of the method chitest_rs.ChiTest2(arg1, arg2, arg3, arg4):

**It takes four inputs:**

**arg1. a dataframe with minimum three columns for input**

**arg2. Associate categorical column name (more than one level)**

**arg3. Output categorical column name (should have two levels 0 and 1. Where 0 refers unfulfiled and 1 refers fulfiled)**

**arg4. Group column name (should have two levels i.e. two group names)**

the column names (arg2, arg3, arg4) must be passed as string (inside double inverted commas)

**It returns two objects:**

**return1: table**

**return2: interpretation**

both outputs are dictionary type.

the table dictionary will have four sub-groups 
1.Good performers in group1 of arg4
2.Bad performers in group1 of arg4
3.Good performers in group2 of arg4
4.Bad performers in group2 of arg4

Each of these will have columns like, 
-individual associate
-actual unfulfiled of that associate
-actual fulfiled of that associate
-expected fulfiled of that associate
-chi value of each associate on basis of actual and expected fulfiled
-fulfiled percentage ((actual fulfiled/(actual fulfiled+actual unfulfiled))*100)



when you are calling the result method from the object you created then you have one optional argument to pass in this method which will decide the percentage of Top and Bottom associates in each group. 
**(by default this percentage is set to 30% )**.

For example:
```
from business_brio import performance_rank_discrete
obj=performance_rank_discrete.test(df,"salesman","saleflag","market")
table,intpret=obj.result(n=20)
print("Interpreted result:")
print(intpret)
print("table result:")
print(table)
```
In this above code you will get interpretation of the salesman performance like 

Associates good in both urban and rural

Associates bad in both urban and rural

Top 20% Associates in urban

Bottom 20% Associates in urban.

Top 20% Associates in rural

Bottom 20% Associates in rural.

N.B: 1.'urban' and 'rural' are the two levels of arg4
     2. 'df' is the name of the dataframe having columns "salesman", "saleflag", "market".

   
## Errors:
 
 If you are getting error messages. Please check the following:
 Whether the arg1 passed is dataframe with no null or not
 Whether the arg2 is name of the salesman column which has more than one levels ( multiple unique names or entries ).
 Whether the arg3 is name of the saleflag column which has only two levels ( only two unique name or entries 0 refers unsold and 1 refers sold).
 Whether the arg4 is name of the group column which has only two levels ( only two unique names or entries ).



Useful links and licenses:

**You can find the example datasheet from this link**:https://github.com/bhargabganguli/business_brio/blob/main/Test_Data.csv

**You can see the output from this link (output is shown in text file)**: https://github.com/bhargabganguli/business_brio/blob/main/test_result.txt
 
You can also see the tested python file : https://github.com/bhargabganguli/business_brio/blob/main/test_code.py

Source code:https://github.com/bhargabganguli/business_brio.git

Bug reports: https://github.com/bhargabganguli/business_brio/issues


License
Â© 2022 Bhargab Ganguli

This repository is licensed under the MIT license. 
See at   https://github.com/bhargabganguli/business_brio/blob/main/README.md   for details.


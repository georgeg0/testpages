#!/usr/bin/env python
# coding: utf-8

# # Lecture 2: SQL - Class 2
# Gittu George, February 24 2022

# ## Today's Agenda
# 
# - Refresher (Warm-up)
# - Refresher exercise
# - Learning objectives
# - More SQL commands (lap 1)
# - Aggregations (lap 2)
# - Grouping (lap 2)
# - Joins (lap 3)
# - Summary (finish line)
# 
# ## Warm-up ☕️
# ### Refresher!! Take some time and think if you know...
# 
# - What are databases?
# - Where is it commonly used?
# - How to set up a database?
# - General structure of a database
# - Various ways of interacting with the database, using
#     - command-line interface
#     - ODBC drivers via developer interfaces like pgadmin and toad.
#     - jupyter notebook ( which we will be using throughout the course)
# - To create a table and various data types 
# - Integrity constraints such as primary key and foreign key
# - Basic SQL commands like SELECT, FROM, and WHERE
# 
# In this class, we will be using the tables that we created in lecture 1. Here are the scripts if you want to recreate the classroom exercise table.
# 
# ```{toggle}
# 
# ```sql
# DROP TABLE IF EXISTS students,courses;
# 
# CREATE TABLE IF NOT EXISTS students(
# student_no integer PRIMARY KEY, 
# stud_name text,
# age integer,
# major text);
# 
# CREATE TABLE IF NOT EXISTS courses(
# id SERIAL PRIMARY KEY,
# student_no integer, 
# course_name text,
# course_year integer,
# course_percentage float);
# 
# INSERT INTO students(student_no,stud_name,age,major) VALUES (111,'Catherine',23,'MBAN'),
# (222,'Tiff',28,'MDS'),
# (333,'John',23,'MBAN'),
# (444,'Amir',28,'MBAN'),
# (555,'Gittu',20,'MDS'),
# (666,'Isha',30,'MBAN'),
# (777,'Heidy',30,'MBAN'),
# (888,'Angela',27,'MBAN'),
# (999,'Jason',30,'MBAN');
# 
# INSERT INTO courses(student_no,course_name,course_year,course_percentage) VALUES (111,'TPCS INFO TECH',2019,88),
# (111,'Data Visualization',2019,88),
# (222,'Health and Technology',2020,80),
# (222,'Web and Cloud Computing',2019,91),
# (222,'Spark Programming',2019,90),
# (333,'Parallel Computing',2019,90),
# (444,'Large Scale Infrastructures',2019,83),
# (444,'TPCS INFO TECH',2019,98),
# (555,'TPCS INFO TECH',2020,78),
# (555,'Health and Technology',2020,81),
# (666,'Data Visualization',2021,85),
# (666,'Parallel Computing',2019,87),
# (888,'Spark Programming',2019,93),
# (999,'TPCS INFO TECH',2019,98),
# (999,'Data Visualization',2019,87),
# (1000,'C programming',2019,87),
# (1111,'Introduction to Genomics',2019,87);
# ```

# First of all let's load SQL to work on this notebook.

# In[1]:


import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS')


# In[2]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[3]:


get_ipython().run_line_magic('sql', 'postgresql://{user}:{password}@{host}:5432/postgres')


# ### Refresher exercise 
# 
# ***Question 1:*** In this table `eg`
# 
# | firstname | countryfrom | continent     | gender | age |
# |-----------|-------------|---------------|--------|-----|
# | matt      | usa         | north america | M      | 23  |
# | jenn      | uk          | europe        | F      | 35  |
# | guy       | france      | europe        | M      | 25  |
# | james     | china       | asia          | M      | 29  |
# | lida      | india       | asia          | F      | 56  |
# | linda     | canada      | north america | F      | 18  |
# | sofia     | germany     | europe        | F      | 22  |
# | george    | india       | asia          | M      | 29  |
# 
# What will be returned from following SQL 
# ```sql
# select firstname,gender from eg where continent ='asia' AND age =29
# ```
# A) george,M
# 
# B) george,M,asia,29
# 
# C) george,india,asia, M,29 
# 
# D) M,george
# 
# E) M,james
# 
# ```{toggle}
# 
# ***Answer: D***
# 
# ```{important}
# Remember the order of the columns returned will be based on the order of columns that we specify within the select statement.
# ```

# ***Question 2:*** Consider a scenario where you want to perform analysis on a table (peopletable) with 100 columns (including personname,age,gender,origin...etc.) that define a person. You are interested in seeing the name of individuals older than 90. Which SQL query is more appropriate in this situation?
# 
# A) ***select * from peopletable where age > 90;***
# 
# B) ***select personname,age from peopletable where age > 90;***
# 
# B) ***select personname,age,gender,origin from peopletable where age < 90;***
# 
# D) ***select personname from peopletable where age > 90;***
# 
# ```{toggle}
# 
# ***Answer:  D***
# 
# ```{important}
# Just bring the columns and rows that are needed. Even though `SELECT` and `WHERE` are very basic SQL commands, it's crucial when you are dealing with a large table
# ```

# ## Learning objectives
# - You will be able to create SQL queries using (Lap 1 & Lap 2)
#     - Distinct, 
#     - ORDER BY, 
#     - LIMIT, 
#     - GROUP BY, 
#     - alias AS
# - You will learn about different kinds of joins and be able to create SQL queries that perform `JOINS`. (Lap 3)

# ## Lap 1 🥛
# ### DISTINCT
# 
# The DISTINCT statement is used only to return distinct elements from a table.
# 
# ***Syntax:***
# 
# ```sql
# SELECT DISTINCT column1, column2, ...columnN
# FROM tablename;
# ```
# 
# `DISTINCT` is applied to all columns that follows the `DISTINCT` keyword. Say for eg if we give `DISTINCT column1, column2` then the combination of values in both `column1` and `column2` columns will be used for returning the unique combination (or removing the duplicate elements).

# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT course_name FROM courses;')


# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT course_name, course_year FROM courses;')


# ### ORDER BY
# 
# `ORDER BY` statement sorts the results returned by `SELECT` based on a sort expression.
# 
# Syntax
# ```sql
# SELECT column1, column2 ...columnN
# FROM table_name
# ORDER BY column1 [ASC | DESC], column2 [ASC | DESC] ....columnN [ASC|DESC];
# ```
# 
# ```{note}
# By default, it will sort in ASC. So you can choose not to give ASC.
# ```

# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT * \nFROM courses\nORDER BY course_year;')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT * \nFROM courses\nORDER BY course_year DESC;')


# ### LIMIT
# 
# Until now, we were returning everything that our SQL query returns. `LIMIT` statement is used to limit the number of rows that are returned. 
# 
# syntax:
# 
# ```sql
# SELECT column1, column2, ...columnN
# FROM tablename
# LIMIT numberofrows;
# ```

# In[8]:


get_ipython().run_cell_magic('sql', '', 'SELECT * \nFROM courses\nLIMIT 2;')


# `LIMIT` keyword is used in a variety of situations. Here are a few cases
# 
# - ***Memory Management:*** Say you just want to look at the output your query returns. If you are dealing with lots and lots of rows, returning the entire rows can slow down the query, cause memory issues, and finally crash your jupyter. In these cases, you can use `LIMIT`. 
# 
# - ***Interest in the first few rows:*** If we are interested in just the first N rows, we can achieve that using `LIMIT`. People tend to use `LIMIT` a lot when they want to return the top 10 rows after performing an `ORDER BY`

# Let's apply all the statements that we learned in one statement.
# 
# ***Question:*** List out the row that got the highest `course_percentage` for the `Data Visualization` course.

# In[9]:


get_ipython().run_cell_magic('sql', '', "SELECT * \nFROM courses\nWHERE  course_name = 'Data Visualization'\nORDER BY course_percentage DESC\nLIMIT 1;")


# In[10]:


get_ipython().run_line_magic('sql', 'select age from eg order by age')


# ### Checkpoint 1 !! Take some time and think if you can...
# 
# - Select columns and bring in rows just what we need (using `SELECT` & `WHERE`)
# - Return `DISTINCT` elements
# - `ORDER BY` rows returned based on column(s)
# - `LIMIT` the number of rows returned
# 
# Now we will learn some more advanced SQL operations to gain more insight into the data. But, before that, let's do some exercise. 

# ### Check point 1 exercise.
# 
# #### iclicker questions
# 
# Answer the following questions using the table `eg`
# 
# | firstname | countryfrom | continent     | gender | age |
# |-----------|-------------|---------------|--------|-----|
# | matt      | usa         | north america | M      | 23  |
# | jenn      | uk          | europe        | F      | 35  |
# | guy       | france      | europe        | M      | 25  |
# | james     | china       | asia          | M      | 29  |
# | lida      | india       | asia          | F      | 56  |
# | linda     | canada      | north america | F      | 18  |
# | sofia     | germany     | europe        | F      | 22  |
# | george    | india       | asia          | M      | 29  |
# 
# 
# ***Question 1:*** How many elements will be returned from this SQL 
# 
# ```sql
# select DISTINCT gender,firstname from eg
# ```
# 
# A) 2
# 
# B) 8
# 
# C) 4 
# 
# ```{toggle}
# ***Answer: B***
# ```
# ***Question 2:*** What will be the first value returned from this SQL 
# 
# ```sql
# select age from eg order by age
# ```
# A) 23
# 
# B) 18
# 
# C) 56
# 
# D) 35
# 
# ```{toggle}
# ***Answer: B***
# ```
# 
# #### Reasoning Question
# 
# ***Question 1:*** Write a SQL query to list the row that got the highest `course_percentage` for the `TPCS INFO TECH'` course. Can you spot any issues by examining the original table?
# 
# ```{toggle}
# 
# You probably might have got this SQL query by changing the SQL query that we discussed for the "Data Visualization" course. 
# 
# ***SELECT * FROM courses
# WHERE  course_name = 'TPCS INFO TECH'
# ORDER BY course_percentage DESC
# LIMIT 1;***
# 
# This gives you 
# 
# | id | student_no |    course_name | course_year | course_percentage |
# |---:|-----------:|---------------:|------------:|------------------:|
# |  8 |        444 | TPCS INFO TECH |        2019 |              98.0 |
# 
# What are possible issues? Take out the `LIMIT`, and you might notice there is a tie, and 2 students, 444 and 999 scored the highest.
# 
# 
# ***SELECT * FROM courses
# WHERE  course_name = 'TPCS INFO TECH'
# ORDER BY course_percentage DESC***
# 
# 
# | id | student_no |    course_name | course_year | course_percentage |
# |---:|-----------:|---------------:|------------:|------------------:|
# |  8 |        444 | TPCS INFO TECH |        2019 |              98.0 |
# | 14 |        999 | TPCS INFO TECH |        2019 |              98.0 |
# |  1 |        111 | TPCS INFO TECH |        2019 |              88.0 |
# |  9 |        555 | TPCS INFO TECH |        2020 |              78.0 |
# 
# So even though many of them use a combination of `ORDER BY` and `LIMIT` for these scenarios we might run into situations like this. There are a couple of ways to deal with these kinds of scenarios, and we will learn about `subquery` in our next class, which will help you capture ties.

# ## Lap 2 🧋
# ### Aggregations
# 
# So far, we have returned columns in our select statement. We can also use aggregation functions that operate on rows to summarize the data in the form of a single value. Here is a list of aggregation functions in SQL:
# 
# | Function | Description      |
# |----------|------------------|
# | MAX()    | maximum value    |
# | MIN()    | minimum value    |
# | AVG()    | average value    |
# | SUM()    | sum of values    |
# | COUNT()  | number of values |

# In[11]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(course_name) FROM courses;')


# The above query is counting number of values in the column `course_name`. it's also sort of like counting the number of rows. We can also pass the `DISTINCT` columns into these operations. For example, the below query will find the number of courses available in the university.

# In[12]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT course_name) FROM courses;')


# In[13]:


get_ipython().run_cell_magic('sql', '', 'select AVG(course_percentage) \nFROM courses')


# Few things to keep in mind when dealing with the aggregation function
# 
# - You are not restricted in using just one aggregation function in the SELECT statement.✅
# 
# ```sql
# SELECT COUNT(DISTINCT course_name),max(course_percentage) FROM courses;
# ```
# 
# - You CAN'T use aggregations and regular columns in a single query. You can use only when you have a `GROUP BY` clause. (will discuss soon)❌
# 
# ```sql
# SELECT COUNT(DISTINCT course_name),course_percentage FROM courses;
# ```
# 
# - You CAN'T use aggregation function in a where clause. The following query is wrong ❌
# 
# ```sql
# SELECT * FROM courses WHERE course_percentage < AVG(course_percentage);
# ```
# 
# You can answer this question when we discuss subqueries in the next class (another reason to learn subqueries :) )

# ### Grouping
# 
# The aggregations we learned in our previous session also become useful when using the `GROUP BY` statement. `GROUP BY` statement divides a table into groups of rows based on the values of one or more columns. Once this grouping is done, you can apply your aggregation to these groups.
# 
# Syntax:
# ```sql
# SELECT
#     grouping_columns, aggregated_columns
# FROM
#     table1
# GROUP BY
#     grouping_columns
# ```
# 
# Example:

# In[14]:


get_ipython().run_cell_magic('sql', '', 'select * from courses;')


# In[15]:


get_ipython().run_cell_magic('sql', '', 'select course_name, AVG(course_percentage) \nFROM courses\ngroup by course_name;')


# We can also perform a multi level grouping;

# In[16]:


get_ipython().run_cell_magic('sql', '', 'select course_name, course_year,AVG(course_percentage) \nFROM courses\ngroup by course_name, course_year\nhaving AVG(course_percentage) <90 ;')


# Now, what if I want to see only the courses with an average of less than 90 %? We mentioned before that this kind of filtering (filtering on the aggregation function) is not possible using `WHERE` statement, and that's why we want the `HAVING` statement to do filtering using these aggregated values.
# 
# ### HAVING
# 
# Syntax:
# ```sql
# SELECT
#     grouping_columns, aggregated_columns
# FROM
#     table1
# GROUP BY
#     grouping_columns
# HAVING
#     group_condition
# 
# ```
# 
# ```{important}
# To summarize:
# 
# - WHERE filters rows before grouping. It filters records in a table level
# - HAVING filters groups after grouping. It filters records in a group level
# ```
# 
# For example, let's get the question we raised at the end of the grouping section. I want to see the courses with a course average of less than 90 %? 

# In[17]:


get_ipython().run_cell_magic('sql', '', 'select course_name, AVG(course_percentage) \nFROM courses\ngroup by course_name\nhaving AVG(course_percentage) <90 ;')


# ### Using alias (AS)
# 
# Until now, we have been referring tables as table names and columns as column names from the schema. But when writing SQL, we are not required to use the same column and table names as in the schema. Instead, we can create aliases for a column or a table using the keyword `AS`.
# 
# Syntax:
# ```sql
# SELECT
#     column1 [AS] c1,
#     column2 [AS] c2
# FROM
#     table1 [AS] t1;
# ```
# 
# It's entirely optional to use AS, but WHY do we want it? 
# - This makes code more readable
# - You can return the columns with a more meaningful name 
# - Helps a lot when we do JOINS ( wait for the next topic)
# 
# Let's rewrite our previous query using AS

# In[18]:


get_ipython().run_cell_magic('sql', '', 'select course_name, course_year,AVG(course_percentage)  AS "average course percentage"\nFROM courses AS c\ngroup by course_name, course_year\nhaving AVG(course_percentage) <90 ;')


# In[19]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM courses;')


# ### Checkpoint 2 !! Take some time and think if you can...
# 
# - Do some aggregations and grouping queries using SQL.
#     - GROUP BY
#     - aggregation functions
#     - HAVING
# 
# Until now, you deal with queries on a single table. What if we are interested in data from another table as well? For example, I am interested in seeing the course details (from the `courses` table) and the students (from the `students` table) related to those courses. In these situations, we use joins. Let's learn how to stitch tables together. Before that, let's do some exercise...

# ### Check point 2 exercise.
# 
# #### iclicker questions
# 
# ***Question 1:*** Spot the issue, if any, in this SQL query 
# 
# ```sql
# SELECT COUNT(DISTINCT course_name),max(course_percentage),course_percentage 
# FROM courses ;
# ```
# 
# A: Multiple aggregation functions in the SELECT statement
# 
# B: No issues
# 
# C: Can't use DISTINCT inside an aggregation function
# 
# D: Can't use aggregations and regular columns in a single query
# 
# ```{toggle}
# ***Answer: D***
# ```
# 
# ***Question 2:*** Spot the issue, if any, in this SQL query 
# 
# ```sql
# SELECT COUNT(DISTINCT course_name),max(course_percentage),course_year
# FROM courses 
# GROUP BY course_year;
# ```
# 
# A: Multiple aggregation functions in the SELECT statement
# 
# B: No issues
# 
# C: Can't use DISTINCT inside an aggregation function
# 
# D: Can't use aggregations and regular columns in a single query
# 
# ```{toggle}
# ***Answer: B***
# ```
# 
# ***Question 3:*** Spot the issue, if any, in this SQL query 
# 
# ```sql
# SELECT COUNT(DISTINCT course_name),max(course_percentage),course_year
# FROM courses 
# WHERE course_name != 'TPCS INFO TECH'
# GROUP BY course_year
# having course_percentage < 90;
# ```
# 
# A: No issues
# 
# B: Can't use column `course_year` in `SELECT`
# 
# C: Can't use WHERE when using aggregation functions
# 
# D: Can't use course_percentage in a `HAVING` statement
# 
# ```{toggle}
# ***Answer: D***
# ```
# 
# #### Reasoning Question
# 
# ***Question 1:*** We learned the `GROUP BY` clause, and we used it with aggregate functions. Using table `courses`, write a SQL query using `GROUP BY` without any aggregation function. Write your findings and learnings.
# 
# ```{toggle}
# You must have tried a variety of SQL queries and got into error;
# 
# ***select * FROM courses
# group by course_name;***
# 
# ***select course_year,course_name
# FROM courses
# group by course_name;***
# 
# Below is one query that runs, and this query can be considered equivalent to using `DISTINCT` if no aggregate functions are used. 
# 
# ***select course_name
# FROM courses
# group by course_name;***
# 
# ```{important}
# In an aggregation query, the unaggregated expressions need to be consistent with the `GROUP BY` expressions. And all other expressions need to use aggregation functions
# ```

# ## Lap 3 🧃
# ### Join
# 
# Syntax:
# ```sql
# SELECT
#     columns
# FROM
#     left_table
# join_type
#     right_table
# ON
#     join_condition
# ;
# ```
# 
# Following are the types of joins
# ### Cross join
# This is the simplest way of performing a join by cross joining 2 tables (like the cartesian product from your relational algebra classes), in our case, table `students` and `courses`. This kind of join returns all possible combinations of rows from `students` and `courses`.

# In[20]:


get_ipython().run_cell_magic('sql', '', '\nSELECT\n    *\nFROM\n    students\nCROSS JOIN\n    courses\n;')


# ```{note}
# But in real life, we usually perform joins on a column, and we will discuss some types of joins on columns in the following sections. Since we are performing joins on a column, we need to pass that information using the `ON` keyword to give which columns are used to stitch the tables together
# ```
# ### Inner join
# 
# Inner join only returns the matching rows from the left and right tables.

# In[21]:


get_ipython().run_cell_magic('sql', '', '\nSELECT s.student_no,s.stud_name,s.age,c.course_name\nFROM\n    students AS s\nINNER JOIN\n    courses AS c\nON\n    s.student_no = c.student_no;')


# ```{margin}
# Check how we are using the alias `AS` we learned in the previous session.
# ```
# 
# ```{note}
# In the returned table, student “Heidy” is missing as that student is not taking any courses and is not mentioned in the `courses`. Also, the courses "C programming" and "Introduction to Genomics" are missing since no students from our `student` table are taking these courses.
# ```
# ### Outer join 
# 
# An outer join returns all the rows from one or both of the tables that join. There are 3 variations of it. 

# #### Left outer
# The first table that appears in the query is the left table, and the one appearing after the `LEFT OUTER JOIN` keyword is the right table.
# 
# A left outer join returns all rows from the left table (matching or not), in addition to the matching rows from both tables. So the non-matching rows from the left table are assigned null values in the columns that belong to the right table.
# 
# If you think about it from a Venn diagram perspective, it will look like...
# 
# <img src ='img/left.png' width="40%"/>

# In[22]:


get_ipython().run_cell_magic('sql', '', '\nSELECT s.student_no,s.stud_name,s.age,c.course_name\nFROM\n    students AS s\nLEFT OUTER JOIN\n    courses AS c\nON\n    s.student_no = c.student_no;')


# #### Right outer 
# It behaves exactly in the same way as a left join, except that it keeps all rows from the right table and only the matching ones from the left table.
# 
# If you think about it from a Venn diagram perspective, it will look like.
# 
# <img src ='img/right.png' width="40%"/>

# In[23]:


get_ipython().run_cell_magic('sql', '', '\nSELECT s.student_no,s.stud_name,s.age,c.course_name\nFROM\n    students AS s\nRIGHT OUTER JOIN\n    courses AS c\nON\n    s.student_no = c.student_no;')


# #### Full outer
# 
# left join + right join = full outer join.
# 
# It retrieves matching and non-matching rows from both tables. 
# 
# If you think about it from a Venn diagram perspective, it will look like.
# 
# <img src ='img/full.png' width="40%"/>

# In[24]:


get_ipython().run_cell_magic('sql', '', '\nSELECT s.student_no,s.stud_name,s.age,c.course_name\nFROM\n    students AS s\nFULL OUTER JOIN\n    courses AS c\nON\n    s.student_no = c.student_no;')


# ### Summarize:
# 
# ***CARTESIAN JOIN:*** returns the Cartesian product of the sets of records from the two or more joined tables.
# 
# ***INNER JOIN:*** returns rows when there is a match in both tables.
# 
# ***LEFT JOIN:*** returns all rows from the left table, even if there are no matches in the right table.
# 
# ***RIGHT JOIN:*** returns all rows from the right table, even if there are no matches in the left table.
# 
# ***FULL JOIN:*** combines the results of both left and right outer joins.

# We learned now about the joins. You know now how to join 2 tables. Once you joined 2 tables its sort of behave like another table that you apply the operations what we learned.

# In[25]:


get_ipython().run_cell_magic('sql', '', "select s.stud_name,c.course_name, c.course_year\nFROM students AS s\nINNER JOIN\ncourses AS c\nON  s.student_no = c.student_no\nWHERE course_name = 'Data Visualization'\nORDER BY course_year DESC;")


# ```{important}
# We can have all the keywords we learned in a single SQL query, and we have come across some in previous examples. `BUT` the order of SQL keywords `DOES` matter: SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT. 
# ```
# ```{seealso}
# We experienced performing joins on 2 tables, but joins can also be performed on multiple tables. Multi joins in SQL work by progressively creating derived tables one after the other. Here is the link that explains this [process](https://www.interfacett.com/blogs/multiple-joins-work-just-like-single-joins/)
# ```

# ### Checkpoint 3 !! Take some time and think if you can...
# - Understand different kinds of joins
# - When to use joins
# - Write SQL queries to join tables

# ### Check point 3 exercise.
# #### iclicker questions
# 
# ***Question 1:*** Spot the issue, if any, in this SQL query 
# 
# ```sql
# select s.stud_name,c.course_name, c.course_year
# FROM students AS s
# INNER JOIN
# courses AS c
# ON  s.student_no = c.student_no
# ORDER BY course_year DESC
# WHERE course_name = 'Data Visualization';
# ```
# 
# A: There are some issues with the join key
# 
# B: No issues
# 
# C: Can't specify alias when performing a join
# 
# D: ORDER BY need to come after the WHERE clause
# 
# ```{toggle}
# ***Answer: D***
# ```
# 
# ***Question 2:*** "In this Venn diagram green color indicate left outer join" - is this statement TRUE/FALSE?
# 
# <img src ='img/color.png' width="40%"/>
# 
# A: TRUE
# 
# B: FALSE
# 
# ```{toggle}
# ***Answer: FALSE***
# 
# The following figure is what indicates the left outer join.
# 
# <img src ='img/left.png' width="40%"/>
# 
# But what is given here is a special scenario where we apply left join to be useful. For example, what if we want to find all students who are not taking any courses?
# 
# 
# SELECT s.student_no,s.stud_name,s.age,c.course_name
# FROM
#     students AS s
# LEFT OUTER JOIN
#     courses AS c
# ON
#     s.student_no = c.student_no
# WHERE c.student_no is NULL
# 
# 
# | student_no | stud_name | age | course_name |
# |-----------:|----------:|----:|------------:|
# |        777 |     Heidy |  30 |        None |
# 
# Ahaa..! looks like "heidy" is not taking any courses; we need to check with her to see why she is not taking any courses :)
# 
# ```

# ## 🏁 Finish line 🏁 🍺
# 
# Are you able to recollect our 3 checkpoints?
# 
# - ***Checkpoint 1:*** Take some time and think if you can...
#     - Select columns and bring in rows just what we needed (using SELECT & WHERE)
#     - Return DISTINCT elements
#     - ORDER BY rows returned based on column(s)
#     - LIMIT the number of rows returned
# - ***Checkpoint 2:*** Take some time and think if you can...
#     - Do some aggregations and grouping queries using SQL.
#         - GROUP BY
#         - aggregation functions
#         - HAVING
# - ***Checkpoint 3:*** Take some time and think if you can...
#     - Understand different kinds of joins
#     - When to use joins
#     - Write SQL queries to join tables

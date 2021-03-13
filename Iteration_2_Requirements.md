# Requirements Document

## Project Summary

CourseMapper is a Django website intended to help SFU students visualize and plan their undergraduate degree. Given courses inputted either manually or via a transcript, the software will fill in a tree diagram showing the various relationships between courses, and will prompt the user to give a destination. Once a student inputs either a course or academic program they wish to achieve, the program will try to find an optimal path they can take. 

## User Stories

### User Story 1

Tom is a student at Simon Fraser University and is trying to plan his course for the next semester but is having trouble deciding which course to take based on if he meets the prerequisites or not. Tom can then sign up and log in to CourseMappers to help him with this. When Tom logs onto CourseMappers he can upload his transcript and which program he is. The transcript is not stored on the website, it is deleted right away. The transcript is just used to understand what courses Tom has already done. Using the SFU API CourseMappers then looks at the requirements for Toms project and then creates a list of classes he can take the next semester based on if Tom has done the pre-reqs. Tom can then search up courses he was planning on taking and CourseMappers will show Tom if he already meets the pre-reqs for the class.

### User Story 2

A student wants to find out his tuition fees for the next semester's courses, and he also needs to know what courses to take next. He wants to add the course and it's fee to a list so he can come back to it at a later time. Then he wants to log out of his account.

### User Story 3

An admin wants to fix a course description / price because it is not updated. He logs into the admin account to search up the name of the course and then edit the deprecated course information. Then he saves it and the saved version is updated for all the users. 

### User Story 4
A user logs in and wants to see a visual representation of the courses they need to take. They enter CourseMapper and submit their academic history, and CourseMapper returns a formatted list of prerequisites. The user can now clearly see a path of courses they need to take in order to reach their goal. 


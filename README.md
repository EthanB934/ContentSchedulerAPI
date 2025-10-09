# Content Scheduler App API

This repository contains the Python Application Programming Interface that will be used by the Content Scheduler Web Application
to manipulate and query data within the PostGreSQL database. 

In order to run this API locally:
1. Click the Green button at the top-right of the repository's window filled with the text, "Code."
2. You may either use the HTTPS or SSH protocol with the given link, copy that link.
3. In your terminal, run the command: `git clone <HTTPS or SSH Link>`
4. This will create a new directory within your current working directory where you have run the command.
5. In your terminal, change directories to the new ContentSchedulerAPI directory.
6. You may switch to any branch found listed after `origin/<branch name>`

You may use whichever interactive development environment that you choose. In my case, I am developing this API using VSCode's IDE. Therefore, I run the `code .` command after I changed to the directory containing this repository. 

This is the current working entity relationship diagram. This diagram lists all of the resources that will be stored within the PostGreSQL database as well as the properties that will be tracked on those resources:
https://dbdiagram.io/d/Content-Scheduler-68e7256cd2b621e422f7438d

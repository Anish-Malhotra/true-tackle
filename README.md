# Tackle Take Home Project

👋 Hello,
If you are reading this then we're likely in the process of chatting with you about a role at Tackle.io. If so, congratulations 🎉!

We designed this take home exercise to give you a taste of the challenges you may encounter in the role, and better understand what it would be like to work closely together.

Please spend no more than four hours completing this challenge. You're welcome to research unfamiliar technologies and set up your node/python environment before you start.

### Scenario

Tackle.io is a software vendor that sells through the AWS marketplace. Tackle has two products listed on the AWS marketplace: an Amazon Machine Image (AMI) called "Tackle Amazon Machine Image" and a Software as a Service (SaaS) listing called "Tackle for GovCloud".

You're helping to build an internal dashboard for Tackle that will enable staff to track sales, manage products, and so forth.

### Business Requirements

- A Dashboard page that displays:
  - A list of all products
  - The total revenue from all orders
  - (Optional stretch goal) a graph of revenue over the last year segmented by month
- Upon selecting a product, the user should be able to see more information about it, including:
  - Product details
  - A list of orders for the product
  - Total revenue from the product's orders

### Implementation

You have been provided a simple full stack web application composed of a SQLite database, Python/Flask server, and a React front end client.

- (Optional stretch goal) Include tests that demonstrate the functionality of your work
- (Optional stretch goal) Optimize the app to work with a large number of products/orders in the database

### Additional Instructions:

- If you're unfamiliar with the languages and tools utilized in this project, you may research them before you start
- Make meaningful git commits as you work, as you would in a team setting
- Use the `time.md` file to break down your development work and track how much time you spent on each item
- Do not publish your work to a public location, such as a GitHub or GitLab public repository


### Grading

The take home project serves as a code sample in a vacuum. We hope it will demonstrate your problem solving abilities within a time constraint. We want to make sure you have some level of mastery over the primary programming languages we use (Python, JavaScript, and TypeScript). There are many factors that we evaluate, but the most important are:

- Adherence to the business requirements
- Intuitive UI/UX
- Code quality, correctness, and idiomatic use of the language and frameworks
- Your approach/process to the challenge and your time-management skills.
- Your software design / architecture skills (e.g. separation of responsibilities, error handling, RESTful API design, efficient/performant code)
- Demonstrated understanding of software engineering best practices (e.g. helpful documentation, meaningful code comments, etc.)
- Test cases that match business requirements or logic. Given the time constraint, we don't expect 100% test coverage. If some tests can't be fully implemented, stubbing out the test cases to show intent is acceptable.

## General Notes

### Run the API (Python 3.7.6)

```
cd tackle-api
```

Optionally create a virtual environment to keep your python packages isolated.

```
python -V
>> Python 3.7.6
python -m virtualenv venv
source venv/bin/activate
```

Install dependencies in requirements.txt.

```
pip install -r requirements.txt
```

Start the server.

```
python server.py
```

In a separate terminal use the canary test to make sure your server is running:

```
curl localhost:5001/canary
```

The response should say:

```
Welcome to the Tackle Take Home Project API!
```

### Run the Client

```
cd tackle-app
yarn --version
>> 1.3.2
yarn install
yarn start
```

To test that the client is running open a browser and navigate to localhost:3000.

### Loading Seed Data into SQLite

To load the seed data into your database start a python shell and import util. Util has a function called build_or_refresh_db you can call to load all of the seed data into a SQLite db called `tkldb`.

```
cd tackle-api
source venv/bin/activate
python
>>> import util
>>> util.build_or_refresh_db()
data refreshed!
>>>
```

## Submission Instructions

Once you are finished:

1. Make sure to commit and push all your changes
2. Return to the link you received over email where you can review your commits and submit your code.
3. Once our team reviews your submission we will get back to you with next steps.

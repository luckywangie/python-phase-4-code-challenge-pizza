# Phase 4 Code Challenge: Pizza Restaurants (INSTRUCTIONS)

In this code challenge, you'll be working with a Pizza Restaurant domain.

In this repo:

- There is a Flask application with some features built out.
- There is a fully built React frontend application.
- There are tests included which you can run using `pytest -x`.
- There is a file `challenge-1-pizzas.postman_collection.json` that contains a
  Postman collection of requests for testing each route you will implement.

Depending on your preference, you can either check your API by:

- Using Postman to make requests
- Running `pytest -x` and seeing if your code passes the tests
- Running the React application in the browser and interacting with the API via
  the frontend

You can import `challenge-1-pizzas.postman_collection.json` into Postman by
pressing the `Import` button.

![import postman](https://curriculum-content.s3.amazonaws.com/6130/phase-4-code-challenge-instructions/import_collection.png)

Select `Upload Files`, navigate to this repo folder, and select
`challenge-1-pizzas.postman_collection.json` as the file to import.

## Setup

The instructions assume you changed into the `code-challenge` folder **prior**
to opening the code editor.

To download the dependencies for the frontend and backend, run:

```console
pipenv install
pipenv shell
npm install --prefix client
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

You can run your React app on [`localhost:4000`](http://localhost:4000) by
running:

```sh
npm start --prefix client
```

You are not being assessed on React, and you don't have to update any of the
React code; the frontend code is available just so that you can test out the
behavior of your API in a realistic setting.

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Core Deliverables

All of the deliverables are graded for the code challenge.

### Models

You will implement an API for the following data model:

![domain diagram](https://curriculum-content.s3.amazonaws.com/6130/code-challenge-1/domain.png)

The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db migrate
flask db upgrade head
```

Now you can implement the relationships as shown in the ER Diagram:

- A `Restaurant` has many `Pizza`s through `RestaurantPizza`
- A `Pizza` has many `Restaurant`s through `RestaurantPizza`
- A `RestaurantPizza` belongs to a `Restaurant` and belongs to a `Pizza`

Update `server/models.py` to establish the model relationships. Since a
`RestaurantPizza` belongs to a `Restaurant` and a `Pizza`, configure the model
to cascade deletes.

Set serialization rules to limit the recursion depth.

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
flask db upgrade head
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

### Validations

Add validations to the `RestaurantPizza` model:

- must have a `price` between 1 and 30

### Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using to_dict() (don't forget the comma if specifying a
single field).

NOTE: If you choose to implement a Flask-RESTful app, you need to add code to
instantiate the `Api` class in server/app.py.

#### GET /restaurants

Return JSON data in the format below:

```json
[
  {
    "address": "address1",
    "id": 1,
    "name": "Karen's Pizza Shack"
  },
  {
    "address": "address2",
    "id": 2,
    "name": "Sanjay's Pizza"
  },
  {
    "address": "address3",
    "id": 3,
    "name": "Kiki's Pizza"
  }
]
```

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using `to_dict()` (don't forget the comma if specifying
a single field).

#### GET /restaurants/<int:id>

If the `Restaurant` exists, return JSON data in the format below:

```json
{
  "address": "address1",
  "id": 1,
  "name": "Karen's Pizza Shack",
  "restaurant_pizzas": [
    {
      "id": 1,
      "pizza": {
        "id": 1,
        "ingredients": "Dough, Tomato Sauce, Cheese",
        "name": "Emma"
      },
      "pizza_id": 1,
      "price": 1,
      "restaurant_id": 1
    }
  ]
}
```

If the `Restaurant` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Restaurant not found"
}
```

#### DELETE /restaurants/<int:id>

If the `Restaurant` exists, it should be removed from the database, along with
any `RestaurantPizza`s that are associated with it (a `RestaurantPizza` belongs
to a `Restaurant`). If you did not set up your models to cascade deletes, you
need to delete associated `RestaurantPizza`s before the `Restaurant` can be
deleted.

After deleting the `Restaurant`, return an _empty_ response body, along with the
appropriate HTTP status code.

If the `Restaurant` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Restaurant not found"
}
```

#### GET /pizzas

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "ingredients": "Dough, Tomato Sauce, Cheese",
    "name": "Emma"
  },
  {
    "id": 2,
    "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni",
    "name": "Geri"
  },
  {
    "id": 3,
    "ingredients": "Dough, Sauce, Ricotta, Red peppers, Mustard",
    "name": "Melanie"
  }
]
```

#### POST /restaurant_pizzas

This route should create a new `RestaurantPizza` that is associated with an
existing `Pizza` and `Restaurant`. It should accept an object with the following
properties in the body of the request:

```json
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 3
}
```

If the `RestaurantPizza` is created successfully, send back a response with the
data related to the `RestaurantPizza`:

```json
{
  "id": 4,
  "pizza": {
    "id": 1,
    "ingredients": "Dough, Tomato Sauce, Cheese",
    "name": "Emma"
  },
  "pizza_id": 1,
  "price": 5,
  "restaurant": {
    "address": "address3",
    "id": 3,
    "name": "Kiki's Pizza"
  },
  "restaurant_id": 3
}
```

If the `RestaurantPizza` is **not** created successfully due to a validation
error, return the following JSON data, along with the appropriate HTTP status
code:

```json
{
  "errors": ["validation errors"]
}
```



# Pizza Restaurant API (Flask Phase 4 Code Challenge) 

## Project Overview  
This is a RESTful API for managing pizza restaurants and their menus. Built using **Flask**, **SQLAlchemy**, and **Flask-Migrate**, the project models the relationship between Restaurants and Pizzas through a join model called `RestaurantPizza`.

---

## Models

There are **three main models**:

1. **Restaurant** – Represents a pizza restaurant with attributes like `name` and `address`.  
2. **Pizza** – Represents a type of pizza with `name` and `ingredients`.  
3. **RestaurantPizza** – The join model that connects a `Pizza` to a `Restaurant`, with an additional `price` attribute.

---

##  Relationships

- A **Restaurant** has many **Pizzas** through **RestaurantPizzas**  
- A **Pizza** can belong to many **Restaurants**  
- A **RestaurantPizza** belongs to one **Restaurant** and one **Pizza**

---

## Objectives

This challenge tests your ability to:

- Build a RESTful API using Flask  
- Design relational models and implement many-to-many associations  
- Implement validations and cascade deletions  
- Create seed data and migrations  
- Return consistent, structured JSON responses  
- Handle validation and error responses gracefully

---

## Features

- View all restaurants or a single restaurant with its pizzas  
- View all pizzas  
- Add a pizza to a restaurant with pricing  
- Delete a restaurant (and cascade delete associated menu items)  
- Validations (e.g., price range 1–30)  
- Error handling for non-existent resources and invalid input

---

## 🗂 Project Structure

```
pizza-api/
 server/
  ── app.py
  ── models.py
  ── seed.py
  ── migrations/
client/ (React frontend for testing)
challenge-1-pizzas.postman_collection.json
README.md

```

---

 ## Technologies Used
Python 3.12

Flask – Web framework

Flask-Migrat Technologies Used
Python 3.12

Flask – Web framework

Flask-Migrate – Database migrations

SQLAlchemy – ORM (Object Relational Mapping)

SQLite – Lightweight relational database (default)

Pipenv – Python dependency manager

React – Frontend (optional, provided for testing)

Postman – API testing

Pytest – Unit testing (optional, included)




## Setup Instructions

### 1. Backend (Flask API)

```bash
pipenv install
pipenv shell
```

### 2. Set up the database

```bash
export FLASK_APP=server/app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Seed the database

```bash
python server/seed.py
```

### 4. Start the API server

```bash
python server/app.py
```

The API will be available at: [http://localhost:5555](http://localhost:5555)

---

### 5. Frontend (Optional React client)

```bash
npm install --prefix client
npm start --prefix client
```

This runs the frontend at: [http://localhost:4000](http://localhost:4000)

---

##  Postman Testing

You can test your API using the provided Postman collection:

1. Open Postman
2. Click **Import**
3. Upload `challenge-1-pizzas.postman_collection.json`
4. Ensure your API is running on `http://localhost:5555`

---

## API Endpoints

-----GET /restaurants--------

Returns a list of all restaurants.

------GET /restaurants/<id>-------

Returns a restaurant and its pizzas.
```
 -----DELETE /restaura*nts/<id>------

Deletes the restaurant and its associated menu items.  

 -----GET /pizzas---------

Returns all pizzas in the database.

------POST /restaurant_pizzas-------

Creates a new RestaurantPizza 
---

**Author**

Name:Lucky Mamati  
Email:wangiemamati@gmail.com

---

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction...
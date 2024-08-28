# Taxi Project

## Overview

This project is a simple taxi booking application built using Flask and SQLAlchemy. It allows users to sign up, log in, and request a taxi. The application uses Dijkstra's algorithm to calculate the shortest path between locations and stores ride information in a MySQL database.

## Features

- User registration and authentication
- Driver management
- Taxi booking with route calculation

## Technologies

- Flask: Web framework for building the web application
- SQLAlchemy: ORM for interacting with the MySQL database
- MySQL: Database for storing user, driver, and ride information
- Dijkstra's Algorithm: Used for calculating the shortest path between locations

## Setup

### Prerequisites

1. **Python 3.x**: Ensure you have Python 3.x installed on your machine.
2. **MySQL**: Install MySQL and create a database named `taxiproject`.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/taxi-project.git
   cd taxi-project

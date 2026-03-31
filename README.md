# FinalProject_GAG1

## Final Project in Database Management Systems 2026, Reykjavík University.

### **Teacher:** Hildur Davíðsdóttir.
### **Group 19**
### **Students:** Hrafnhildur I. Hallsdóttir, Kolbrún Eggerts Kristínardóttir, Sóldís Rós Ragnarsdóttir, Steinunn Helga Pálsdóttir.

## **Description:** 
### This project was developed for the course Database Management System. The goal was to work with designed database, improve it´s schema and build a backend system using FastAPI.
### The project is based on a simulated electricity grid where energy is produced at power plats, transfered through substations and consumed in Vestmannaeyjar. 

## Project Structure

### Part A - Analysis

* Set up a PostgreSQL database
* Explored the legacy schema
* SQL queries

### Part B - API

* Set up a FastAPI backend
* Connected the database using SQLAlchemy
* Created GET endpoints for queries

### Part C - Refactoring

* Normalized the databasse
* Designed a new schema
* Created an ER diagram
* Migrated data from legacy database

### Part D - Performance

* Designed an indexing strategy to improve query performance

## Technologies

* PostgreSQL
* Python
* FastAPI
* SQLAlchemy

## How to run

### Set up the database
createdb OrkuFlaediIsland 
psql -d OrkuFlaediIsland -f DDL_DML.sql

### Run the API
pip install -r requirements.txt 
uvicorn app.main:app --reload

Swagger UI:
http://127.0.0.1:8000/docs

## ER - Diagram 

<img width="6384" height="2396" alt="image" src="https://github.com/user-attachments/assets/52bb5c8a-5453-43ca-9f98-5160c4c0f0f1" />

    

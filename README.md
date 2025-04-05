# Library Catalog System (SQLite3 + Python)

## Project Description

This Python application implements a simple library catalog system using SQLite3 for data storage. It allows users to manage authors and books in a database with basic CRUD (Create, Read, Update, Delete) operations.

## Features

- **Author Management**:
  - Add new authors with name and country of origin
  - Automatic prevention of duplicate authors

- **Book Management**:
  - Add new books with title, author, publication year, and page count
  - Unique constraint prevents duplicate books by the same author
  - Update publication years
  - Delete books from the catalog

- **Search Functions**:
  - Find all books by a specific author
  - View complete list of authors with their book counts

## Technical Details

- **Database Schema**:
  - `authors` table: Stores author information (ID, name, country)
  - `books` table: Stores book information (ID, title, author ID, year, pages) with foreign key relationship to authors

- **Implementation**:
  - Uses Python's built-in `sqlite3` module
  - Parameterized queries to prevent SQL injection
  - Case-insensitive handling of author names and book titles
  - Simple console-based menu interface

## How to Use

1. Run the Python script
2. Use the menu to select operations:
   - Add authors/books
   - Search for books
   - View catalog statistics
   - Update or delete entries

## Requirements

- Python 3.x
- No external dependencies (uses built-in sqlite3)

## Example Use Case

1. Librarian adds new authors and their books
2. Patrons search for books by specific authors
3. Staff updates publication information
4. Administrator removes outdated books

The system maintains data integrity through database constraints while providing simple text-based interaction.

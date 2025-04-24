# 🧠 Django Community Room Web App

A full-stack web application built with Django where users can create and join rooms to discuss topics of interest. It includes user authentication, messaging features, topic filtering, and user profile customization.

---

## 🚀 Features

### 🧑‍💻 Authentication
- User **registration**, **login**, and **logout** functionality
- **Custom user model** using email instead of username
- Protected routes with `@login_required` decorators

### 📚 Room and Topic Management
- Users can **create**, **update**, and **delete** discussion rooms
- Create or auto-generate **topics** while creating/updating rooms
- Rooms are associated with specific topics and hosts
- Room search functionality based on:
  - Topic name
  - Room name
  - Description

### 🗨 Messaging System
- Post messages inside rooms
- View message history per room
- Only message owners can **delete their messages**

### 👥 User Profiles
- View public user profiles showing:
  - Rooms hosted
  - Messages sent
  - Topics of interest
- Edit personal information and upload profile images

### 🔍 Filtering & Search
- Global search for rooms and topics using `Q` queries with `icontains`
- Dynamic topic filtering from homepage
- Separate **Topics** page for full browsing
- **Activity** page listing recent messages

### 📁 Forms and Models
- **Custom Django forms** for user creation and profile updates
- Room creation/update using Django `ModelForm`
- Usage of `get_or_create()` for dynamic topic handling

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Django templates)
- **Database:** SQLite (default Django database)
- **Authentication:** Django Auth system
- **ORM:** Django ORM for all DB operations





---

## ✅ What I Did in This Project
- Built full CRUD functionality for rooms, messages, and users
- Implemented authentication and session management
- Designed the user experience around real-time interaction (message posting)
- Used Django’s generic tools to simplify and speed up development
- Focused on clean code structure, security (login required decorators), and error handling with messages

---

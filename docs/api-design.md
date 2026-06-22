# API Design — Taxpayer Management System

## Base URL
`/api/v1`

## 1. Authentication

### Login
`POST /auth/login`

**Request:**
- email
- password

**Response:**
- access_token
- user_role

## 2. Users

### Create User (Admin only)
`POST /users`

### Get All Users
`GET /users`

## 3. Taxpayers

### Create Taxpayer
`POST /taxpayers`

### Get All Taxpayers
`GET /taxpayers`

### Get Taxpayer by ID
`GET /taxpayers/{id}`

### Update Taxpayer
`PUT /taxpayers/{id}`

### Delete Taxpayer
`DELETE /taxpayers/{id}`

## 4. Documents

### Upload Document
`POST /taxpayers/{id}/documents`

### Get Documents
`GET /taxpayers/{id}/documents`

## 5. Registration Workflow

### Submit Registration
`POST /registrations`

### Approve Registration
`PUT /registrations/{id}/approve`

### Reject Registration
`PUT /registrations/{id}/reject`

## 6. Audit Logs

### Get Audit Logs
`GET /audit-logs`
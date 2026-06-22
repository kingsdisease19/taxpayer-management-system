# Database Design

## Entities

### Users
**Purpose:** Stores system users.

**Attributes:**
- id
- username
- email
- password_hash
- role
- created_at

### Taxpayers
**Purpose:** Stores taxpayer information.

**Attributes:**
- id
- tpin
- taxpayer_type
- business_name
- first_name
- last_name
- phone
- email
- address
- registration_status
- created_at

### Documents
**Purpose:** Stores uploaded documents.

**Attributes:**
- id
- taxpayer_id
- document_type
- file_path
- uploaded_at

### Registrations
**Purpose:** Tracks taxpayer registration workflow.

**Attributes:**
- id
- taxpayer_id
- status
- approved_by
- submitted_at

### Audit Logs
**Purpose:** Tracks system activity.

**Attributes:**
- id
- user_id
- action
- timestamp
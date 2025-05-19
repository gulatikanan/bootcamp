# Persistence Learning Path: File & Database Systems

**Author: kanan**

A comprehensive hands-on guide to mastering data persistence in Python, covering everything from basic file serialization to advanced database engineering patterns. This curriculum emphasizes practical learning through progressive exercises that build real-world skills.

## 🎯 Learning Philosophy

These drills are designed for active learning - **do not delegate to LLMs**. Each exercise builds foundational understanding through hands-on implementation. Like physical drills, repetition and practice develop muscle memory for persistence patterns you'll use throughout your career.

---

## 📚 Prerequisites & Essential Concepts

### Core Database Concepts

Before diving into the exercises, i have  written about these fundamental concepts. 

#### 🗃️ Understanding Transactions and ACID Properties

**What are transactions?**

A transaction is a group of operations that are executed as a single unit. Either all operations succeed, or none do. This ensures data safety and consistency.

**Real-life Example**: Transferring ₹1,000 from your savings to your friend's account:
1. ₹1,000 is deducted from your savings
2. ₹1,000 is added to your friend's account

If step 2 fails but step 1 succeeded, your money would disappear! Transactions ensure both steps succeed or both are rolled back.

**What are ACID Properties?**

ACID ensures transactions are processed reliably:
- **A – Atomicity**: Everything in a transaction must succeed. If one thing fails, everything is rolled back
- **C – Consistency**: Data must stay valid before and after the transaction  
- **I – Isolation**: Multiple transactions don't affect each other
- **D – Durability**: Once complete, data is saved even if the system crashes

#### 🤔 Self-Assessment Questions

**Suppose you don't have transactions. Is that system useful? Why?**

Without transactions, there's risk of partial updates leading to inconsistent data. However, some systems still work:
- ✅ **When it's useful**: Reading configuration files, logging systems, simple lookup tables
- ❌ **Problems**: Two operations might leave data in an incomplete state

**What properties does your file system have?**

Most file systems (NTFS, ext4) offer:
- **Durability**: Data remains after restart
- **Basic atomicity**: Can replace entire files, but not partial contents  
- ❌ **No consistency or isolation**: Two apps writing simultaneously can cause corruption

**What if you don't have "A" (Atomicity)?**

- ❌ **Problem**: Partial completion leaves broken data
- ✅ **When it's OK**: Log files (missing one line), analytics with error tolerance
- **Example**: Writing two log values but only one saves - acceptable for monitoring, not finance

**What if you don't have "C" (Consistency)?**

- ❌ **Problem**: Invalid or mismatched data
- ✅ **When it's OK**: Data migration, eventual consistency systems (NoSQL)
- **Example**: Customer exists but order isn't linked yet - temporary state is acceptable

**What if you don't have "I" (Isolation)?**

- ❌ **Problem**: Concurrent processes interfere (dirty reads, lost updates)
- ✅ **When it's OK**: Real-time dashboards where performance > perfect accuracy
- **Example**: Two users editing same document - minor overwrites acceptable in fast tools

**What if you don't have "D" (Durability)?**

- ❌ **Problem**: "Saved" data lost after crashes
- ✅ **When it's OK**: Cache systems (Redis), rebuildable data
- **Example**: Chat app status messages don't need crash survival

#### 🏗️ Database Selection Guide

**Use Redis (Key-Value) when:**
- You need fast, simple lookups (session data, cache)
- No relations or complex queries required

**Use SQLite when:**
- Single application needs local storage (mobile app, small web app)
- No multiple users or external access required

**Use PostgreSQL when:**
- Multiple apps/users need access
- Building large, distributed, production systems
- Need powerful queries and scalability

### Technical Prerequisites

- **Python Basics**: Classes, exception handling, context managers
- **SQL Knowledge**: Basic CRUD operations, joins, indexing


---

## 🗺️ Learning Path

### Phase 1: File-Based Persistence

Master Python's built-in serialization capabilities before moving to databases.

#### Serialization Foundations
- **Pickle Operations**: Serialize/deserialize custom objects (Person class with complex attributes)
- **JSON Handling**: Implement custom JSON serialization for Book objects
- **YAML Processing**: Work with PyYAML for Car object persistence
- **Custom Serialization**: Handle complex data structures like Graph objects with nodes/edges

#### Advanced File Persistence
- **Selective Serialization**: Skip sensitive attributes during User object serialization
- **State Management**: Save/restore game session state
- **Version Compatibility**: Handle object schema evolution gracefully
- **Collection Serialization**: Persist custom collection classes
- **Cyclic References**: Serialize objects with circular dependencies

### Phase 2: SQLite Fundamentals

Transition to relational databases with SQLite's lightweight, file-based approach.

#### Environment Setup
1. Install SQLite locally and test basic operations
2. Create your first database: `sqlite3 example.db`
3. Practice basic SQL: `CREATE TABLE`, `INSERT`, `SELECT`
4. Verify portability by copying database files between systems

#### Core SQLite Operations
- **Database Creation**: Set up `store.db` with proper connection handling
- **Table Management**: Create `products` table with appropriate schema
- **CRUD Operations**: Implement insert, read, update, delete functions
- **Error Handling**: Add robust exception handling for database operations
- **Search & Filtering**: Build flexible query functions
- **Data Validation**: Ensure data integrity before persistence

#### Advanced SQLite Features
- **Transactions**: Implement ACID compliance for multi-step operations
- **Joins**: Work with related tables (products ↔ categories)
- **Aggregations**: Calculate summaries and statistics
- **Batch Operations**: Optimize performance with bulk insertions
- **Data Export**: Generate CSV reports from database queries

#### Transaction Deep Dive
- **Basic Transactions**: Single-table operations with rollback
- **Multi-Table Updates**: Ensure consistency across related entities
- **Batch Processing**: Transactional bulk operations
- **Banking Simulation**: Implement atomic money transfers
- **Complex Business Logic**: Handle inventory management with logging

### Phase 3: ORM with SQLAlchemy + Pydantic

Bridge the gap between Python objects and relational data.

#### Beginner ORM Patterns
- **Model Definition**: Create SQLAlchemy models with Pydantic validation
- **Basic CRUD**: Implement validated database operations
- **Session Management**: Handle database sessions properly
- **Data Conversion**: Transform between ORM objects and Pydantic schemas

#### Intermediate ORM Concepts
- **Filtering & Querying**: Build flexible search functionality
- **Updates & Deletions**: Modify existing records safely
- **Relationship Mapping**: Implement User ↔ Post relationships
- **Nested Queries**: Fetch related data efficiently

#### Advanced ORM Techniques
- **Async Operations**: Use SQLAlchemy 2.0 with async/await patterns
- **Transaction Management**: Ensure atomicity in complex operations
- **Performance Optimization**: Handle bulk operations efficiently

### Phase 4: Production Engineering Challenges

Apply your skills to realistic engineering scenarios.

#### **1. Schema Evolution and Migrations**
Safely modify database schemas in production without data loss.

#### **2. Model Boundary Enforcement**
Maintain clean separation between persistence and API layers.

#### **3. Idempotent Upserts**
Handle duplicate operations gracefully across different databases.

#### **4. Versioned Data Storage**
Implement audit trails and historical data access.

#### **5. Concurrency and Race Condition Management**
Prevent data corruption in high-traffic scenarios.

#### **6. Handling Large Binary Data**
Compare filesystem vs. database storage strategies.

#### **7. Schema-First vs Code-First Modeling**
Work with existing schemas and design new ones effectively.

#### **8. Data Lifecycle Management**
Implement soft deletes and data archival strategies.

#### **9. Boundary Testing with Large Datasets**
Optimize performance for production-scale data volumes.

---

## 🛠️ Setup Instructions

### Python Environment
```bash
# Install required packages
pip install sqlalchemy pydantic psycopg2-binary PyYAML

# For async functionality
pip install asyncpg
```

### Database Setup
```bash
# SQLite (included with Python)
sqlite3 test.db

# PostgreSQL (for advanced exercises)
# Install locally or use Docker
docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
```

---

## 📈 Progress Tracking

### Skill Checkpoints
- [ ] **File Persistence**: Successfully serialize complex objects with custom logic
- [ ] **Basic SQL**: Write and execute database operations confidently
- [ ] **Transaction Management**: Implement robust multi-step operations
- [ ] **ORM Proficiency**: Build and query related models effectively
- [ ] **Production Readiness**: Handle real-world engineering challenges

---


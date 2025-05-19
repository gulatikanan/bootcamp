# 🗃️ Python Persistence Exercises – File & DB

**Author:** Kanan  
This project demonstrates how to store and retrieve Python objects using different serialization formats such as Pickle, JSON, and YAML. It also includes handling custom objects, versioning, collections, and cyclic references.

All outputs from the programs are saved in a file named `output.txt` for reference. You can check it to quickly review inputs and outputs for each task.

---

## 📦 Requirements

Before running the examples, install PyYAML (required for YAML tasks):

```bash
pip install pyyaml
```

---

## 📂 Project Structure

Each task is stored in its own folder: `task1_pickle_serialization`, `task2_pickle_deserialization`, etc.  
You can run the programs by navigating into the folder and using:

```bash
python <script_name>.py
```

---

## ✅ Tasks Performed (Step-by-Step)

---

### **Step 1: Pickle Serialization**

- **What:** Serialize a `Person` object to a file.
- **How:** Using the built-in `pickle` module.
- **File:** `01_pickle_serialization/serialize.py`

---

### **Step 2: Pickle Deserialization**

- **What:** Load back the `Person` object from the Pickle file.
- **How:** `pickle.load()`
- **File:** `02_pickle_deserialization/deserialize.py`

---

### **Step 3: JSON Serialization**

- **What:** Serialize a `Book` object to JSON.
- **How:** Using `json.dumps()` and a `to_json()` method.
- **File:** `03_json_serialization/serialize_book.py`

---

### **Step 4: JSON Deserialization**

- **What:** Create a `Book` object from JSON.
- **How:** Using `json.loads()` with a `from_json()` class method.
- **File:** `04_json_deserialization/deserialize_book.py`

---

### **Step 5: YAML Serialization**

- **What:** Serialize a `Car` object into YAML format.
- **How:** Using `yaml.dump()`
- **File:** `05_yaml_serialization/serialize_car.py`

---

### **Step 6: YAML Deserialization**

- **What:** Load a `Car` object from YAML format.
- **How:** Using `yaml.safe_load()`
- **File:** `06_yaml_deserialization/deserialize_car.py`

---

### **Step 7: Custom Serialization (Graph)**

- **What:** Serialize and deserialize a `Graph` with nodes and edges.
- **How:** Using custom `to_dict()` and `load_from_file()` methods.
- **File:**  
  - `07_custom_serialization/serialize_graph.py`  
  - `07_custom_serialization/deserialize_graph.py`

---

### **Step 8: Skip Sensitive Attributes**

- **What:** Serialize a `User` object but skip sensitive info like `password`.
- **How:** Manually remove sensitive fields before dumping to JSON.
- **File:** `08_skipping_attributes/serialize_user.py`

---

### **Step 9: Restore Game State**

- **What:** Save and reload the state of a `Game` object.
- **How:** Save to and read from a file using `json.dump()` and `json.load()`.
- **File:**  
  - `09_restoring_game_state/save_game.py`  
  - `09_restoring_game_state/load_game.py`

---

### **Step 10: Versioning Serialized Objects**

- **What:** Handle changes in object structure while maintaining compatibility with older serialized versions.
- **Files:**  
  - `10_versioning/create_old_user.py`  
  - `10_versioning/load_old_user_new_version.py`

---

### **Step 11: Custom Collection Serialization**

- **What:** Serialize a collection object (`MyCollection`) with mixed items.
- **How:** Serialize the `items` list using JSON.
- **Files:**  
  - `11_custom_collections/deserialize.py`
  - `11_custom_collections/serialize.py`

---

### **Step 12: Cyclic References**

- **What:** Serialize two objects that reference each other (e.g., `Manager` and `Employee`).
- **How:** Use `pickle`, which automatically handles cycles.
- **Files:**  
  - `12_cyclic_reference_serialization/serialize_org.py`  
  - `12_cyclic_reference_serialization/deserialize_org.py`

---

## 📄 Output Storage

- Every output (like print statements) is saved in a file called `output.txt` for easier verification and checking later.
- Make sure to redirect or write your print outputs to `output.txt` from each script if needed.

---

## 👩‍💻 Author

**Kanan**  
This project was created to deeply understand Python object persistence and data handling across various formats and use-cases.

---

## 📜 License

This is a learning project. Feel free to reuse any part of it.

# 📘 CRUD Operations on the `Book` Model (Django Shell)

This file documents the Django shell commands and outputs for Create, Retrieve, Update, and Delete operations on the `Book` model.

---

## 🟩 CREATE a Book instance

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
```

### ✅ Output:
```python
<Book: 1984 by George Orwell>
```

---

## 🔍 RETRIEVE the Book instance

```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
```

### ✅ Output:
```python
1984 George Orwell 1949
```

---

## ✏️ UPDATE the Book's title

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```

### ✅ Output:
```python
Nineteen Eighty-Four
```

---

## ❌ DELETE the Book instance

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
Book.objects.all()
```

### ✅ Output:
```python
(1, {'bookshelf.Book': 1})
<QuerySet []>
```


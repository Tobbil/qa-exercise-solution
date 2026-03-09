# ShopEasy – QA Take-Home Exercise

Welcome! This exercise should take approximately **1–1.5 hours**.  
Please read this file fully before starting.

---

## What You'll Be Working With

**ShopEasy** is a small e-commerce web application with the following pages:

| Page | URL |
|---|---|
| Product listing | `http://localhost:5050/` |
| Product detail | `http://localhost:5050/product/<id>` |
| Cart | `http://localhost:5050/cart` |
| Checkout | `http://localhost:5050/checkout` |
| Order confirmation | *(shown after successful checkout)* |

It also exposes a REST API under `/api/`. The frontend communicates with the backend exclusively over this API using JSON — there are no traditional HTML form submissions.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/products` | List all products |
| `GET` | `/api/products/<id>` | Get a single product |
| `GET` | `/api/cart` | Get current cart (items, total, item_count) |
| `POST` | `/api/cart/<id>` | Add a product to the cart |
| `DELETE` | `/api/cart/<id>` | Remove a product from the cart |
| `POST` | `/api/checkout` | Submit order `{"name", "email", "address"}` |

---

## Setup Instructions

**Prerequisites:** Python 3.9+, Google Chrome installed

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
python -m app.main

# 4. Verify the app is running — open http://localhost:5050 in your browser

# 5. In a second terminal (with venv active), run the existing tests
pytest tests/ -v
```

All existing tests should pass before you start writing your own.

---

## Your Tasks

### Task 1 – Write 3 new UI test cases (main task)

Open `tests/ui/test_candidate.py`. Three scenarios are described in comments.  
Write a test for each one:

**Scenario A – Product detail page**  
When a user clicks on a product name on the home page, they should land on the correct product detail page. The detail page must display the product name, price, and stock status.

**Scenario B – Cart total calculation**  
When a user adds two different in-stock products to the cart, the total displayed on the cart page should equal the sum of both products' prices.

**Scenario C – Checkout form validation**  
When a user submits the checkout form while leaving required fields empty, an error message should appear and the user should remain on the checkout page (not reach the confirmation page).

---

### Task 2 – Refactor a flawed test

In `tests/ui/test_candidate.py` there is a pre-written test called `test_add_to_cart_bad`.  
It works, but it has quality problems. Refactor it without changing what is being tested.  
You do not need to write a comment explaining your changes — the improved code should speak for itself.

---

### Task 3 – Leave a short note

At the bottom of `tests/ui/test_candidate.py` there is a comment block asking:  
*"What else would you test if you had more time?"*  
Write 3–5 bullet points. A few sentences is all we need.

---

### Bonus – API tests (optional)

If time permits, open `tests/api/test_candidate_api.py` and add 2–3 API test cases.  
This is optional and will not negatively affect your evaluation if skipped.

---

## How to Run Your Tests

```bash
# Run everything
pytest tests/ -v

# Run only your UI tests
pytest tests/ui/test_candidate.py -v

# Run only API tests
pytest tests/api/ -v

# Generate an HTML report (optional)
pytest tests/ -v --html=report.html
```

---

## Submission

Please send us either:
- A `.zip` of the project folder, **or**
- A link to a GitHub/GitLab repository

Include any notes in a file called `NOTES.md` if you want to share context about your decisions or anything you ran out of time for.

---

## Evaluation Criteria

| Area | What we look at |
|---|---|
| **Test design** | Are scenarios well-chosen? Are assertions meaningful? |
| **Code quality** | Is the code clean, readable, and maintainable? |
| **Framework usage** | Correct use of pytest fixtures, waits, and selectors |
| **Refactoring** | Does the improved test follow best practices? |
| **Analysis thinking** | Does the Task 3 note show QA instincts? |

We are **not** evaluating for speed. A clean, well-reasoned partial submission is better than rushed, complete code.

Good luck!

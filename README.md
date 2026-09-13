# PromoFlow — Discount & Promotion Management System

A Python CLI application for managing products, promotions, discounts and sales.

## Why the CLI is not boring

PromoFlow uses **Rich** to provide panels, tables, colors, emojis, progress/spinner feedback and clear role-based screens. Rich is designed for styled terminal output, tables and progress indicators and works on Windows, macOS and Linux. Used the Victor-recommended ThemeSelection article for examples of Rich and other CLI libraries.

## Features

 Registration and login
 PBKDF2 password hashing with salt
 Admin / Staff role-based access
 Product CRUD
 Promotion management
 Percentage and fixed discounts using inheritance + polymorphism
 Sales checkout
 Stock reduction after sales
 JSON persistence
 Dashboard and sales reports
 Input validation and decorators
 Pytest tests

## Default admin

Username: `admin`
Password: `admin123`

Change this by editing/deleting `data/users.json` if you want a fresh first-run account.

## Project structure

```text
promo_management_system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── users.json
│   ├── products.json
│   ├── promotions.json
│   └── sales.json
├── models/
│   ├── user.py
│   ├── product.py
│   ├── discount.py
│   ├── promotion.py
│   └── sale.py
├── services/
│   ├── auth_service.py
│   ├── product_service.py
│   ├── promotion_service.py
│   └── sale_service.py
├── utils/
│   ├── storage.py
│   ├── security.py
│   ├── decorators.py
│   └── validators.py
└── tests/
    ├── test_discount.py
    ├── test_product.py
    └── test_sale.py
```

## OOP used

- **Inheritance:** `Admin` and `Staff` inherit from `User`; `PercentageDiscount` and `FixedDiscount` inherit from `Discount`.
- **Encapsulation:** business data and behavior are grouped inside classes/services.

## Discount formulas

Percentage:

`Discount = Price × Quantity × Rate / 100`

`Final Price = Original Total − Discount`

Fixed:

`Discount = min(Fixed Amount, Original Total)`

`Final Price = Original Total − Discount`


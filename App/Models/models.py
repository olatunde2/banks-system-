from .extensions import db
from Auth.user import User
from datetime import datetime
    

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)  
    balance = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True)
    
    def deposit(self, amount):
        self.balance += amount
        db.session.commit()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            db.session.commit()
            return True
        return False
    
    def __init__(self, account_number, account_type, balance, user_id):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.user_id = user_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    
    def __repr__(self):
        return f'<Account {self.account_number}>'
    

    

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(10), nullable=False)  
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    
    def __init__(self, transaction_type, amount, account_id):
        self.transaction_type = transaction_type
        self.amount = amount
        self.account_id = account_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'<Transaction {self.id}>'
    
    

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.String(20), nullable=False)  
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime(), default=datetime.utcnow)
    is_paid_off = db.Column(db.Boolean, default=False)
        
    def __init__(self, loan_type, principal, interest_rate, duration_months, user_id):
        self.loan_type = loan_type
        self.principal = principal
        self.interest_rate = interest_rate
        self.duration_months = duration_months
        self.user_id = user_id
        self.start_date = datetime.utcnow()
        
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Loan {self.id}>'


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    card_type = db.Column(db.String(10), nullable=False)  
    expiration_date = db.Column(db.Date, nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, card_number, card_type, expiration_date, cvv, account_id, user_id):
        self.card_number = card_number
        self.card_type = card_type
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.account_id = account_id
        self.user_id = user_id

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Card {self.card_number}>'

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, name, account_number, user_id):
        self.name = name
        self.account_number = account_number
        self.user_id = user_id
        
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Beneficiary {self.name}>'

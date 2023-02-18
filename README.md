# Simulated operation of the "ATM/terminal" system. 
The amount of the user's balance and the access pin code is transferred when creating the object attributes.

Pin code verification is called automatically when the object is created and requires three attempts. If the login is completed, the balance is automatically recorded in a separate text file + the balance of the system itself is stored in another file.

The following actions are available to the user:

1. Withdraw funds. In this case, the amount cannot exceed the available balance of the user and the system itself. When withdrawing, the amount is automatically deducted from the balance of the user and the system.

2. Top up the balance. In this case, the balance of the user and the system will be replenished by the corresponding amount.

3. Find out the current exchange rate, the rate itself is obtained from the website of the private bank using bs4.

4. Transfer a certain amount to any currency. After the operation, another attribute will be created for the user (amount of funds in the specified currency), the value of which will be stored in a new text file.

5. Each operation is recorded in a separate txt-file in a dictionary, where the key is time + date (datetime.now()), and the value is the type of operation performed.

Imitation and encapsulation are present.

### Scenario 1: Successful Registration
#### Steps
1. Enter valid username (e.g., "johnDoe")
2. Enter strong password (e.g., "Qwerty123!")
3. Confirm password matches the original one
4. Click "Register"

#### Expected Result
User account created successfully, redirect to login page or confirmation message.

### Scenario 2: Invalid Username
#### Steps
1. Enter invalid username (e.g., "johndoe! * (contains special characters and spaces)")
2. Enter strong password (e.g., "Qwerty123!")
3. Confirm password matches the original one
4. Click "Register"

#### Expected Result
Error message indicating invalid username, e.g., "Username must only contain letters, numbers, or underscores".

### Scenario 3: Weak Password
#### Steps
1. Enter valid username (e.g., "johnDoe")
2. Enter weak password (e.g., "password123")
3. Confirm password matches the original one
4. Click "Register"

#### Expected Result
Error message indicating weak password, e.g., "Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters".

### Scenario 4: Non-Matching Passwords
#### Steps
1. Enter valid username (e.g., "johnDoe")
2. Enter strong password (e.g., "Qwerty123!")
3. Enter different password for confirmation (e.g., "wrongPassword")
4. Click "Register"

#### Expected Result
Error message indicating non-matching passwords, e.g., "Passwords do not match. Please try again".

### Scenario 5: Empty Fields
#### Steps
1. Leave username field empty
2. Leave password fields empty
3. Click "Register"

#### Expected Result
Error messages for each empty field, e.g., "Username is required", "Password is required".
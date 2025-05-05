Feature: User Signup
  As a new visitor
  I want to create an account
  So that I can log in and use the application

  Scenario: Successful signup with valid credentials
    Given I am on the signup page
    When I fill in "signup-username-input" with "newuser"
    When I fill in "signup-password-input" with "newpassword123"
    When I fill in "signup-password-confirm-input" with "newpassword123"
    And I press the signup button
    then I should see a message "Signup successful. Please log in."

  Scenario: Attempt signup with existing username
    Given I am on the signup page
    When I fill in "signup-username-input" with "newuser"
    When I fill in "signup-password-input" with "newpassword123"
    When I fill in "signup-password-confirm-input" with "newpassword123"
    And I press the signup button
    then I should see a message "Signup successful. Please log in."
    When I fill in "signup-username-input" with "newuser"
    When I fill in "signup-password-input" with "password123"
    When I fill in "signup-password-confirm-input" with "password123"
    And I press the signup button
    then I should see a message "Username already taken."

  Scenario: Attempt signup with mismatched passwords
    Given I am on the signup page
    When I fill in "signup-username-input" with "anotheruser"
    When I fill in "signup-password-input" with "password123"
    When I fill in "signup-password-confirm-input" with "differentpassword"
    And I press the signup button
    then I should see a message "Passwords do not match."
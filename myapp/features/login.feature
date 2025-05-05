 Feature: User Login
   In order to access personalized content
   As a registered user
   I want to log into my account

   Scenario: UnSuccessful login with invalid credentials
     Given I am on the login page
     When I fill in "login-username-input" with "testuser"
     And I fill in "login-password-input" with "password"
     And I press "//*[@id="login-section"]/button"
     Then I should see on "login-error" the message "Invalid Credentials"

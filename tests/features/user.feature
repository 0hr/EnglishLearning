Feature: User Management
    This feature tests user login, registration, password reset, and forgot password functionalities.

    Background:
        Given a clean database

    Scenario Outline: Login with valid credentials
        Given a registered user with email "<email>" and password "<password>"
        When I login with email "<email>" and password "<password>"
        Then I should receive a token if the credentials are valid
        Examples:
            | email            | password     |
            | test@example.com | Password123! |

    Scenario Outline: Register a new user
        When I register a new user with email "<email>" and password "<password>"
        Then I should receive a success message if the registration is valid
        Examples:
            | email            | password     |
            | test@example.com | Password123! |

    Scenario Outline: Forgot password
        Given a registered user with email "<email>" and password "<password>"
        When I request a password reset for email "<email>"
        Then I should receive a password reset token
        Examples:
            | email            | password     |
            | test@example.com | Password123! |

    Scenario Outline: Reset password
        Given a registered user with email "<email>" and password "<password>"
        When I request a password reset for email "test@example.com"
        And I reset my password with token "<reset_token>" and new password "<new_password>"
        Then I should receive a success message for the password reset
        Examples:
            | email            | password     | new_password    | reset_token    |
            | test@example.com | Password123! | NewPassword123! | test_token     |

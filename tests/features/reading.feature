Feature: Reading API

    Scenario: Get reading texts
        Given a clean database
        And a reading material exists
        And a registered user with email "test@example.com" and password "Password123!"
        When I login with email "test@example.com" and password "Password123!"
        Then I should receive a token if the credentials are valid
        When I request reading texts
        Then I should receive the reading texts

    Scenario: Get questions by category
        Given a clean database
        Given a question with category "general"
        And a registered user with email "test@example.com" and password "Password123!"
        When I login with email "test@example.com" and password "Password123!"
        Then I should receive a token if the credentials are valid
        When I request questions with category "general"
        Then I should receive the questions with category "general"
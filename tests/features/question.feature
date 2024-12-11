Feature: Question API

  Scenario: Get placement questions
    Given a clean database
    And a question with category "placement"
    And a registered user with email "test@example.com" and password "Password123!"
    When I login with email "test@example.com" and password "Password123!"
    Then I should receive a token if the credentials are valid
    When I request placement questions
    Then I should receive the placement questions
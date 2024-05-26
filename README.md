# My Space Intelligent Recommendation System
A system that analyses user behaviour and preferences to  provide tailored suggestions for music, friends, and content.
The system makes use of machine learning and artificial intelligence to improve the user experience.

# Run tests: 
1. Run the `unit_test.py` script:
    ```sh
    python unit_test.py
    ```

2. Run the `uintegration_testing.py` script:
    ```sh
    python integration_testing.py
    ```

This will execute the unit and integration tests and provide output indicating whether the tests passed or failed.

# Run application:
1. Run the Flask application by executing the following command in the terminal:
    ```sh
    python recommendation_api.py
    ```
2. Access song recommender by navigating to `http://localhost:5000/get-recommended-songs?song_name=Blinding Lights` in your web browser.

3. Access artist recommender by navigating to `http://localhost:5000/get-recommended-artists?artist_name=Taylor Swift` in your web browser.
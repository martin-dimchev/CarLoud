# CarLoud 🚗

CarLoud is an innovative project designed to give car enthusiasts a platform in which they can share pictures of their rides.
The main goal is to build a strong and friendly community of people which share the same passion about cars.

---

## 🛠️ Installation

### Steps

1. Clone this repository:
   ```
    git clone https://github.com/martin-dimchev/CarLoud.git

2. Create and activate virtual environment
3. Install dependencies:
    ```
    pip install -r requirements.txt
   
4. Create and configure database
5. Start Redis as a service:  
    You can use Docker for example:
    ```
    docker pull redis:latest
    docker run -d --name redis -p 6379:6379 redis:latest
   
6. Setup .env
7. Apply migrations:
    ```
    python manage.py migrate
8. Run Celery
    ```
   celery -A carLoudApp  worker --loglevel=info
    ```
   OR
    ```
   celery -A carLoudApp  worker --pool=threads --concurrency=10 --loglevel=info
   
9. Run the app:
    ```
   python manage.py runserver
    
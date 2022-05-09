STACK
Rest API for performing basic operation on a Stack including:
 - push 
 - pop
 - max (get the current maximum integer in the stack)
 - stack (get all elements in the stack
 

How to run it:

1. Create virtual environment: python -m venv venv
2. Activate environment
   - Windows: ./venv/Scripts/activate
   - Linux: source venv/bin/activate
3. Install requirements: pip install -r ./requirements.txt
4. Run it: python app.py
  - Swagger doc: http://127.0.0.1:5000/swagger/#/Stack
  - Swagger UI: http://127.0.0.1:5000/swagger-ui/#/Stack

Run stress test:
  (make sure server is running)
  python /Tests/stress_test.py
  
  
 
 

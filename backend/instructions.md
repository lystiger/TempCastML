To run the backend manually, remember to create your own venv in the backend folder in your editor's terminal(or system terminal if you're a pro): 

+ For Linux and Mac: python3 -m venv venv

+ For Windows: python -m venv venv

After that activate it: 

+ For Linux and Mac: source venv/bin/activate

+ For Windows: venv\Scripts\activate

Then you download the requirements.txt(relax just the bunch of libraries):

+ All OS: pip install -r requirements.txt


Okay, let's continue by running these:

+ For Windows: 1. cd.
               2. uvicorn backend.main:app --reload

+ For Linux or Mac: 1. cd ..
                    2. uvicorn backend.main:app --reload

Now it is up and running !
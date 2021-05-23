# Tags-Overflow
## _The Stack Overflow Tag Predictor_

Tags-Overflow is a Python-3 Flask API that runs locally on your computer. 
Once started, you have to navigate to __localhost:5000__ (__127.0.0.1:5000__) with your web browser. 
A web interface will be displayed asking to enter a question.
Once the question is entered, you have to click the submit button. 
A python script will processed the question and some relevant tags from Stack Overflow will be displayed below the question. 
The process can be run as many times as wanted.

## More Information

The tags recommendation system is based on a OneVSRest classifier using Logistic Regressions.
The input features is a TF-IDF matrix that has been computed on a vocabulary of 30000 words from about
2 millions questions taken from Stack Overflow. It has obtained a Jaccard Index of 0.42 on the test set
with 1000 different tags to predict.

## Installation

- To run the application, first download the entire repository. If you are cloning the repository with git, 
you will have to use git LFS (Large File Storage)  as one of the file is above 100 MB. In both cases, make sure that the _classifier.pkl_ file is properly downloaded (around 230 MB).
- Once downloaded, it is recommended to create and activate a virtual environment using Python `venv`. 
On Windows, inside the repository you just downloaded, use the command:
    ```
    python -m venv env
    .\env\Scripts\activate
    ```
- Once the environment activated, you have to install the packages listed in _requirements.txt_. You can do so using `pip`:
    ```
    pip install -r requirements.txt
    ```
- You can finally run the application. Note that you may need admin rights to do so (otherwise some DLL loading error may be returned).
    ```
    python api.py
    ```
- A local server will be launched on port __5000__ by default. Navigate to it with your browser.
You can then ask the application to predict tags for all your questions.

## Acknowledgments

Thanks to Stack Overflow for making all the questions on their website available.
I am also particularly thankful to [macloo](https://github.com/macloo) and its [GitHub Repository](https://github.com/macloo/python-adv-web-apps/blob/master/docs/flask_forms.rst) to build Flask application using Boostrap. It has been really handy to make this API looks nicer without being too much time consumming. 

## Licence

This is a Free Software.

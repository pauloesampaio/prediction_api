# Prediction API

When you work in a product based company, it is almost certain that the developers from the product team will access your model's result through an [API](https://en.wikipedia.org/wiki/API), following a [microservice architecture](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices). This means that each model will be deployed in the form of an independent and self-contained service. In this scenario, whenever the application need an answer from your model, it will make a request to which your model will answer with a response. Something like this:

For a quick example, let's use again our [multitask classifier](https://pauloesampaio.github.io/posts/2020-12-31-multitask_learning/). Imagine that for some reason our application need the prediction for [this image](https://images-na.ssl-images-amazon.com/images/I/6191a2CIrKL._AC_UX385_.jpg). The request and answer will be something like this:

<img src="https://paulo-blog-media.s3-sa-east-1.amazonaws.com/posts/2021-01-24-prediction_api/request.jpg" alt="" width=460>

## Building the API

All right, so let's build an API! We'll use [FastAPI](https://fastapi.tiangolo.com/), which makes this task really easy. For instance, let's create an API that just says that everything is running. Create a `main.py` file with:

```python
app = FastAPI()

@app.get("/")
def check_api():
    return {"API status": "Up and running!"}
```

To run it, on the terminal, go to the app directory (`cd app`) and run: `uvicorn main:app --reload`

If everything worked, open your browser and go to `http://127.0.0.1:8000/` you should see:

<img src="https://paulo-blog-media.s3-sa-east-1.amazonaws.com/posts/2021-01-24-prediction_api/ok.jpg" alt="" width=460>

Notice that `get` is the method that this API is using and `"/"` is the path where it is running. Here we will use the get method cause we are simply returning a result. There are [other methods](https://restfulapi.net/http-methods/) that can be leverage according to your need.

Cool, so now let's suppose you already have a trained model with a predict function that produces a json answer (which is exactly what we had on our [multitask project](ttps://pauloesampaio.github.io/posts/2020-12-31-multitask_learning/)). Now it is easy, it is just a matter of implementing the following code:

```python
@app.get("/predict/")
async def get_prediction(url: str):
    image = download_image(url)
    predictions = predict(model, image, config)
    response = {"url": url, "predictions": predictions}
```

Again, we are using the `get` method but now our path is pointing to `/predict`. Also, notice that our function `get prediction` expects to receive an url. That's why our call on the example was `http://127.0.0.1:8000/predict/?url=`. Here `127.0.0.1:8000` is the address of the server where the API is running (in this case our localhost), `/predict/` is the path and the `?url=` will pass whatever comes after it as `url` to our `get_prediction` function. Easy as that. Then the function will answer with the json:

```json
{
    "url": url, 
    "predictions": predictions
}
```

If you look at the code, I added a couple more tricks there, just for error handling and to deal with the fact that the predictions are in `np.float32` format and FastAPI vanilla json encoder doesn't like this format very much...
For instance, if you try to download an invalid image:

<img src="https://paulo-blog-media.s3-sa-east-1.amazonaws.com/posts/2021-01-24-prediction_api/error.jpg" alt="" width=460>

## Using docker container

Remember the "self-contained" when we described the microservices architecture? So ideally this means that our API should runThe folks at FastAPI provided a Docker in its own environment, with its own stack and so on. Docker container is a great tool for that. A container have its own OS, its own python and its own libraries, isolated from the host OS.

The folks ate FastAPI made it really easy to put our API in a container. They provided an image that can be fetched in the Dockerfile. So you can simply create a `Dockerfile` with:

```dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app/app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ /app/app/
```

Here, the `FROM` is getting the base image from the fastapi repository. Then we are setting the working directory inside the container were the app will run, copying the requirements from the local repository to the container, pip installing the requirements and copying our app to the container working directory. Done.

Then, on the root directory of the project, to build the image, you do: `docker build -t myapi .`, where `myapi` is the name of your image. When it finishes building, you can run `docker run -d --name apicontainer -p 8000:80 myapi` and your API should be available on the server where you docker is running!

## Running this repo:

To summarize, if you want to run it locally:

```bash
cd app
uvicorn main:app --reload
```

To run it on a container, I'm providing a `docker-compose` file, so from the project's root folder you can simply:

```bash
docker-compose up
```

Done!

## Other cool FastAPI paths

FastAPI builds the documentation automatically, so if you check the `/docs` path, you'll find a page with the documentation and where you can test your API, as on the screenshot above. This is incredibly helpful to debug and test.

<img src="https://paulo-blog-media.s3-sa-east-1.amazonaws.com/posts/2021-01-24-prediction_api/docs.jpg" alt="" width=460>

## Closing thoughts

I think that being able to build a simple API to serve your model is an essential skill for the data scientist working in any professional scenario. Specially if you are working in a product based company with a team of developers. This will make your communication with them easier and the workflow smoother. Best of all, it is simple and easy to do!

Hope you enjoyed this, feel free to contact me if you have any questions or comments!

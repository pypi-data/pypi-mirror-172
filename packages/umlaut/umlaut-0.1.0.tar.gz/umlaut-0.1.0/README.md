# uMLaut

The uMLaut library simplifies data science model deployment and querying. It provides a single access point for all your models and an interface to interact with them. uMLaut models can be as extensive as deep learning models or as simple as a reusable code block.

uMLaut offers
- simple commands to track and query models
- history of all model query inputs and results
- model lifecycle management
- access to multiple versions of the same model
- a user interface with `MLflow`
- model audit tracking history (roadmap)
- auto-deployed models that can be queried through an API (roadmap)

## MLflow Setup
[MLflow](https://bit.ly/3eHJsx3) is a powerful machine learning library created by Databricks for data science teams. It offers an extensive API for tracking and querying models, but the learning curve can be a deterrent for small teams without dedicated data scientists. uMLaut strips away much of the complexity of MLflow while maintaining the immense value of tracking and querying your models in a single location. 

MLflow has two requirements:
1) A model artifact storage location
- This can be a local directory or a cloud storage URI. More info in the MLflow [docs](https://mlflow.org/docs/latest/tracking.html#artifact-stores).
2) A model registry
- The model registry is where model changes and query data are stored. More info in the MLflow [docs](https://mlflow.org/docs/latest/tracking.html#backend-stores).

An `mlflow server` must be running in order to work with uMLaut. The command to start an MLflow server with local artifact storage and a Postgres model registry is as follows:

`mlflow server --backend-store-uri postgresql+psycopg2://admin:password@localhost:5432/database --default-artifact-root "mlruns/"`

Once the server is running you can navigate to the MLflow UI and begin interacting with models.

____
## Core Functionality
uMLaut offers a simple Python class to assist with saving and querying business logic in MLflow.

- `track_model`: Converts a data science model or block of business logic into an MLflow compatible `model`
- `query_model`: Queries a previously trained `model` and saves audit metadata
- `track_dataset (roadmap)`: Saves reporting datasets along with the initial query and underlying data that built it (roadmap)
- `audit_model (roadmap)`: Retrieve the results of a model run for a historic date
- `audit_dataset (roadmap)`: Retrieve a dataset as it was on a historic date

### Deploying models with Umlaut
Custom data science models or business logic can be deployed simply by running `umlaut.track_model()`. Ensure the model code block is in a Python `Class` and follow the example below.

```
class ExampleModel():
    """
    Example business logic that can be wrapped into a model.
    The class _must_ contain a 'predict' method.
    """
    def business_logic(self, revenue: int) -> bool:
        if revenue > 5:
            return True
        else:
            return False

    def predict(self, model_input: dict) -> bool:
        return self.business_logic(revenue=model_input.get("revenue"))


if __name__ == "__main__":
    """Saves the model to MLflow in an experiment run"""
    from core import Umlaut

    umlaut = Umlaut()
    umlaut.track_model(
        model=ExampleModel(),
        model_name="Quarterly Revenue",
        run_name="Update",
    )
```

This will push the latest changes of `ExampleModel()` to MLflow as a new model version. Navigate to the MLflow server where you can find details for the example "Quarterly Revenue" model.


### Querying models with Umlaut
Once a model is deployed in MLflow with `umlaut.track_model()`, it can be queried by calling `umlaut.query_model()`.

```
from core import Umlaut

umlaut = Umlaut()
result = umlaut.query_model(
    model_name="Quarterly Revenue",
    input_config={"revenue": 3},
    stage="Staging",
)
print(f"Revenue will{'' if result else ' not'} exceed target")
```

If we query the simple `Quarterly Revenue` example model with `revenue = 3`, the model will return `False` as the revenue does not exceed the target of 5. The call to the model will be tracked in MLflow with model inputs and results.

Mycelium CLI
============

### What is Mycelium?

Mycelium is a framework that helps you easily write highly scalable (microservice) applications.

Mycelium automatically generates **Terraform** from your code, and handles load balancing for you.

The goal is to write your code without thinking about the infrastructure as if it was a simple monolithic application, and then have Mycelium decide on how to split your app into components, handle load balancing, communication between components, etc...

### How to use Mycelium?
Import this [runtime library](https://github.com/BizarreCake/myc) into your app and use it to annotate your code with service hints/constraints.

The more this framework evolves, the less help you will have to give in the form annotations.

Finally, invoke this CLI (`myc` command) and watch it automatically generate Terraform for you (and optionally deploy it for you).

### Example Usage

Create an empty Poetry application with `myc` (runtime) as dependency and `myccli` (compiler) as a development dependency.

Add some package (e.g. `test_app`) to your project with `__init__.py` containing:

```python
from myc import Mycelium

app = Mycelium()
foo_service = app.create_service("foo")
bar_service = app.create_service("bar")

@foo_service.fastapi.get("/")
def foo():
    return f'The answer is: {bar()}'

@bar_service.fastapi.get("/")
def bar():
    return 42
```

Then run `myc compile test_app:app` to generate Terraform, followed by `myc deploy` to deploy your app!

What will happen:
* A Dockerfile will be generated for each service
* Docker images will be built and pushed to a private ECR repository
    * *Temporary caveat*: The framework expects you to have a repository called `mycelium` in your AWS region of choice (an update will come soon to have this repo created automatically)
* Two ECS services will be created in a new cluster for `foo` and `bar` services.
* The call to `bar()` in `foo` function will be transformed to an HTTP get request!

### Limitations

This project is in its earliest stages, and feature count is limited at the moment.
The framework (currently) assumes projects to use Poetry as a package manager

#### Currently supported features:
* AWS as a cloud provider
* ECS as a platform in AWS (Lambda support will come very soon)
* Poetry as the package manager

More will come soon!

### Upcoming Features

* Dynamic and static load measurements to determine optimal load balancing strategy
* Support more cloud providers: Google Cloud, Azure, etc...
* Support more service platforms: AWS Lambda, EC2, etc...
* Support more package managers other than Poetry
* Flexible serialization/deserialization strategies
* Command to launch dashboard to watch:
    * Service topology
    * Aggregated logs
    * Load balancing metrics

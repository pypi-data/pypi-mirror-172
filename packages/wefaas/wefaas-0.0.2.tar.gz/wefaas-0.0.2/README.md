<!-- markdownlint-disable MD033 MD041 -->
<h1 align="center">
    wefass
</h1>

<p align="center">
    <strong>Instantly turn your Python function into production-ready microservice.</strong>
</p>

<p align="center">
    <a href="https://pypi.org/project/wefaas/" title="PyPi Version"><img src="https://img.shields.io/pypi/v/wefaas?color=green&style=flat"></a>
    <a href="https://pypi.org/project/wefaas/" title="Python Version"><img src="https://img.shields.io/badge/Python-3.8%2B-blue&style=flat"></a>
    <a href="https://github.com/weanalyze/orpyter/blob/main/LICENSE" title="Project License"><img src="https://img.shields.io/badge/License-Apache2.0-blue.svg"></a>
</p>

<p align="center">
  <a href="#getting-started">Getting Started</a> •
  <a href="#license">License</a> •
  <a href="https://github.com/weanalyze/orpyter/releases">Changelog</a>
</p>

Instantly turn your Python function into production-ready microservice. 

<sup>Pre-alpha Version: Not feature-complete and only suggested for experimental usage.</sup>

---

## Highlights

- 🪄&nbsp; Turn functions into production-ready services within seconds.
- 🔌&nbsp; Auto-generated HTTP API based on FastAPI.
- 📦&nbsp; Deploy microservice into weanalye FaaS cloud.
- 🧩&nbsp; Reuse pre-defined templates & combine with existing components.
- 📈&nbsp; Instantly deploy and scale for production usage.

## Getting Started

### Installation

> _Requirements: Python 3.8+._

```bash
pip install wefaas
```

### Usage

1. A simple orpyter-compatible function could look like this:

    ```python
    from pydantic import BaseModel

    class Input(BaseModel):
        message: str

    class Output(BaseModel):
        message: str

    def hello_world(input: Input) -> Output:
        """Returns the `message` of the input data."""
        return Output(message=input.message)
    ```

    _💡 An wefaas-compatible function is required to have an `input` parameter and return value based on [Pydantic models](https://pydantic-docs.helpmanual.io/). The input and output models are specified via [type hints](https://docs.python.org/3/library/typing.html)._

2. Copy this code to a file, e.g. `my_function.py`
3. Run the HTTP API server from command-line:

    ```bash
    wefaas serve my_function:hello_world
    ```
    _In the output, there's a line that shows where your web service is being served, on your local machine._
4. Deploy the service into weanalyze cloud from command-line:

    ```bash
    wefass login -u admin --gateway faas.weanalyze.co
    wefaas deploy my_function:hello_world 
    ```
    _In the output, there's a line that shows where your web service is being served, on your local machine._
5. Find out more usage information in the [Features](#features) section or get inspired by our [examples](#examples).

## License

Apache-2.0 License.

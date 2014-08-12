# airbrake-tornado

Airbrake notifier for Tornado web framework.

## Installation

Install via pip:

    pip install git+ssh://git@github.com/fullcontact/airbrake-tornado.git

When things become more stable, it will most likely be added to PyPi too.

## Usage

```python
  from airbrake import airbrake

  # In your RequestHandler:

  API_KEY = "Airbrake API key"
  ENV_NAME = "Airbrake env name"

  def write_error(self, status_code, **kwargs):
      if exc_info and status_code == 500:
          airbrake.notify(kwargs["exc_info"],
                          self.request,
                          "My-cool-app",
                          api_key=self.API_KEY,
                          environment=self.ENV_NAME)
```


## License

airbrake-tornado is available under the MIT license. See the [LICENSE](LICENSE) file for more info.

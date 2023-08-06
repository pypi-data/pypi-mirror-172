from ._data_provider import (
    DataProvider,
    ContentValidator,
    ResponseFactory,
    ValidatorContainer,
    RequestFactory,
)
from ._endpoint_data import EndpointData


class EndpointValidator(ContentValidator):
    def validate(self, data) -> bool:
        return True


class EndpointRequestFactory(RequestFactory):
    def get_body_parameters(self, *args, **kwargs):
        return kwargs.get("body_parameters") or {}

    def get_query_parameters(self, *args, **kwargs):
        return kwargs.get("query_parameters") or []

    def extend_body_parameters(self, body_params, **kwargs):
        return body_params


endpoint_data_provider = DataProvider(
    validator=ValidatorContainer(content_validator=EndpointValidator()),
    response=ResponseFactory(data_class=EndpointData),
    request=EndpointRequestFactory(),
)

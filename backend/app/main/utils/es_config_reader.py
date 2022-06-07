import environ

# from app.main.model.dataset import ValueType, IntervalES

env = environ.Env(
    # set casting, default value
    # DEBUG=(bool, False)
    DEBUG=(bool, True)
)
# reading .env file
environ.Env.read_env('app/main/utils/es_config.env')

elastic_index_config = {
    'es_index_caching': env("ES_CACHING"),
}
import environ

# from app.main.model.dataset import ValueType, IntervalES

env = environ.Env(
    # set casting, default value
    # DEBUG=(bool, False)
    DEBUG=(bool, True)
)
# reading .env file
environ.Env.read_env('app/config.env')

elastic = {
    'host': env("ES_HOST"),
    'port': env("ES_PORT"),
    'user': env("ES_USER"),
    'password': env("ES_PASSWORD"),
}
indices = {
    'data_index': env("DATA_INDEX"),
}

application = {
    'clear_data_index_at_startup': env.bool("CLEAR_DATA_INDEX_AT_STARTUP"),
}
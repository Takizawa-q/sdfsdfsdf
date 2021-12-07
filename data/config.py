from environs import Env
env = Env()
env.read_env()

TEST_API_TOKEN = env.str("TEST_TOKEN")
API_TOKEN = env.str("TOKEN")
ADMINS = env.list("ADMIN_ID")
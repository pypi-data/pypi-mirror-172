from algo_beast_core.helpers import parse_args

def validate_session(session):
  id = parse_args("id", session)

  if not id:
    raise Exception("id is missing")

  return session
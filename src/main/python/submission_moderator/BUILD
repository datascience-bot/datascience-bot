python_library(
  name='lib',
  sources=['*.py'],
  dependencies=[
    '3rdparty/python:flask',
    '3rdparty/python:packaging',
    '3rdparty/python:praw',
    'src/main/python/authpraw:lib',
  ],
)

python_binary(
  name='submission_moderator-bin',
  source='api.py',
  dependencies=[
    ':lib'
  ]
)

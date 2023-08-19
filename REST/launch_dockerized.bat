start cmd /k "cd user && docker build -t rest-user . && docker run --rm -p 127.0.0.1:3203:3203 rest-user"
start cmd /k "cd booking && docker build -t rest-booking . && docker run --rm -p 127.0.0.1:3201:3201 rest-booking"
start cmd /k "cd movie && docker build -t rest-movie . && docker run --rm -p 127.0.0.1:3200:3200 rest-movie"
start cmd /k "cd showtime && docker build -t rest-showtime . && docker run --rm -p 127.0.0.1:3202:3202 rest-showtime"
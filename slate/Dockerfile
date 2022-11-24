FROM ruby:3.1-slim AS middleman-builder

WORKDIR /app

COPY Gemfile Gemfile.lock /app/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        nodejs \
    && gem install bundler \
    && bundle install \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN bundle exec middleman build --verbose

# Copy the resulting code to the nginx container
FROM nginx:alpine
COPY --from=middleman-builder /app/build /usr/share/nginx/html

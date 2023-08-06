twitterEye is a python library, designed for making twitter sentiment analysis easy and approachable to every one,
First you have to signup for twitter developers portal, use the provided secret keys in the builtin function with
the topic keyword you want to analyze and opt for results visualization.
The function can be called as follows with mentioned data types of arguments.
analyze_keyword(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str, keyword: str, tweets_limit: int = 1000, visualize: bool = True)  
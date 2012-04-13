Gateway WSGI Application
========================

The gateway application is what the various market data uploaders toss their
data at. It parses whatever custom format they're using into our standard
Python representation of a market order (src.core.market_data.MarketOrder), and
serializes it to JSON, to be sent off to a Broker.

From there, the broker sends the data to a processor daemon, which picks it 
up and does magical things to it.
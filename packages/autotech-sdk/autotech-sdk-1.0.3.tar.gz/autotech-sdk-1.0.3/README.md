************************************************************
autotech-sdk: software development kit for autotech company
***********************************************************

**autotech-sdk** is a library for common task in cloud development such as: MongoDB setup, Confluent-kafka setup.

Mongo setup example:

        from autotech_sdk.database.mongo import BaseMongDB
        from pymongo import IndexModel        

        class UserModel(BaseMongoDB):
            indexes = [
                IndexModel(
                    keys="username",
                    unique=True,
                    background=True
                ),
            ]

Confluent-kafka consumer example:
        
        from autotech_sdk.kafka import ConfluentConsumerConfig, ConfluentConsumer
        
        class GetInforConsumer(ConfluentConsumer):
            def process_data(self, data):
                print(data)
            
            def process_data_error(self, msg, err):
                pass
            


In short, autotech_sdk can be used to:

- **MongoDB** setup connection.
- **Kafka** setup connection.

Get It Now
==========

    $ pip install -U autotech-sdk


Requirements
============

- Python >= 3.9



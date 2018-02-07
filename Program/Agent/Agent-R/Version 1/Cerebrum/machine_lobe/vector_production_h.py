"""
Agent: Cerebrum::MachineLobe::VectorProduction
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from datetime import datetime
import numpy


class VectorMachine:

    def __init__(self, **kwargs):

        self.creation_date = datetime.utcnow()

        print(self.creation_date)


        # If vector provided with instantiation, create new vector.
        if "container" in kwargs:

            self.new_vector(container= kwargs["container"])



    def new_vector(self, container):


        # Create a new vector.
        new_vector = numpy.array(container)


        return new_vector



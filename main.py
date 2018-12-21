from ExperimentSuite import ExperimentSuite
import tensorflow as tf
import Preprocessor
from Vectorizer import Vectorizer
from datetime import datetime

DEFAULT_EPOCH = 75
DEFAULT_LAYERS = (512,)
DEFAULT_ACTIVATION = tf.nn.relu
DEFAULT_LOSS = "categorical_hinge"
#DEFAULT_LOSS = "logcosh"



if __name__ == "__main__":
    # TODO: Make your experiments here
    es = ExperimentSuite()
    v1 = Vectorizer(max_df=0.97,min_df=0.5)
    temp = v1.fit_transform(es.train_contents,"count")
    temp_test = v1.transform(es.test_contents,"count")
    #v2 = Vectorizer(max_df=0.97,min_df=0.25)
    #v3 = Vectorizer(max_df=0.97,min_df=0.1)
    #print datetime.now()
    tbCall = tf.keras.callbacks.TensorBoard(log_dir='./Graph',histogram_freq=0,write_graph=True,write_images=True)
    result = es.train_model(DEFAULT_LAYERS,tbCall,temp,es.train_y,temp_test,es.test_y,DEFAULT_LOSS,tf.nn.sigmoid,500)

    print result
    #print v.vocabulary
    #print datetime.now()
    #print temp
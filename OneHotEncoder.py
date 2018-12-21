import numpy as np

class OneHotEncoder:
    def __init__(self):
        self.tags=[]

    def fit(self,X):
        """Converts list of labels into unique list and stores in self.tags.

        :param X: list of labels
        :return: None
        """
        # TODO: Implement this method
        for label in X:
            if label not in self.tags:
                self.tags.append(label)

    def fit_transform(self,X):
        """Calls fit and transform methods respectively with X.

        :param X: list of labels
        :return: numpy array of one-hot vectors for each element in X
        """
        # TODO: Implement this method
        self.fit(X)
        return self.transform(X)

    def transform(self, X):
        """Converts each element in the list into their one-hot representations

        :param X: list of labels
        :return: numpy array of one-hot vectors for each element in X
        """
        # TODO: Implement this method
        result = np.zeros((len(X),len(self.tags)),dtype=int)
        i=0
        size = len(X)
        for i in range(size):
            for j in range(len(self.tags)):
                if X[i] == self.tags[j]:
                    result[i,j] = 1
        return result

    def get_feature_names(self):
        """Returns the tags
        :return: tags
        """
        # TODO: Implement this method
        return self.tags

    def decode(self, one_hot_vector):
        """Decodes given one-hot-vector into its value.

        :param one_hot_vector: numpy array for one-hot-vector
        :return: corresponding element in self.tags
        """
        # TODO: Implement this method
        for i in range(len(self.tags)):
            if one_hot_vector[i] == 1:
                return self.tags[i]

if __name__=="__main__":
    o = OneHotEncoder()
    train_labels = ["Action","Comedy","Crime","Comedy","Crime","Musical","Action"]
    test_labels = ["Comedy","Action","Crime","Musical","Crime","War"]
    train_one_hot_vectors = o.fit_transform(train_labels)
    test_one_hot_vectors = o.transform(test_labels) 
    print o.get_feature_names()
    print train_one_hot_vectors
    print test_one_hot_vectors
    one_hot_vector = np.array([0,1,0,0])
    print o.decode(one_hot_vector)

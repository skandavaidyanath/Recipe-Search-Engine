import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
from torch.autograd import Variable
import pickle
import random
import json
from app import get_db

# Architecture of the Stacked AutoEncoder

class SAE(nn.Module):
    '''
    Architecture of the Stacked Auto-encoder.
    '''
    def __init__(self, nb_documents, ):
        super(SAE, self).__init__()
        self.fc1 = nn.Linear(nb_documents, 20)
        self.fc2 = nn.Linear(20, 10)
        self.fc3 = nn.Linear(10, 20)
        self.fc4 = nn.Linear(20, nb_documents)
        self.activation = nn.Sigmoid()

    def forward(self, x):
        '''
        Function to perform feed forward.
        '''
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = self.fc4(x)
        return x


# Creating User-Document matrix
def convert(data, min_user_index, max_user_index, doc_ids, nb_documents):
    '''
    Converts our user document data into a matrix such that each user gets a row with his "ratings" for each recipe. 
    Ratings is guven by number of times the user has opened the recipe.
    The matrix is number of users * number of recipes.
    '''
    new_data = []
    for id_users in range(min_user_index, max_user_index + 1):
        id_movies = data[:, 1][data[:, 0] == id_users]
        id_ratings = data[:, 2][data[:, 0] == id_users]
        ratings = np.zeros(nb_documents)
        ratings[id_movies - 1] = id_ratings
        new_data.append(list(ratings))
    return new_data


def main():
    # Getting the data
    training_set = pd.read_csv('q1.base', delimiter='\t')
    test_set = pd.read_csv('q1.test', delimiter='\t')
    training_set = np.array(training_set, dtype='int')
    test_set = np.array(test_set, dtype='int')
    # Getting total number of users and documents
    db = get_db()
    cursor = db.cursor()
    nb_users = 0
    try:
        sql = "SELECT COUNT(*) FROM USERS"
        cursor.execute(sql)
        row = cursor.fetchone()
        nb_users = row[0]
    except Exception as e:
        print(e)
        db.rollback()
    fp = open("corpus/dish_names_dict.json", "r")
    corpus = json.load(fp)
    fp.close()
    nb_documents = len(corpus)
    doc_ids = corpus.keys()
    min_user_index = 1
    max_user_index = nb_users
    training_set = convert(training_set, min_user_index,
                           max_user_index, doc_ids, nb_documents)
    test_set = convert(test_set, min_user_index,
                       max_user_index, doc_ids, nb_documents)
    # Converting data to Torch tensors
    training_set = torch.FloatTensor(training_set)
    test_set = torch.FloatTensor(test_set)
    # Creating the SAE
    sae = SAE(nb_documents)
    criterion = nn.MSELoss()
    optimizer = optim.RMSprop(sae.parameters(), lr=0.01, weight_decay=0.5)
    # Training the SAE
    nb_epoch = 300
    for epoch in range(1, nb_epoch + 1):
        train_loss = 0
        s = 0.
        for id_user in range(nb_users):
            input_data = Variable(training_set[id_user]).unsqueeze(0)
            target = input_data.clone()
            if torch.sum(target.data > 0) > 0:
                output = sae.forward(input_data)
                target.require_grad = False
                output[target == 0] = 0
                loss = criterion(output, target)
                mean_corrector = nb_documents / \
                    float(torch.sum(target.data > 0) + 1e-10)
                loss.backward()
                train_loss += np.sqrt(loss.data[0]*mean_corrector)
                s += 1
                optimizer.step()
        print('epoch: ' + str(epoch) + ' loss: ' + str(train_loss/s))
    # Testing the SAE
    test_loss = 0
    s = 0.
    for id_user in range(nb_users):
        input_data = Variable(training_set[id_user]).unsqueeze(0)
        target = Variable(test_set[id_user]).unsqueeze(0)
        if torch.sum(target.data > 0) > 0:
            output = sae.forward(input_data)
            target.require_grad = False
            output[target == 0] = 0
            loss = criterion(output, target)
            mean_corrector = nb_documents / \
                float(torch.sum(target.data > 0) + 1e-10)
            test_loss += np.sqrt(loss.data[0]*mean_corrector)
            s += 1
    print('test loss: ' + str(test_loss/s))
    # Saving our model
    torch.save(sae, 'my_sae.pt')


if __name__ == '__main__':
    main()

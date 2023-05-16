from django.shortcuts import render, HttpResponse
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from .models import UploadedData

# Create your views here.

def upload_data(request):
    if request.method == "POST":
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data_file = request.FILES.get('data_file')
        raw_data = UploadedData.objects.create(
            name=data_file.name,
            data_file=data_file,
            user=request.user
        )
    return render(request, "train/upload_data.html")    



def train_model(request):
    rawdata = UploadedData.objects.filter(user=request.user)
    if request.method == "POST": 
        print("request.POST", request.POST)

        # raw data read
        rawdata = request.POST.get('rawdata')
        # dataset = pd.read_csv('media/train_data/Data.csv')
        dataset = pd.read_csv(f'media/{rawdata}')
        # print(dataset)


        ## split dataset into x and y
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        # print(X)

        ## Taking care of missing data
        from sklearn.impute import SimpleImputer
        missing_data_strategy = request.POST.get('missing-data-strategy')
        if missing_data_strategy == "constant":
            imputer = SimpleImputer(missing_values=np.nan, strategy=missing_data_strategy, fill_value=request.POST.get('missing-constant-value'))
        else:
            imputer = SimpleImputer(missing_values=np.nan, strategy=missing_data_strategy)
        imputer.fit(X[:, 1:3])
        X[:, 1:3] = imputer.transform(X[:, 1:3])
        # print(X)

        ## Encoding independent data
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        remainder = request.POST.get('remainder')
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder=remainder)
        X = np.array(ct.fit_transform(X))

        # print(X)

        ## Encoding dependent data
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = le.fit_transform(y)
        print(y)

        # save data to csv
        print(X)
        # np.savetxt(f"media/{rawdata}-x.csv", X, delimiter=",")
        df = pd.DataFrame(X)
        df.to_csv(f"media/{rawdata}-x.csv", index=False)
        df = pd.DataFrame(y)
        df.to_csv(f"media/{rawdata}-y.csv", index=False)
        


        # ## Splitting the dataset into the Training set and Test set
        # from sklearn.model_selection import train_test_split
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

        # # print(X_train)

        # ## Feature Scaling
        # from sklearn.preprocessing import StandardScaler
        # sc = StandardScaler()
        # X_train = sc.fit_transform(X_train)
        # X_test = sc.transform(X_test)

        # print(X_train)

    # return HttpResponse(f"Train model {dataset}")
    return render(request, "train/train_model.html", {"rawdata": rawdata})